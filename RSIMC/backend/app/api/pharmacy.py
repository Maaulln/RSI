"""
Pharmacy queue management API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import List
import uuid
import logging

from app.database import get_db
from app.models import PharmacyQueue, Patient

logger = logging.getLogger(__name__)
router = APIRouter()


class PharmacyQueueCreate(BaseModel):
    patient_id: str = None
    prescription_data: dict = None


class PharmacyQueueResponse(BaseModel):
    id: str
    patient_id: str = None
    queue_number: int
    status: str
    created_at: str


@router.post("/queue", response_model=PharmacyQueueResponse, status_code=status.HTTP_201_CREATED)
async def add_to_pharmacy_queue(
    request: PharmacyQueueCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Add patient to pharmacy queue
    """
    
    # Get next queue number
    stmt = select(func.max(PharmacyQueue.queue_number))
    result = await db.execute(stmt)
    max_queue = result.scalar() or 0
    next_queue = max_queue + 1
    
    # Create queue entry
    queue_entry = PharmacyQueue(
        id=uuid.uuid4(),
        patient_id=uuid.UUID(request.patient_id) if request.patient_id else None,
        prescription_data=request.prescription_data,
        queue_number=next_queue,
        status="waiting"
    )
    
    db.add(queue_entry)
    await db.commit()
    await db.refresh(queue_entry)
    
    logger.info(f"Patient added to pharmacy queue #{next_queue}")
    
    return PharmacyQueueResponse(
        id=str(queue_entry.id),
        patient_id=str(queue_entry.patient_id),
        queue_number=queue_entry.queue_number,
        status=queue_entry.status,
        created_at=str(queue_entry.created_at)
    )


@router.get("/queue")
async def get_pharmacy_queue(
    status_filter: str = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get pharmacy queue
    """
    
    if status_filter:
        stmt = select(PharmacyQueue).where(
            PharmacyQueue.status == status_filter
        ).order_by(PharmacyQueue.queue_number)
    else:
        stmt = select(PharmacyQueue).order_by(PharmacyQueue.queue_number)
    
    result = await db.execute(stmt)
    queue = result.scalars().all()
    
    return queue


@router.get("/queue/{queue_id}")
async def get_queue_entry(
    queue_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific queue entry
    """
    
    stmt = select(PharmacyQueue).where(PharmacyQueue.id == uuid.UUID(queue_id))
    result = await db.execute(stmt)
    entry = result.scalar_one_or_none()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Queue entry not found"
        )
    
    return entry


@router.patch("/queue/{queue_id}/status")
async def update_queue_status(
    queue_id: str,
    new_status: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Update queue entry status
    """
    
    stmt = select(PharmacyQueue).where(PharmacyQueue.id == uuid.UUID(queue_id))
    result = await db.execute(stmt)
    entry = result.scalar_one_or_none()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Queue entry not found"
        )
    
    valid_statuses = ["waiting", "called", "dispensed", "completed"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of {valid_statuses}"
        )
    
    entry.status = new_status
    await db.commit()
    
    return {"queue_id": queue_id, "status": new_status}


@router.get("/current-number")
async def get_current_queue_number(db: AsyncSession = Depends(get_db)):
    """
    Get current being served queue number
    """
    
    stmt = select(PharmacyQueue).where(
        PharmacyQueue.status == "called"
    ).order_by(PharmacyQueue.queue_number)
    result = await db.execute(stmt)
    current = result.scalars().first()
    
    if current:
        return {
            "queue_number": current.queue_number,
            "patient_id": str(current.patient_id) if current.patient_id else None,
            "status": current.status
        }
    
    return {"queue_number": None, "message": "No patient being served"}


@router.post("/queue/{queue_id}/call")
async def call_next_patient(
    queue_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Call next patient from queue
    """
    
    stmt = select(PharmacyQueue).where(PharmacyQueue.id == uuid.UUID(queue_id))
    result = await db.execute(stmt)
    entry = result.scalar_one_or_none()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Queue entry not found"
        )
    
    # Mark as called
    entry.status = "called"
    await db.commit()
    
    logger.info(f"Called patient #{entry.queue_number}")
    
    return {
        "queue_number": entry.queue_number,
        "status": "called",
        "announcement": f"Antrian nomor {entry.queue_number}, silakan menuju loket farmasi"
    }


@router.delete("/queue/{queue_id}")
async def remove_from_queue(
    queue_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Remove patient from queue
    """
    
    stmt = select(PharmacyQueue).where(PharmacyQueue.id == uuid.UUID(queue_id))
    result = await db.execute(stmt)
    entry = result.scalar_one_or_none()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Queue entry not found"
        )
    
    await db.delete(entry)
    await db.commit()
    
    return {"message": "Removed from queue"}
