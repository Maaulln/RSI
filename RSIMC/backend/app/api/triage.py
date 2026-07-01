"""
Triage and symptom assessment API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List
import uuid
import logging
import httpx

from app.database import get_db
from app.config import settings
from app.models import TriageRecord, TriageRule, Patient

logger = logging.getLogger(__name__)
router = APIRouter()


class TriageRequest(BaseModel):
    patient_id: str
    session_id: str = None
    complaint_text: str
    symptoms: List[str] = []


class TriageResponse(BaseModel):
    id: str
    patient_id: str
    complaint_text: str
    symptoms: List[str]
    recommended_poli: str
    triage_level: str
    confidence_score: float


@router.post("/assess", response_model=TriageResponse)
async def assess_triage(
    request: TriageRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Assess patient symptoms and recommend department
    """
    
    # Get LLM recommendation from Ollama
    try:
        triage_result = await _get_llm_triage(request.complaint_text)
    except Exception as e:
        logger.error(f"LLM triage failed: {e}")
        triage_result = await _fallback_triage(request.complaint_text, db)
    
    # Create triage record
    triage_record = TriageRecord(
        id=uuid.uuid4(),
        patient_id=uuid.UUID(request.patient_id),
        session_id=uuid.UUID(request.session_id) if request.session_id else None,
        complaint_text=request.complaint_text,
        symptoms=request.symptoms,
        recommended_poli=triage_result["poli"],
        triage_level=triage_result["level"],
        confidence_score=triage_result["confidence"]
    )
    
    db.add(triage_record)
    await db.commit()
    await db.refresh(triage_record)
    
    return TriageResponse(
        id=str(triage_record.id),
        patient_id=str(triage_record.patient_id),
        complaint_text=triage_record.complaint_text,
        symptoms=triage_record.symptoms,
        recommended_poli=triage_record.recommended_poli,
        triage_level=triage_record.triage_level,
        confidence_score=triage_record.confidence_score
    )


async def _get_llm_triage(complaint_text: str):
    """
    Call Ollama LLM for triage recommendation
    """
    try:
        prompt = f"""Berdasarkan keluhan pasien berikut, tentukan departemen/poli yang tepat dan tingkat urgensi.

Keluhan: {complaint_text}

Jawab dalam format JSON:
{{
    "poli": "Nama Poli (contoh: Umum, Kardio, Neurologi, IGD)",
    "level": "red|yellow|green|blue",
    "confidence": 0.85,
    "reasoning": "alasan singkat"
}}
"""
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.OLLAMA_URL}/api/generate",
                json={
                    "model": settings.LLM_MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30.0
            )
        
        if response.status_code == 200:
            result = response.json()
            # Parse the response (Ollama returns text)
            import json
            # Try to extract JSON from response
            text = result.get("response", "")
            try:
                json_data = json.loads(text)
                return json_data
            except:
                return {
                    "poli": "Umum",
                    "level": "green",
                    "confidence": 0.5,
                    "reasoning": "Default routing"
                }
        else:
            raise Exception(f"Ollama error: {response.status_code}")
    
    except Exception as e:
        logger.error(f"LLM triage error: {e}")
        raise


async def _fallback_triage(complaint_text: str, db: AsyncSession):
    """
    Fallback triage using rule-based matching
    """
    stmt = select(TriageRule).where(TriageRule.is_active == True)
    result = await db.execute(stmt)
    rules = result.scalars().all()
    
    # Simple keyword matching
    complaint_lower = complaint_text.lower()
    matched_rules = []
    
    for rule in rules:
        keywords = rule.keywords
        if any(keyword.lower() in complaint_lower for keyword in keywords):
            matched_rules.append(rule)
    
    if matched_rules:
        # Use rule with highest priority
        best_rule = sorted(matched_rules, key=lambda r: r.priority, reverse=True)[0]
        return {
            "poli": best_rule.recommended_poli,
            "level": best_rule.triage_level,
            "confidence": 0.6
        }
    else:
        # Default fallback
        return {
            "poli": "Umum",
            "level": "green",
            "confidence": 0.4
        }


@router.get("/rules")
async def get_triage_rules(db: AsyncSession = Depends(get_db)):
    """
    Get all active triage rules
    """
    stmt = select(TriageRule).where(TriageRule.is_active == True)
    result = await db.execute(stmt)
    rules = result.scalars().all()
    return rules


@router.post("/rules", status_code=status.HTTP_201_CREATED)
async def create_triage_rule(
    rule: dict,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new triage rule
    """
    new_rule = TriageRule(
        id=uuid.uuid4(),
        name=rule["name"],
        keywords=rule["keywords"],
        recommended_poli=rule["recommended_poli"],
        triage_level=rule.get("triage_level", "green"),
        priority=rule.get("priority", 0),
        is_emergency=rule.get("is_emergency", False)
    )
    
    db.add(new_rule)
    await db.commit()
    await db.refresh(new_rule)
    
    return new_rule
