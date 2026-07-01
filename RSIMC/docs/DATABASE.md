# Database Schema

## PostgreSQL Tables

### Users
System users (admin, staff, doctors, operators)

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  full_name VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'staff', -- admin, staff, doctor, operator
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Nodes
Kiosk hardware units throughout hospital

```sql
CREATE TABLE nodes (
  id UUID PRIMARY KEY,
  node_code VARCHAR(50) UNIQUE NOT NULL, -- NODE-01, NODE-02, etc
  location VARCHAR(255) NOT NULL,
  node_type VARCHAR(50) NOT NULL, -- full_screen, speaker
  avatar_character VARCHAR(255) NOT NULL,
  language VARCHAR(20) DEFAULT 'id',
  status VARCHAR(50) DEFAULT 'offline', -- online, offline, maintenance
  is_active BOOLEAN DEFAULT true,
  ip_address VARCHAR(50),
  last_heartbeat TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Patients
Patient records linked to hospital system

```sql
CREATE TABLE patients (
  id UUID PRIMARY KEY,
  nik VARCHAR(50) UNIQUE NOT NULL,
  full_name VARCHAR(255) NOT NULL,
  date_of_birth VARCHAR(20),
  phone VARCHAR(20),
  bpjs_number VARCHAR(50),
  fingerprint_hash VARCHAR(255),
  face_encoding TEXT, -- JSON encoded
  address TEXT,
  is_synced_with_bpjs BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Sessions
Patient interaction sessions on nodes

```sql
CREATE TABLE sessions (
  id UUID PRIMARY KEY,
  patient_id UUID FOREIGN KEY REFERENCES patients(id),
  node_id UUID FOREIGN KEY REFERENCES nodes(id),
  auth_method VARCHAR(50), -- fingerprint, face, nik_ocr, manual
  session_token VARCHAR(255) UNIQUE,
  status VARCHAR(50) DEFAULT 'active', -- active, completed, abandoned
  conversation_log JSONB, -- Log of interaction
  duration_seconds INTEGER,
  completed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### TriageRecords
Patient symptom assessment and triage results

```sql
CREATE TABLE triage_records (
  id UUID PRIMARY KEY,
  patient_id UUID FOREIGN KEY REFERENCES patients(id),
  session_id UUID,
  complaint_text TEXT NOT NULL,
  symptoms JSONB, -- Array of symptoms
  triage_level VARCHAR(20), -- red, yellow, green, blue
  recommended_poli VARCHAR(100),
  confidence_score FLOAT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### TriageRules
Rules for triage decision-making

```sql
CREATE TABLE triage_rules (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  keywords JSONB NOT NULL, -- Array of keywords
  recommended_poli VARCHAR(100) NOT NULL,
  triage_level VARCHAR(20) DEFAULT 'green',
  priority INTEGER DEFAULT 0,
  is_emergency BOOLEAN DEFAULT false,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### PharmacyQueue
Pharmacy queue management

```sql
CREATE TABLE pharmacy_queue (
  id UUID PRIMARY KEY,
  patient_id UUID FOREIGN KEY REFERENCES patients(id),
  prescription_data JSONB,
  queue_number INTEGER,
  status VARCHAR(50) DEFAULT 'waiting', -- waiting, called, dispensed, completed
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### AuditLogs
Audit trail for compliance

```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY,
  user_id UUID FOREIGN KEY REFERENCES users(id),
  action VARCHAR(255) NOT NULL,
  resource_type VARCHAR(100) NOT NULL,
  resource_id VARCHAR(255),
  details JSONB,
  ip_address VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Indexes

```sql
-- Performance optimization indexes
CREATE INDEX idx_patients_nik ON patients(nik);
CREATE INDEX idx_patients_bpjs ON patients(bpjs_number);
CREATE INDEX idx_nodes_code ON nodes(node_code);
CREATE INDEX idx_nodes_status ON nodes(status);
CREATE INDEX idx_sessions_patient ON sessions(patient_id);
CREATE INDEX idx_sessions_node ON sessions(node_id);
CREATE INDEX idx_sessions_status ON sessions(status);
CREATE INDEX idx_triage_patient ON triage_records(patient_id);
CREATE INDEX idx_triage_level ON triage_records(triage_level);
CREATE INDEX idx_queue_status ON pharmacy_queue(status);
CREATE INDEX idx_audit_created ON audit_logs(created_at);
```

## Relationships

```
Users
  ↓ (creator)
AuditLogs

Nodes
  ↓ (has)
Sessions
  ↓ (for)
Patients
  ↓ (has)
TriageRecords
TriageRules (referenced by LLM)

PharmacyQueue ← Patients (in queue)
```

## Data Retention Policies

- **Sessions**: Keep for 1 year, archive older
- **TriageRecords**: Keep for 5 years (medical records requirement)
- **AuditLogs**: Keep for 3 years minimum
- **PharmacyQueue**: Keep for 1 month after completion
- **Patients**: Keep indefinitely but mark as inactive if no visit for 2 years

## Backup Strategy

- Daily automated PostgreSQL backups
- Backup retention: 30 days
- Off-site backup copy to external storage
- Monthly integrity verification
- Quarterly disaster recovery drill

## Performance Tuning

- Connection pooling: Max 20 connections
- Query timeout: 30 seconds
- Table statistics auto-analyze enabled
- VACUUM frequency: Every 6 hours
- WAL archiving: Enabled for recovery
