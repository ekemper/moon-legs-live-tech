import { ErrorDisplay } from './ErrorDisplay'
import { InitWorkflowModal } from './InitWorkflowModal'
import { LessonDisplay } from './LessonDisplay'
import { MIDIStatus } from './MIDIStatus'
import { NextLessonButton } from './NextLessonButton'
import { VolumeControl } from './VolumeControl'
import { VirtualKeyboard } from './VirtualKeyboard'
import { useApp } from '../contexts/AppContext'

export function MainPage() {
  const { devices, selectDevice, selectedDeviceId, showRootIndicator, setShowRootIndicator } = useApp()
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <ErrorDisplay />
      <header style={{ padding: '12px 16px', borderBottom: '1px solid #333' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 16 }}>
          <div>
            <h1 style={{ margin: 0, fontSize: '1.25rem' }}>Piano Practice</h1>
            <MIDIStatus />
          </div>
          <label style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 14, whiteSpace: 'nowrap', flexShrink: 0 }}>
            <span style={{ color: '#aaa' }}>Show root</span>
            <input
              type="checkbox"
              checked={showRootIndicator}
              onChange={(e) => setShowRootIndicator(e.target.checked)}
              style={{ width: 18, height: 18, accentColor: '#4a90d9' }}
              title="Show blue triangle above the lesson root note on the keyboard"
            />
          </label>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap', marginTop: 8 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <label htmlFor="midi-device" style={{ fontSize: 14 }}>MIDI device</label>
            <select
              id="midi-device"
              value={selectedDeviceId ?? ''}
              onChange={(e) => {
                const id = e.target.value
                if (id) selectDevice(id)
              }}
              style={{
                padding: '6px 10px',
                background: '#2a2a2a',
                color: '#eee',
                border: '1px solid #555',
                borderRadius: 4,
                minWidth: 200,
              }}
            >
              <option value="">— Select —</option>
              {devices.map((name) => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
            </select>
          </div>
          <VolumeControl />
          <NextLessonButton />
        </div>
      </header>
      <main style={{ flex: 1, padding: 16 }}>
        <LessonDisplay />
        <VirtualKeyboard />
      </main>
      <InitWorkflowModal />
    </div>
  )
}
