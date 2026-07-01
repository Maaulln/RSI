# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication

#### POST /api/auth/login
Login and get tokens

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### POST /api/auth/refresh
Refresh access token

**Request:**
```json
{
  "token": "<refresh_token>"
}
```

### Nodes Management

#### GET /api/nodes
List all nodes

**Response:**
```json
[
  {
    "id": "uuid",
    "node_code": "NODE-01",
    "location": "Pendaftaran",
    "node_type": "full_screen",
    "avatar_character": "doctor",
    "language": "id",
    "status": "online",
    "is_active": true,
    "created_at": "2024-06-30T10:00:00"
  }
]
```

#### POST /api/nodes
Create a new node

**Request:**
```json
{
  "node_code": "NODE-07",
  "location": "Area Terapi",
  "node_type": "full_screen",
  "avatar_character": "nurse",
  "language": "id"
}
```

#### GET /api/nodes/{node_id}
Get specific node details

#### PATCH /api/nodes/{node_id}
Update node configuration

#### DELETE /api/nodes/{node_id}
Delete a node

#### POST /api/nodes/{node_id}/heartbeat
Update node heartbeat (called every 30 seconds)

**Request:**
```json
{
  "ip_address": "192.168.1.100"
}
```

### Biometrics

#### POST /api/biometrics/verify-fingerprint
Verify patient via fingerprint

**Request:**
```json
{
  "fingerprint_data": "base64_encoded_fingerprint"
}
```

**Response:**
```json
{
  "patient_id": "uuid",
  "nik": "1234567890123456",
  "name": "Budi Santoso",
  "method": "fingerprint",
  "confidence": 0.95
}
```

#### POST /api/biometrics/verify-face
Verify patient via face recognition

**Request:**
```json
{
  "image_base64": "base64_encoded_image"
}
```

#### POST /api/biometrics/ocr-ktp
Extract data from KTP image

**Request:**
```json
{
  "image_base64": "base64_encoded_ktp_image"
}
```

**Response:**
```json
{
  "nik": "1234567890123456",
  "name": "Budi Santoso",
  "date_of_birth": "1970-01-01",
  "address": "Jl. Raya No. 123",
  "phone": "081234567890",
  "patient_found": true,
  "confidence": 0.90
}
```

### Triage

#### POST /api/triage/assess
Assess patient symptoms and get recommendation

**Request:**
```json
{
  "patient_id": "uuid",
  "session_id": "uuid",
  "complaint_text": "Saya merasa pusing dan mual",
  "symptoms": ["pusing", "mual", "demam"]
}
```

**Response:**
```json
{
  "id": "uuid",
  "patient_id": "uuid",
  "complaint_text": "Saya merasa pusing dan mual",
  "symptoms": ["pusing", "mual", "demam"],
  "recommended_poli": "Umum",
  "triage_level": "yellow",
  "confidence_score": 0.87
}
```

#### GET /api/triage/rules
Get all active triage rules

#### POST /api/triage/rules
Create new triage rule

**Request:**
```json
{
  "name": "Sakit Kepala Berat",
  "keywords": ["sakit kepala", "pusing", "migrain"],
  "recommended_poli": "Neurologi",
  "triage_level": "yellow",
  "priority": 5,
  "is_emergency": false
}
```

### Pharmacy

#### POST /api/pharmacy/queue
Add patient to pharmacy queue

**Request:**
```json
{
  "patient_id": "uuid",
  "prescription_data": { }
}
```

**Response:**
```json
{
  "id": "uuid",
  "queue_number": 45,
  "status": "waiting",
  "created_at": "2024-06-30T10:15:00"
}
```

#### GET /api/pharmacy/queue
Get pharmacy queue

**Query Parameters:**
- `status_filter` (optional): Filter by status (waiting, called, dispensed, completed)

#### POST /api/pharmacy/queue/{queue_id}/call
Call next patient

#### GET /api/pharmacy/current-number
Get currently served queue number

### Integration

#### GET /api/integration/my-ersiy/patient/{nik}
Get patient from My eRSIy API

#### POST /api/integration/my-ersiy/visit
Sync visit data to My eRSIy

#### GET /api/integration/bpjs/verify/{nik}
Verify BPJS coverage

#### POST /api/integration/sim-rs/patient
Create patient in SIM RS

#### GET /api/integration/health
Check integration health

### Admin

#### GET /api/admin/overview
Get system overview dashboard data

**Response:**
```json
{
  "total_nodes": 6,
  "online_nodes": 5,
  "offline_nodes": 1,
  "today_sessions": 234,
  "pending_pharmacy_queue": 12,
  "timestamp": "2024-06-30T10:30:00"
}
```

#### GET /api/admin/analytics
Get system analytics

**Query Parameters:**
- `days` (optional, default: 7): Number of days to analyze

#### GET /api/admin/audit-logs
Get audit logs

**Query Parameters:**
- `limit` (optional, default: 100)
- `offset` (optional, default: 0)

#### GET /api/admin/node-performance
Get node performance metrics

#### GET /api/admin/system-health
Get overall system health status

## Error Responses

All errors return appropriate HTTP status codes:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common status codes:
- 200: OK
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Rate Limiting

- 100 requests per minute per IP address
- Triage assessment: 10 requests per minute per session
- Biometrics verification: 5 attempts per minute
