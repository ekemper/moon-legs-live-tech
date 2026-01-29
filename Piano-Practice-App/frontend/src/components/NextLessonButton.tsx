import { useApp } from '../contexts/AppContext'

export function NextLessonButton() {
  const { nextLesson } = useApp()
  return (
    <button
      type="button"
      onClick={nextLesson}
      style={{
        padding: '10px 20px',
        fontSize: '1rem',
        background: '#2a4a6a',
        color: '#eee',
        border: 'none',
        borderRadius: 6,
        cursor: 'pointer',
      }}
    >
      Next lesson
    </button>
  )
}
