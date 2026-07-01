'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useSessionStore } from '@/services/session-store'
import { api } from '@/services/api'

interface AuthScreenProps {
  onComplete: () => void
}

export default function AuthScreen({ onComplete }: AuthScreenProps) {
  const [authMethod, setAuthMethod] = useState<'fingerprint' | 'face' | 'nik' | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [nik, setNik] = useState('')
  const { setPatient } = useSessionStore()

  const handleFingerprint = async () => {
    setLoading(true)
    setError(null)
    try {
      // Simulate fingerprint reader
      const response = await api.verifyFingerprint('mock_fingerprint_data')
      const { patient_id, nik: patientNik, name } = response.data
      
      setPatient({
        id: patient_id,
        nik: patientNik,
        name
      })
      
      onComplete()
    } catch (err) {
      setError('Sidik jari tidak ditemukan. Silakan coba metode lain.')
    } finally {
      setLoading(false)
    }
  }

  const handleFace = async () => {
    setLoading(true)
    setError(null)
    try {
      // Simulate face recognition
      const response = await api.verifyFace('mock_face_encoding')
      const { patient_id, nik: patientNik, name } = response.data
      
      setPatient({
        id: patient_id,
        nik: patientNik,
        name
      })
      
      onComplete()
    } catch (err) {
      setError('Wajah tidak dikenali. Silakan coba metode lain.')
    } finally {
      setLoading(false)
    }
  }

  const handleNikSubmit = async () => {
    if (!nik || nik.length < 16) {
      setError('NIK harus 16 digit')
      return
    }
    
    setLoading(true)
    setError(null)
    try {
      const response = await api.verifyNik(nik)
      const { patient_id, patient_found } = response.data
      
      if (patient_found) {
        setPatient({
          id: patient_id,
          nik,
          name: response.data.name
        })
        onComplete()
      } else {
        setError('Data pasien tidak ditemukan')
      }
    } catch (err) {
      setError('Gagal memverifikasi NIK')
    } finally {
      setLoading(false)
    }
  }

  if (!authMethod) {
    return (
      <motion.div 
        className="w-full h-screen flex flex-col items-center justify-center p-8"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <div className="text-center space-y-8 max-w-2xl">
          <h2 className="text-4xl font-bold text-gray-800">
            Pilih Metode Verifikasi
          </h2>
          
          <p className="text-xl text-gray-600">
            Silakan pilih salah satu metode untuk memverifikasi identitas Anda
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-12">
            <AuthMethodButton
              icon="👆"
              label="Sidik Jari"
              onClick={() => setAuthMethod('fingerprint')}
              loading={loading}
            />
            
            <AuthMethodButton
              icon="👤"
              label="Pengenalan Wajah"
              onClick={() => setAuthMethod('face')}
              loading={loading}
            />
            
            <AuthMethodButton
              icon="📱"
              label="NIK"
              onClick={() => setAuthMethod('nik')}
              loading={loading}
            />
          </div>
        </div>
      </motion.div>
    )
  }

  if (authMethod === 'fingerprint') {
    return (
      <FingerprintAuth 
        onBack={() => setAuthMethod(null)}
        onComplete={handleFingerprint}
        loading={loading}
        error={error}
      />
    )
  }

  if (authMethod === 'face') {
    return (
      <FaceAuth 
        onBack={() => setAuthMethod(null)}
        onComplete={handleFace}
        loading={loading}
        error={error}
      />
    )
  }

  if (authMethod === 'nik') {
    return (
      <NikAuth 
        onBack={() => setAuthMethod(null)}
        onSubmit={handleNikSubmit}
        nik={nik}
        setNik={setNik}
        loading={loading}
        error={error}
      />
    )
  }

  return null
}

interface AuthMethodButtonProps {
  icon: string
  label: string
  onClick: () => void
  loading?: boolean
}

function AuthMethodButton({ icon, label, onClick, loading }: AuthMethodButtonProps) {
  return (
    <motion.button
      onClick={onClick}
      disabled={loading}
      className="p-8 bg-white rounded-lg shadow-lg hover:shadow-xl transition border-2 border-gray-200 hover:border-blue-500"
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
    >
      <div className="text-5xl mb-4">{icon}</div>
      <div className="text-xl font-bold text-gray-800">{label}</div>
    </motion.button>
  )
}

interface FingerprintAuthProps {
  onBack: () => void
  onComplete: () => Promise<void>
  loading: boolean
  error: string | null
}

function FingerprintAuth({ onBack, onComplete, loading, error }: FingerprintAuthProps) {
  return (
    <motion.div 
      className="w-full h-screen flex flex-col items-center justify-center p-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <div className="text-center space-y-8">
        <h2 className="text-4xl font-bold text-gray-800">
          Verifikasi Sidik Jari
        </h2>
        
        <motion.div
          animate={{ scale: [1, 1.1, 1] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="text-9xl"
        >
          👆
        </motion.div>
        
        <p className="text-xl text-gray-600 max-w-xl">
          Sentuh sensor sidik jari atau gunakan tombol di layar untuk memulai verifikasi.
        </p>
        {loading && <p className="text-xl text-blue-600">Memverifikasi...</p>}
        {error && <p className="text-xl text-red-600">{error}</p>}
        
        <div className="space-x-4">
          <motion.button
            onClick={onBack}
            className="px-8 py-4 bg-gray-400 text-white text-lg font-bold rounded-lg"
            whileHover={{ scale: 1.05 }}
          >
            Kembali
          </motion.button>
          
          <motion.button
            onClick={onComplete}
            disabled={loading}
            className="px-8 py-4 bg-blue-600 text-white text-lg font-bold rounded-lg disabled:opacity-50"
            whileHover={{ scale: 1.05 }}
          >
            {loading ? 'Memverifikasi...' : 'Mulai Verifikasi'}
          </motion.button>
        </div>
      </div>
    </motion.div>
  )
}

interface FaceAuthProps {
  onBack: () => void
  onComplete: () => Promise<void>
  loading: boolean
  error: string | null
}

function FaceAuth({ onBack, onComplete, loading, error }: FaceAuthProps) {
  return (
    <motion.div 
      className="w-full h-screen flex flex-col items-center justify-center p-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <div className="text-center space-y-8">
        <h2 className="text-4xl font-bold text-gray-800">
          Verifikasi Wajah
        </h2>
        
        <motion.div
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="text-9xl"
        >
          📸
        </motion.div>
        
        <p className="text-xl text-gray-600 max-w-xl">
          Hadapkan wajah ke kamera. Tekan tombol di bawah saat Anda siap untuk mengenali wajah.
        </p>
        {loading && <p className="text-xl text-blue-600">Mengenali wajah...</p>}
        {error && <p className="text-xl text-red-600">{error}</p>}
        
        <div className="space-x-4">
          <motion.button
            onClick={onBack}
            className="px-8 py-4 bg-gray-400 text-white text-lg font-bold rounded-lg"
            whileHover={{ scale: 1.05 }}
          >
            Kembali
          </motion.button>
          
          <motion.button
            onClick={onComplete}
            disabled={loading}
            className="px-8 py-4 bg-blue-600 text-white text-lg font-bold rounded-lg disabled:opacity-50"
            whileHover={{ scale: 1.05 }}
          >
            {loading ? 'Mengenali...' : 'Mulai Pengenalan'}
          </motion.button>
        </div>
      </div>
    </motion.div>
  )
}

interface NikAuthProps {
  onBack: () => void
  onSubmit: () => Promise<void>
  nik: string
  setNik: (nik: string) => void
  loading: boolean
  error: string | null
}

function NikAuth({ onBack, onSubmit, nik, setNik, loading, error }: NikAuthProps) {
  return (
    <motion.div 
      className="w-full h-screen flex flex-col items-center justify-center p-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <div className="text-center space-y-8 max-w-lg">
        <h2 className="text-4xl font-bold text-gray-800">
          Masukkan NIK
        </h2>
        
        <input
          type="text"
          value={nik}
          onChange={(e) => setNik(e.target.value.replace(/[^0-9]/g, ''))}
          placeholder="1234567890123456"
          className="w-full px-6 py-4 text-2xl border-2 border-gray-300 rounded-lg text-center"
          maxLength={16}
        />
        
        {error && <p className="text-xl text-red-600">{error}</p>}
        
        <div className="space-x-4">
          <motion.button
            onClick={onBack}
            className="px-8 py-4 bg-gray-400 text-white text-lg font-bold rounded-lg"
            whileHover={{ scale: 1.05 }}
          >
            Kembali
          </motion.button>
          
          <motion.button
            onClick={onSubmit}
            disabled={loading || nik.length !== 16}
            className="px-8 py-4 bg-blue-600 text-white text-lg font-bold rounded-lg disabled:opacity-50"
            whileHover={{ scale: 1.05 }}
          >
            {loading ? 'Verifikasi...' : 'Lanjutkan'}
          </motion.button>
        </div>
      </div>
    </motion.div>
  )
}
