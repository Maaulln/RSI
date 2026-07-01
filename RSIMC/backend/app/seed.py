"""
Seed demo data for local development and kiosk testing.
"""

import hashlib
import uuid
import logging

from sqlalchemy import select, func

from app.models import User, Node, Patient, TriageRule

logger = logging.getLogger(__name__)

DEMO_NIK = "3573010101010001"
DEMO_FINGERPRINT = "mock_fingerprint_data"
DEMO_FACE_ENCODING = "mock_face_encoding"


def _hash_fingerprint(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


async def seed_demo_data(session) -> None:
    """Insert demo records when the database is empty."""
    patient_count = await session.scalar(select(func.count(Patient.id)))
    if patient_count and patient_count > 0:
        return

    logger.info("Seeding demo data for development...")

    admin = User(
        id=uuid.uuid4(),
        email="admin@darsi.local",
        hashed_password="admin123",
        full_name="Admin DARSI",
        role="admin",
        is_active=True,
    )
    session.add(admin)

    node = Node(
        id=uuid.uuid4(),
        node_code="NODE-01",
        location="Pendaftaran Utama",
        node_type="full_screen",
        avatar_character="doctor",
        language="id",
        status="online",
        is_active=True,
    )
    session.add(node)

    patient = Patient(
        id=uuid.uuid4(),
        nik=DEMO_NIK,
        full_name="Budi Santoso",
        date_of_birth="1985-01-01",
        phone="081234567890",
        bpjs_number="0001234567890",
        fingerprint_hash=_hash_fingerprint(DEMO_FINGERPRINT),
        face_encoding=DEMO_FACE_ENCODING,
        address="Jl. Raya Surabaya No. 123",
        is_synced_with_bpjs=True,
    )
    session.add(patient)

    triage_rules = [
        TriageRule(
            id=uuid.uuid4(),
            name="Demam dan Batuk",
            keywords=["demam", "batuk", "pilek", "flu"],
            recommended_poli="Umum",
            triage_level="yellow",
            priority=10,
            is_emergency=False,
            is_active=True,
        ),
        TriageRule(
            id=uuid.uuid4(),
            name="Nyeri Dada",
            keywords=["nyeri dada", "sesak", "jantung"],
            recommended_poli="Kardiologi",
            triage_level="red",
            priority=20,
            is_emergency=True,
            is_active=True,
        ),
        TriageRule(
            id=uuid.uuid4(),
            name="Sakit Kepala",
            keywords=["pusing", "sakit kepala", "migrain"],
            recommended_poli="Neurologi",
            triage_level="yellow",
            priority=5,
            is_emergency=False,
            is_active=True,
        ),
    ]
    session.add_all(triage_rules)

    await session.commit()
    logger.info("Demo data seeded (admin, node, patient, triage rules)")
