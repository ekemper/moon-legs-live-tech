# Additive Synthesis: Deep Dive

Additive synthesis is one of the four most popular software synthesis methods [1]. It builds complex tones by **summing sinusoids** (partials) with chosen frequencies, amplitudes, and phases. This document covers how the sound is produced, the mathematics (Fourier series, amplitudes, phases), and implementation in SuperCollider.

---

## 1. How the Sound Is Produced

### Signal flow

1. **Oscillators** — Many sinusoidal oscillators (e.g. one per partial). Each has:
   - **Frequency** \(f_l\) (often \(l \cdot f_0\) for harmonic \(l\), or inharmonic for bells).
   - **Amplitude** \(A_l\) (envelope or constant).
   - **Phase** \(\phi_l\) (optional; less critical for steady timbre).
2. **Sum** — All oscillator outputs are **added**.
3. **Global shaping** — Optional amplitude envelope or gain on the sum.

So the sound is produced by **adding** many simple tones. No filter is required; timbre is determined by **which partials** are present and **how loud** each one is. Time-varying amplitudes (e.g. different attack/decay per partial) create evolving spectra (e.g. brass, strings).

### Why sinusoids?

[Fourier theory](https://ccrma.stanford.edu/~bilbao/booktop/node7.html) says that (under mild conditions) any periodic waveform can be represented as a **sum of sinusoids** at integer multiples of the fundamental (plus possibly a DC term) [2][3]. So additive synthesis is the **direct** way to build a desired spectrum: choose amplitudes (and phases) and add the corresponding sinusoids. The downside is **cost**: many oscillators per note. Tricks (e.g. grouping partials, envelopes per band, or analysis–resynthesis) make it tractable.

---

## 2. Mathematics at Play

### 2.1 Single sinusoid (continuous and discrete time)

Continuous time:

\[
u(t) = A \cos(2\pi f_0 t + \phi).
\]

Discrete time (sample rate \(f_s\), sample index \(n\)):

\[
u^n = A \cos(2\pi f_0 n / f_s + \phi).
\]

\(A\) = amplitude, \(f_0\) = frequency, \(\phi\) = initial phase.

### 2.2 Additive sum: the core equation

Sum of \(N\) sinusoids (discrete time):

\[
u^n = \sum_{l=1}^{N} A_l \cos(2\pi f_l \, n / f_s + \phi_l).
\]

- **Harmonic case**: \(f_l = l \cdot f_0\) (\(f_0\) = fundamental). Then the result is **periodic** with period \(1/f_0\) and has a harmonic spectrum. Timbre is set by \(\{A_l\}\) (and, to a lesser extent, \(\phi_l\)).
- **Inharmonic case**: \(f_l\) not integer multiples of a common \(f_0\) → bells, metallic, unpitched.

So the **math that produces the sound** is this sum. No filter, no modulation—just a weighted sum of cosines.

### 2.3 Fourier series connection

For a **periodic** waveform with period \(T\) and fundamental \(f_0 = 1/T\), the [Fourier series](https://wp.nyu.edu/computer_music/4-adding-sine-waves-the-fourier-series-and-additive-synthesis/) is [3][4]:

\[
x(t) = \sum_{k=-\infty}^{\infty} c_k e^{j k \omega_0 t}, \qquad \omega_0 = 2\pi f_0.
\]

For a **real** signal, this can be written as a sum of cosines with amplitudes and phases. So:

- **Analysis**: given a waveform, compute \(A_l\), \(\phi_l\) (or \(c_k\)) → spectrum.
- **Synthesis**: choose \(A_l\), \(\phi_l\) and use the additive sum → **additive synthesis**.

Classic examples:

- **Square wave**: odd harmonics only, \(A_l \propto 1/l\).
- **Sawtooth**: all harmonics, \(A_l \propto 1/l\) (with sign).
- **Triangle**: odd harmonics, \(A_l \propto 1/l^2\).

So the **mathematics at play** is the **Fourier series**: amplitudes (and phases) of each partial define the timbre; additive synthesis is the inverse of Fourier decomposition.

### 2.4 Phase

- **Amplitude** \(A_l\): strongly affects perceived timbre (balance of brightness, character).
- **Phase** \(\phi_l\): changes the **waveform** shape; for **steady** tones the ear is relatively insensitive to phase [5]. For transients or when mixing sources, phase can matter (e.g. cancellation).

In practice, many additive synths use **amplitude envelopes per partial** and fixed or random phases.

---

## 3. SuperCollider Implementation

### 3.1 One partial per oscillator

The direct approach: one `SinOsc` per partial, then sum.

```supercollider
(
SynthDef(\additive_harmonic, {
	arg out = 0, freq = 220, amp = 0.3, gate = 1, numHarmonics = 8;
	var partials, env, fundamental;
	env = EnvGen.ar(Env.adsr(0.01, 0.2, 0.6, 0.5), gate, doneAction: 2);
	fundamental = freq;
	partials = (1..numHarmonics).collect { |l|
		// Amplitude 1/l like saw; scale so sum doesn't clip
		SinOsc.ar(fundamental * l, 0) * (1 / l)
	}.sum;
	partials = partials / numHarmonics;  // rough normalization
	Out.ar(out, (partials * env * amp) ! 2);
}).add;
)
```

This approximates a **saw-like** spectrum (all harmonics, 1/l). For a **square-like** spectrum use only odd \(l\) and same 1/l.

### 3.2 Additive with per-partial amplitude envelopes

```supercollider
(
SynthDef(\additive_brass, {
	arg out = 0, freq = 220, amp = 0.3, gate = 1, numHarmonics = 6;
	var partials, env;
	env = EnvGen.ar(Env.adsr(0.01, 0.1, 0.7, 0.4), gate, doneAction: 2);
	partials = (1..numHarmonics).collect { |l|
		var partialEnv;
		partialEnv = EnvGen.ar(Env.perc(0.01, 0.5 * (1 - (l * 0.05)), 1, -4), gate);
		SinOsc.ar(freq * l, 0) * (1 / l) * partialEnv
	}.sum;
	partials = partials / numHarmonics;
	Out.ar(out, (partials * env * amp) ! 2);
}).add;
)
```

Higher partials decay faster → brass-like brightness evolution.

### 3.3 Inharmonic (bell-like) additive

```supercollider
(
SynthDef(\additive_bell, {
	arg out = 0, freq = 440, amp = 0.2, gate = 1;
	var partials, env, ratios, amps;
	env = EnvGen.ar(Env.perc(0.001, 4), gate, doneAction: 2);
	ratios = [1, 2.2, 3.4, 4.8, 6.1];  // inharmonic
	amps = [1, 0.5, 0.25, 0.125, 0.06];
	partials = (0..4).collect { |i|
		SinOsc.ar(freq * ratios[i], 0) * amps[i] * EnvGen.ar(Env.perc(0.001, 2 + (i * 0.5)), gate)
	}.sum;
	Out.ar(out, (partials * env * amp) ! 2);
}).add;
)
```

### 3.4 Using arrays for many partials (e.g. 32)

```supercollider
(
SynthDef(\additive_saw32, {
	arg out = 0, freq = 110, amp = 0.2, gate = 1;
	var n = 32, env, sig;
	env = EnvGen.ar(Env.adsr(0.01, 0.3, 0.5, 0.5), gate, doneAction: 2);
	sig = (1..n).sum { |l| SinOsc.ar(freq * l, 0) * (1 / l) };
	sig = sig / (1..n).sum { |l| 1/l };  // normalize by sum of 1/l
	Out.ar(out, (sig * env * amp) ! 2);
}).add;
)
```

Larger \(N\) gives a brighter, more "saw-like" tone; CPU cost grows with \(N\).

---

## Summary

| Aspect | Content |
|--------|--------|
| **Sound production** | Many sinusoids (partials) with chosen \(f_l\), \(A_l\), \(\phi_l\) are **added**; timbre = spectrum of partials. |
| **Math** | \(u^n = \sum_l A_l \cos(2\pi f_l n/f_s + \phi_l)\); Fourier series links waveform ↔ amplitudes/phases; harmonic vs inharmonic by choice of \(f_l\). |
| **SuperCollider** | Multiple `SinOsc.ar(freq * l, 0) * (amp_l)` summed; optional per-partial envelopes; normalize to avoid clipping. |

---

## References

1. [The difference between subtractive, additive, FM, and wavetable synthesis](https://splice.com/blog/difference-between-synthesis-types/) (Splice).
2. [Additive Synthesis](https://ccrma.stanford.edu/~bilbao/booktop/node7.html) (CCRMA/Stanford, Stefan Bilbao).
3. [Adding Sine Waves, the Fourier Series, and Additive Synthesis](https://wp.nyu.edu/computer_music/4-adding-sine-waves-the-fourier-series-and-additive-synthesis/) (NYU Computer Music).
4. [Fourier Synthesis](https://www.sfu.ca/sonic-studio-webdav/cmns/Handbook5/handbook/Fourier_Synthesis.html) (SFU Sonic Studio Handbook).
5. [Waveforms and Spectra – Amplitude and Phase](https://www.colinpykett.org.uk/waveforms-and-spectra.htm) (Colin Pykett).
