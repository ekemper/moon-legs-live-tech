import { useApp } from '../contexts/AppContext'

export function NextLessonButton() {
  const { nextLesson, connected } = useApp()
  return (
    <button
      type="button"
      onClick={nextLesson}
      disabled={!connected}
      title={!connected ? 'Connect to use' : 'Load a new random lesson'}
      style={{
        padding: '10px 20px',
        fontSize: '1rem',
        background: connected ? '#2a4a6a' : '#444',
        color: '#eee',
        border: 'none',
        borderRadius: 6,
        cursor: connected ? 'pointer' : 'not-allowed',
        opacity: connected ? 1 : 0.7,
      }}
    >
      Next lesson
    </button>
  )
}
