#!/usr/bin/env python3
"""
Setup verification script
Checks if everything is configured correctly
"""

import sys

def check_dependencies():
    """Check if required Python packages are installed"""
    print("📦 Checking Python dependencies...")
    try:
        import mido
        import rtmidi
        print("  ✅ mido installed")
        print("  ✅ python-rtmidi installed")
        return True
    except ImportError as e:
        print(f"  ❌ Missing dependency: {e}")
        print("\n  Run: pip3 install -r requirements.txt")
        return False

def check_midi_ports():
    """Check if required MIDI ports are available"""
    print("\n🎹 Checking MIDI ports...")
    
    try:
        import mido
        
        input_ports = mido.get_input_names()
        output_ports = mido.get_output_names()
        
        print("\n  Available Input Ports:")
        for port in input_ports:
            print(f"    - {port}")
        
        print("\n  Available Output Ports:")
        for port in output_ports:
            print(f"    - {port}")
        
        # Check for TriggerIO (DDTI)
        has_triggerio = any("TriggerIO" in port for port in input_ports)
        if has_triggerio:
            print("\n  ✅ TriggerIO (DDTI) detected")
        else:
            print("\n  ❌ TriggerIO (DDTI) not found")
            print("     Make sure your DDTI is connected via USB")
        
        # Check for IAC Driver (virtual MIDI)
        has_iac = any("IAC" in port for port in output_ports)
        if has_iac:
            print("  ✅ IAC Driver detected")
        else:
            print("  ❌ IAC Driver not found")
            print("     You need to enable it in Audio MIDI Setup:")
            print("     1. Open Audio MIDI Setup (Applications → Utilities)")
            print("     2. Press CMD+2 or Window → Show MIDI Studio")
            print("     3. Double-click 'IAC Driver'")
            print("     4. Check 'Device is online'")
            print("     5. Click Apply")
        
        return has_triggerio and has_iac
        
    except Exception as e:
        print(f"  ❌ Error checking MIDI ports: {e}")
        return False

def check_config():
    """Check if config file exists and is valid"""
    print("\n⚙️  Checking configuration...")
    
    try:
        import config
        
        if hasattr(config, 'NOTE_SEQUENCE') and len(config.NOTE_SEQUENCE) > 0:
            print(f"  ✅ Note sequence configured: {len(config.NOTE_SEQUENCE)} notes")
            print(f"     {config.NOTE_SEQUENCE}")
        else:
            print("  ❌ NOTE_SEQUENCE not configured in config.py")
            return False
        
        if hasattr(config, 'INPUT_PORT'):
            print(f"  ✅ Input port: {config.INPUT_PORT}")
        
        if hasattr(config, 'OUTPUT_PORT'):
            print(f"  ✅ Output port: {config.OUTPUT_PORT}")
        
        return True
        
    except ImportError:
        print("  ❌ config.py not found")
        return False
    except Exception as e:
        print(f"  ❌ Error reading config: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 DDTI MIDI Sequencer Setup Check")
    print("=" * 60)
    
    checks = [
        check_dependencies(),
        check_midi_ports(),
        check_config()
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ All checks passed! You're ready to run midi_sequencer.py")
        print("\nRun: python3 midi_sequencer.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nSee README.md for detailed setup instructions.")
    print("=" * 60)
    
    return 0 if all(checks) else 1

if __name__ == "__main__":
    sys.exit(main())

