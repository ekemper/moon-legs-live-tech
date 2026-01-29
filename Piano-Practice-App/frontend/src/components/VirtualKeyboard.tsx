import { useCallback, useState } from 'react'
import { useApp } from '../contexts/AppContext'

const PITCH_CLASS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
function noteName(midi: number): string {
  return PITCH_CLASS[midi % 12] + String(Math.floor(midi / 12) - 1)
}

function isBlack(midi: number): boolean {
  const pc = midi % 12
  return pc === 1 || pc === 3 || pc === 6 || pc === 8 || pc === 10
}

export function VirtualKeyboard() {
  const { send, selectedDeviceConfig, activeNotes, noteCorrect, lesson } = useApp()
  const [hoverNote, setHoverNote] = useState<number | null>(null)

  const lowNote = selectedDeviceConfig?.lowNote ?? 36
  const highNote = selectedDeviceConfig?.highNote ?? 96
  const keyCount = highNote - lowNote + 1
  const keys = Array.from({ length: keyCount }, (_, i) => lowNote + i)

  const sendVirtualNote = useCallback(
    (note: number, on: boolean) => {
      send({ type: 'virtual_note', note, on, velocity: 80 })
    },
    [send],
  )

  const getKeyStyle = (note: number): React.CSSProperties => {
    const active = activeNotes.get(note)
    const correct = noteCorrect.get(note)
    const black = isBlack(note)
    let bg = black ? '#2a2a2a' : '#f0f0f0'
    let color = black ? '#ddd' : '#222'
    if (active !== undefined) {
      bg = correct ? '#2d5a2d' : '#5a2d2d'
      color = '#eee'
    }
    return {
      background: bg,
      color,
      border: '1px solid #444',
      minWidth: 22,
      height: 100,
      cursor: 'pointer',
      userSelect: 'none' as const,
      display: 'flex',
      alignItems: 'flex-end',
      justifyContent: 'center',
      paddingBottom: 4,
      fontSize: 10,
    }
  }

  return (
    <div style={{ margin: '16px 0' }}>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 1, justifyContent: 'center' }}>
        {keys.map((note) => (
          <div
            key={note}
            role="button"
            tabIndex={0}
            title={noteName(note)}
            style={getKeyStyle(note)}
            onMouseDown={() => sendVirtualNote(note, true)}
            onMouseUp={() => sendVirtualNote(note, false)}
            onMouseLeave={() => {
              sendVirtualNote(note, false)
              setHoverNote(null)
            }}
            onMouseEnter={() => setHoverNote(note)}
          >
            {hoverNote === note ? noteName(note) : ''}
          </div>
        ))}
      </div>
      <div style={{ fontSize: 12, color: '#666', marginTop: 4 }}>
        {keyCount} keys ({lowNote}–{highNote}). Hover for note name.
      </div>
    </div>
  )
}
