import React, { createContext, useCallback, useContext, useEffect, useRef, useState } from 'react'

export interface Lesson {
  type: string
  key: string
  octave?: number
  name: string
  intervals: number[]
  intervalLabels?: string[]  // scale degrees: 1, ♭3, 5, etc. (from backend)
  noteNames: string[]
  midiNotes: number[]
  historicalBlurb: string
}

export interface DeviceConfig {
  lowNote: number
  highNote: number
  keyCount: number
}

const SHOW_ROOT_INDICATOR_KEY = 'piano-practice-show-root-indicator'

function getInitialShowRootIndicator(): boolean {
  try {
    const v = localStorage.getItem(SHOW_ROOT_INDICATOR_KEY)
    return v === 'true'
  } catch {
    return false
  }
}

type AppState = {
  connected: boolean
  error: string | null
  lesson: Lesson | null
  devices: string[]
  deviceConfigs: Record<string, DeviceConfig>
  selectedDeviceId: string | null
  selectedDeviceConfig: DeviceConfig | null
  activeNotes: Map<number, boolean>
  noteCorrect: Map<number, boolean>
  volume: number
  showRootIndicator: boolean
  initWorkflow: { deviceId: string; step: 'low' | 'high' } | null
}

const defaultState: AppState = {
  connected: false,
  error: null,
  lesson: null,
  devices: [],
  deviceConfigs: {},
  selectedDeviceId: null,
  selectedDeviceConfig: null,
  activeNotes: new Map(),
  noteCorrect: new Map(),
  volume: 0.8,
  showRootIndicator: getInitialShowRootIndicator(),
  initWorkflow: null,
}

type AppContextValue = AppState & {
  ws: WebSocket | null
  send: (obj: object) => void
  selectDevice: (deviceId: string) => void
  nextLesson: () => void
  setVolume: (value: number) => void
  setShowRootIndicator: (value: boolean) => void
  clearError: () => void
}

const AppContext = createContext<AppContextValue | null>(null)

function getWsUrl(): string {
  const proto = location.protocol === 'https:' ? 'wss:' : 'ws:'
  return `${proto}//${location.host}/ws`
}

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [ws, setWs] = useState<WebSocket | null>(null)
  const wsRef = useRef<WebSocket | null>(null)
  const [state, setState] = useState<AppState>(defaultState)
  const setStateRef = useRef(setState)
  setStateRef.current = setState

  const send = useCallback((obj: object) => {
    const s = wsRef.current
    if (s && s.readyState === WebSocket.OPEN) {
      s.send(JSON.stringify(obj))
    }
  }, [])

  const selectDevice = useCallback((deviceId: string) => {
    send({ type: 'midi_device_select', deviceId })
  }, [send])

  const nextLesson = useCallback(() => {
    send({ type: 'next_lesson' })
  }, [send])

  const setVolume = useCallback((value: number) => {
    const v = Math.max(0, Math.min(1, Number(value)))
    setState((prev) => ({ ...prev, volume: v }))
    send({ type: 'set_volume', value: v })
  }, [send])

  const setShowRootIndicator = useCallback((value: boolean) => {
    setState((prev) => ({ ...prev, showRootIndicator: value }))
    try {
      localStorage.setItem(SHOW_ROOT_INDICATOR_KEY, String(value))
    } catch {
      // ignore
    }
  }, [])

  const clearError = useCallback(() => {
    setState((prev) => ({ ...prev, error: null }))
  }, [])

  useEffect(() => {
    const url = getWsUrl()
    const socket = new WebSocket(url)
    wsRef.current = socket

    socket.onopen = () => {
      setState((prev) => ({ ...prev, connected: true, error: null }))
    }

    socket.onclose = () => {
      if (wsRef.current === socket) wsRef.current = null
      setWs(null)
      setState((prev) => ({ ...prev, connected: false, error: 'Disconnected. Refresh to reconnect.' }))
    }

    socket.onerror = () => {
      setState((prev) => ({ ...prev, error: 'WebSocket error.' }))
    }

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        const t = data.type
        if (t === 'lesson') {
          setStateRef.current((prev) => ({ ...prev, lesson: data.lesson ?? null }))
        } else if (t === 'midi_devices') {
          setStateRef.current((prev) => ({ ...prev, devices: data.devices || [] }))
        } else if (t === 'device_configs') {
          setStateRef.current((prev) => ({ ...prev, deviceConfigs: data.configs || {} }))
        } else if (t === 'midi_device') {
          setStateRef.current((prev) => ({
            ...prev,
            selectedDeviceId: data.deviceId,
            selectedDeviceConfig: data.config || null,
            initWorkflow: null,
          }))
        } else if (t === 'init_workflow') {
          setStateRef.current((prev) => ({ ...prev, initWorkflow: { deviceId: data.deviceId, step: 'low' } }))
        } else if (t === 'init_step') {
          setStateRef.current((prev) => ({
            ...prev,
            initWorkflow: prev.initWorkflow ? { ...prev.initWorkflow, step: data.step || 'high' } : null,
          }))
        } else if (t === 'init_complete') {
          setStateRef.current((prev) => {
            const deviceId = prev.initWorkflow?.deviceId ?? prev.selectedDeviceId ?? ''
            return {
              ...prev,
              selectedDeviceId: deviceId || prev.selectedDeviceId,
              selectedDeviceConfig: data.config,
              initWorkflow: null,
              deviceConfigs: { ...prev.deviceConfigs, [deviceId]: data.config },
            }
          })
        } else if (t === 'midi_note') {
          const note = data.note as number
          const on = data.on as boolean
          const isCorrect = data.isCorrect as boolean
          setStateRef.current((prev) => {
            const nextActive = new Map(prev.activeNotes)
            const nextCorrect = new Map(prev.noteCorrect)
            if (on) {
              nextActive.set(note, true)
              nextCorrect.set(note, isCorrect)
            } else {
              nextActive.set(note, false)
              nextCorrect.set(note, isCorrect)
            }
            return { ...prev, activeNotes: nextActive, noteCorrect: nextCorrect }
          })
        } else if (t === 'volume') {
          setStateRef.current((prev) => ({ ...prev, volume: data.value ?? prev.volume }))
        } else if (t === 'error') {
          setStateRef.current((prev) => ({ ...prev, error: data.message || 'Error' }))
        }
      } catch {
        // ignore parse errors
      }
    }

    setWs(socket)
    return () => {
      if (wsRef.current === socket) wsRef.current = null
      // Avoid close() while CONNECTING: React Strict Mode unmounts immediately and would
      // trigger "WebSocket is closed before the connection is established". If already open, close.
      // If still connecting, close once it opens so we don't leave a dangling connection.
      if (socket.readyState === WebSocket.OPEN) {
        socket.close()
      } else if (socket.readyState === WebSocket.CONNECTING) {
        socket.onopen = () => socket.close()
      }
    }
  }, [])

  const value: AppContextValue = {
    ...state,
    ws,
    send,
    selectDevice,
    nextLesson,
    setVolume,
    setShowRootIndicator,
    clearError,
  }

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used within AppProvider')
  return ctx
}
