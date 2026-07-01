"""
External API integration endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
import httpx
import logging

from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/my-ersiy/patient/{nik}")
async def get_patient_from_my_ersiy(nik: str):
    """
    Get patient information from My eRSIy API
    """
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {settings.MY_ERSIY_API_KEY}"}
            response = await client.get(
                f"{settings.MY_ERSIY_API_URL}/patients/{nik}",
                headers=headers,
                timeout=30.0
            )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Patient not found in My eRSIy"
            )
    
    except Exception as e:
        logger.error(f"My eRSIy integration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="External API error"
        )


@router.post("/my-ersiy/visit")
async def sync_visit_to_my_ersiy(visit_data: dict):
    """
    Sync patient visit data to My eRSIy
    """
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {settings.MY_ERSIY_API_KEY}"}
            response = await client.post(
                f"{settings.MY_ERSIY_API_URL}/visits",
                json=visit_data,
                headers=headers,
                timeout=30.0
            )
        
        if response.status_code == 201:
            return {"message": "Visit data synced successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to sync visit data"
            )
    
    except Exception as e:
        logger.error(f"My eRSIy sync error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sync failed"
        )


@router.get("/bpjs/verify/{nik}")
async def verify_bpjs(nik: str):
    """
    Verify BPJS/JKN coverage
    """
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {settings.BPJS_API_KEY}"}
            response = await client.get(
                f"{settings.BPJS_API_URL}/verify/{nik}",
                headers=headers,
                timeout=30.0
            )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="BPJS verification failed"
            )
    
    except Exception as e:
        logger.error(f"BPJS verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="BPJS API error"
        )


@router.post("/sim-rs/patient")
async def create_patient_in_sim_rs(patient_data: dict):
    """
    Create patient record in SIM RS
    """
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {settings.SIM_RS_API_KEY}"}
            response = await client.post(
                f"{settings.SIM_RS_API_URL}/patients",
                json=patient_data,
                headers=headers,
                timeout=30.0
            )
        
        if response.status_code == 201:
            return response.json()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create patient in SIM RS"
            )
    
    except Exception as e:
        logger.error(f"SIM RS error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="SIM RS API error"
        )


@router.get("/health")
async def check_integration_health():
    """
    Check health of external API integrations
    """
    health_status = {}
    
    # Check My eRSIy
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.MY_ERSIY_API_URL}/health",
                timeout=5.0
            )
            health_status["my_ersiy"] = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        health_status["my_ersiy"] = "unavailable"
    
    # Check BPJS
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.BPJS_API_URL}/health",
                timeout=5.0
            )
            health_status["bpjs"] = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        health_status["bpjs"] = "unavailable"
    
    # Check SIM RS
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.SIM_RS_API_URL}/health",
                timeout=5.0
            )
            health_status["sim_rs"] = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        health_status["sim_rs"] = "unavailable"
    
    return health_status
