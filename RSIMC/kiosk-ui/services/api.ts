import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const api = {
  // Biometrics
  verifyFingerprint: (fingerprintData: string) =>
    apiClient.post('/api/biometrics/verify-fingerprint', {
      fingerprint_data: fingerprintData
    }),
  
  verifyFace: (imageBase64: string) =>
    apiClient.post('/api/biometrics/verify-face', {
      image_base64: imageBase64
    }),
  
  ocrKtp: (imageBase64: string) =>
    apiClient.post('/api/biometrics/ocr-ktp', {
      image_base64: imageBase64
    }),

  verifyNik: (nik: string) =>
    apiClient.post('/api/biometrics/verify-nik', { nik }),
  
  // Triage
  assessTriage: (patientId: string, complaintText: string, symptoms: string[]) =>
    apiClient.post('/api/triage/assess', {
      patient_id: patientId,
      complaint_text: complaintText,
      symptoms
    }),
  
  // Pharmacy
  addToQueue: (patientId: string, prescriptionData?: any) =>
    apiClient.post('/api/pharmacy/queue', {
      patient_id: patientId,
      prescription_data: prescriptionData
    }),
  
  getQueueStatus: () =>
    apiClient.get('/api/pharmacy/queue'),
  
  // Integration
  verifyBpjs: (nik: string) =>
    apiClient.get(`/api/integration/bpjs/verify/${nik}`),
  
  // Health
  health: () =>
    apiClient.get('/health')
}

export default apiClient
