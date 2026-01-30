import { useApp } from '../contexts/AppContext'

export function VolumeControl() {
  const { volume, setVolume, connected } = useApp()
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <label htmlFor="volume" style={{ fontSize: 14 }}>Volume</label>
      <input
        id="volume"
        type="range"
        min={0}
        max={1}
        step={0.01}
        value={volume}
        onChange={(e) => setVolume(parseFloat(e.target.value))}
        disabled={!connected}
        title={!connected ? 'Connect to use' : undefined}
        style={{ width: 100, opacity: connected ? 1 : 0.6 }}
      />
      <span style={{ fontSize: 12, color: '#888' }}>{Math.round(volume * 100)}%</span>
    </div>
  )
}
