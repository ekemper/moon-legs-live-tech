# Midas MR18 Multitrack Recording with Ableton Live 12.3
## Complete Setup and Configuration Guide

---

## Table of Contents
1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Ableton Live 12.3 Features](#ableton-live-123-features)
4. [Midas MR18 Specifications](#midas-mr18-specifications)
5. [Initial Setup](#initial-setup)
6. [Ableton Live Configuration](#ableton-live-configuration)
7. [MR18 Routing Configuration](#mr18-routing-configuration)
8. [Recording Workflow](#recording-workflow)
9. [Monitoring Setup](#monitoring-setup)
10. [Troubleshooting](#troubleshooting)
11. [Best Practices](#best-practices)
12. [Advanced Techniques](#advanced-techniques)

---

## Overview

This guide details how to use the Midas MR18 digital mixer as an 18x18 USB audio interface for multitrack recording directly into Ableton Live 12.3. The MR18 provides professional-grade preamps, digital mixing capabilities, and simultaneous recording of up to 18 channels via USB.

### What You'll Achieve
- Record up to 18 individual channels simultaneously
- Zero-latency monitoring through the MR18
- Digital mixing capabilities while tracking
- Professional live sound reinforcement with simultaneous recording
- Flexible routing options for various recording scenarios

---

## System Requirements

### Hardware
- **Midas MR18** digital mixer
- **Mac** with available USB 2.0 or 3.0 port
- **USB Type B cable** (USB-A to USB-B or USB-C to USB-B depending on your computer)
- Sufficient **storage space** for multitrack recordings (approximately 1GB per 10 minutes of 18-track recording at 24-bit/48kHz)
- Minimum **4GB RAM** (8GB+ recommended for 18-track recording)

### Software
- **Ableton Live 12.3** (Suite, Standard, or Intro)
- **Midas MR18 USB drivers** (macOS compatible)
- **M-Air Control App** or web browser for MR18 configuration (optional but recommended)

### Operating System
- **macOS**: 10.13.6 or later (macOS 12+ recommended)

---

## Ableton Live 12.3 Features

Ableton Live 12.3, released in November 2025, includes several features particularly useful for multitrack recording:

### Key Features for Recording

**Stem Separation**

*What are Stems?*
Stems are individual audio files or tracks that represent grouped elements of a mix. For example, a "drums stem" contains all drum tracks (kick, snare, hi-hats, etc.) mixed together into a single stereo file, while a "vocals stem" contains all vocal tracks. Stems are commonly used for:
- Archiving and backup (easier to manage than 18+ individual tracks)
- Mixing in other DAWs or studios
- Creating alternate mixes or remixes
- Sharing with collaborators who don't have the full multitrack session
- Live performance (playing back stems instead of full multitrack)

*Stem Separation Feature:*
- Uses AI to automatically isolate vocals, drums, bass, and other instruments from existing recordings
- Works on stereo or mono recordings, even if they weren't originally multitrack
- Perfect for remixing and sampling from multitrack recordings
- Works directly in Session or Arrangement view
- Creates new tracks with the separated elements

**Bounce to New Track**

*What is Bouncing?*
Bouncing (also called "rendering" or "printing") is the process of converting audio tracks with all their effects, processing, and automation into a new audio file. The bounced track contains the final processed sound, not the original audio plus effects. This is useful for:
- Freeing up CPU by rendering processor-heavy tracks
- Committing to effects and processing decisions
- Creating consolidated versions of multiple takes or layers
- Exporting stems for mixing or sharing
- Archiving final versions of tracks

*Bounce to New Track Feature:*
- Quickly consolidate and bounce clips or time selections to new audio tracks
- Includes all processing and effects in the bounced audio
- Optimizes CPU usage during complex sessions
- Creates a new track with the bounced audio, leaving the original track intact
- Useful for creating stems or committing to processing decisions

**Auto Filter Overhaul**
- Real-time visualization
- New filter types: Resampling, Comb, Vowel, and DJ
- Enhanced sound design capabilities for post-production

**Splice Integration**
- Direct sample browsing from Splice
- "Search with Sound" feature for finding similar sounds
- Streamlined workflow integration

**Enhanced MIDI and MPE Support**
- Expressive Chords device for nuanced harmonies
- Improved MIDI control and automation

---

## Midas MR18 Specifications

### USB Audio Interface Capabilities
- **18x18 channels** of simultaneous recording/playback
- **USB 2.0** interface (class-compliant on macOS)
- **Sample rates**: 44.1kHz, 48kHz
- **Bit depth**: 24-bit

### Input Configuration
- **16 Midas microphone preamps** (channels 1-16)
  - Channels 1-8: XLR with phantom power
  - Channels 9-16: XLR/TRS combo jacks
- **2 stereo auxiliary inputs** (channels 17-18)
- All inputs can be routed to USB

### USB Channel Routing
The MR18 sends audio to your computer via 18 USB channels:
- **Channels 1-16**: Individual input channels (pre or post-processing)
- **Channels 17-18**: Stereo aux returns or main mix

### Additional Features
- Built-in effects processors (reverb, delay, chorus)
- 4-band parametric EQ per channel
- Dynamics processing (gate, compressor, de-esser)
- 6 aux/monitor mixes
- Built-in WiFi for wireless control

---

## Initial Setup

### Step 1: Install Midas MR18 USB Drivers

#### macOS
1. Download the latest USB audio driver from the [Midas website](https://www.musictri.be/Categories/Midas/Mixers/Digital/MR18)
2. Open the downloaded `.dmg` file
3. Run the installer package
4. Restart your computer after installation
5. Grant necessary permissions in **System Preferences > Security & Privacy**

**Note**: macOS 10.14+ may recognize the MR18 as a class-compliant device without additional drivers. However, installing the official driver ensures optimal performance and stability.

### Step 2: Physical Connection

1. **Power on** the MR18
2. Connect the **USB Type B cable** from the MR18's USB port to your computer
3. Wait for your computer to recognize the device (typically 10-30 seconds)
4. Verify connection by checking:
   - **macOS**: Audio MIDI Setup app (Applications > Utilities)

### Step 3: MR18 Network Setup (Optional but Recommended)

The MR18 can be controlled via WiFi or Ethernet for remote configuration:

#### WiFi Setup
1. Connect your device (tablet/phone/laptop) to the MR18's WiFi network
   - Default SSID: `MR18-XX-XX-XX`
   - Default password: Check the label on the mixer
2. Open a web browser and navigate to `192.168.1.1`
3. The MR18 control interface will load

#### M-Air App
- Download the **M-Air** app (iOS/Android/macOS)
- Connect to the MR18 WiFi network
- Launch the app; it should automatically detect the mixer

---

## Ableton Live Configuration

### Step 1: Audio Preferences Setup

1. **Open Ableton Live 12.3**
2. Navigate to **Preferences** (`Ableton Live > Preferences`)
3. Select the **Audio** tab

### Step 2: Select Audio Interface

**Audio Input Device**:
- Select **MR18** from the dropdown menu
- Full name may appear as "Midas MR18" or "MR18 Audio"

**Audio Output Device**:
- Select **MR18** (same as input device)
- This allows you to monitor through the MR18

### Step 3: Sample Rate and Buffer Size

**Sample Rate**:
- Set to **48000 Hz** (48kHz recommended)
- Alternatively: 44100 Hz (44.1kHz)
- **Important**: Match this setting in the MR18 control interface

**Buffer Size** (Latency):
- Start with **256 samples** for a balance of performance and latency
- Lower values (128, 64 samples): Lower latency but higher CPU load
- Higher values (512, 1024 samples): More stable but increased latency
- For live tracking: aim for **128-256 samples** (3-6ms latency)

**Overall Latency**:
- Monitor the displayed latency at the bottom of the Audio Preferences
- Target: **10ms or less** for comfortable live tracking

### Step 4: Enable Input Channels

1. In Audio Preferences, click **Input Config** button
2. A window will display all available input channels
3. **Enable channels 1-18**:
   - Check the boxes next to:
     - Input 1 (Ext. In 1)
     - Input 2 (Ext. In 2)
     - ...
     - Input 18 (Ext. In 18)
4. You can rename these inputs for easier identification (e.g., "Kick", "Snare", "Bass", etc.)
5. Click **OK** to save

### Step 5: Output Configuration (Optional)

1. Click **Output Config** in Audio Preferences
2. Enable outputs as needed for monitoring
3. Typically, outputs 1-2 (Main L/R) are sufficient

---

## MR18 Routing Configuration

The MR18's USB routing determines which signals are sent to Ableton Live. This is a critical step for multitrack recording.

### Access MR18 Control Interface

**Via Web Browser**:
1. Connect to MR18 WiFi or Ethernet
2. Navigate to `192.168.1.1`
3. Interface loads in browser

**Via M-Air App**:
1. Launch M-Air app
2. Connect to MR18

### Linux Control Computer Setup (Dual Network Configuration)

For setups where a Linux computer is used for MR18 mixer control while maintaining internet connectivity:

**Network Configuration Overview**:
- **WiFi**: Connected to your regular network for internet access
- **Ethernet**: Direct connection to MR18 for mixer control (typically `192.168.1.1`)
- **Mac**: Connected via USB to MR18 for Ableton Live recording

**Step 1: Physical Connections**
1. Connect Ethernet cable from Linux computer to MR18's Ethernet port
2. Ensure WiFi is connected to your regular network (for internet)
3. Mac remains connected to MR18 via USB for recording

**Step 2: Configure Ethernet Interface on Linux**

The MR18 typically uses the `192.168.1.1` IP address. Configure your Linux Ethernet interface with a static IP in the same subnet:

**Using NetworkManager (most modern Linux distributions)**:
1. Open NetworkManager settings (GUI or `nmcli`)
2. Select your Ethernet connection
3. Set IPv4 configuration to **Manual**
4. Configure:
   - **IP Address**: `192.168.1.100` (or any address in `192.168.1.x` range, avoiding `.1`)
   - **Netmask**: `255.255.255.0` (or `/24`)
   - **Gateway**: Leave empty (or `192.168.1.1` if needed)
   - **DNS**: Leave empty or use your WiFi network's DNS
5. Save and activate the connection

**Using `nmcli` (command line)**:
```bash
# Set Ethernet interface to static IP
sudo nmcli connection modify "Wired connection 1" \
  ipv4.addresses 192.168.1.100/24 \
  ipv4.method manual \
  ipv4.gateway "" \
  ipv4.dns ""

# Activate the connection
sudo nmcli connection up "Wired connection 1"
```

**Using `/etc/network/interfaces` (Debian/Ubuntu traditional method)**:
```bash
# Edit /etc/network/interfaces
auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    # No gateway needed for direct connection
```

**Step 3: Verify Network Configuration**

1. **Check Ethernet interface**:
   ```bash
   ip addr show
   # or
   ifconfig
   ```
   Should show your Ethernet interface with IP `192.168.1.100` (or your chosen IP)

2. **Test connectivity to MR18**:
   ```bash
   ping 192.168.1.1
   ```
   Should receive responses from the MR18

3. **Verify internet still works**:
   ```bash
   ping 8.8.8.8
   # or
   curl https://www.google.com
   ```
   Internet should still be accessible via WiFi

**Step 4: Access MR18 Web Interface**

1. Open web browser on Linux computer
2. Navigate to `http://192.168.1.1`
3. MR18 control interface should load
4. You can now control the mixer from Linux while maintaining internet access

**Step 5: Routing Configuration (if needed)**

If you encounter routing issues where the system tries to use Ethernet for internet:

**Check routing table**:
```bash
ip route show
# or
route -n
```

**Expected behavior**:
- Default route should point to WiFi gateway (for internet)
- Direct route to `192.168.1.0/24` should use Ethernet interface

**If routing needs adjustment**:
```bash
# Ensure default route uses WiFi (wlan0 or similar)
sudo ip route add default via <your-wifi-gateway-ip> dev wlan0

# Ensure MR18 subnet uses Ethernet
sudo ip route add 192.168.1.0/24 dev eth0
```

**Troubleshooting**:

- **Can't reach MR18**: Verify Ethernet cable is connected and MR18 is powered on. Check IP configuration matches MR18's subnet.
- **Lost internet connection**: Ensure WiFi is still connected and default route points to WiFi gateway.
- **MR18 not at 192.168.1.1**: Check MR18's network settings via WiFi connection first, or consult MR18 manual for default IP.
- **Both networks work but routing is slow**: Use `ip route` to verify routes are correct. Consider adding explicit routes if needed.

**Benefits of This Setup**:
- **Separation of concerns**: Mac handles recording, Linux handles mixer control
- **Internet access maintained**: Can access documentation, updates, cloud services from Linux
- **Stable direct connection**: Ethernet provides reliable, low-latency connection to MR18
- **Flexible workflow**: Control mixer remotely while Mac focuses on recording

### Configure USB Interface Mode

1. In the MR18 interface, tap/click the **Setup** or **Config** button (gear icon)
2. Navigate to **Audio/MIDI** or **USB Configuration** section
3. Set **USB Interface Mode** to **18x18**
   - This enables all 18 input channels for recording
   - Confirms 18 channels of playback from Ableton

### USB Send Routing Options

For each input channel (1-18), you can choose what signal is sent to USB:

**Option 1: Direct (Pre-EQ/Pre-Dynamics)** - Recommended for most scenarios
- Records the raw input signal
- Bypasses all MR18 processing (EQ, compression, etc.)
- Gives you maximum flexibility for processing in Ableton
- Navigate to **Routing** > **USB Send** and set each channel to **Direct** or **Pre**

**Option 2: Post-Processing**
- Records the signal after MR18's EQ, dynamics, and effects
- Useful if you want to commit to processing during tracking
- Set channels to **Post** in the USB Send routing

**Recommendation**: Use **Direct/Pre** routing for maximum flexibility. You can always add processing in Ableton, but you can't remove it once recorded.

### Step-by-Step Routing Setup

1. **Select Channel 1** in the MR18 interface
2. Navigate to **Routing** or **USB** tab
3. Set **USB Send 1** to **Channel 1 Direct** (or Pre-Fader)
4. Repeat for **Channels 2-18**:
   - USB Send 2 → Channel 2 Direct
   - USB Send 3 → Channel 3 Direct
   - ...
   - USB Send 18 → Channel 18 Direct (or Aux/Stereo In as needed)

**Alternative Quick Setup** (if available):
- Some firmware versions offer a **"USB Default Routing"** preset
- This automatically routes all inputs to their corresponding USB sends
- Look for this in **Setup > USB > Default Routing**

### Verify Routing

1. Connect a microphone or instrument to **Channel 1**
2. In Ableton Live, create an audio track with input set to **Ext. In 1**
3. Arm the track and adjust input gain on the MR18
4. You should see the input meter responding in Ableton
5. Repeat verification for other channels as needed

---

## Recording Workflow

### Step 1: Create Audio Tracks

1. In Ableton Live, create a new session or open an existing project
2. Create audio tracks for each input you want to record:
   - **Keyboard shortcut**: `Cmd+T`
   - Or: Right-click in the track area > **Insert Audio Track**
3. For full 18-channel recording, create 18 audio tracks

### Step 2: Assign Input Channels

For each audio track:
1. Click the track's **Audio From** dropdown (top of track)
2. Select **Ext. In**
3. Choose the corresponding channel:
   - Track 1: **Ext. In 1**
   - Track 2: **Ext. In 2**
   - ...
   - Track 18: **Ext. In 18**

**Quick Tip**: You can also select **stereo pairs** if needed:
- Some tracks can be set to **Ext. In 1/2** (stereo)
- Useful for stereo keyboards, overhead mics, etc.

### Step 3: Name Your Tracks

Organize your session by naming tracks according to their sources:
1. Double-click the track name field
2. Enter descriptive names: "Kick", "Snare", "Bass DI", "Guitar", "Vocals", etc.
3. This makes mixing and editing much easier later

### Step 4: Set Input Monitoring

For each track, set the **Monitor** mode (small speaker icon in track controls):

- **Off**: No input monitoring (saves CPU)
- **In**: Monitor input only when track is armed
- **Auto**: Monitor when armed and not playing (recommended for most scenarios)

**For Live Performance Recording**:
- Use the MR18's direct monitoring instead of Ableton's monitoring
- This eliminates latency issues
- Set tracks to **Monitor: Off** in Ableton

### Step 5: Arm Tracks for Recording

1. Click the **Record Arm** button on each track you want to record (circular button)
2. Track arm buttons will turn red when armed
3. You should see input levels on the track meters
4. **Tip**: Hold `Cmd` to arm multiple tracks simultaneously

**Troubleshooting: Only One Track Arms at a Time**

If you find that arming one track automatically disarms another (only one track can be armed at a time), this is **not related to your Ableton license**. All versions of Ableton Live (Intro, Standard, Suite) support multiple armed tracks. The issue is caused by the **"Exclusive Arm"** preference being enabled.

**Solution**:
1. Go to **Preferences** (`Ableton Live > Preferences`)
2. Select the **Record/Warp/Launch** tab
3. Look for **"Exclusive Arm"** option
4. **Uncheck** or **disable** "Exclusive Arm"
5. Close Preferences

After disabling Exclusive Arm, you'll be able to arm multiple tracks simultaneously. This setting is useful for live performance (prevents accidentally recording on multiple tracks), but for multitrack recording, you'll want it disabled.

**Alternative Method** (if Exclusive Arm is disabled but issue persists):
- Try holding `Cmd` while clicking multiple arm buttons
- Or use `Cmd+Shift+A` to arm all tracks at once (if configured)

### Step 6: Set Input Levels on MR18

Proper gain staging is critical:
1. On the MR18, adjust the **Gain** knob for each input channel
2. Watch the channel meters in the MR18 interface
3. **Target levels**:
   - Peak around **-12dB to -6dB** (yellow zone)
   - Avoid clipping (red/0dB)
   - Leave **6-12dB of headroom** for dynamics
4. Verify levels are also showing correctly in Ableton's track meters

### Step 7: Start Recording

1. **Click the Record button** in Ableton's transport (or press `F9`)
2. The transport will show the record button active (red circle)
3. **Start playback** by clicking Play or pressing `Spacebar`
4. Recording begins on all armed tracks simultaneously
5. Perform your music!

### Step 8: Stop Recording

1. Press `Spacebar` to stop playback
2. Recording stops automatically
3. New audio clips appear on all recorded tracks
4. **Save your project**: `Cmd+S`

### Step 9: Review and Edit

1. **Disarm all tracks** to prevent accidental recording
2. **Play back** the recording to review
3. Use Ableton's editing tools to:
   - Trim clips
   - Adjust timing
   - Apply processing and effects
   - Mix the multitrack recording

---

## Monitoring Setup

Proper monitoring is essential for comfortable tracking and performance.

### Zero-Latency Monitoring via MR18

**Why Use Hardware Monitoring?**
- **Zero latency**: Hear yourself in real-time without computer-induced delay
- **Lower CPU usage**: Reduces strain on your computer
- **Professional workflow**: Standard practice in studios

**Setup**:
1. Connect **headphones** or **monitors** to the MR18:
   - Main Out L/R: For main monitoring
   - Aux Outputs: For individual performer mixes
   - Headphone output: Direct monitoring
2. In the MR18 interface, create monitor mixes:
   - **Main Mix**: Set input faders for overall balance
   - **Aux Mixes**: Create custom mixes for performers (e.g., more vocals in the vocalist's mix)
3. In **Ableton Live**, set all tracks to **Monitor: Off**
4. This routes audio through the MR18's internal mixer before going to outputs


---

## Troubleshooting

### No Audio in Ableton Live

**Symptoms**: Meters not moving, no sound when recording

**Solutions**:
1. **Verify USB connection**: Disconnect and reconnect the USB cable
2. **Check Audio Preferences**:
   - Ensure MR18 is selected as both input and output device
   - Verify sample rate matches between Ableton and MR18
3. **Enable input channels**: Go to Input Config and enable all channels
4. **Check track routing**: Ensure tracks are set to correct Ext. In channels
5. **Arm tracks**: Recording won't work without armed tracks
6. **MR18 routing**: Verify USB sends are configured correctly in MR18 interface

### High Latency / Audio Glitches

**Symptoms**: Delayed monitoring, clicks, pops, dropouts

**Solutions**:
1. **Lower buffer size**: Start at 256, reduce to 128 if needed
2. **Close background applications**: Free up CPU resources
3. **Disable WiFi/Bluetooth**: Can cause audio dropouts on some systems
4. **Use direct monitoring**: Monitor through MR18 instead of Ableton
5. **Increase buffer size**: If CPU is maxed out, increase to 512 samples
6. **Freeze tracks**: Freeze existing tracks to reduce CPU load
7. **Check USB port**: Use USB 2.0/3.0 ports directly on computer (avoid hubs)

### Audio Dropouts / "System Overload" Message

**Symptoms**: Recording stops, error messages, choppy playback

**Solutions**:
1. **Increase buffer size**: Go to 512 or 1024 samples
2. **Disable unnecessary plugins**: Remove CPU-heavy effects during tracking
3. **Reduce track count**: Record in smaller batches if needed
4. **Disk speed**: Ensure you're recording to a fast drive (SSD preferred)
5. **Update drivers**: Check for latest MR18 and Ableton updates
6. **Simplify project**: Disable automation, reduce visual elements

### Channels Recording Incorrectly

**Symptoms**: Wrong channels appearing on tracks, mixed-up inputs

**Solutions**:
1. **Verify MR18 USB routing**: Check that USB Send 1 = Channel 1, etc.
2. **Check Ableton track inputs**: Ensure Track 1 = Ext. In 1, Track 2 = Ext. In 2, etc.
3. **Test one channel at a time**: Isolate the issue by recording one channel
4. **Reset USB routing**: In MR18, reset to default USB routing configuration

### MR18 Not Recognized by Computer

**Symptoms**: Device doesn't appear in audio settings

**Solutions**:
1. **Restart MR18 and computer**: Power cycle both devices
2. **Try different USB cable**: Use a high-quality USB 2.0 cable
3. **Try different USB port**: Some ports may have power limitations
4. **Reinstall drivers**: Uninstall and reinstall MR18 USB drivers
5. **Check USB mode**: Ensure MR18 is in USB audio interface mode (not just MIDI)
6. **macOS**: Check **System Preferences > Security & Privacy** for blocked drivers

### Phantom Power Issues

**Symptoms**: Condenser microphones not working on certain channels

**Solutions**:
1. **Enable phantom power (+48V)** on the MR18 for channels 1-16
2. In MR18 interface: Select channel > Config > Enable 48V
3. **Wait 10 seconds** after enabling phantom power before connecting mics
4. **Check cable**: Ensure XLR cable is properly connected

---

## Best Practices

### Pre-Recording Checklist

**Audio Setup**:
- [ ] MR18 connected via USB and powered on
- [ ] All input sources connected to correct channels
- [ ] Phantom power enabled for condenser mics (channels 1-16)
- [ ] Input levels properly set (-12dB to -6dB peaks)
- [ ] Monitoring system connected and working

**Ableton Configuration**:
- [ ] MR18 selected as audio interface
- [ ] Sample rate set (48kHz recommended)
- [ ] Buffer size optimized (256 samples starting point)
- [ ] All 18 input channels enabled in Input Config
- [ ] Audio tracks created and assigned to correct inputs
- [ ] Tracks armed for recording
- [ ] Monitor mode set appropriately

**MR18 Routing**:
- [ ] USB interface mode set to 18x18
- [ ] USB sends routed correctly (Direct/Pre mode)
- [ ] Monitor mixes created for performers
- [ ] Headphone/monitor levels set

### During Recording

1. **Watch levels constantly**: Avoid clipping at all costs
2. **Save frequently**: Use Auto-Save feature in Ableton preferences
3. **Name takes**: Use Ableton's Scene naming for multiple takes
4. **Monitor CPU**: Keep CPU usage below 70% during recording
5. **Communication**: Use talkback feature on MR18 for clear communication with performers

### Post-Recording

1. **Disarm all tracks immediately**: Prevent accidental recording
2. **Save project with descriptive name**: Include date and session type
3. **Consolidate clips**: Use "Consolidate" to create single files per track
4. **Back up immediately**: Copy project folder to external drive
5. **Export stems**: Bounce individual tracks or grouped tracks (e.g., all drums, all vocals) as audio files for archival or mixing elsewhere. Stems are processed audio files that can be opened in any DAW.
6. **Document settings**: Note any special MR18 routing or processing used

### Gain Staging

Proper gain staging ensures clean, professional recordings:

**Input Stage (MR18)**:
1. Set **Gain** on MR18 so peaks hit **-12dB to -6dB** (yellow)
2. Use **High-Pass Filter** (HPF) to reduce rumble on vocals/instruments (80-100Hz)
3. Keep **faders near unity (0dB)** for USB sends in Direct mode

**Recording Stage (Ableton)**:
1. Track meters should peak at **-12dB to -6dB** (yellow to green)
2. Leave adequate **headroom** (never hit 0dB/red)
3. Record at **24-bit** depth for maximum dynamic range

**Mixing Stage**:
1. Keep **master fader at 0dB** initially
2. Mix with faders down (-6dB to -12dB) to create headroom
3. Use **gain utilities** instead of drastically adjusting track volumes

### File Management

**Project Organization**:
```
Project_Name_2026-01-04/
├── Project_Name.als (Ableton project file)
├── Samples/
│   └── Recorded/
│       ├── 01_Kick.wav
│       ├── 02_Snare.wav
│       ├── 03_Bass.wav
│       └── ...
├── Stems/
│   └── (exported stems for backup)
└── Notes.txt (session notes, settings, etc.)
```

**Backup Strategy**:
1. **Local backup**: Save to external SSD/HDD immediately after recording
2. **Cloud backup**: Upload to cloud storage within 24 hours
3. **Multiple versions**: Keep raw recordings separate from edited versions
4. **Archive**: Once project is complete, create a consolidated project file

---

## Advanced Techniques

### Recording with MR18 Effects

The MR18 includes built-in effects (reverb, delay, chorus):

**Method 1: Dry Recording with Effects on Monitors**
- Record **dry signal** to Ableton (USB sends set to Direct/Pre)
- Send effects to **monitor mixes** only (Aux/FX buses)
- Performers hear effects, but they're not recorded
- **Advantage**: Maximum flexibility in post-production

**Method 2: Printing Effects to Separate Tracks**
- Record **dry signal** on Track 1 (USB Send 1 = Direct)
- Record **wet signal with effects** on Track 2 (USB Send 2 = Post-FX)
- **Advantage**: Capture the live performance vibe while maintaining dry backup

**Setup for Method 2**:
1. In MR18, set USB Send 1 to Channel 1 Direct
2. Create an Aux Send with reverb/delay
3. Set USB Send 2 to Aux 1 (with effects)
4. In Ableton, record both Ext. In 1 (dry) and Ext. In 2 (wet)

### Using MR18 as a Live Sound Mixer + Recorder

The MR18 excels at simultaneous live sound and recording:

**Setup**:
1. **Main Mix**: Configure for front-of-house sound
2. **Monitor Mixes (Aux 1-6)**: Create for stage monitors/in-ears
3. **USB Recording**: Runs independently, capturing all inputs
4. **Effects**: Apply to live mix without affecting recorded signals (if using Direct routing)

**Workflow**:
1. Soundcheck and set up monitor mixes on MR18
2. In Ableton, verify recording levels and arm tracks
3. Start Ableton recording before the performance
4. Engineer focuses on live mix using MR18 interface
5. Recording happens automatically in the background

**Advantages**:
- Capture every show for archival, remixing, or live albums
- No need for additional recording setup
- Focus on live sound; multitrack recording is automatic

### Creating Custom Track Templates

Save time by creating reusable templates:

1. **Set up 18 audio tracks** with:
   - Correct input assignments (Ext. In 1-18)
   - Descriptive names (Kick, Snare, Bass, etc.)
   - Monitoring preferences
   - Optional: color coding by instrument type
2. **Add utility processing**:
   - High-pass filters on vocal/instrument tracks
   - Light compression on master bus
3. **Save as Default Set**:
   - **File > Save Live Set As**
   - Save to: `~/Music/Ableton/User Library/Templates`
   - Name: "MR18 18-Track Recording Template"
4. **Access template**:
   - **File > New Live Set from Template**
   - Select your MR18 template

### Multi-Session Recording

For projects that require multiple recording sessions:

**Session 1: Rhythm Section**
1. Record drums, bass, rhythm guitar (Channels 1-10)
2. Save project as "ProjectName_Session1_Rhythm"

**Session 2: Overdubs**
1. **Open Session 1 project**
2. **Disarm rhythm tracks** (already recorded)
3. Enable playback from MR18 to monitor existing tracks
4. Record vocals, leads, keys (Channels 11-18)
5. Save as "ProjectName_Session2_Overdubs"

**Managing Playback from Ableton to MR18**:
1. Ableton's **Main Out** routes to MR18 via USB
2. In MR18, assign **USB Return (stereo)** to a mix bus
3. Send this bus to monitors so performers hear playback
4. Mix live inputs with Ableton playback in MR18

### Using Ableton's New Features with MR18 Recordings

**Stem Separation** (Live 12.3):
- After recording, use Stem Separation to extract elements
- Example: Isolate drums from a stereo overhead recording
- Creates new flexibility even if you didn't use all 18 channels

**Bounce to New Track**:
- Quickly print effects or processing to new tracks
- Consolidate multiple takes or layers
- Free up CPU by bouncing processor-heavy tracks

**Splice Integration**:
- Audition samples to complement your live recordings
- Find drum samples to replace/augment recorded drums
- Enhance productions with additional layers

### Hybrid Recording: Analog Mixing with Digital Multitracking

Use the MR18's analog-style mixing alongside digital multitracking:

**Technique**:
1. **Record all inputs dry** to Ableton (Direct routing)
2. **Use MR18's EQ and dynamics** during live performance/monitoring
3. In **post-production**, choose between:
   - Re-applying processing in Ableton (more flexibility)
   - Using the MR18 again to print processed stems (analog workflow)

**Printing Processed Stems from MR18**:
1. Play back tracks from Ableton to MR18 via USB
2. Route each playback channel through MR18's processing
3. Re-record the processed outputs back to new tracks in Ableton
4. Combines the best of analog mixing feel with digital flexibility

---

## Conclusion

The Midas MR18 and Ableton Live 12.3 combination provides a powerful, professional multitrack recording solution suitable for:
- Live performance recording (concerts, rehearsals)
- Studio tracking (bands, singer-songwriters, podcasts)
- Multi-instrumentalist home recording
- Mobile/remote recording setups
- Educational environments (music schools, universities)

By following this guide, you'll be able to:
- Configure the MR18 as an 18-channel USB interface
- Set up Ableton Live for seamless multitrack recording
- Create professional workflows for tracking and monitoring
- Troubleshoot common issues
- Leverage advanced techniques for complex projects

### Key Takeaways

1. **USB routing is critical**: Always verify MR18's USB sends are configured correctly
2. **Direct/Pre-fader recording** gives maximum flexibility
3. **Zero-latency monitoring** through the MR18 provides the best tracking experience
4. **Proper gain staging** prevents clipping and ensures clean recordings
5. **Template creation** saves time on recurring projects
6. **Regular backups** protect your work

### Resources

- **Midas MR18 Support**: [https://www.musictri.be/Categories/Midas/Mixers/Digital/MR18](https://www.musictri.be/Categories/Midas/Mixers/Digital/MR18)
- **Ableton Live Manual**: [https://www.ableton.com/en/manual/welcome-to-live/](https://www.ableton.com/en/manual/welcome-to-live/)
- **Ableton Live 12.3 Release Notes**: [https://help.ableton.com/hc/en-us/articles/6003767793436](https://help.ableton.com/hc/en-us/articles/6003767793436)
- **User Forums**: Ableton Forum, Gearslutz, Reddit (r/ableton, r/audioengineering)

---

**Document Version**: 1.0  
**Last Updated**: January 4, 2026  
**Covers**: Ableton Live 12.3, Midas MR18 (latest firmware)

