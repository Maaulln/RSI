"""
Nodes management API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

from app.database import get_db
from app.models import Node

router = APIRouter()


class NodeCreate(BaseModel):
    node_code: str
    location: str
    node_type: str  # full_screen, speaker
    avatar_character: str
    language: str = "id"


class NodeUpdate(BaseModel):
    location: str = None
    avatar_character: str = None
    language: str = None
    status: str = None
    is_active: bool = None


class NodeResponse(BaseModel):
    id: str
    node_code: str
    location: str
    node_type: str
    avatar_character: str
    language: str
    status: str
    is_active: bool
    ip_address: str | None = None
    last_heartbeat: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_node(cls, node: Node) -> "NodeResponse":
        return cls(
            id=str(node.id),
            node_code=node.node_code,
            location=node.location,
            node_type=node.node_type,
            avatar_character=node.avatar_character,
            language=node.language,
            status=node.status,
            is_active=node.is_active,
            ip_address=node.ip_address,
            last_heartbeat=node.last_heartbeat,
            created_at=node.created_at,
            updated_at=node.updated_at,
        )


@router.get("/", response_model=List[NodeResponse])
async def list_nodes(db: AsyncSession = Depends(get_db)):
    """
    List all nodes
    """
    stmt = select(Node).order_by(Node.node_code)
    result = await db.execute(stmt)
    nodes = result.scalars().all()
    return [NodeResponse.from_node(node) for node in nodes]


@router.post("/", response_model=NodeResponse, status_code=status.HTTP_201_CREATED)
async def create_node(
    node: NodeCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new node
    """
    # Check if node code already exists
    stmt = select(Node).where(Node.node_code == node.node_code)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Node with code {node.node_code} already exists"
        )
    
    # Create new node
    new_node = Node(
        id=uuid.uuid4(),
        node_code=node.node_code,
        location=node.location,
        node_type=node.node_type,
        avatar_character=node.avatar_character,
        language=node.language,
        status="offline"
    )
    
    db.add(new_node)
    await db.commit()
    await db.refresh(new_node)

    return NodeResponse.from_node(new_node)


@router.get("/{node_id}", response_model=NodeResponse)
async def get_node(
    node_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific node
    """
    stmt = select(Node).where(Node.id == uuid.UUID(node_id))
    result = await db.execute(stmt)
    node = result.scalar_one_or_none()
    
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found"
        )
    
    return NodeResponse.from_node(node)


@router.patch("/{node_id}", response_model=NodeResponse)
async def update_node(
    node_id: str,
    node_update: NodeUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a node
    """
    stmt = select(Node).where(Node.id == uuid.UUID(node_id))
    result = await db.execute(stmt)
    node = result.scalar_one_or_none()
    
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found"
        )
    
    # Update fields
    update_data = node_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(node, key, value)
    
    node.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(node)
    
    return NodeResponse.from_node(node)


@router.delete("/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_node(
    node_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a node
    """
    stmt = select(Node).where(Node.id == uuid.UUID(node_id))
    result = await db.execute(stmt)
    node = result.scalar_one_or_none()
    
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found"
        )
    
    await db.delete(node)
    await db.commit()


@router.post("/{node_id}/heartbeat")
async def node_heartbeat(
    node_id: str,
    ip_address: str = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Node heartbeat - update status and IP address
    """
    stmt = select(Node).where(Node.id == uuid.UUID(node_id))
    result = await db.execute(stmt)
    node = result.scalar_one_or_none()
    
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found"
        )
    
    node.status = "online"
    node.last_heartbeat = datetime.utcnow()
    if ip_address:
        node.ip_address = ip_address
    
    await db.commit()
    
    return {"status": "updated", "node_id": node_id}


@router.get("/{node_id}/status")
async def get_node_status(
    node_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get node real-time status
    """
    stmt = select(Node).where(Node.id == uuid.UUID(node_id))
    result = await db.execute(stmt)
    node = result.scalar_one_or_none()
    
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found"
        )
    
    return {
        "node_id": str(node.id),
        "node_code": node.node_code,
        "status": node.status,
        "location": node.location,
        "avatar_character": node.avatar_character,
        "is_active": node.is_active,
        "last_heartbeat": node.last_heartbeat
    }
