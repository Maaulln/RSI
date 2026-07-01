"""
Admin dashboard API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
import logging

from app.database import get_db
from app.models import Node, Session, TriageRecord, AuditLog, PharmacyQueue

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/overview")
async def get_overview(db: AsyncSession = Depends(get_db)):
    """
    Get system overview/dashboard data
    """
    
    # Count nodes
    node_stmt = select(func.count(Node.id))
    node_result = await db.execute(node_stmt)
    total_nodes = node_result.scalar() or 0
    
    # Count online nodes
    online_stmt = select(func.count(Node.id)).where(Node.status == "online")
    online_result = await db.execute(online_stmt)
    online_nodes = online_result.scalar() or 0
    
    # Count today's sessions
    today = datetime.utcnow().date()
    session_stmt = select(func.count(Session.id)).where(
        func.date(Session.created_at) == today
    )
    session_result = await db.execute(session_stmt)
    today_sessions = session_result.scalar() or 0
    
    # Count pending pharmacy queue
    queue_stmt = select(func.count(PharmacyQueue.id)).where(
        PharmacyQueue.status.in_(["waiting", "called"])
    )
    queue_result = await db.execute(queue_stmt)
    pending_queue = queue_result.scalar() or 0
    
    return {
        "total_nodes": total_nodes,
        "online_nodes": online_nodes,
        "offline_nodes": total_nodes - online_nodes,
        "today_sessions": today_sessions,
        "pending_pharmacy_queue": pending_queue,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/analytics")
async def get_analytics(
    days: int = 7,
    db: AsyncSession = Depends(get_db)
):
    """
    Get analytics for past N days
    """
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Sessions by day
    sessions_stmt = select(
        func.date(Session.created_at).label("date"),
        func.count(Session.id).label("count")
    ).where(Session.created_at >= start_date).group_by(func.date(Session.created_at))
    
    sessions_result = await db.execute(sessions_stmt)
    sessions_data = sessions_result.all()
    
    # Triage by poli
    triage_stmt = select(
        TriageRecord.recommended_poli,
        func.count(TriageRecord.id).label("count")
    ).where(TriageRecord.created_at >= start_date).group_by(
        TriageRecord.recommended_poli
    )
    
    triage_result = await db.execute(triage_stmt)
    triage_data = triage_result.all()
    
    return {
        "period_days": days,
        "sessions_by_day": [
            {"date": str(row[0]), "count": row[1]} 
            for row in sessions_data
        ],
        "referrals_by_poli": [
            {"poli": row[0], "count": row[1]} 
            for row in triage_data
        ]
    }


@router.get("/audit-logs")
async def get_audit_logs(
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """
    Get audit logs
    """
    
    stmt = select(AuditLog).order_by(
        AuditLog.created_at.desc()
    ).limit(limit).offset(offset)
    
    result = await db.execute(stmt)
    logs = result.scalars().all()
    
    return logs


@router.post("/audit-log")
async def create_audit_log(
    action: str,
    resource_type: str,
    resource_id: str = None,
    details: dict = None,
    ip_address: str = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Create audit log entry
    """
    
    log = AuditLog(
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address
    )
    
    db.add(log)
    await db.commit()
    
    return {"message": "Audit log created"}


@router.get("/node-performance")
async def get_node_performance(db: AsyncSession = Depends(get_db)):
    """
    Get node performance metrics
    """
    
    stmt = select(Node)
    result = await db.execute(stmt)
    nodes = result.scalars().all()
    
    performance = []
    
    for node in nodes:
        # Count sessions for this node
        session_stmt = select(func.count(Session.id)).where(
            Session.node_id == node.id
        )
        session_result = await db.execute(session_stmt)
        session_count = session_result.scalar() or 0
        
        performance.append({
            "node_id": str(node.id),
            "node_code": node.node_code,
            "location": node.location,
            "status": node.status,
            "total_sessions": session_count,
            "last_heartbeat": node.last_heartbeat.isoformat() if node.last_heartbeat else None
        })
    
    return performance


@router.get("/system-health")
async def get_system_health(db: AsyncSession = Depends(get_db)):
    """
    Get overall system health status
    """
    
    # Count nodes
    node_stmt = select(func.count(Node.id))
    node_result = await db.execute(node_stmt)
    total_nodes = node_result.scalar() or 0
    
    # Count online nodes
    online_stmt = select(func.count(Node.id)).where(Node.status == "online")
    online_result = await db.execute(online_stmt)
    online_nodes = online_result.scalar() or 0
    
    # Calculate uptime percentage
    uptime_percentage = (online_nodes / total_nodes * 100) if total_nodes > 0 else 0
    
    # Database status
    try:
        test_stmt = select(func.count(Node.id))
        await db.execute(test_stmt)
        db_status = "healthy"
    except:
        db_status = "unhealthy"
    
    # Overall status
    if uptime_percentage >= 80 and db_status == "healthy":
        overall_status = "healthy"
    elif uptime_percentage >= 50:
        overall_status = "degraded"
    else:
        overall_status = "critical"
    
    return {
        "overall_status": overall_status,
        "uptime_percentage": round(uptime_percentage, 2),
        "online_nodes": online_nodes,
        "total_nodes": total_nodes,
        "database_status": db_status,
        "timestamp": datetime.utcnow().isoformat()
    }
