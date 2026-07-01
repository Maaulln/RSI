'use client'

import { ReactNode } from 'react'
import { create } from 'zustand'

interface Patient {
  id: string
  nik: string
  name: string
  dateOfBirth?: string
  bpjsNumber?: string
}

interface Session {
  id: string
  patient: Patient | null
  startedAt: Date
  nodeId: string
  authMethod?: 'fingerprint' | 'face' | 'nik_ocr' | 'manual'
}

interface TriageResult {
  recommendedPoli: string
  triageLevel: 'red' | 'yellow' | 'green' | 'blue'
  confidenceScore: number
  symptoms: string[]
}

interface SessionStore {
  session: Session | null
  patient: Patient | null
  triage: TriageResult | null
  startSession: () => void
  endSession: () => void
  setPatient: (patient: Patient) => void
  setTriage: (triage: TriageResult) => void
  clearSession: () => void
}

export const useSessionStore = create<SessionStore>((set) => ({
  session: null,
  patient: null,
  triage: null,

  startSession: () => {
    set({
      session: {
        id: `session_${Date.now()}`,
        patient: null,
        startedAt: new Date(),
        nodeId: process.env.NODE_ID || 'NODE-01'
      }
    })
  },

  endSession: () => {
    set({ session: null, patient: null, triage: null })
  },

  setPatient: (patient: Patient) => {
    set({ patient })
  },

  setTriage: (triage: TriageResult) => {
    set({ triage })
  },

  clearSession: () => {
    set({ session: null, patient: null, triage: null })
  }
}))

export interface SessionProviderProps {
  children: ReactNode
}

export function SessionProvider({ children }: SessionProviderProps) {
  return <>{children}</>
}
