'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import AuthScreen from '@/components/screens/AuthScreen'
import TriageScreen from '@/components/screens/TriageScreen'
import ConfirmationScreen from '@/components/screens/ConfirmationScreen'
import { useSessionStore } from '@/services/session-store'

type KioskScreen = 'welcome' | 'auth' | 'triage' | 'confirmation' | 'queue'

export default function Home() {
  const [currentScreen, setCurrentScreen] = useState<KioskScreen>('welcome')
  const { patient, startSession, endSession } = useSessionStore()

  useEffect(() => {
    // Auto-idle timeout (5 minutes)
    const idleTimer = setTimeout(() => {
      if (currentScreen !== 'welcome') {
        endSession()
        setCurrentScreen('welcome')
      }
    }, 5 * 60 * 1000)

    return () => clearTimeout(idleTimer)
  }, [currentScreen, endSession])

  const handleStartSession = () => {
    startSession()
    setCurrentScreen('auth')
  }

  const handleAuthComplete = () => {
    setCurrentScreen('triage')
  }

  const handleTriageComplete = () => {
    setCurrentScreen('confirmation')
  }

  return (
    <div className="w-full h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {currentScreen === 'welcome' && (
        <WelcomeScreen onStart={handleStartSession} />
      )}
      
      {currentScreen === 'auth' && (
        <AuthScreen onComplete={handleAuthComplete} />
      )}
      
      {currentScreen === 'triage' && (
        <TriageScreen onComplete={handleTriageComplete} />
      )}
      
      {currentScreen === 'confirmation' && (
        <ConfirmationScreen 
          onReset={() => {
            endSession()
            setCurrentScreen('welcome')
          }}
        />
      )}
    </div>
  )
}

interface WelcomeScreenProps {
  onStart: () => void
}

function WelcomeScreen({ onStart }: WelcomeScreenProps) {
  return (
    <motion.div 
      className="w-full h-screen flex flex-col items-center justify-center"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className="text-center space-y-8">
        <motion.div
          animate={{ y: [0, -10, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <div className="text-6xl mb-4">👋</div>
          <h1 className="text-5xl font-bold text-gray-800">
            Selamat Datang
          </h1>
        </motion.div>
        
        <p className="text-2xl text-gray-600 max-w-2xl">
          Sistem Asisten AI Pelayanan Pelanggan RSI A. Yani Surabaya
        </p>
        
        <div className="space-y-4 mt-8">
          <p className="text-xl text-gray-700">
            Silakan klik tombol di bawah untuk memulai. Anda akan diberi pilihan masuk dengan sidik jari, NIK, atau pengenalan wajah, lalu dapat memilih memakai suara atau tombol interaktif.
          </p>
          
          <motion.button
            onClick={onStart}
            className="px-12 py-6 bg-blue-600 text-white text-3xl font-bold rounded-lg hover:bg-blue-700 transition"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            MULAI KIOSK
          </motion.button>
        </div>
      </div>
    </motion.div>
  )
}
