# Powerbeats / Bluetooth + SuperCollider (output only)

We use **output only** (no input): `numInputBusChannels = 0`, `inDevice = nil`, and **supernova** as the server.

## Why supernova?

On macOS, **scsynth** (the default server) still queries an input device even when you set `numInputBusChannels = 0`. That can pull in the Powerbeats mic at 16 kHz and cause "48000 not available" or init failure. **Supernova** uses a different backend (PortAudio) and handles output-only correctly, so no input device is opened and no sample-rate mismatch.

See: [GitHub #4281](https://github.com/supercollider/supercollider/issues/4281) (scsynth fails with 0 inputs; supernova works).

## What the scripts do

- `Server.supernova` — use supernova instead of scsynth.
- `options.numInputBusChannels = 0`, `options.inDevice = nil` — no input.
- `options.outDevice = "Powerbeats Pro"`, `options.sampleRate = 48000` — output device and rate (change in code if you use different hardware).

No aggregate device and no Audio MIDI Setup changes are required.
