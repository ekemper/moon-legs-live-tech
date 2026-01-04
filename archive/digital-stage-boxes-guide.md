# Digital Stage Boxes - Comprehensive Guide

**Price Range**: $500 - $1,500
**Focus**: Software control capabilities, custom software development, and multitrack recording interfaces

---

## Table of Contents
1. [What Are Digital Stage Boxes?](#what-are-digital-stage-boxes)
2. [Software Control & Custom Development](#software-control--custom-development)
3. [Multitrack Recording & DAW Integration](#multitrack-recording--daw-integration)
4. [Product Comparison](#product-comparison)
5. [Behringer/Midas Models](#behringermidas-models)
6. [Allen & Heath Models](#allen--heath-models)
7. [PreSonus Models](#presonus-models)
8. [Soundcraft Models](#soundcraft-models)
9. [Other Notable Brands](#other-notable-brands)
10. [Comparison Matrix](#comparison-matrix)
11. [Software Development Guide](#software-development-guide)

---

## What Are Digital Stage Boxes?

Digital stage boxes are remote I/O units that convert analog audio signals (from microphones, instruments) into digital audio and transmit them to a mixing console via a single digital cable (Cat5e/Cat6, fiber, or proprietary cable). This eliminates the need for heavy analog snakes.

**Key Benefits:**
- Reduced cable clutter (one cable vs. 16-32+ analog cables)
- Improved signal quality (digital transmission = no signal degradation)
- Remote controllable preamps (adjust gain from FOH position)
- Integration with digital mixers and recording systems
- Lower setup/teardown time

**Common Protocols:**
- **AES50**: Used by Behringer/Midas (based on SuperMAC)
- **dSNAKE**: Allen & Heath proprietary protocol
- **Dante**: Network audio protocol (Audinate)
- **AVB**: Audio Video Bridging (IEEE standard)
- **MADI**: Multi-channel Audio Digital Interface
- **EtherSound**: Digigram/Auvitran protocol

---

## Software Control & Custom Development

### Can You Write Custom Software?

**Short Answer**: It depends on the protocol and manufacturer.

### Protocols That Support Custom Software Development:

#### **1. Dante** ⭐ BEST FOR CUSTOM SOFTWARE
- **Open Protocol**: Yes (with Audinate SDK license)
- **APIs Available**: Dante API, Dante Controller API
- **Programming Languages**: C/C++, Python (via libraries)
- **Cost**: Dante API requires licensing from Audinate (~$1,500-3,000+)
- **Capabilities**:
  - Full routing control
  - Device discovery
  - Subscription management
  - Sample rate changes
  - Integration with custom applications

**Dante-Enabled Stage Boxes:**
- TASCAM SB-16D ($2,499 - outside budget)
- Focusrite RedNet MP8R ($2,995 - outside budget)
- Many high-end stage boxes

**Developer Resources:**
- Dante Controller SDK
- Audinate Developer Network
- Third-party libraries (dante-audio, PyDante)

#### **2. AVB (Audio Video Bridging)** ⭐ OPEN STANDARD
- **Open Protocol**: Yes (IEEE 1722.1)
- **APIs Available**: AVDECC controller libraries
- **Programming Languages**: C/C++, Python
- **Cost**: Free (open standard)
- **Capabilities**:
  - Device discovery and enumeration
  - Stream routing
  - Control of AVB entities
  - Clock domain management

**AVB-Enabled Stage Boxes:**
- PreSonus NSB 16.8 ($1,099)
- PreSonus NSB 8.8 ($799)
- MOTU AVB interfaces

**Developer Resources:**
- Open AVB project (GitHub)
- AVDECC controller implementations
- AVnu Alliance specifications

#### **3. OSC (Open Sound Control)** ⭐ EASIEST TO IMPLEMENT
- **Open Protocol**: Yes
- **APIs Available**: Multiple open-source libraries
- **Programming Languages**: Python, JavaScript, C++, Java, Max/MSP, etc.
- **Cost**: Free
- **Capabilities**:
  - Control mixer parameters
  - Limited to devices that support OSC
  - Network-based (UDP/TCP)
  - Human-readable message format

**OSC-Compatible Systems:**
- Behringer X32/Midas M32 ecosystem (via mixer)
- Some Yamaha digital mixers
- Allen & Heath SQ series
- Many software mixers

**Developer Resources:**
- OSC specification (open)
- Python: python-osc, pythonosc
- JavaScript: osc.js, node-osc
- Extensive open-source community

**Example OSC Control (Python):**
```python
from pythonosc import udp_client

# Connect to X32 mixer
client = udp_client.SimpleUDPClient("192.168.1.100", 10023)

# Set channel 1 gain
client.send_message("/ch/01/preamp/gain", 0.5)

# Mute channel 2
client.send_message("/ch/02/mix/on", 0)
```

#### **4. MIDI** (Limited)
- **Open Protocol**: Yes (but very limited for audio control)
- **Capabilities**: Basic parameter control only
- **Limitations**: Not suitable for routing or preamp control
- **Use Case**: Triggering scenes, basic automation

---

### Proprietary Protocols (Limited/No Custom Software Support):

#### **AES50** (Behringer/Midas)
- **Open Protocol**: Partially (based on SuperMAC, but implementation is closed)
- **Custom Software**: Very difficult
- **Official Control**: Through X32/M32 mixer or X32-Edit/M32-Edit software
- **Community Efforts**: Some reverse engineering, but no official API
- **Workaround**: Control the mixer via OSC, which then controls the stage box

**Behringer/Midas Software:**
- X32-Edit (Windows/Mac) - free
- X32-Mix (iOS/Android) - free
- Mixing Station (third-party, very popular) - $6-10

#### **dSNAKE** (Allen & Heath)
- **Open Protocol**: No
- **Custom Software**: No official API
- **Official Control**: Through compatible mixer (SQ, GLD, iLive)
- **Workaround**: Control mixer via MIDI or OSC (SQ series supports both)

#### **MADI**
- **Open Protocol**: Standard is open, but implementation varies
- **Custom Software**: Depends on device manufacturer
- **Typically**: Requires manufacturer's software for routing

---

## Multitrack Recording & DAW Integration

### Types of Multitrack Recording:

#### **1. Built-in USB Audio Interface** ⭐ BEST FOR DAW RECORDING
Stage boxes/mixers with USB audio interfaces can stream audio directly to a DAW.

**Advantages:**
- Plug-and-play with most DAWs
- Low latency
- Simple setup
- No additional hardware needed

**Models with USB Recording:**
- **Behringer X32 Rack** (32x32 USB interface) - $1,299
- **Behringer XR18** (18x18 USB interface) - $377
- **Behringer XR12** (12x12 USB interface) - $349
- **Midas M32R** (32x32 USB interface) - $2,499 (over budget)
- **Soundcraft Ui24R** (24x24 USB interface) - $1,199
- **PreSonus StudioLive** series (varies by model)

**Compatible DAWs:**
- Reaper (excellent multitrack recording)
- Pro Tools
- Logic Pro
- Ableton Live
- Studio One
- Cubase
- FL Studio
- Audacity (free)

**Setup Example (Behringer XR18):**
1. Connect XR18 to computer via USB
2. Install ASIO driver (Windows) or use Core Audio (Mac)
3. Open DAW and select "X18/XR18" as audio interface
4. Create 18 audio tracks
5. Assign each track to corresponding input channel
6. Record!

#### **2. Dante/AVB Virtual Soundcard** ⭐ PROFESSIONAL OPTION
Network audio protocols can stream audio over Ethernet to your computer.

**Dante Virtual Soundcard (DVS):**
- Cost: $34.99/year subscription or $349 perpetual license
- Channels: Up to 64x64 channels
- Latency: Low (configurable)
- Compatibility: Windows/Mac

**AVB Virtual Interface:**
- MOTU AVB interfaces include software for Mac
- Free with MOTU hardware

**Requirements:**
- Fast computer with good network interface
- Dedicated network (don't share with internet traffic)
- Low-latency mode enabled

#### **3. Direct Recording to USB Drive**
Some mixers can record multitrack directly to a USB thumb drive without a computer.

**Advantages:**
- No computer needed
- Simple backup recording
- Portable

**Disadvantages:**
- Limited track count
- No real-time monitoring in DAW
- Post-event transfer needed

**Models with USB Direct Recording:**
- Soundcraft Ui24R (22 tracks to USB)
- Behringer X32 series (32 tracks to USB)
- Allen & Heath QU series (18 tracks to USB - slightly over budget)

#### **4. SD Card Recording**
Some portable mixers record to SD cards.

**Models:**
- Zoom LiveTrak series
- Tascam Model series

---

## Product Comparison

### Comparison Criteria:
- **I/O Count**: Number of inputs and outputs
- **Protocol**: Digital audio protocol used
- **Software Control**: Available control software
- **Custom Software**: Ability to write custom control software
- **Multitrack Recording**: DAW interface capabilities
- **Ecosystem**: Compatible mixers/devices
- **Price**: USD pricing

---

## Behringer/Midas Models

### Behringer X32 Rack
- **Type**: Digital mixer with stage box functionality
- **I/O**: 16 preamps (local) + 32 via AES50 expansion
- **Protocol**: AES50 (2 ports)
- **Software Control**: X32-Edit, X32-Mix, OSC
- **Custom Software**: ⭐ YES via OSC protocol
- **Multitrack Recording**: ✅ 32x32 USB audio interface
- **Ecosystem**: X32/S16/S32/DL16/DL32
- **Price**: ~$1,299
- **Weight**: 20.5 lbs (9.3 kg)
- **Features**:
  - 16 Midas-designed preamps onboard
  - 40-bit floating point processing
  - 8 DCA groups
  - 6 mute groups
  - Effects processors
  - RTA (Real-Time Analyzer)
  - Wi-Fi control via app
  - Stereo recording to USB drive
  - 32-track recording to DAW via USB
- **Reviews**: Industry standard for prosumer/professional digital mixing. Excellent value, reliable, massive user community. OSC protocol is well-documented and widely supported.
- **DAW Integration**: Excellent - plug and play with all major DAWs
- **Custom Software**: ⭐⭐⭐⭐⭐ Excellent OSC support, extensive documentation, large community

### Behringer XR18
- **Type**: Digital mixer with built-in stage box
- **I/O**: 16 preamps + 2 stereo aux inputs
- **Protocol**: Wi-Fi/Ethernet control only (no expansion)
- **Software Control**: X Air Edit, X Air app, OSC
- **Custom Software**: ⭐ YES via OSC protocol
- **Multitrack Recording**: ✅ 18x18 USB audio interface
- **Ecosystem**: Standalone (no expansion)
- **Price**: ~$377
- **Weight**: 8.8 lbs (4 kg)
- **Features**:
  - 16 Midas-designed preamps
  - Tablet/phone control (iOS/Android)
  - 40-bit floating point processing
  - 4 stereo effects
  - 6 aux sends
  - Wifi control
  - Ultra-compact
  - Perfect for portable recording rig
- **Reviews**: Incredible value for portable recording and live sound. No physical faders (tablet/phone control only). Great for small venues, podcast studios, live recording.
- **DAW Integration**: ⭐⭐⭐⭐⭐ Perfect for home/project studios
- **Custom Software**: ⭐⭐⭐⭐⭐ Full OSC support

### Behringer XR12
- **Type**: Ultra-compact digital mixer
- **I/O**: 8 preamps + 4 stereo inputs
- **Protocol**: Wi-Fi/Ethernet
- **Software Control**: X Air Edit, X Air app, OSC
- **Custom Software**: ⭐ YES via OSC protocol
- **Multitrack Recording**: ✅ 12x12 USB audio interface
- **Ecosystem**: Standalone
- **Price**: ~$349
- **Weight**: 5.3 lbs (2.4 kg)
- **Features**:
  - 8 Midas preamps
  - Tablet control
  - 4 effects processors
  - Extremely portable
  - Perfect for small bands/podcasts
- **Reviews**: Smallest in XR series, perfect for ultra-portable applications. Limited I/O but excellent sound quality.
- **DAW Integration**: ⭐⭐⭐⭐⭐ Excellent for smaller projects
- **Custom Software**: ⭐⭐⭐⭐⭐ Full OSC support

### Behringer S16
- **Type**: Digital stage box (I/O expander only)
- **I/O**: 16 preamps + 8 outputs
- **Protocol**: AES50 (Ultranet on outputs)
- **Software Control**: Via X32/M32 mixer only
- **Custom Software**: ⚠️ NO (requires X32/M32 mixer, then OSC control)
- **Multitrack Recording**: ❌ No (requires mixer with USB interface)
- **Ecosystem**: X32/M32 ecosystem
- **Price**: ~$579
- **Weight**: 15.4 lbs (7 kg)
- **Features**:
  - 16 Midas-designed preamps
  - Rugged metal chassis
  - Remote preamp control via mixer
  - P16 personal monitoring outputs
  - Rack mountable (3U)
- **Reviews**: Solid I/O expander for X32 ecosystem. No standalone functionality - requires compatible mixer.
- **DAW Integration**: ⭐ Via connected mixer only
- **Custom Software**: ⭐ Only through mixer via OSC

### Behringer S32
- **Type**: Digital stage box (I/O expander only)
- **I/O**: 32 preamps + 16 outputs
- **Protocol**: AES50
- **Software Control**: Via X32/M32 mixer only
- **Custom Software**: ⚠️ NO (requires mixer)
- **Multitrack Recording**: ❌ No (requires mixer)
- **Ecosystem**: X32/M32 ecosystem
- **Price**: ~$659
- **Weight**: 19.6 lbs (8.9 kg)
- **Features**:
  - 32 Midas-designed preamps
  - 16 XLR outputs
  - Dual AES50 ports (redundancy)
  - Remote preamp control
  - Rack mountable (3U)
- **Reviews**: High channel count for the price. Great for larger productions. Requires X32/M32 mixer.
- **DAW Integration**: ⭐ Via connected mixer only
- **Custom Software**: ⭐ Only through mixer via OSC

### Midas DL16
- **Type**: Digital stage box (I/O expander only)
- **I/O**: 16 preamps + 8 outputs
- **Protocol**: AES50
- **Software Control**: Via M32/PRO series mixer
- **Custom Software**: ⚠️ NO (requires mixer)
- **Multitrack Recording**: ❌ No (requires mixer)
- **Ecosystem**: Midas/X32 ecosystem
- **Price**: ~$999
- **Weight**: 15 lbs (6.8 kg)
- **Features**:
  - 16 Midas PRO preamps (higher quality than S16)
  - Rugged touring construction
  - Remote preamp control
  - Redundant PSU option
  - Rack mountable (3U)
- **Reviews**: Premium quality compared to S16. Midas brand with better preamps. Excellent for professional touring.
- **DAW Integration**: ⭐ Via connected mixer only
- **Custom Software**: ⭐ Only through mixer via OSC

### Midas DL32
- **Type**: Digital stage box (I/O expander only)
- **I/O**: 32 preamps + 16 outputs
- **Protocol**: AES50 (dual ports)
- **Software Control**: Via M32/PRO series mixer
- **Custom Software**: ⚠️ NO (requires mixer)
- **Multitrack Recording**: ❌ No (requires mixer)
- **Ecosystem**: Midas/X32 ecosystem
- **Price**: ~$1,199
- **Weight**: 20 lbs (9.1 kg)
- **Features**:
  - 32 Midas PRO preamps
  - Redundant AES50 ports
  - Touring-grade construction
  - Remote preamp control
  - Dual power supplies
- **Reviews**: Professional-grade I/O expander. Used on major tours. Excellent preamp quality.
- **DAW Integration**: ⭐ Via connected mixer only
- **Custom Software**: ⭐ Only through mixer via OSC

---

## Allen & Heath Models

### Allen & Heath DX168
- **Type**: Digital stage box (I/O expander only)
- **I/O**: 16 preamps + 8 outputs
- **Protocol**: dSNAKE (96kHz)
- **Software Control**: Via SQ/Avantis mixer
- **Custom Software**: ⚠️ LIMITED (SQ mixers support MIDI/OSC)
- **Multitrack Recording**: ❌ No (requires mixer)
- **Ecosystem**: Allen & Heath SQ/Avantis
- **Price**: ~$1,199
- **Weight**: 13.2 lbs (6 kg)
- **Features**:
  - 16 preamps with phantom power
  - 96kHz operation
  - Redundant dSNAKE ports
  - Compact 2U design
  - Touring-grade build quality
  - Remote preamp control
- **Reviews**: High-quality preamps. Excellent for SQ series mixers. Professional build quality.
- **DAW Integration**: ⭐⭐ Via SQ mixer (varies by model)
- **Custom Software**: ⭐⭐ Limited to SQ mixer control via MIDI/OSC

### Allen & Heath AB168
- **Type**: Digital stage box (I/O expander only)
- **I/O**: 16 preamps + 8 outputs
- **Protocol**: dSNAKE (48kHz)
- **Software Control**: Via GLD mixer
- **Custom Software**: ❌ NO
- **Multitrack Recording**: ❌ No (requires mixer)
- **Ecosystem**: Allen & Heath GLD series
- **Price**: ~$1,199
- **Weight**: 13.2 lbs (6 kg)
- **Features**:
  - 16 preamps
  - 48kHz operation
  - Designed for GLD series
  - Touring construction
- **Reviews**: Solid I/O for GLD ecosystem. Older technology (48kHz). Good reliability.
- **DAW Integration**: ⭐ Via GLD mixer
- **Custom Software**: ❌ Very limited

### Allen & Heath AR2412
- **Type**: Digital stage box (I/O expander only)
- **I/O**: 24 preamps + 12 outputs
- **Protocol**: dSNAKE (96kHz)
- **Software Control**: Via iLive/GLD mixer
- **Custom Software**: ❌ NO
- **Multitrack Recording**: ❌ No (requires mixer)
- **Ecosystem**: Allen & Heath iLive/GLD
- **Price**: ~$1,499
- **Weight**: 31 lbs (14 kg)
- **Features**:
  - 24 preamps
  - 12 outputs
  - 96kHz capable
  - Modular I/O cards
  - Redundant power supplies
- **Reviews**: Professional I/O expander for larger systems. Modular flexibility.
- **DAW Integration**: ⭐ Via mixer
- **Custom Software**: ❌ Very limited

---

## PreSonus Models

### PreSonus NSB 16.8
- **Type**: Digital stage box (AVB networked I/O)
- **I/O**: 16 preamps + 8 outputs
- **Protocol**: AVB (Audio Video Bridging)
- **Software Control**: Via StudioLive mixer or UC Surface
- **Custom Software**: ⭐⭐⭐ YES via AVB (open standard)
- **Multitrack Recording**: ✅ Via AVB virtual interface
- **Ecosystem**: StudioLive Series III
- **Price**: ~$1,099
- **Weight**: 12.8 lbs (5.8 kg)
- **Features**:
  - 16 XMAX preamps
  - 8 line outputs
  - AVB networking (open standard)
  - Dual AVB ports
  - Software control via UC Surface
  - Rack mountable (1U)
  - Can function standalone with computer + AVB software
- **Reviews**: Excellent AVB implementation. Open standard allows flexibility. Great preamps. Can be used without mixer if you have AVB software/interface.
- **DAW Integration**: ⭐⭐⭐⭐ Excellent via AVB
- **Custom Software**: ⭐⭐⭐⭐ AVB is open standard with APIs

### PreSonus NSB 8.8
- **Type**: Digital stage box (AVB networked I/O)
- **I/O**: 8 preamps + 8 outputs
- **Protocol**: AVB
- **Software Control**: Via StudioLive mixer or UC Surface
- **Custom Software**: ⭐⭐⭐ YES via AVB
- **Multitrack Recording**: ✅ Via AVB
- **Ecosystem**: StudioLive Series III
- **Price**: ~$799
- **Weight**: 8.6 lbs (3.9 kg)
- **Features**:
  - 8 XMAX preamps
  - 8 line outputs
  - AVB networking
  - Dual AVB ports
  - Compact 1U
  - Remote preamp control
- **Reviews**: Smaller version of NSB 16.8. Perfect for small-medium applications. AVB flexibility.
- **DAW Integration**: ⭐⭐⭐⭐ Excellent via AVB
- **Custom Software**: ⭐⭐⭐⭐ AVB open standard

---

## Soundcraft Models

### Soundcraft Ui24R
- **Type**: Digital mixer with stage box functionality
- **I/O**: 20 preamps + 2 HiZ inputs
- **Protocol**: Wi-Fi/Ethernet control
- **Software Control**: Ui24R app (browser-based), MIDI
- **Custom Software**: ⚠️ LIMITED (MIDI only, no official API)
- **Multitrack Recording**: ✅ 24x24 USB interface + direct USB recording
- **Ecosystem**: Standalone
- **Price**: ~$1,199
- **Weight**: 17.6 lbs (8 kg)
- **Features**:
  - 20 onboard preamps
  - 24x24 USB audio interface
  - 22-track recording to USB drive
  - dbx DriveRack processing
  - Lexicon reverbs
  - Browser-based control (no app download)
  - Wi-Fi access point built-in
  - MIDI control
  - Dual power supplies
  - 4-band parametric EQ per channel
- **Reviews**: Unique browser-based control. Excellent built-in effects. Great for installed systems. USB recording is convenient. No physical faders.
- **DAW Integration**: ⭐⭐⭐⭐⭐ 24x24 USB, plus direct USB recording
- **Custom Software**: ⭐⭐ MIDI control only, no official API

### Soundcraft Ui16
- **Type**: Digital mixer (compact)
- **I/O**: 12 preamps
- **Protocol**: Wi-Fi/Ethernet
- **Software Control**: Browser-based
- **Custom Software**: ⚠️ LIMITED (MIDI only)
- **Multitrack Recording**: ✅ 16x16 USB interface
- **Ecosystem**: Standalone
- **Price**: ~$699
- **Weight**: 9.7 lbs (4.4 kg)
- **Features**:
  - 12 preamps
  - Browser control
  - dbx processing
  - Lexicon effects
  - Compact design
- **Reviews**: Budget-friendly option. Good for small venues. Limited I/O.
- **DAW Integration**: ⭐⭐⭐⭐ 16x16 USB
- **Custom Software**: ⭐⭐ MIDI only

---

## Other Notable Brands

### Yamaha Rio1608-D2
- **Type**: Digital stage box (Dante I/O)
- **I/O**: 16 preamps + 8 outputs
- **Protocol**: Dante
- **Software Control**: Via Yamaha CL/QL/TF mixer
- **Custom Software**: ⭐⭐⭐⭐⭐ YES via Dante API (requires licensing)
- **Multitrack Recording**: ✅ Via Dante Virtual Soundcard
- **Ecosystem**: Yamaha CL/QL/TF series
- **Price**: ~$2,700 (OVER BUDGET)
- **Features**:
  - Dante networking
  - Premium preamps
  - Redundant Dante ports
  - High-end professional
- **Note**: Over budget but included for Dante reference

### TASCAM SB-16D
- **Type**: Dante stage box
- **I/O**: 16 preamps + 16 outputs
- **Protocol**: Dante
- **Software Control**: Dante Controller
- **Custom Software**: ⭐⭐⭐⭐⭐ YES via Dante API
- **Multitrack Recording**: ✅ Via Dante Virtual Soundcard
- **Ecosystem**: Universal Dante
- **Price**: ~$2,499 (OVER BUDGET)
- **Features**:
  - Full Dante implementation
  - Universal compatibility
  - Software-controlled preamps
- **Note**: Over budget but best for custom software development

---

## Comparison Matrix

### Main Comparison

| Model | Type | I/O | Protocol | Custom Software | USB DAW Recording | Price | Best For |
|-------|------|-----|----------|----------------|-------------------|-------|----------|
| **Behringer XR18** | Mixer | 16+2 | Wi-Fi | ⭐⭐⭐⭐⭐ OSC | ✅ 18x18 | $377 | **Best value for recording & custom software** |
| **Behringer X32 Rack** | Mixer | 16+32 | AES50 | ⭐⭐⭐⭐⭐ OSC | ✅ 32x32 | $1,299 | **Best professional recording option** |
| **Soundcraft Ui24R** | Mixer | 20+2 | Wi-Fi | ⭐⭐ MIDI | ✅ 24x24 + USB | $1,199 | **Best for direct USB recording** |
| **PreSonus NSB 16.8** | Stage Box | 16/8 | AVB | ⭐⭐⭐⭐ AVB | ✅ Via AVB | $1,099 | **Best open protocol (AVB)** |
| **PreSonus NSB 8.8** | Stage Box | 8/8 | AVB | ⭐⭐⭐⭐ AVB | ✅ Via AVB | $799 | **Budget AVB option** |
| **Behringer S16** | Stage Box | 16/8 | AES50 | ⭐ Via mixer | ❌ Via mixer | $579 | **Budget I/O expander** |
| **Behringer S32** | Stage Box | 32/16 | AES50 | ⭐ Via mixer | ❌ Via mixer | $659 | **High channel count expander** |
| **Midas DL16** | Stage Box | 16/8 | AES50 | ⭐ Via mixer | ❌ Via mixer | $999 | **Premium I/O expander** |
| **Midas DL32** | Stage Box | 32/16 | AES50 | ⭐ Via mixer | ❌ Via mixer | $1,199 | **Professional I/O expander** |
| **Allen & Heath DX168** | Stage Box | 16/8 | dSNAKE | ⭐⭐ Limited | ❌ Via mixer | $1,199 | **SQ ecosystem** |
| **Behringer XR12** | Mixer | 8+4 | Wi-Fi | ⭐⭐⭐⭐⭐ OSC | ✅ 12x12 | $349 | **Ultra-portable recording** |
| **Soundcraft Ui16** | Mixer | 12 | Wi-Fi | ⭐⭐ MIDI | ✅ 16x16 | $699 | **Budget recording mixer** |

### Software Control Capabilities

| Model | OSC | MIDI | Dante API | AVB API | Proprietary API | Community Support |
|-------|-----|------|-----------|---------|-----------------|-------------------|
| Behringer XR18 | ✅ Full | ❌ | ❌ | ❌ | ❌ | ⭐⭐⭐⭐⭐ Excellent |
| Behringer X32 Rack | ✅ Full | ✅ Basic | ❌ | ❌ | ❌ | ⭐⭐⭐⭐⭐ Excellent |
| Soundcraft Ui24R | ❌ | ✅ Yes | ❌ | ❌ | ❌ | ⭐⭐⭐ Good |
| PreSonus NSB 16.8 | ⚠️ Via mixer | ❌ | ❌ | ✅ Yes | ❌ | ⭐⭐⭐ Good |
| PreSonus NSB 8.8 | ⚠️ Via mixer | ❌ | ❌ | ✅ Yes | ❌ | ⭐⭐⭐ Good |
| Behringer S16 | ⚠️ Via mixer | ❌ | ❌ | ❌ | ❌ | ⭐⭐⭐⭐ Good |
| Midas DL16 | ⚠️ Via mixer | ❌ | ❌ | ❌ | ❌ | ⭐⭐⭐⭐ Good |
| Allen & Heath DX168 | ⚠️ Via mixer | ⚠️ Via mixer | ❌ | ❌ | ❌ | ⭐⭐⭐ Good |

### Recording Capabilities

| Model | USB Interface | Dante | AVB | Direct USB Recording | Max Tracks | Latency |
|-------|---------------|-------|-----|---------------------|------------|---------|
| Behringer XR18 | ✅ 18x18 | ❌ | ❌ | ❌ | 18 | Low |
| Behringer X32 Rack | ✅ 32x32 | ❌ | ❌ | ✅ 32-track | 32 | Low |
| Soundcraft Ui24R | ✅ 24x24 | ❌ | ❌ | ✅ 22-track | 24 | Low |
| PreSonus NSB 16.8 | ❌ | ❌ | ✅ Yes | ❌ | 16 | Very Low |
| PreSonus NSB 8.8 | ❌ | ❌ | ✅ Yes | ❌ | 8 | Very Low |
| Behringer XR12 | ✅ 12x12 | ❌ | ❌ | ❌ | 12 | Low |
| Soundcraft Ui16 | ✅ 16x16 | ❌ | ❌ | ❌ | 16 | Low |

---

## Software Development Guide

### Best Options for Custom Software Development:

#### 🥇 **#1 Recommendation: Behringer XR18 ($377)**
**Why:**
- Full OSC protocol support
- Extensive documentation
- Large community
- Built-in USB interface for recording
- Affordable
- Standalone operation

**What You Can Control:**
- All channel parameters (gain, EQ, compression, etc.)
- Routing
- Effects
- Mutes, solos, faders
- Scene recall
- Metering

**Development Tools:**
- Python: `pythonosc` library
- JavaScript: `osc.js`, `node-osc`
- C++: `oscpack`
- Max/MSP: built-in OSC objects
- TouchOSC: visual editor for custom control surfaces

**Example Projects:**
- Custom mixing apps
- Automated mixing based on audio analysis
- Integration with lighting systems
- Remote control via web interface
- Automated scene changes
- Custom metering displays

**Getting Started:**
```python
# Install: pip install python-osc
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server

# Send commands to XR18
client = udp_client.SimpleUDPClient("192.168.1.1", 10024)

# Set channel 1 gain
client.send_message("/ch/01/preamp/gain", 0.5)

# Set channel 1 EQ
client.send_message("/ch/01/eq/1/f", 250.0)  # Frequency
client.send_message("/ch/01/eq/1/g", 3.0)     # Gain
client.send_message("/ch/01/eq/1/q", 2.0)     # Q factor

# Receive feedback from XR18
def handle_meter(address, *args):
    print(f"Meter: {address} = {args}")

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/meters/*", handle_meter)

server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", 10023), dispatcher)
server.serve_forever()
```

**Resources:**
- [X32 OSC Protocol Documentation](https://wiki.munichmakerlab.de/images/1/17/UNOFFICIAL_X32_OSC_REMOTE_PROTOCOL_%28preliminary_draft%29.pdf)
- [XR18 Community Forum](https://community.musictribe.com/)
- [GitHub: X32 OSC projects](https://github.com/topics/x32-osc)
- [Mixing Station app](https://mixing-station.com/) (example of third-party control)

---

#### 🥈 **#2 Recommendation: Behringer X32 Rack ($1,299)**
**Why:**
- Same OSC protocol as XR18
- 32-track recording
- More professional features
- Expandable with S16/S32 stage boxes
- Physical controls available

**Best For:**
- Professional recording
- Larger productions
- Systems requiring expansion

---

#### 🥉 **#3 Recommendation: PreSonus NSB 16.8 ($1,099)**
**Why:**
- AVB is an open protocol
- Can be used standalone with computer
- Professional sound quality
- IEEE standard (future-proof)

**Challenges:**
- More complex than OSC
- Requires AVB hardware/software on computer
- Smaller community than X32
- More programming effort required

**Development Tools:**
- [Open AVB GitHub](https://github.com/AVnu/OpenAvnu)
- AVDECC controller libraries
- C/C++ primarily

**Best For:**
- Advanced developers
- Systems requiring low latency
- Networked audio installations
- Future-proof open standards

---

### OSC Protocol Deep Dive (X32/XR18):

#### Message Format:
```
/ch/01/mix/fader <float>  # Channel 1 fader (0.0 to 1.0)
/ch/01/mix/on <int>       # Channel 1 mute (0=off, 1=on)
/ch/01/preamp/gain <float> # Preamp gain (0.0 to 1.0)
```

#### Common OSC Addresses:

**Channel Strip:**
```
/ch/01/preamp/gain        # Input gain
/ch/01/preamp/invert      # Phase invert
/ch/01/gate/on            # Gate on/off
/ch/01/gate/thr           # Gate threshold
/ch/01/dyn/on             # Compressor on/off
/ch/01/dyn/thr            # Compressor threshold
/ch/01/dyn/ratio          # Compressor ratio
/ch/01/eq/on              # EQ on/off
/ch/01/eq/1/f             # EQ band 1 frequency
/ch/01/eq/1/g             # EQ band 1 gain
/ch/01/mix/fader          # Channel fader
/ch/01/mix/on             # Channel mute
/ch/01/mix/pan            # Channel pan
```

**Auxiliary Sends:**
```
/ch/01/mix/01/level       # Channel 1 → Aux 1 send level
/ch/01/mix/01/on          # Channel 1 → Aux 1 mute
```

**Master Controls:**
```
/main/st/mix/fader        # Main LR fader
/main/st/mix/on           # Main LR mute
```

**Scene Recall:**
```
/scene/load <int>         # Load scene number
```

**Metering:**
```
/meters/0                 # Subscribe to meters (sends continuous data)
```

#### Example: Auto-Ducking (Duck music when mic is active)

```python
from pythonosc import udp_client, dispatcher, osc_server
import threading

client = udp_client.SimpleUDPClient("192.168.1.1", 10024)
music_level = 0.75  # Normal music level
ducked_level = 0.30  # Ducked music level
mic_threshold = 0.1  # Mic activity threshold

def handle_meter(address, *args):
    # Parse meter data (simplified)
    mic_level = args[0]  # Assuming first value is mic level
    
    if mic_level > mic_threshold:
        # Mic is active - duck music
        client.send_message("/ch/02/mix/fader", ducked_level)
    else:
        # Mic is inactive - restore music
        client.send_message("/ch/02/mix/fader", music_level)

# Set up meter subscription
disp = dispatcher.Dispatcher()
disp.map("/meters/0", handle_meter)

server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", 10023), disp)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()

# Subscribe to meters
client.send_message("/meters", "/meters/0")
```

#### Example: Scene Manager with Web Interface

```python
from flask import Flask, render_template, request
from pythonosc import udp_client

app = Flask(__name__)
client = udp_client.SimpleUDPClient("192.168.1.1", 10024)

scenes = {
    1: "Intro Music",
    2: "Speaker 1",
    3: "Speaker 2",
    4: "Panel Discussion",
    5: "Q&A",
    6: "Outro Music"
}

@app.route('/')
def index():
    return render_template('scenes.html', scenes=scenes)

@app.route('/load/<int:scene_num>')
def load_scene(scene_num):
    client.send_message("/scene/load", scene_num)
    return f"Loaded scene {scene_num}: {scenes[scene_num]}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

---

### AVB Protocol Deep Dive (PreSonus NSB):

#### What is AVB?
AVB (Audio Video Bridging) is an IEEE standard for low-latency, synchronized audio/video streaming over Ethernet.

**Key Standards:**
- IEEE 802.1AS (timing and synchronization)
- IEEE 802.1Qat (stream reservation)
- IEEE 802.1Qav (traffic shaping)
- IEEE 1722 (audio/video transport)
- IEEE 1722.1 (AVDECC - device discovery and control)

#### AVB Advantages:
- Open standard (not proprietary)
- Very low latency (<2ms)
- Deterministic (guaranteed bandwidth)
- Interoperable between brands
- Future-proof

#### AVB Challenges:
- Requires AVB-compatible network switches
- More complex than USB
- Smaller community than Dante
- Less mature ecosystem

#### Software Development:
AVB development is more complex than OSC:

```cpp
// Example: AVDECC controller (simplified)
#include "avdecc/controller.hpp"

// Discover AVB entities
auto controller = avdecc::controller::Controller::create();

controller->discoverEntities([](avdecc::entity::Entity const& entity) {
    std::cout << "Found: " << entity.getEntityName() << std::endl;
    
    // Get audio streams
    auto streams = entity.getInputStreams();
    for (auto& stream : streams) {
        std::cout << "Stream: " << stream.getName() << std::endl;
    }
});

// Connect streams
controller->connectStream(
    sourceEntityID, sourceStreamIndex,
    destEntityID, destStreamIndex
);
```

**Resources:**
- [AVnu Alliance](https://avnu.org/)
- [Open AVB GitHub](https://github.com/AVnu/OpenAvnu)
- [AVDECC Controller Library](https://github.com/L-Acoustics/avdecc)

---

## Selection Guide by Use Case

### For Custom Software Development:

**Best Overall: Behringer XR18 ($377)**
- Full OSC protocol
- Great documentation
- Large community
- Built-in recording

**Professional: Behringer X32 Rack ($1,299)**
- Same OSC as XR18
- More channels
- More features
- Expandable

**Open Standards: PreSonus NSB 16.8 ($1,099)**
- AVB open protocol
- Professional quality
- Future-proof
- More complex development

### For Multitrack Recording to DAW:

**Best Value: Behringer XR18 ($377)**
- 18x18 USB interface
- Plug and play
- Excellent preamps
- Portable

**Most Channels: Behringer X32 Rack ($1,299)**
- 32x32 USB interface
- Professional features
- Direct USB recording
- Expandable

**Browser-Based: Soundcraft Ui24R ($1,199)**
- 24x24 USB interface
- Direct USB recording (22 tracks)
- No app download needed
- Great effects

**Open Standard: PreSonus NSB 16.8 ($1,099)**
- AVB networking
- Low latency
- Professional quality
- Flexible routing

### For Live Recording Without Computer:

**Best: Soundcraft Ui24R ($1,199)**
- 22-track recording to USB drive
- No computer needed
- Browser control
- Dual power supplies

**Alternative: Behringer X32 Rack ($1,299)**
- 32-track recording to USB drive
- Professional features
- Also has 32x32 USB interface

### For Portable Recording Rig:

**Ultra-Portable: Behringer XR12 ($349)**
- Extremely compact
- 12x12 USB
- Tablet control
- Great for podcasts

**Best Balance: Behringer XR18 ($377)**
- 16 channels
- 18x18 USB
- Still portable
- More versatile

### For Stage Box + Mixer Combo:

**Budget: Behringer S16 + X32 Rack ($579 + $1,299 = $1,878)**
- 16+16 = 32 inputs
- Full OSC control
- 32x32 USB recording
- Expandable

**Premium: Midas DL16 + M32R (over budget)**
- Better preamps
- Professional quality

---

## Key Takeaways

### ✅ **Can You Write Custom Software?**

**YES - With These Devices:**
1. **Behringer XR18/XR12/X32** - OSC protocol (easiest)
2. **PreSonus NSB series** - AVB protocol (advanced)
3. **Soundcraft Ui24R** - MIDI control (limited)

**NO - These Require Proprietary Mixer:**
- Behringer S16/S32
- Midas DL16/DL32 (standalone)
- Allen & Heath DX168/AB168/AR2412 (standalone)

### ✅ **Best for Multitrack Recording:**

**USB Interface (Easiest):**
1. Behringer X32 Rack (32x32) - $1,299
2. Soundcraft Ui24R (24x24) - $1,199
3. Behringer XR18 (18x18) - $377

**Direct USB Recording (No Computer):**
1. Soundcraft Ui24R (22 tracks)
2. Behringer X32 Rack (32 tracks)

**Network Audio:**
1. PreSonus NSB 16.8 (AVB) - $1,099

### 🏆 **Overall Recommendations:**

**Best Value Overall:**
**Behringer XR18 ($377)**
- OSC control ✅
- 18x18 USB recording ✅
- Portable ✅
- Great preamps ✅
- Large community ✅

**Best Professional Option:**
**Behringer X32 Rack ($1,299)**
- Full OSC control ✅
- 32x32 USB recording ✅
- Direct USB recording ✅
- Expandable ✅
- Industry standard ✅

**Best Open Protocol:**
**PreSonus NSB 16.8 ($1,099)**
- AVB open standard ✅
- Professional quality ✅
- Low latency ✅
- Future-proof ✅

---

## Frequently Asked Questions

### Q: Can I control a stage box without a mixer?
**A:** Depends on the model:
- **YES**: Devices with USB/AVB/Dante and software control (XR18, NSB 16.8, Ui24R)
- **NO**: Traditional stage boxes (S16, DL16, DX168) require compatible mixer

### Q: What's the difference between a stage box and a mixer?
**A:** 
- **Stage Box**: Remote I/O only, controlled by external mixer
- **Mixer**: Has processing, mixing, and control interface
- **Hybrid**: XR18, X32 Rack, Ui24R combine both functions

### Q: Which protocol is easiest for custom software?
**A:** OSC (Open Sound Control) - human-readable, well-documented, large community

### Q: Can I record to my DAW and mix live simultaneously?
**A:** YES - all models with USB interfaces support this (XR18, X32 Rack, Ui24R)

### Q: Do I need special network switches for AVB?
**A:** YES - AVB requires AVB-compatible switches (about $200-500 for prosumer models)

### Q: Can I use these stage boxes with any DAW?
**A:** YES - models with USB interfaces work with all major DAWs (Reaper, Pro Tools, Logic, Ableton, etc.)

### Q: What's the latency for USB recording?
**A:** Typically 5-10ms round-trip, depending on buffer size and computer performance

### Q: Can I expand channel count later?
**A:** 
- **YES**: X32 Rack (add S16/S32 stage boxes via AES50)
- **NO**: XR18, Ui24R are fixed channel count

### Q: Which has the best preamps?
**A:** Midas models (DL16, DL32, M32R) > Behringer/PreSonus/Soundcraft (all very good for the price)

### Q: Can I control these from a tablet/phone?
**A:** 
- **YES**: XR18, X32 Rack, Ui24R all have iOS/Android apps
- **Third-party apps**: Mixing Station (highly recommended, $6-10)

---

*Last Updated: October 2025*
*Prices are approximate USD and may vary by region and dealer*
*Software development information based on current manufacturer specifications and community resources*

