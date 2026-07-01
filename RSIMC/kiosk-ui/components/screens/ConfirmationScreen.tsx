'use client'

import { useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { useSessionStore } from '@/services/session-store'

interface ConfirmationScreenProps {
  onReset: () => void
}

const triageLevelInfo = {
  red: {
    label: 'DARURAT',
    color: 'bg-red-600',
    icon: '🚨',
    description: 'Ini adalah kasus darurat. Segera menuju IGD.'
  },
  yellow: {
    label: 'URGEN',
    color: 'bg-yellow-600',
    icon: '⚠️',
    description: 'Kondisi memerlukan perhatian segera.'
  },
  green: {
    label: 'TIDAK MENDESAK',
    color: 'bg-green-600',
    icon: '✅',
    description: 'Kondisi tidak terlalu mendesak.'
  },
  blue: {
    label: 'INFORMASI',
    color: 'bg-blue-600',
    icon: 'ℹ️',
    description: 'Silakan hubungi puskesmas terdekat untuk konsultasi lebih lanjut.'
  }
}

export default function ConfirmationScreen({ onReset }: ConfirmationScreenProps) {
  const { patient, triage } = useSessionStore()
  const audioRef = useRef<HTMLAudioElement>(null)

  useEffect(() => {
    // Announce result using text-to-speech
    if (triage) {
      const message = `
        Hasil triage: 
        Pasien ${patient?.name}, 
        Tingkat kedaruratan: ${triageLevelInfo[triage.triageLevel].label},
        Rekomendasi poli: ${triage.recommendedPoli},
        Silakan menuju ${triage.recommendedPoli} untuk pemeriksaan lebih lanjut.
      `
      announceMessage(message)
    }
  }, [patient, triage])

  const announceMessage = (text: string) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = 'id-ID'
      window.speechSynthesis.speak(utterance)
    }
  }

  if (!patient || !triage) {
    return <div>Loading...</div>
  }

  const level = triageLevelInfo[triage.triageLevel]

  return (
    <motion.div 
      className={`w-full h-screen flex flex-col items-center justify-center p-8 ${level.color} text-white`}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <div className="text-center space-y-8 max-w-2xl">
        <motion.div
          animate={{ scale: [1, 1.1, 1] }}
          transition={{ duration: 1 }}
          className="text-9xl"
        >
          {level.icon}
        </motion.div>

        <div className="space-y-4">
          <h2 className="text-5xl font-bold">
            {level.label}
          </h2>
          <p className="text-3xl">
            {level.description}
          </p>
        </div>

        <div className="bg-white bg-opacity-20 rounded-lg p-8 space-y-4">
          <div className="text-left space-y-3">
            <div className="text-2xl">
              <strong>Nama Pasien:</strong> {patient.name}
            </div>
            <div className="text-2xl">
              <strong>Tingkat Kedaruratan:</strong> {level.label}
            </div>
            <div className="text-2xl">
              <strong>Rekomendasi Poli:</strong> {triage.recommendedPoli}
            </div>
            <div className="text-2xl">
              <strong>Kepercayaan Diagnosis:</strong> {(triage.confidenceScore * 100).toFixed(0)}%
            </div>
          </div>
        </div>

        <div className="bg-white bg-opacity-20 rounded-lg p-6">
          <p className="text-2xl font-semibold">
            📍 Silakan menuju ke <strong>{triage.recommendedPoli}</strong> untuk pemeriksaan lebih lanjut.
          </p>
          <p className="text-xl mt-4">
            Petugas akan membantu Anda di lokasi tersebut.
          </p>
        </div>

        <motion.button
          onClick={onReset}
          className="px-12 py-6 bg-white text-gray-800 text-2xl font-bold rounded-lg hover:bg-gray-100 transition"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          MULAI ULANG
        </motion.button>
      </div>

      {/* Auto-reset after 2 minutes */}
      <AutoResetTimer onReset={onReset} />
    </motion.div>
  )
}

function AutoResetTimer({ onReset }: { onReset: () => void }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onReset()
    }, 2 * 60 * 1000) // 2 minutes

    return () => clearTimeout(timer)
  }, [onReset])

  return null
}
