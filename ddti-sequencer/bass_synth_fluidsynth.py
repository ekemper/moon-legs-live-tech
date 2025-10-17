#!/usr/bin/env python3
"""
Bass Synthesizer using FluidSynth + SoundFont
More realistic bass sounds using sample-based synthesis
Requires FluidSynth and a SoundFont file
"""

import mido
import sys
import time

try:
    import fluidsynth
except ImportError:
    print("❌ FluidSynth not installed!")
    print("\nInstall with:")
    print("  Mac:   brew install fluidsynth && pip install pyfluidsynth")
    print("  Linux: sudo apt install fluidsynth && pip install pyfluidsynth")
    sys.exit(1)


class FluidSynthBass:
    """FluidSynth-based bass synthesizer"""
    def __init__(self, soundfont_path: str, input_port: str, note_sequence: list):
        """
        Args:
            soundfont_path: Path to .sf2 SoundFont file
            input_port: MIDI input port name
            note_sequence: List of MIDI notes to cycle through
        """
        self.soundfont_path = soundfont_path
        self.input_port_name = input_port
        self.note_sequence = note_sequence
        self.current_index = 0
        
        # Initialize FluidSynth
        self.fs = fluidsynth.Synth()
        self.fs.start(driver='coreaudio')  # Use 'alsa' on Linux
        
        # Load SoundFont
        try:
            self.sfid = self.fs.sfload(soundfont_path)
            print(f"✅ Loaded SoundFont: {soundfont_path}")
        except Exception as e:
            print(f"❌ Failed to load SoundFont: {e}")
            sys.exit(1)
        
        # Select bass program (typically program 32-39 are bass instruments)
        # 32 = Acoustic Bass, 33 = Electric Bass (finger), 34 = Electric Bass (pick)
        # 35 = Fretless Bass, 36 = Slap Bass 1, 37 = Slap Bass 2
        # 38 = Synth Bass 1, 39 = Synth Bass 2
        self.fs.program_select(0, self.sfid, 0, 38)  # Synth Bass 1
        
        print(f"✅ Selected instrument: Synth Bass 1 (program 38)")
    
    def get_next_note(self) -> int:
        """Get next note in sequence"""
        note = self.note_sequence[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.note_sequence)
        return note
    
    def get_note_name(self, note: int) -> str:
        """Get readable note name"""
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (note // 12) - 1
        note_name = note_names[note % 12]
        return f"{note_name}{octave}"
    
    def process_midi(self, msg: mido.Message):
        """Process incoming MIDI message"""
        if msg.type == 'note_on' and msg.velocity > 0:
            # Get next note in sequence
            midi_note = self.get_next_note()
            
            # Play note on FluidSynth
            self.fs.noteon(0, midi_note, msg.velocity)
            
            print(f"🎵 Playing {self.get_note_name(midi_note)} (velocity: {msg.velocity}) "
                  f"[Step {self.current_index}/{len(self.note_sequence)}]")
            
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            # Note off - let the previous note decay naturally
            prev_index = (self.current_index - 1) % len(self.note_sequence)
            prev_note = self.note_sequence[prev_index]
            self.fs.noteoff(0, prev_note)
    
    def run(self):
        """Main loop"""
        try:
            print(f"\n📝 Note sequence: {[self.get_note_name(n) for n in self.note_sequence]}")
            print(f"🎵 Listening for triggers...\n")
            
            # Open MIDI input
            with mido.open_input(self.input_port_name) as inport:
                for msg in inport:
                    self.process_midi(msg)
                    
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down...")
        finally:
            self.fs.delete()


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
    # Path to SoundFont file
    # Download free SoundFonts from:
    # - https://musical-artifacts.com/artifacts?tags=soundfont
    # - https://schristiancollins.com/generaluser.php (GeneralUser GS)
    
    SOUNDFONT_PATH = "/usr/local/share/soundfonts/default.sf2"  # Adjust path
    
    print("=" * 60)
    print("🎸 DDTI Bass Synthesizer - FluidSynth")
    print("=" * 60)
    
    # Create synth
    synth = FluidSynthBass(
        soundfont_path=SOUNDFONT_PATH,
        input_port=INPUT_PORT,
        note_sequence=NOTE_SEQUENCE
    )
    
    synth.run()


if __name__ == "__main__":
    main()


