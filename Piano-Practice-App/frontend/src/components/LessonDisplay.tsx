import { useApp } from '../contexts/AppContext'

export function LessonDisplay() {
  const { lesson } = useApp()
  if (!lesson) return <div style={{ padding: 16 }}>No lesson loaded.</div>
  const { key: keyName, octave, name, type, noteNames, intervalLabels, intervals, historicalBlurb } = lesson
  const keyLabel = octave != null ? `${keyName}${octave}` : keyName
  const intervalDisplay = Array.isArray(intervalLabels) && intervalLabels.length
    ? intervalLabels.join(', ')
    : Array.isArray(intervals) ? intervals.join(', ') : '—'
  return (
    <div style={{ padding: 16, maxWidth: 560 }}>
      <div style={{ fontSize: '1.1rem', marginBottom: 8 }}>
        <strong>{keyLabel} {name}</strong> <span style={{ color: '#888', textTransform: 'capitalize' }}>({type})</span>
      </div>
      <div style={{ marginBottom: 8 }}>
        Notes: {Array.isArray(noteNames) ? noteNames.join(', ') : '—'}
      </div>
      <div style={{ marginBottom: 8, color: '#aaa' }}>
        Scale degrees: {intervalDisplay}
      </div>
      {historicalBlurb && (
        <div style={{ fontSize: '0.9rem', color: '#888', marginTop: 12 }}>{historicalBlurb}</div>
      )}
    </div>
  )
}
