"""
Configuration file for MIDI Note Sequencer
Edit the NOTE_SEQUENCE to change which notes are played
"""

# MIDI Note Reference:
# C1  = 36    C#1 = 37    D1  = 38    D#1 = 39
# E1  = 40    F1  = 41    F#1 = 42    G1  = 43
# G#1 = 44    A1  = 45    A#1 = 46    B1  = 47
# C2  = 48    C#2 = 49    D2  = 50    D#2 = 51
# E2  = 52    F2  = 53    F#2 = 54    G2  = 55

# Your note sequence (edit this!)
NOTE_SEQUENCE = [36, 40, 43, 48]  # C1 → E1 → G1 → C2

# MIDI Port Names
INPUT_PORT = "TriggerIO MIDI Out"   # Your DDTI
OUTPUT_PORT = "IAC Driver Bus 1"     # Virtual MIDI port

# ===== Preset Sequences =====
# Uncomment one of these to use it, or create your own!

# Major triad
# NOTE_SEQUENCE = [36, 40, 43, 48]  # C1 → E1 → G1 → C2

# Minor triad  
# NOTE_SEQUENCE = [36, 39, 43, 48]  # C1 → Eb1 → G1 → C2

# Power fifth
# NOTE_SEQUENCE = [36, 43, 36, 43]  # C1 → G1 → C1 → G1

# Chromatic run
# NOTE_SEQUENCE = [36, 37, 38, 39, 40, 41, 42, 43]  # C1 → C#1 → D1... → G1

# Blues scale
# NOTE_SEQUENCE = [36, 39, 41, 42, 43]  # C1 → Eb1 → F1 → F#1 → G1

# Octave bounce
# NOTE_SEQUENCE = [36, 48, 36, 48]  # C1 → C2 → C1 → C2

# Ascending scale
# NOTE_SEQUENCE = [36, 38, 40, 41, 43, 45, 47, 48]  # C major scale

# Bass groove pattern
# NOTE_SEQUENCE = [36, 36, 43, 36, 40, 36, 43, 43]  # Root-Root-Fifth-Root-Third-Root-Fifth-Fifth

