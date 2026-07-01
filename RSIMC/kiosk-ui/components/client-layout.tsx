'use client'

import { ReactNode } from 'react'
import { SessionProviderProps } from '@/services/session-store'

export function SessionProvider({ children }: SessionProviderProps) {
  return <>{children}</>
}

export default function ClientLayout({ children }: { children: ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>
}
