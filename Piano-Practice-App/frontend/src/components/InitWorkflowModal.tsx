import { useApp } from '../contexts/AppContext'

export function InitWorkflowModal() {
  const { initWorkflow } = useApp()
  if (!initWorkflow) return null
  const step = initWorkflow.step
  const prompt = step === 'low' ? 'Play the lowest note on your keyboard.' : 'Now play the highest note on your keyboard.'
  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        background: 'rgba(0,0,0,0.7)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 100,
      }}
    >
      <div
        style={{
          background: '#2a2a2a',
          padding: 32,
          borderRadius: 8,
          maxWidth: 360,
          textAlign: 'center',
        }}
      >
        <h3 style={{ marginTop: 0 }}>Set up keyboard</h3>
        <p style={{ color: '#ccc' }}>{prompt}</p>
        <p style={{ fontSize: 12, color: '#888' }}>
          {step === 'low' ? 'Step 1 of 2' : 'Step 2 of 2'}
        </p>
      </div>
    </div>
  )
}
