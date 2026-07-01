"""
SQLAlchemy ORM Models for DARSI-CS
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class User(Base):
    """System users (admin, staff, etc)"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="staff")  # admin, staff, doctor, operator
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Node(Base):
    """Kiosk nodes scattered across hospital"""
    __tablename__ = "nodes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_code = Column(String(50), unique=True, index=True, nullable=False)  # NODE-01, NODE-02, etc
    location = Column(String(255), nullable=False)
    node_type = Column(String(50), nullable=False)  # full_screen, speaker
    avatar_character = Column(String(255), nullable=False)
    language = Column(String(20), default="id")  # id, jv, mad
    status = Column(String(50), default="offline")  # online, offline, maintenance
    is_active = Column(Boolean, default=True)
    ip_address = Column(String(50), nullable=True)
    last_heartbeat = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sessions = relationship("Session", back_populates="node")


class Patient(Base):
    """Patient records (linked to hospital system)"""
    __tablename__ = "patients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nik = Column(String(50), unique=True, index=True, nullable=False)  # NIK from KTP
    full_name = Column(String(255), nullable=False)
    date_of_birth = Column(String(20), nullable=True)
    phone = Column(String(20), nullable=True)
    bpjs_number = Column(String(50), nullable=True)
    fingerprint_hash = Column(String(255), nullable=True)
    face_encoding = Column(Text, nullable=True)  # JSON encoded
    address = Column(Text, nullable=True)
    is_synced_with_bpjs = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sessions = relationship("Session", back_populates="patient")
    triage_records = relationship("TriageRecord", back_populates="patient")


class Session(Base):
    """Patient session on a node"""
    __tablename__ = "sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    node_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id"), nullable=False)
    auth_method = Column(String(50))  # fingerprint, face, nik_ocr, manual
    session_token = Column(String(255), unique=True, index=True)
    status = Column(String(50), default="active")  # active, completed, abandoned
    conversation_log = Column(JSON, nullable=True)  # Log of interaction
    duration_seconds = Column(Integer, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="sessions")
    node = relationship("Node", back_populates="sessions")


class TriageRecord(Base):
    """Patient triage/symptom assessment"""
    __tablename__ = "triage_records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    session_id = Column(UUID(as_uuid=True), nullable=True)
    complaint_text = Column(Text, nullable=False)  # Patient's complaint
    symptoms = Column(JSON, nullable=True)  # Array of extracted symptoms
    triage_level = Column(String(20), nullable=True)  # red, yellow, green, blue
    recommended_poli = Column(String(100), nullable=True)  # Recommended department
    confidence_score = Column(Float, nullable=True)  # 0-1
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="triage_records")


class TriageRule(Base):
    """Rules for triage decision making"""
    __tablename__ = "triage_rules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    keywords = Column(JSON, nullable=False)  # Array of keywords
    recommended_poli = Column(String(100), nullable=False)
    triage_level = Column(String(20), default="green")
    priority = Column(Integer, default=0)
    is_emergency = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PharmacyQueue(Base):
    """Pharmacy queue and medication dispensing"""
    __tablename__ = "pharmacy_queue"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=True)
    prescription_data = Column(JSON, nullable=True)
    queue_number = Column(Integer, nullable=True)
    status = Column(String(50), default="waiting")  # waiting, called, dispensed, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AuditLog(Base):
    """Audit trail for compliance"""
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    action = Column(String(255), nullable=False)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(String(255), nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
