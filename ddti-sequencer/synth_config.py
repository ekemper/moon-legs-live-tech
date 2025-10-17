"""
Bass Synthesizer Configuration
Edit these settings to customize your bass sound
"""

# ===== MIDI Configuration =====
INPUT_PORT = "TriggerIO MIDI Out"  # Your DDTI
NOTE_SEQUENCE = [36, 40, 43, 48]   # C1 → E1 → G1 → C2

# ===== Synthesis Configuration =====

# Waveform type for simple synthesizer
# Options: 'sine', 'triangle', 'saw'
WAVEFORM = 'sine'

# Note duration in seconds
NOTE_DURATION = 0.5

# ===== ADSR Envelope Configuration =====
# Attack: Time to reach full volume (seconds)
ATTACK = 0.005   # 5ms - very punchy

# Decay: Time to decay from peak to sustain level (seconds)
DECAY = 0.1      # 100ms

# Sustain: Level to hold while note is on (0.0 to 1.0)
SUSTAIN = 0.7    # 70% of peak volume

# Release: Time to fade out after note off (seconds)
RELEASE = 0.3    # 300ms tail

# ===== Audio Configuration =====
SAMPLE_RATE = 44100  # Hz

# ===== FluidSynth Configuration =====
# Path to SoundFont file (.sf2)
SOUNDFONT_PATH = "/usr/local/share/soundfonts/default.sf2"

# Bass instrument program number (32-39 are typically bass sounds)
# 32 = Acoustic Bass
# 33 = Electric Bass (finger)
# 34 = Electric Bass (pick)
# 35 = Fretless Bass
# 36 = Slap Bass 1
# 37 = Slap Bass 2
# 38 = Synth Bass 1 (good for electronic music)
# 39 = Synth Bass 2 (deeper/darker)
BASS_PROGRAM = 38

# ===== Preset Configurations =====

# Deep sub-bass
SUB_BASS_CONFIG = {
    'waveform': 'sine',
    'attack': 0.001,   # Very quick attack
    'decay': 0.05,
    'sustain': 0.9,    # High sustain for long notes
    'release': 0.5,    # Long release for sub rumble
    'note_duration': 0.8
}

# Punchy synth bass
SYNTH_BASS_CONFIG = {
    'waveform': 'saw',
    'attack': 0.005,
    'decay': 0.15,
    'sustain': 0.6,
    'release': 0.2,
    'note_duration': 0.4
}

# Smooth electric bass
SMOOTH_BASS_CONFIG = {
    'waveform': 'triangle',
    'attack': 0.01,
    'decay': 0.2,
    'sustain': 0.75,
    'release': 0.4,
    'note_duration': 0.6
}


