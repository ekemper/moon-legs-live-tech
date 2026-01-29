import { ErrorDisplay } from './ErrorDisplay'
import { InitWorkflowModal } from './InitWorkflowModal'
import { LessonDisplay } from './LessonDisplay'
import { MIDIStatus } from './MIDIStatus'
import { NextLessonButton } from './NextLessonButton'
import { VolumeControl } from './VolumeControl'
import { VirtualKeyboard } from './VirtualKeyboard'
import { useApp } from '../contexts/AppContext'

export function MainPage() {
  const { devices, selectDevice, selectedDeviceId } = useApp()
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <ErrorDisplay />
      <header style={{ padding: '12px 16px', borderBottom: '1px solid #333' }}>
        <h1 style={{ margin: 0, fontSize: '1.25rem' }}>Piano Practice</h1>
        <MIDIStatus />
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
