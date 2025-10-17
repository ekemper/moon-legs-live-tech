# DDTI MIDI Note Sequencer & Bass Synthesizer

Converts your DDrum DDTI drum triggers into a cycling sequence of bass notes. 

**Two modes:**
1. **Ableton Live Integration** - Route sequenced notes to Ableton via virtual MIDI
2. **Standalone Synthesizer** - Generate bass audio directly in Python (no DAW needed)

Each trigger hit advances to the next note in your custom sequence.

## What This Does

Instead of triggering the same note/sound repeatedly, each drum hit plays the **next note in a sequence**:
- Hit 1: C1
- Hit 2: E1  
- Hit 3: G1
- Hit 4: C2
- Hit 5: C1 (loops back)

Perfect for creating basslines, melodies, or rhythmic note patterns with your drum triggers.

## Choose Your Mode

### Mode 1: Ableton Live Integration

Route MIDI notes to Ableton, trigger any virtual instrument.

**Pros:** Full Ableton power, use any plugin  
**Cons:** Requires Ableton, slightly higher latency  
**Latency:** ~15-30ms

→ Follow setup instructions below

### Mode 2: Standalone Bass Synthesizer ⭐ NEW

Generate bass audio directly in Python, no DAW needed.

**Pros:** Ultra-low latency, portable, lightweight  
**Cons:** Limited to Python synthesis  
**Latency:** ~8-22ms

→ **[See SYNTH_README.md](./SYNTH_README.md)**

```bash
# Quick start for standalone synth
pip install -r requirements_synth.txt
python3 bass_synth_simple.py
```

---

# Ableton Live Integration Setup

## Setup Instructions

### 1. Create Virtual MIDI Port (One-time setup)

Mac has a built-in virtual MIDI driver called **IAC Driver**. We need to enable it:

1. Open **Audio MIDI Setup** (Applications → Utilities → Audio MIDI Setup)
2. Press **CMD+2** or go to **Window → Show MIDI Studio**
3. Double-click the **IAC Driver** icon (looks like a keyboard)
4. Check the box: **"Device is online"**
5. You should see **"IAC Driver Bus 1"** in the Ports list
6. Click **Apply**, then close the window

**The IAC Driver Bus 1 is your virtual MIDI cable.**

### 2. Install Python Dependencies

```bash
cd /Users/ek/dev/moon-legs-live-tech/ddti-sequencer
pip3 install -r requirements.txt
```

Or if you use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Your Note Sequence

Edit `config.py` to set your desired note sequence:

```python
NOTE_SEQUENCE = [36, 40, 43, 48]  # C1 → E1 → G1 → C2
```

See the file for MIDI note reference and preset sequences.

### 4. Configure Ableton Live

1. Open Ableton Live
2. Go to **Preferences → Link/MIDI**
3. Find **"IAC Driver Bus 1"** in the MIDI Ports section
4. Enable **Track** (and optionally **Remote**)
5. Create a MIDI track
6. Set **MIDI From** to **"IAC Driver Bus 1"** (not TriggerIO!)
7. Load a bass instrument (Operator, Wavetable, or any synth)
8. Arm the track, set Monitor to **"In"**

### 5. Run the Sequencer

```bash
python3 midi_sequencer.py
```

Or use the convenient run script:
```bash
./run.sh
```

You should see:
```
=== Available MIDI Input Ports ===
0: TriggerIO MIDI Out
1: IAC Driver Bus 1

=== Available MIDI Output Ports ===
0: TriggerIO MIDI In
1: IAC Driver Bus 1

Opening input: TriggerIO MIDI Out
Opening output: IAC Driver Bus 1

✅ Connected successfully!
📝 Note sequence: C1 → E1 → G1 → C2
🎵 Waiting for triggers...
```

Now hit your drum pads! Each hit advances through the sequence.

## How It Works

```
DDTI Trigger → Python Script → Virtual MIDI Port → Ableton Live
     (any note)   (sequences)    (IAC Driver)      (bass synth)
```

The Python script:
1. Listens to your DDTI (TriggerIO)
2. When it receives ANY note from a trigger
3. Sends the NEXT note in your sequence to the virtual port
4. Ableton receives the sequenced note and plays it with your synth

## Customization

### Change the Note Sequence

Edit `config.py`:

```python
# Major triad
NOTE_SEQUENCE = [36, 40, 43, 48]  # C1 → E1 → G1 → C2

# Minor triad
NOTE_SEQUENCE = [36, 39, 43, 48]  # C1 → Eb1 → G1 → C2

# Bass groove
NOTE_SEQUENCE = [36, 36, 43, 36, 40, 36, 43, 43]

# Chromatic
NOTE_SEQUENCE = [36, 37, 38, 39, 40, 41, 42, 43]
```

### MIDI Note Reference

```
C1  = 36    C#1 = 37    D1  = 38    D#1 = 39
E1  = 40    F1  = 41    F#1 = 42    G1  = 43
G#1 = 44    A1  = 45    A#1 = 46    B1  = 47
C2  = 48    C#2 = 49    D2  = 50    D#2 = 51
```

### Advanced: Multiple Sequences

You can create multiple config files and run different sequences:

```bash
# Bass sequence
python3 midi_sequencer.py

# Or modify the script to load different configs
```

## Reducing Latency

Minimize the delay between drum hit and sound:

### 1. Reduce Ableton's Buffer Size (BIGGEST IMPACT)

**Preferences → Audio → Buffer Size:**
- Set to **128 samples** (good balance)
- Or **64 samples** (ultra-low, more CPU intensive)
- Check **Overall Latency** - aim for under 10ms

**Tradeoff:** Lower buffer = more CPU usage, possible audio glitches if too low.

### 2. Use an Audio Interface

Built-in Mac speakers have ~14ms latency. An external audio interface typically has:
- 3-5ms latency at 128 samples
- 1-3ms latency at 64 samples

**Set it up:**
- Preferences → Audio → Audio Output Device → Your Interface

### 3. Use Lightweight Instruments

- ✅ **Best:** Operator, Analog, Simpler (Ableton built-ins)
- ⚠️ **Heavy:** 3rd-party synths with oversampling
- Disable effects you don't need

### 4. Use Low-Latency Script Version

Run the optimized version with minimal logging:
```bash
python3 midi_sequencer_fast.py
```

This removes print statements that can add microseconds of delay.

### Expected Latency Breakdown

| Component | Latency |
|-----------|---------|
| DDTI USB | ~1ms |
| Python Script | <1ms |
| Virtual MIDI | <1ms |
| Ableton (64 buffer) | 1-3ms |
| Audio Interface | 2-5ms |
| **Total** | **5-10ms** |

Below 10ms feels instant. Above 20ms feels noticeable.

## Troubleshooting

### "Port not found" error

**Check DDTI is connected:**
```bash
python3 -c "import mido; print(mido.get_input_names())"
```
You should see `TriggerIO MIDI Out` in the list.

**Check IAC Driver is enabled:**
```bash
python3 -c "import mido; print(mido.get_output_names())"
```
You should see `IAC Driver Bus 1` in the list.

### No sound in Ableton

1. Check Ableton's MIDI From is set to **"IAC Driver Bus 1"** (NOT TriggerIO)
2. Check track Monitor is set to **"In"**
3. Check track is armed (red button)
4. Check an instrument is loaded on the track
5. Check Master volume is up

### Sequence not advancing

- Make sure the Python script is running
- Check the terminal output - you should see log messages when you hit pads
- Try hitting harder (velocity threshold issue)

### Wrong notes playing

- Verify your `NOTE_SEQUENCE` in `config.py`
- Check the terminal output to see what notes are being sent
- Make sure your bass synth isn't transposed

## Running in Background

To keep the script running while you work:

```bash
# Run in background
python3 midi_sequencer.py &

# Or use screen/tmux
screen -S midi
python3 midi_sequencer.py
# Press Ctrl+A then D to detach
```

To stop:
```bash
# Find the process
ps aux | grep midi_sequencer

# Kill it
kill [PID]
```

## Next Steps

Ideas to extend this:
- Add randomization (random note from sequence)
- Velocity-based note selection (soft = low notes, hard = high notes)
- Multiple sequences with DDTI preset switching
- Web UI to change sequences on the fly
- Record sequences and play them back
- Scale quantization (force notes into a specific scale)

## Support

If you run into issues:
1. Check the terminal output for error messages
2. Verify MIDI connections in Audio MIDI Setup
3. Test with a simple sequence like `[36, 36, 36, 36]` (same note)
4. Make sure the DDTI is working directly in Ableton first

Have fun making basslines with your drums! 🥁🎹

