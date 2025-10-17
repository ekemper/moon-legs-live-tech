#!/bin/bash
# Quick start script for DDTI MIDI Sequencer

cd "$(dirname "$0")"

echo "🎵 Starting DDTI MIDI Note Sequencer..."
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the sequencer
python3 midi_sequencer.py


