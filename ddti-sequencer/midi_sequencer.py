#!/usr/bin/env python3
"""
DDTI to Ableton MIDI Note Sequencer
Converts drum triggers into a cycling sequence of bass notes
"""

import mido
import time
import sys
from typing import List


class MIDINoteSequencer:
    def __init__(self, sequence: List[int], input_port_name: str, output_port_name: str):
        """
        Initialize the MIDI note sequencer
        
        Args:
            sequence: List of MIDI note numbers to cycle through (e.g., [36, 38, 40, 43] for C1, D1, E1, F1)
            input_port_name: Name of input MIDI device (your DDTI)
            output_port_name: Name of output virtual MIDI port
        """
        self.sequence = sequence
        self.current_index = 0
        self.input_port_name = input_port_name
        self.output_port_name = output_port_name
        self.input_port = None
        self.output_port = None
        
    def connect(self):
        """Connect to MIDI ports"""
        try:
            # List available ports
            print("\n=== Available MIDI Input Ports ===")
            for i, port in enumerate(mido.get_input_names()):
                print(f"{i}: {port}")
            
            print("\n=== Available MIDI Output Ports ===")
            for i, port in enumerate(mido.get_output_names()):
                print(f"{i}: {port}")
            
            # Open input port (DDTI/TriggerIO)
            print(f"\nOpening input: {self.input_port_name}")
            self.input_port = mido.open_input(self.input_port_name)
            
            # Open output port (Virtual MIDI port for Ableton)
            print(f"Opening output: {self.output_port_name}")
            self.output_port = mido.open_output(self.output_port_name)
            
            print("\n✅ Connected successfully!")
            print(f"📝 Note sequence: {self.get_note_names()}")
            print("🎵 Waiting for triggers...\n")
            
        except Exception as e:
            print(f"❌ Error connecting to MIDI ports: {e}")
            sys.exit(1)
    
    def get_note_names(self) -> str:
        """Convert MIDI note numbers to readable names"""
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        names = []
        for note in self.sequence:
            octave = (note // 12) - 1
            note_name = note_names[note % 12]
            names.append(f"{note_name}{octave}")
        return " → ".join(names)
    
    def get_next_note(self) -> int:
        """Get the next note in the sequence and advance the counter"""
        note = self.sequence[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.sequence)
        return note
    
    def process_message(self, msg: mido.Message):
        """Process incoming MIDI message and send sequenced note"""
        # Only process note_on messages with velocity > 0
        if msg.type == 'note_on' and msg.velocity > 0:
            next_note = self.get_next_note()
            
            # Create new message with sequenced note, preserving velocity and channel
            new_msg = mido.Message(
                'note_on',
                note=next_note,
                velocity=msg.velocity,
                channel=msg.channel
            )
            
            self.output_port.send(new_msg)
            
            # Log the conversion
            print(f"🥁 Trigger {msg.note} (vel: {msg.velocity}) → 🎹 Note {next_note} ({self.get_note_name(next_note)}) [Step {self.current_index}/{len(self.sequence)}]")
        
        # Pass through note_off messages with the last sent note
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            # Send note_off for the previous note in sequence
            prev_index = (self.current_index - 1) % len(self.sequence)
            prev_note = self.sequence[prev_index]
            
            new_msg = mido.Message(
                'note_off',
                note=prev_note,
                velocity=0,
                channel=msg.channel
            )
            self.output_port.send(new_msg)
    
    def get_note_name(self, note: int) -> str:
        """Get readable name for a single note"""
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (note // 12) - 1
        note_name = note_names[note % 12]
        return f"{note_name}{octave}"
    
    def run(self):
        """Main loop - listen and process messages"""
        self.connect()
        
        try:
            for msg in self.input_port:
                self.process_message(msg)
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down...")
        finally:
            if self.input_port:
                self.input_port.close()
            if self.output_port:
                self.output_port.close()


def main():
    # Configuration
    # MIDI note numbers: C1=36, C#1=37, D1=38, D#1=39, E1=40, F1=41, F#1=42, G1=43, etc.
    # Adjust these to your desired bass note sequence
    
    # Example: C1 → E1 → G1 → C2 (root position C major triad)
    NOTE_SEQUENCE = [36, 40, 43, 48]
    
    # Alternatively, try these:
    # Minor: [36, 39, 43, 48]  # C1 → Eb1 → G1 → C2
    # Fifth pattern: [36, 43, 36, 43]  # C1 → G1 → C1 → G1
    # Chromatic: [36, 37, 38, 39]  # C1 → C#1 → D1 → D#1
    # Blues: [36, 39, 41, 42, 43]  # C1 → Eb1 → F1 → F#1 → G1
    
    INPUT_PORT = "TriggerIO MIDI Out"  # Your DDTI
    OUTPUT_PORT = "IAC Driver Bus 1"   # Virtual MIDI port (we'll create this)
    
    print("=" * 60)
    print("🎵 DDTI MIDI Note Sequencer")
    print("=" * 60)
    
    sequencer = MIDINoteSequencer(
        sequence=NOTE_SEQUENCE,
        input_port_name=INPUT_PORT,
        output_port_name=OUTPUT_PORT
    )
    
    sequencer.run()


if __name__ == "__main__":
    main()

