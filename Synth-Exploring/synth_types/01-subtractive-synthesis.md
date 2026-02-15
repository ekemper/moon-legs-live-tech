# Subtractive Synthesis: Deep Dive

One of the four most popular software synthesis methods [1]. This document covers how the sound is produced, the mathematics involved, and implementation in SuperCollider.

---

## 1. How the Sound Is Produced

### Signal flow

In [subtractive synthesis](https://ccrma.stanford.edu/~bilbao/booktop/node8.html) [2], the approach is to begin with a rich sound and shape the spectrum using filters [2]:

1. **Source (oscillator)** — A waveform with a **rich spectrum** is generated: sawtooth, square, pulse, or (for noise-based sounds) white/pink noise. These contain many harmonics.
2. **Filter (VCF)** — A low-pass (or band-pass, high-pass) filter **removes** or **attenuates** selected frequency bands. The filter’s cutoff frequency and resonance are usually controlled by envelopes and LFOs.
3. **Amplitude shaping** — An envelope (e.g. ADSR) and optionally a VCA shape the final amplitude over time.

So the sound is produced by **starting rich, then subtracting** frequencies. The spectral envelope of the output is (in the frequency domain) the **product** of the source’s spectrum and the filter’s frequency response [3]. Time-varying filter parameters approximate how many acoustic instruments change brightness over time (e.g. brighter at attack, darker at release).

### Why these waveforms?

- **Sawtooth**: All harmonics present with amplitudes ∝ 1/n → very bright, ideal for subtractive shaping (see [Fourier series—sawtooth](https://mathworld.wolfram.com/FourierSeriesSawtoothWave.html) [4]).
- **Square / pulse**: Odd (or adjustable) harmonics, 1/n rolloff → hollow, clarinet-like (see [Fourier series—square wave](https://mathworld.wolfram.com/FourierSeriesSquareWave.html) [5]).
- **Noise**: Broadband → used for breath, percussion, and effects.

Classic analog subtractive synths (e.g. [Moog Minimoog](https://splice.com/blog/difference-between-synthesis-types/)) use this source–filter–amplitude structure [1]; digital and software synths replicate it with oscillators and digital filters.

---

## 2. Mathematics at Play

### 2.1 Fourier content of common source waveforms

Any periodic waveform can be written as a **Fourier series** [4][5]. For a period \(T\) and fundamental angular frequency \(\omega_0 = 2\pi/T\):

\[
x(t) = \sum_{n=1}^{\infty} \bigl( a_n \cos(n\omega_0 t) + b_n \sin(n\omega_0 t) \bigr)
\]

- **Sawtooth** (odd symmetric, e.g. \(x(t) \propto t\) on \((-T/2, T/2)\)):  
  Harmonics \(n = 1, 2, 3, \ldots\) with amplitudes proportional to **1/n** and alternating sign:
  \[
  x_{\mathrm{saw}}(t) = \frac{2}{\pi} \sum_{n=1}^{\infty} \frac{(-1)^{n+1}}{n} \sin(n\omega_0 t).
  \]

- **Square wave**: Only **odd** harmonics, amplitude ∝ 1/n:
  \[
  x_{\mathrm{sq}}(t) = \frac{4}{\pi} \sum_{n=1,3,5,\ldots} \frac{1}{n} \sin(n\omega_0 t).
  \]

So the “rich spectrum” in subtractive synthesis is exactly this harmonic series; the filter then multiplies these components by its gain at each frequency.

### 2.2 Filtering: spectral multiplication

In the frequency domain, if the source has spectrum \(X(\omega)\) and the filter has **frequency response** \(H(\omega)\) (see [transfer function analysis](https://ccrma.stanford.edu/~jos/filters/Transfer_Function_Analysis.html) [6]), the output spectrum is:

\[
Y(\omega) = H(\omega) \, X(\omega).
\]

So the filter **scales** each harmonic. A low-pass filter has \(|H(\omega)| \approx 1\) below cutoff and falls off above it, thus **subtracting** high-frequency content. Resonance adds a peak near the cutoff, boosting a narrow band.

### 2.3 Transfer function and poles (digital filters)

In discrete time, a filter is described by a **transfer function** \(H(z)\) (z-transform of its impulse response) [6][7]:

\[
H(z) = \frac{Y(z)}{X(z)} = \frac{\sum_k b_k z^{-k}}{1 + \sum_k a_k z^{-k}}.
\]

- **Frequency response**: Evaluate on the unit circle, \(z = e^{j\omega}\), to get \(H(e^{j\omega})\) (gain and phase vs frequency).
- **Poles**: Roots of the denominator. For a **two-pole resonator** (e.g. resonant low-pass), poles are complex conjugates. As pole magnitude \(|p| \to 1\), resonance becomes sharper; pole angle sets center frequency.

So the math of subtractive synthesis is: **Fourier series (source) × filter transfer function (frequency response)**. Time-varying filter coefficients give time-varying brightness and resonance.

---

## 3. SuperCollider Implementation

### 3.1 Building blocks

- **Oscillators**: `Saw`, `Pulse`, `LFTri`, `LFPar`, `LFSaw`, or `WhiteNoise` / `PinkNoise`.
- **Filters**: `LPF`, `HPF`, `BPF`, `RLPF`, `RHPF`, `Resonz`, or Moog-style [`MoogFF`](https://doc.sccode.org/Classes/MoogFF.html) [8], [`MoogVCF`](https://doc.sccode.org/Classes/MoogVCF.html).
- **Envelopes**: `Env`, `EnvGen` (e.g. ADSR for amplitude and/or filter cutoff).
- **LFOs**: `LFNoise`, `LFSaw`, `SinOsc` at control rate (e.g. for filter or pitch modulation).

### 3.2 Minimal subtractive SynthDef (saw + low-pass)

```supercollider
(
SynthDef(\subtractive_saw, {
	arg out = 0, freq = 440, amp = 0.3, gate = 1,
	    cutoff = 2000, res = 0.5, cutoffEnv = 0.5;
	var sig, env, filtEnv;
	env = EnvGen.ar(Env.adsr(0.01, 0.3, 0.5, 0.5), gate, doneAction: 2);
	filtEnv = EnvGen.ar(Env.perc(0.01, 0.5), gate) * 8000 + 200;
	sig = Saw.ar(freq);
	sig = RLPF.ar(sig, cutoff * cutoffEnv + filtEnv, res.reciprocal.clip(0.01, 10));
	sig = sig * env * amp;
	Out.ar(out, sig ! 2);
}).add;
)
```

- `Saw.ar(freq)` provides the rich spectrum (1/n harmonics).
- `RLPF` (resonant LPF) does the “subtraction”; cutoff and resonance can be modulated by envelopes/LFOs.

### 3.3 Using Moog-style filters

```supercollider
SynthDef(\subtractive_moog, {
	arg out = 0, freq = 440, amp = 0.3, gate = 1, cutoff = 3000, res = 0.7;
	var sig, env;
	env = EnvGen.ar(Env.adsr(0.01, 0.3, 0.5, 0.5), gate, doneAction: 2);
	sig = Saw.ar(freq) + Pulse.ar(freq * 1.01, 0.5, 0.3);  // rich source
	sig = MoogFF.ar(sig, cutoff, res * 4);  // MoogFF: res 0–4
	sig = sig * env * amp;
	Out.ar(out, sig ! 2);
}).add;
```

- `MoogFF`: cutoff in Hz, resonance typically 0–4.
- `MoogVCF` is an alternative (e.g. resonance 0–1); both emulate a Moog-style ladder filter for that classic subtractive character.

### 3.4 Modulating cutoff from an envelope

To mimic “bright attack, darker release”, drive the filter cutoff with an envelope (as in the first example with `filtEnv`). You can use the same ADSR as amplitude or a dedicated envelope; key point: **multiply or add envelope to cutoff** so the filter opens and closes over time. That time-varying spectral shaping is the core of subtractive sound design in SuperCollider.

---

## Summary

| Aspect | Content |
|--------|--------|
| **Sound production** | Rich source (saw/square/noise) → filter (LP/BP/HP + resonance) → amplitude envelope. |
| **Math** | Source = Fourier series (e.g. 1/n harmonics); output spectrum = source spectrum × filter \(H(\omega)\); digital filter = \(H(z)\), poles control resonance. |
| **SuperCollider** | `Saw`/`Pulse`/noise → `RLPF`/`MoogFF`/`MoogVCF` + `EnvGen` for amplitude and filter cutoff. |

---

## References

1. [The difference between subtractive, additive, FM, and wavetable synthesis](https://splice.com/blog/difference-between-synthesis-types/) (Splice).
2. [Subtractive Synthesis](https://ccrma.stanford.edu/~bilbao/booktop/node8.html) (CCRMA/Stanford, Stefan Bilbao).
3. [Subtractive synthesis – spectral envelope](https://msp.ucsd.edu/techniques/v0.11/book-html/node152.html) (UCSD MSP).
4. [Fourier Series – Sawtooth Wave](https://mathworld.wolfram.com/FourierSeriesSawtoothWave.html) (Wolfram MathWorld).
5. [Fourier Series – Square Wave](https://mathworld.wolfram.com/FourierSeriesSquareWave.html) (Wolfram MathWorld).
6. [Transfer Function Analysis](https://ccrma.stanford.edu/~jos/filters/Transfer_Function_Analysis.html) (CCRMA/Stanford, JOS).
7. [Transfer Function](https://ccrma.stanford.edu/~jos/fp3/Transfer_Function.html) (CCRMA/Stanford, JOS).
8. [MoogFF – SuperCollider Help](https://doc.sccode.org/Classes/MoogFF.html) (SuperCollider documentation).
