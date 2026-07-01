"""
Biometrics API - fingerprint, face recognition, OCR
"""

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import uuid
import httpx
import logging

from app.database import get_db
from app.config import settings
from app.models import Patient

logger = logging.getLogger(__name__)
router = APIRouter()


class FingerprintVerificationRequest(BaseModel):
    fingerprint_data: str
    node_id: str = None


class FaceVerificationRequest(BaseModel):
    image_base64: str
    node_id: str = None


class OCRKTPRequest(BaseModel):
    image_base64: str


class VerifyNikRequest(BaseModel):
    nik: str


class FacialRecognitionResponse(BaseModel):
    patient_id: str
    confidence: float
    name: str
    nik: str


@router.post("/verify-fingerprint")
async def verify_fingerprint(
    request: FingerprintVerificationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Verify patient via fingerprint
    """
    fingerprint_hash = _hash_fingerprint(request.fingerprint_data)

    stmt = select(Patient).where(Patient.fingerprint_hash == fingerprint_hash)
    result = await db.execute(stmt)
    patient = result.scalar_one_or_none()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    return {
        "patient_id": str(patient.id),
        "nik": patient.nik,
        "name": patient.full_name,
        "method": "fingerprint",
        "confidence": 0.95
    }


@router.post("/verify-nik")
async def verify_nik(
    request: VerifyNikRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Verify patient by NIK (manual entry at kiosk)
    """
    nik = request.nik.strip()
    if len(nik) != 16 or not nik.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="NIK must be 16 digits"
        )

    stmt = select(Patient).where(Patient.nik == nik)
    result = await db.execute(stmt)
    patient = result.scalar_one_or_none()

    if not patient:
        return {
            "nik": nik,
            "patient_found": False,
            "method": "nik_manual",
        }

    return {
        "patient_id": str(patient.id),
        "nik": patient.nik,
        "name": patient.full_name,
        "patient_found": True,
        "method": "nik_manual",
        "confidence": 0.99
    }


@router.post("/verify-face")
async def verify_face(
    request: FaceVerificationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Verify patient via face recognition
    """
    # Demo shortcut for kiosk development without external face service
    if request.image_base64 == "mock_face_encoding":
        stmt = select(Patient).where(Patient.face_encoding == "mock_face_encoding")
        result = await db.execute(stmt)
        patient = result.scalar_one_or_none()
        if patient:
            return {
                "patient_id": str(patient.id),
                "nik": patient.nik,
                "name": patient.full_name,
                "method": "face_recognition",
                "confidence": 0.92
            }

    try:
        # Call face recognition service
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.FACE_RECOGNITION_URL}/recognize",
                json={"image": request.image_base64},
                timeout=30.0
            )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Face recognition failed"
            )
        
        recognition_result = response.json()
        face_encoding = recognition_result.get("encoding")
        
        # Find patient by face encoding (simplified - in production use face distance matching)
        stmt = select(Patient).where(Patient.face_encoding != None)
        result = await db.execute(stmt)
        patients = result.scalars().all()
        
        # Find best match
        best_match = None
        best_confidence = 0.8  # Minimum confidence threshold
        
        for patient in patients:
            # Simplified matching (use proper face distance calculation in production)
            confidence = _face_distance(face_encoding, patient.face_encoding)
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = patient
        
        if not best_match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No matching face found"
            )
        
        return {
            "patient_id": str(best_match.id),
            "nik": best_match.nik,
            "name": best_match.full_name,
            "method": "face_recognition",
            "confidence": best_confidence
        }
    
    except Exception as e:
        logger.error(f"Face verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Face verification service error"
        )


@router.post("/ocr-ktp")
async def ocr_ktp(
    request: OCRKTPRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Extract data from KTP using OCR, or look up by NIK when digits are provided
    """
    raw_input = request.image_base64.strip()

    # Allow direct NIK lookup from kiosk manual entry
    if raw_input.isdigit() and len(raw_input) == 16:
        stmt = select(Patient).where(Patient.nik == raw_input)
        result = await db.execute(stmt)
        patient = result.scalar_one_or_none()
        if patient:
            return {
                "patient_id": str(patient.id),
                "nik": patient.nik,
                "name": patient.full_name,
                "patient_found": True,
                "method": "nik_lookup",
                "confidence": 0.99
            }
        return {
            "nik": raw_input,
            "patient_found": False,
            "method": "nik_lookup",
        }

    try:
        # Call OCR service
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.OCR_URL}/ocr-ktp",
                json={"image": request.image_base64},
                timeout=30.0
            )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OCR failed"
            )
        
        ocr_data = response.json()
        nik = ocr_data.get("nik")
        
        # Search for patient by NIK
        stmt = select(Patient).where(Patient.nik == nik)
        result = await db.execute(stmt)
        patient = result.scalar_one_or_none()
        
        if not patient:
            # Return OCR data for new patient registration
            return {
                "nik": nik,
                "name": ocr_data.get("name"),
                "date_of_birth": ocr_data.get("date_of_birth"),
                "address": ocr_data.get("address"),
                "phone": ocr_data.get("phone"),
                "patient_found": False
            }
        
        return {
            "patient_id": str(patient.id),
            "nik": patient.nik,
            "name": patient.full_name,
            "patient_found": True,
            "method": "ocr_ktp",
            "confidence": ocr_data.get("confidence", 0.85)
        }
    
    except Exception as e:
        logger.error(f"OCR error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OCR service error"
        )


@router.post("/register-biometric")
async def register_biometric(
    patient_id: str,
    fingerprint_data: str = None,
    face_encoding: str = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Register patient biometric data
    """
    
    stmt = select(Patient).where(Patient.id == uuid.UUID(patient_id))
    result = await db.execute(stmt)
    patient = result.scalar_one_or_none()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    if fingerprint_data:
        patient.fingerprint_hash = _hash_fingerprint(fingerprint_data)
    
    if face_encoding:
        patient.face_encoding = face_encoding
    
    await db.commit()
    
    return {"message": "Biometric data registered"}


def _hash_fingerprint(fingerprint_data: str):
    """Hash fingerprint data for storage"""
    import hashlib
    return hashlib.sha256(fingerprint_data.encode()).hexdigest()


def _face_distance(encoding1: str, encoding2: str):
    """
    Calculate distance between two face encodings
    Returns confidence score (0-1)
    """
    # Simplified implementation - in production use proper face distance calculation
    if encoding1 == encoding2:
        return 1.0
    return 0.5
