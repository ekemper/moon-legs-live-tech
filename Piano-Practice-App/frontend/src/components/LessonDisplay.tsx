import { useApp } from '../contexts/AppContext'

export function LessonDisplay() {
  const { lesson } = useApp()
  if (!lesson) return <div style={{ padding: 16 }}>No lesson loaded.</div>
  const { key: keyName, name, type, noteNames, intervals, historicalBlurb } = lesson
  return (
    <div style={{ padding: 16, maxWidth: 560 }}>
      <div style={{ fontSize: '1.1rem', marginBottom: 8 }}>
        <strong>{keyName} {name}</strong> <span style={{ color: '#888', textTransform: 'capitalize' }}>({type})</span>
      </div>
      <div style={{ marginBottom: 8 }}>
        Notes: {Array.isArray(noteNames) ? noteNames.join(', ') : '—'}
      </div>
      <div style={{ marginBottom: 8, color: '#aaa' }}>
        Intervals: {Array.isArray(intervals) ? intervals.join(', ') : '—'}
      </div>
      {historicalBlurb && (
        <div style={{ fontSize: '0.9rem', color: '#888', marginTop: 12 }}>{historicalBlurb}</div>
      )}
    </div>
  )
}
