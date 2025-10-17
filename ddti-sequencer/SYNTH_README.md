# Bass Synthesizer - Standalone (No Ableton)

Generate bass notes directly in Python, bypassing Ableton entirely. Ultra-low latency, configurable ADSR envelope, cross-platform.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_synth.txt
```

### 2. Run the Synthesizer

**Simple Sine/Sub-Bass (Recommended):**
```bash
python3 bass_synth_simple.py
```

**Realistic Bass (FluidSynth):**
```bash
python3 bass_synth_fluidsynth.py
```

## Feature Comparison

| Feature | Simple Synth | FluidSynth |
|---------|-------------|------------|
| Dependencies | numpy, sounddevice | FluidSynth, SoundFont file |
| Sound Quality | Clean sine/saw/triangle waves | Realistic sampled bass |
| Latency | ~5-10ms | ~10-20ms |
| CPU Usage | Very low | Low-medium |
| File Size | Minimal | Requires SoundFont (~MB) |
| Customization | Full ADSR control | SoundFont dependent |

## Configuration

Edit `synth_config.py` to customize:

### Basic Settings

```python
# Waveform type
WAVEFORM = 'sine'  # 'sine', 'triangle', or 'saw'

# Note duration
NOTE_DURATION = 0.5  # seconds

# ADSR Envelope
ATTACK = 0.005   # 5ms - punchy attack
DECAY = 0.1      # 100ms decay
SUSTAIN = 0.7    # 70% sustain level
RELEASE = 0.3    # 300ms release tail
```

### Preset Configurations

The config file includes presets:
- **SUB_BASS_CONFIG** - Deep sub-bass with long sustain
- **SYNTH_BASS_CONFIG** - Punchy saw bass
- **SMOOTH_BASS_CONFIG** - Smooth triangle bass

## How It Works

```
DDTI Trigger → Python Script → Direct Audio Output
     (any note)   (sequences)     (speakers/interface)
```

Unlike the Ableton version, this:
- Generates audio directly in Python
- No virtual MIDI port needed
- No DAW required
- Lower latency (no extra software layers)

## Simple Synth (Recommended)

**Pros:**
- Pure Python, minimal dependencies
- Full control over waveform and ADSR
- Perfect for sub-bass and electronic sounds
- Ultra-low latency (~5-10ms)

**Sound Options:**
- **sine** - Clean sub-bass, pure tone
- **triangle** - Warmer, hollow sound
- **saw** - Bright, aggressive synth bass

**ADSR Envelope:**
```
Volume
  |     /\  
  |    /  \___________
  |   /               \
  |  /                 \___
  |_________________________
     A  D   Sustain    R
```

- **Attack (A)**: How fast the note "hits"
  - Short (0.001-0.01s): Punchy, percussive
  - Long (0.1-0.5s): Smooth, swelling
  
- **Decay (D)**: How fast it drops to sustain
  - Affects initial impact

- **Sustain (S)**: Held volume level (0.0-1.0)
  - High (0.8-1.0): Long, droning notes
  - Low (0.3-0.5): Plucky, short notes

- **Release (R)**: Tail after note off
  - Short (0.1s): Staccato
  - Long (0.5-1.0s): Ambient tail

## FluidSynth Synth (Realistic)

**Pros:**
- Realistic bass guitar/synth bass samples
- Professional sound quality
- Multiple bass instruments available

**Cons:**
- Requires SoundFont file download
- Slightly higher latency
- Less direct control over envelope

### Setup FluidSynth

**Mac:**
```bash
brew install fluidsynth
pip install pyfluidsynth
```

**Linux:**
```bash
sudo apt install fluidsynth
pip install pyfluidsynth
```

### Download SoundFont

Free SoundFonts:
- **GeneralUser GS** (recommended): https://schristiancollins.com/generaluser.php
- **FluidR3_GM**: https://member.keymusician.com/Member/FluidR3_GM/
- **Musical Artifacts**: https://musical-artifacts.com/artifacts?tags=soundfont

Place the `.sf2` file somewhere and update `synth_config.py`:
```python
SOUNDFONT_PATH = "/path/to/your/soundfont.sf2"
```

### Bass Programs

FluidSynth SoundFonts typically include:
- **32** - Acoustic Bass
- **33** - Electric Bass (finger)
- **34** - Electric Bass (pick)
- **35** - Fretless Bass
- **36** - Slap Bass 1
- **37** - Slap Bass 2
- **38** - Synth Bass 1 ⭐ (default, good for electronic)
- **39** - Synth Bass 2 (deeper/darker)

## Examples

### Deep Sub-Bass

```python
# In synth_config.py
WAVEFORM = 'sine'
ATTACK = 0.001   # Instant
DECAY = 0.05
SUSTAIN = 0.9    # Very high
RELEASE = 0.5    # Long rumble
NOTE_DURATION = 0.8
```

### Punchy Synth Bass

```python
WAVEFORM = 'saw'
ATTACK = 0.005   # Quick hit
DECAY = 0.15
SUSTAIN = 0.6
RELEASE = 0.2    # Short tail
NOTE_DURATION = 0.4
```

### 808-Style Kick Bass

```python
NOTE_SEQUENCE = [36, 36, 36, 36]  # All C1
WAVEFORM = 'sine'
ATTACK = 0.001
DECAY = 0.3      # Long decay
SUSTAIN = 0.0    # No sustain (one-shot)
RELEASE = 0.1
NOTE_DURATION = 0.5
```

## Latency Optimization

Both synthesizers are already optimized for low latency:

**Simple Synth:**
- Uses `sounddevice` with 128-sample buffer
- Direct numpy array generation
- ~5-10ms total latency

**FluidSynth:**
- Hardware-accelerated synthesis
- ~10-20ms total latency

**Expected Total Latency:**
- DDTI USB: ~1ms
- Python processing: <1ms
- Audio synthesis: 5-15ms
- Audio output: 2-5ms
- **Total: 8-22ms** (imperceptible)

## Troubleshooting

### No sound output

**Check audio device:**
```python
import sounddevice as sd
print(sd.query_devices())
```

Set default device if needed:
```python
# In bass_synth_simple.py, add:
sd.default.device = 'Your Device Name'
```

### "sounddevice not found"

```bash
pip install sounddevice
```

May need portaudio on Linux:
```bash
sudo apt install libportaudio2
```

### FluidSynth crashes

Make sure SoundFont path is correct:
```python
# Test loading
import fluidsynth
fs = fluidsynth.Synth()
fs.start()
sfid = fs.sfload('/path/to/soundfont.sf2')
print(f"Loaded SoundFont ID: {sfid}")
```

### Clicks/pops in audio

Increase buffer size in `bass_synth_simple.py`:
```python
self.stream = sd.OutputStream(
    blocksize=256  # Increase from 128
)
```

### High CPU usage

- Use Simple Synth instead of FluidSynth
- Reduce sample rate (22050 Hz instead of 44100 Hz)
- Shorten note duration

## Advanced Customization

### Multiple Waveform Layers

Edit `bass_synth_simple.py` to add harmonics:

```python
# Generate fundamental + octave up
wave1 = np.sin(2 * np.pi * frequency * t)
wave2 = np.sin(2 * np.pi * frequency * 2 * t) * 0.3
wave = wave1 + wave2
```

### Velocity-Based Filtering

Add brightness based on velocity:

```python
if velocity < 64:
    waveform = 'sine'  # Dark, soft hits
else:
    waveform = 'saw'   # Bright, hard hits
```

### Dynamic ADSR

Change envelope based on note:

```python
if midi_note < 40:  # Low notes
    self.adsr.release = 0.5  # Longer tail
else:  # Higher notes
    self.adsr.release = 0.2  # Shorter tail
```

## Performance Tips

1. **Pre-warm the synth:** First note might have slight latency
2. **Use 'sine' waveform:** Lowest CPU usage
3. **Shorter durations:** Less memory usage
4. **Direct audio device:** Don't use system mixer if possible

## Comparison to Ableton Setup

| Aspect | Python Synth | Ableton + Virtual MIDI |
|--------|-------------|------------------------|
| Latency | 8-22ms | 15-30ms |
| Setup | 1 config file | Multiple steps |
| Customization | Full code access | Plugin dependent |
| CPU Usage | Very low | Medium-high |
| Sound Quality | Good | Excellent |
| Portability | Python only | Requires Ableton |
| Live Use | Excellent | Excellent |

## Next Steps

- Try different waveforms and ADSR settings
- Experiment with note sequences
- Add effects (reverb, distortion) using scipy
- Create multiple synthesizer presets
- Layer multiple synthesizers for complex sounds

Enjoy your ultra-low-latency bass triggers! 🎸🥁


