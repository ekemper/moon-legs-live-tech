import { useApp } from '../contexts/AppContext'

export function ErrorDisplay() {
  const { error, clearError } = useApp()
  if (!error) return null
  return (
    <div
      role="alert"
      style={{
        padding: '12px 16px',
        background: '#4a1a1a',
        color: '#ffb0b0',
        borderBottom: '1px solid #6a2a2a',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}
    >
      <span>{error}</span>
      <button type="button" onClick={clearError} style={{ background: 'transparent', border: '1px solid', color: 'inherit', cursor: 'pointer', padding: '4px 8px' }}>
        Dismiss
      </button>
    </div>
  )
}
