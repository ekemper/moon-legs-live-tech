#!/usr/bin/env python3
"""Debug version with verbose output"""

import numpy as np
import mido
import wave
import subprocess
import tempfile
import os

sample_rate = 44100
note_sequence = [36, 40, 43, 48]  # C1 → E1 → G1 → C2
current_index = 0

def midi_to_freq(note):
    return 440.0 * (2.0 ** ((note - 69) / 12.0))

def get_note_name(note):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (note // 12) - 1
    note_name = note_names[note % 12]
    return f"{note_name}{octave}"

print("=" * 60)
print("🔍 DEBUG Bass Synthesizer")
print("=" * 60)
print("\n✅ Script started")
print(f"📝 Note sequence: {[get_note_name(n) for n in note_sequence]}")
print("🎵 Hit your drum pad!\n")

try:
    with mido.open_input('TriggerIO MIDI Out') as inport:
        print("✅ MIDI port opened successfully")
        print("Waiting for messages...\n")
        
        for msg in inport:
            print(f"📥 Received: {msg}")
            
            if msg.type == 'note_on' and msg.velocity > 0:
                # Get next note
                midi_note = note_sequence[current_index]
                current_index = (current_index + 1) % len(note_sequence)
                frequency = midi_to_freq(midi_note)
                
                print(f"   → Playing {get_note_name(midi_note)} ({frequency:.1f} Hz)")
                
                # Generate audio
                print(f"   → Generating audio...")
                duration = 0.5
                t = np.linspace(0, duration, int(sample_rate * duration))
                wave_data = np.sin(2 * np.pi * frequency * t)
                
                # Add envelope
                attack = int(0.005 * sample_rate)
                release = int(0.1 * sample_rate)
                env = np.ones(len(wave_data))
                env[:attack] = np.linspace(0, 1, attack)
                env[-release:] = np.linspace(1, 0, release)
                wave_data *= env * 0.9
                
                # Convert to int16
                audio_int = (wave_data * 32767).astype(np.int16)
                print(f"   → Audio generated: {len(audio_int)} samples")
                
                # Write WAV file
                tmp_path = f'/tmp/bass_{current_index}.wav'
                print(f"   → Writing to: {tmp_path}")
                
                with wave.open(tmp_path, 'w') as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(sample_rate)
                    wav_file.writeframes(audio_int.tobytes())
                
                print(f"   → WAV file written: {os.path.getsize(tmp_path)} bytes")
                
                # Play with afplay
                print(f"   → Calling afplay...")
                result = subprocess.Popen(['afplay', tmp_path])
                print(f"   ✅ afplay started (PID: {result.pid})")
                print(f"   🔊 SHOULD BE PLAYING NOW!\n")
                
except KeyboardInterrupt:
    print("\n\n👋 Stopped")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

