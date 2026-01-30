import { useCallback, useMemo, useState } from 'react'
import { useApp } from '../contexts/AppContext'
import './VirtualKeyboard.css'

const PITCH_CLASS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
const WHITE_PC = new Set([0, 2, 4, 5, 7, 9, 11]) // C, D, E, F, G, A, B

function noteName(midi: number): string {
  return PITCH_CLASS[midi % 12] + String(Math.floor(midi / 12) - 1)
}

function isBlack(midi: number): boolean {
  return !WHITE_PC.has(midi % 12)
}

// Count white keys from A0 (MIDI 21) up to and including midi
function whiteKeyIndex(midi: number): number {
  let count = 0
  for (let n = 21; n <= midi; n++) {
    if (WHITE_PC.has(n % 12)) count++
  }
  return count
}

// 88-key standard: A0 (21) to C8 (108)
const DEFAULT_88_LOW = 21
const DEFAULT_88_HIGH = 108

export function VirtualKeyboard() {
  const { send, selectedDeviceConfig, activeNotes, lesson, showRootIndicator } = useApp()
  const [hoverNote, setHoverNote] = useState<number | null>(null)
  const rootMidi = lesson?.midiNotes?.[0] ?? null

  const lowNote = selectedDeviceConfig?.lowNote ?? DEFAULT_88_LOW
  const highNote = selectedDeviceConfig?.highNote ?? DEFAULT_88_HIGH
  const keyCount = highNote - lowNote + 1
  const keys = useMemo(() => Array.from({ length: keyCount }, (_, i) => lowNote + i), [keyCount, lowNote])

  const lessonMidiSet = useMemo(
    () => new Set(lesson?.midiNotes ?? []),
    [lesson?.midiNotes],
  )

  const sendVirtualNote = useCallback(
    (note: number, on: boolean) => {
      send({ type: 'virtual_note', note, on, velocity: 80 })
    },
    [send],
  )

  const whiteKeys = useMemo(() => keys.filter((n) => !isBlack(n)), [keys])
  const blackKeys = useMemo(() => keys.filter((n) => isBlack(n)), [keys])

  const getKeyState = useCallback(
    (note: number) => {
      const isPressed = activeNotes.get(note) === true
      const isHovered = hoverNote === note
      const showFeedback = isPressed || isHovered
      const correct = lessonMidiSet.has(note)
      return { showFeedback, correct, isBlack: isBlack(note) }
    },
    [activeNotes, hoverNote, lessonMidiSet],
  )

  return (
    <div className="virtual-keyboard">
      <div className="piano" style={{ '--white-count': whiteKeys.length } as React.CSSProperties}>
        <div className="piano-whites">
          {whiteKeys.map((note) => {
            const { showFeedback, correct } = getKeyState(note)
            const feedbackClass = showFeedback ? (correct ? 'correct' : 'incorrect') : ''
            const isRoot = showRootIndicator && rootMidi !== null && note === rootMidi
            return (
              <div
                key={note}
                className={`key white ${feedbackClass} ${isRoot ? 'has-root-indicator' : ''}`}
                role="button"
                tabIndex={0}
                title={noteName(note)}
                onMouseDown={(e) => {
                  e.preventDefault()
                  sendVirtualNote(note, true)
                }}
                onMouseUp={() => sendVirtualNote(note, false)}
                onMouseLeave={() => {
                  sendVirtualNote(note, false)
                  setHoverNote(null)
                }}
                onMouseEnter={() => setHoverNote(note)}
              >
                {isRoot && <span className="root-indicator" aria-hidden />}
                {hoverNote === note ? noteName(note) : ''}
              </div>
            )
          })}
        </div>
        <div className="piano-blacks">
          {blackKeys.map((note) => {
            const leftWhite = whiteKeyIndex(note - 1) - 1
            const { showFeedback, correct } = getKeyState(note)
            const feedbackClass = showFeedback ? (correct ? 'correct' : 'incorrect') : ''
            const isRoot = showRootIndicator && rootMidi !== null && note === rootMidi
            return (
              <div
                key={note}
                className={`key black ${feedbackClass} ${isRoot ? 'has-root-indicator' : ''}`}
                role="button"
                tabIndex={0}
                title={noteName(note)}
                style={{ '--black-left': leftWhite } as React.CSSProperties}
                onMouseDown={(e) => {
                  e.preventDefault()
                  sendVirtualNote(note, true)
                }}
                onMouseUp={() => sendVirtualNote(note, false)}
                onMouseLeave={() => {
                  sendVirtualNote(note, false)
                  setHoverNote(null)
                }}
                onMouseEnter={() => setHoverNote(note)}
              >
                {isRoot && <span className="root-indicator" aria-hidden />}
                {hoverNote === note ? noteName(note) : ''}
              </div>
            )
          })}
        </div>
      </div>
      <div className="virtual-keyboard-footer">
        {keyCount} keys ({lowNote}–{highNote}). Hover for note name.
      </div>
    </div>
  )
}
