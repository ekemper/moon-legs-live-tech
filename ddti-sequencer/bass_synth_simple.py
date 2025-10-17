#!/usr/bin/env python3
"""
Simple Bass Synthesizer - Low Latency Version
Pure Python sine/sub-bass generation with configurable ADSR
Uses sounddevice with system default routing (same as Spotify)
"""

import numpy as np
import sounddevice as sd
import mido
import sys


class ADSREnvelope:
    """ADSR Envelope Generator"""
    def __init__(self, attack: float = 0.01, decay: float = 0.1, 
                 sustain: float = 0.7, release: float = 0.2, sample_rate: int = 44100):
        """
        Args:
            attack: Attack time in seconds
            decay: Decay time in seconds
            sustain: Sustain level (0.0 to 1.0)
            release: Release time in seconds
            sample_rate: Audio sample rate
        """
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
        self.sample_rate = sample_rate
    
    def generate(self, duration: float) -> np.ndarray:
        """Generate ADSR envelope for given duration"""
        total_samples = int(duration * self.sample_rate)
        attack_samples = int(self.attack * self.sample_rate)
        decay_samples = int(self.decay * self.sample_rate)
        release_samples = int(self.release * self.sample_rate)
        
        # Calculate sustain duration
        sustain_samples = max(0, total_samples - attack_samples - decay_samples - release_samples)
        
        # Generate envelope segments
        envelope = np.zeros(total_samples)
        
        # Attack: 0 -> 1
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Decay: 1 -> sustain level
        if decay_samples > 0:
            envelope[attack_samples:attack_samples + decay_samples] = np.linspace(
                1, self.sustain, decay_samples
            )
        
        # Sustain: constant at sustain level
        if sustain_samples > 0:
            envelope[attack_samples + decay_samples:attack_samples + decay_samples + sustain_samples] = self.sustain
        
        # Release: sustain -> 0
        if release_samples > 0:
            envelope[-release_samples:] = np.linspace(self.sustain, 0, release_samples)
        
        return envelope


class BassSynthesizer:
    """Real-time bass synthesizer using sounddevice with system default"""
    def __init__(self, sample_rate: int = 44100, adsr: ADSREnvelope = None):
        self.sample_rate = sample_rate
        # Use system default output device (same routing as Spotify/afplay)
        sd.default.device = None  # Let system choose
        self.adsr = adsr or ADSREnvelope(
            attack=0.005,   # 5ms attack for punchy bass
            decay=0.1,      # 100ms decay
            sustain=0.7,    # 70% sustain level
            release=0.3,    # 300ms release
            sample_rate=sample_rate
        )
        
    def midi_to_freq(self, note: int) -> float:
        """Convert MIDI note to frequency in Hz"""
        return 440.0 * (2.0 ** ((note - 69) / 12.0))
    
    def generate_bass_note(self, frequency: float, duration: float = 1.0, 
                          velocity: int = 127, waveform: str = 'sine') -> np.ndarray:
        """
        Generate a bass note with ADSR envelope
        
        Args:
            frequency: Frequency in Hz
            duration: Note duration in seconds
            velocity: MIDI velocity (0-127)
            waveform: 'sine', 'triangle', or 'saw'
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        
        # Generate waveform
        if waveform == 'sine':
            wave = np.sin(2 * np.pi * frequency * t)
        elif waveform == 'triangle':
            wave = 2 * np.abs(2 * (frequency * t - np.floor(frequency * t + 0.5))) - 1
        elif waveform == 'saw':
            wave = 2 * (frequency * t - np.floor(frequency * t + 0.5))
        else:
            wave = np.sin(2 * np.pi * frequency * t)
        
        # Apply ADSR envelope
        envelope = self.adsr.generate(duration)
        wave *= envelope
        
        # Apply velocity
        velocity_factor = velocity / 127.0
        wave *= velocity_factor
        
        # Boost volume significantly for external speakers
        wave *= 0.9  # Increased from 0.5 to 0.9 for louder output
        
        return wave.astype(np.float32)
    
    def play_note(self, frequency: float, duration: float = 1.0, 
                  velocity: int = 127, waveform: str = 'sine'):
        """Generate and play a note using sounddevice (low latency)"""
        audio = self.generate_bass_note(frequency, duration, velocity, waveform)
        # Play to system default device (no device number specified = use macOS default routing)
        sd.play(audio, self.sample_rate)


class MIDIBassSynth:
    """MIDI-triggered bass synthesizer"""
    def __init__(self, input_port: str, note_sequence: list, 
                 waveform: str = 'sine', note_duration: float = 0.5):
        """
        Args:
            input_port: MIDI input port name
            note_sequence: List of MIDI notes to cycle through
            waveform: Waveform type ('sine', 'triangle', 'saw')
            note_duration: Duration of each note in seconds
        """
        self.input_port_name = input_port
        self.note_sequence = note_sequence
        self.current_index = 0
        self.waveform = waveform
        self.note_duration = note_duration
        
        # Initialize synthesizer
        self.synth = BassSynthesizer()
        
    def get_next_note(self) -> int:
        """Get next note in sequence"""
        note = self.note_sequence[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.note_sequence)
        return note
    
    def process_midi(self, msg: mido.Message):
        """Process incoming MIDI message"""
        if msg.type == 'note_on' and msg.velocity > 0:
            # Get next note in sequence
            midi_note = self.get_next_note()
            frequency = self.synth.midi_to_freq(midi_note)
            
            # Play the note
            self.synth.play_note(
                frequency=frequency,
                duration=self.note_duration,
                velocity=msg.velocity,
                waveform=self.waveform
            )
            
            print(f"🎵 {self.get_note_name(midi_note)} ({frequency:.1f} Hz) "
                  f"vel:{msg.velocity} [Step {self.current_index}/{len(self.note_sequence)}]")
    
    def get_note_name(self, note: int) -> str:
        """Get readable note name"""
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (note // 12) - 1
        note_name = note_names[note % 12]
        return f"{note_name}{octave}"
    
    def run(self):
        """Main loop"""
        try:
            print(f"\n🔊 Audio: System default output (same as Spotify)")
            print(f"   Using device: {sd.default.device}")
            print(f"📝 Note sequence: {[self.get_note_name(n) for n in self.note_sequence]}")
            print(f"🎸 Waveform: {self.waveform}")
            print(f"⏱️  Note duration: {self.note_duration}s")
            print(f"⚡ Low latency mode")
            print(f"🎵 Listening for triggers...\n")
            
            # Open MIDI input
            with mido.open_input(self.input_port_name) as inport:
                for msg in inport:
                    self.process_midi(msg)
                    
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down...")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


def main():
    # Import config
    try:
        import config
        NOTE_SEQUENCE = config.NOTE_SEQUENCE
        INPUT_PORT = config.INPUT_PORT
    except ImportError:
        NOTE_SEQUENCE = [36, 40, 43, 48]  # C1 → E1 → G1 → C2
        INPUT_PORT = "TriggerIO MIDI Out"
    
    # ===== CONFIGURATION =====
    WAVEFORM = 'sine'        # 'sine', 'triangle', or 'saw'
    NOTE_DURATION = 0.5      # Duration in seconds
    
    # ADSR Configuration
    ADSR_CONFIG = ADSREnvelope(
        attack=0.005,   # 5ms - punchy attack
        decay=0.1,      # 100ms decay
        sustain=0.7,    # 70% sustain level
        release=0.3,    # 300ms release tail
        sample_rate=44100
    )
    
    print("=" * 60)
    print("🎸 DDTI Bass Synthesizer - Low Latency")
    print("=" * 60)
    
    print(f"\nADSR: A={ADSR_CONFIG.attack*1000:.0f}ms "
          f"D={ADSR_CONFIG.decay*1000:.0f}ms "
          f"S={ADSR_CONFIG.sustain*100:.0f}% "
          f"R={ADSR_CONFIG.release*1000:.0f}ms")
    
    # Create synth
    synth = MIDIBassSynth(
        input_port=INPUT_PORT,
        note_sequence=NOTE_SEQUENCE,
        waveform=WAVEFORM,
        note_duration=NOTE_DURATION
    )
    
    # Override ADSR if needed
    synth.synth.adsr = ADSR_CONFIG
    
    synth.run()


if __name__ == "__main__":
    main()
