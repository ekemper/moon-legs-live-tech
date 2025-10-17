#!/usr/bin/env python3
"""
DDTI to Ableton MIDI Note Sequencer - LOW LATENCY VERSION
Minimal logging for maximum performance
"""

import mido
import sys
from typing import List


class MIDINoteSequencer:
    def __init__(self, sequence: List[int], input_port_name: str, output_port_name: str):
        self.sequence = sequence
        self.current_index = 0
        self.input_port_name = input_port_name
        self.output_port_name = output_port_name
        self.input_port = None
        self.output_port = None
        
    def connect(self):
        """Connect to MIDI ports"""
        try:
            self.input_port = mido.open_input(self.input_port_name)
            self.output_port = mido.open_output(self.output_port_name)
            
            print(f"✅ Connected: {self.input_port_name} → {self.output_port_name}")
            print(f"📝 Sequence: {self.sequence}")
            print("🎵 Running in LOW LATENCY mode (minimal logging)\n")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    def get_next_note(self) -> int:
        """Get the next note in the sequence and advance the counter"""
        note = self.sequence[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.sequence)
        return note
    
    def process_message(self, msg: mido.Message):
        """Process incoming MIDI message and send sequenced note - OPTIMIZED"""
        # Only process note_on messages with velocity > 0
        if msg.type == 'note_on' and msg.velocity > 0:
            next_note = self.get_next_note()
            
            # Create and send message immediately (no logging for speed)
            new_msg = mido.Message(
                'note_on',
                note=next_note,
                velocity=msg.velocity,
                channel=msg.channel
            )
            self.output_port.send(new_msg)
        
        # Pass through note_off messages
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            prev_index = (self.current_index - 1) % len(self.sequence)
            prev_note = self.sequence[prev_index]
            
            new_msg = mido.Message(
                'note_off',
                note=prev_note,
                velocity=0,
                channel=msg.channel
            )
            self.output_port.send(new_msg)
    
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
    # Import config
    try:
        import config
        NOTE_SEQUENCE = config.NOTE_SEQUENCE
        INPUT_PORT = config.INPUT_PORT
        OUTPUT_PORT = config.OUTPUT_PORT
    except ImportError:
        # Fallback defaults
        NOTE_SEQUENCE = [36, 40, 43, 48]
        INPUT_PORT = "TriggerIO MIDI Out"
        OUTPUT_PORT = "IAC Driver Bus 1"
    
    print("=" * 60)
    print("⚡ DDTI MIDI Sequencer - LOW LATENCY MODE")
    print("=" * 60)
    
    sequencer = MIDINoteSequencer(
        sequence=NOTE_SEQUENCE,
        input_port_name=INPUT_PORT,
        output_port_name=OUTPUT_PORT
    )
    
    sequencer.run()


if __name__ == "__main__":
    main()

