'use client'

import { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useSessionStore } from '@/services/session-store'
import { api } from '@/services/api'

interface TriageScreenProps {
  onComplete: () => void
}

export default function TriageScreen({ onComplete }: TriageScreenProps) {
  const [complaint, setComplaint] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isListening, setIsListening] = useState(false)
  const { patient, setTriage } = useSessionStore()
  const recognitionRef = useRef<any>(null)

  useEffect(() => {
    // Initialize Web Speech API
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition()
      recognitionRef.current.lang = 'id-ID'
      recognitionRef.current.continuous = false
      
      recognitionRef.current.onstart = () => setIsListening(true)
      recognitionRef.current.onend = () => setIsListening(false)
      recognitionRef.current.onresult = (event: any) => {
        const transcript = Array.from(event.results)
          .map((result: any) => result[0].transcript)
          .join('')
        setComplaint(transcript)
      }
    }
  }, [])

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      recognitionRef.current.start()
    }
  }

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop()
    }
  }

  const handleSubmit = async () => {
    if (!complaint.trim()) {
      setError('Silakan jelaskan keluhan Anda')
      return
    }

    setLoading(true)
    setError(null)

    try {
      if (!patient) {
        throw new Error('Patient data not found')
      }

      const response = await api.assessTriage(
        patient.id,
        complaint,
        []
      )

      const triageResult = {
        recommendedPoli: response.data.recommended_poli,
        triageLevel: response.data.triage_level,
        confidenceScore: response.data.confidence_score,
        symptoms: response.data.symptoms || []
      }

      setTriage(triageResult)
      onComplete()
    } catch (err) {
      setError('Gagal melakukan triage. Silakan coba lagi.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <motion.div 
      className="w-full h-screen flex flex-col items-center justify-center p-8 bg-gradient-to-b from-blue-50 to-indigo-100"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <div className="w-full max-w-2xl space-y-8">
        <div className="text-center">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">
            Jelaskan Keluhan Anda
          </h2>
          <p className="text-xl text-gray-600">
            Silakan sampaikan gejala atau keluhan yang Anda alami
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8 space-y-6">
          {/* Complaint text area */}
          <textarea
            value={complaint}
            onChange={(e) => setComplaint(e.target.value)}
            placeholder="Ketik atau gunakan suara untuk menjelaskan keluhan Anda..."
            className="w-full h-32 px-4 py-3 border-2 border-gray-300 rounded-lg text-lg focus:border-blue-500 focus:outline-none"
          />

          {/* Voice input button */}
          <motion.button
            onClick={isListening ? stopListening : startListening}
            disabled={loading}
            className={`w-full py-4 text-xl font-bold rounded-lg transition ${
              isListening
                ? 'bg-red-600 hover:bg-red-700 text-white'
                : 'bg-blue-600 hover:bg-blue-700 text-white'
            }`}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {isListening ? '🎙️ Sedang Merekam... Klik untuk Berhenti' : '🎤 Gunakan Suara'}
          </motion.button>

          {error && (
            <motion.div 
              className="p-4 bg-red-100 border-l-4 border-red-600 text-red-700"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              {error}
            </motion.div>
          )}

          {/* Submit button */}
          <motion.button
            onClick={handleSubmit}
            disabled={loading || !complaint.trim()}
            className={`w-full py-4 text-xl font-bold rounded-lg transition ${
              loading || !complaint.trim()
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-green-600 hover:bg-green-700 text-white'
            }`}
            whileHover={{ scale: !loading && complaint.trim() ? 1.02 : 1 }}
            whileTap={{ scale: !loading && complaint.trim() ? 0.98 : 1 }}
          >
            {loading ? '⏳ Menganalisis...' : '✓ Lanjutkan'}
          </motion.button>
        </div>

        {/* Info */}
        <div className="bg-blue-50 border-l-4 border-blue-600 p-4 rounded">
          <p className="text-gray-700">
            💡 <strong>Tip:</strong> Jelaskan keluhan Anda dengan detail sehingga sistem dapat memberikan rekomendasi yang akurat.
          </p>
        </div>
      </div>
    </motion.div>
  )
}
