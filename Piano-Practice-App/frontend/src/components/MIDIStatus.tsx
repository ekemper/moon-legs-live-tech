import { useApp } from '../contexts/AppContext'

export function MIDIStatus() {
  const { selectedDeviceId, selectedDeviceConfig, connected, error } = useApp()
  return (
    <div style={{ padding: '8px 12px', fontSize: '14px', color: '#aaa' }}>
      {!connected && <span>{error || 'Connecting…'}</span>}
      {connected && selectedDeviceId && (
        <span>
          {selectedDeviceId}
          {selectedDeviceConfig && ` (${selectedDeviceConfig.keyCount} keys, ${selectedDeviceConfig.lowNote}–${selectedDeviceConfig.highNote})`}
        </span>
      )}
    </div>
  )
}
