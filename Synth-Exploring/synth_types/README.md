# Software Synthesizer Types: Documentation Index

Deep-dive docs on the **four most popular** software synthesis methods: how sound is produced, the mathematics involved, and how to implement each in **SuperCollider**.

| # | Type | Doc | One-line summary |
|---|------|-----|------------------|
| 1 | **Subtractive** | [01-subtractive-synthesis.md](01-subtractive-synthesis.md) | Rich source (saw/square/noise) → filter (LP/BP/HP + resonance) → envelope. |
| 2 | **FM** | [02-fm-synthesis.md](02-fm-synthesis.md) | Modulator added into carrier **phase**; spectrum = Bessel sidebands. |
| 3 | **Additive** | [03-additive-synthesis.md](03-additive-synthesis.md) | Sum of sinusoids (Fourier series); timbre = amplitudes (and phases) of partials. |
| 4 | **Wavetable** | [04-wavetable-synthesis.md](04-wavetable-synthesis.md) | Stored single-cycle waveform read by phase accumulator + interpolation; optional morphing. |

Each doc includes:

- **How the sound is produced** — Signal flow and main building blocks.
- **Mathematics** — Core equations (Fourier, transfer functions, Bessel, phase increment, interpolation).
- **SuperCollider** — SynthDefs and UGens (e.g. `Saw`, `RLPF`, `MoogFF`, `SinOsc` phase input, `Osc`, `Phasor`/`BufRd`).
- **References** — Numbered citations and links throughout to CCRMA/Stanford, MathWorld, Wikipedia, SuperCollider docs, and other sources; each doc ends with a **References** section listing all URLs.

The Piano Practice App's Rhodes in `Piano-Practice-App/sc_programs/rhodes_piano.scd` is an example of **nested FM**; see [02-fm-synthesis.md](02-fm-synthesis.md) for the link to the math and implementation.

**Run the subtractive synth GUI** (envelope-modulated cutoff, SC widgets): from repo root run `sclang Synth-Exploring/subtractive_synth_gui.scd`. Requires SuperCollider with Qt GUI (sclang).
