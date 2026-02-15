# Wavetable Synthesis: Deep Dive

Wavetable synthesis is one of the four most popular software synthesis methods [1]. It plays back **stored single-cycle (or short) waveforms** from a table at a rate that sets the pitch, often with **interpolation** and **morphing** between tables. This document covers how the sound is produced, the mathematics (phase accumulator, interpolation), and implementation in SuperCollider.

---

## 1. How the Sound Is Produced

### Signal flow

1. **Wavetable** — A buffer (array) of samples representing one cycle (or a short loop) of a waveform. Can be a sinusoid, saw, square, or any arbitrary shape.
2. **Phase accumulator** — A value that increases each sample by a **phase increment** \(\Delta\phi\), wrapping in \([0, 1)\) or \([0, N)\) (table length). It represents "position in the cycle."
3. **Lookup** — The accumulator indexes into the table. Because \(\Delta\phi\) is usually fractional, **interpolation** (linear, cubic, etc.) is used between adjacent samples.
4. **Output** — The interpolated value is the oscillator output. Optionally, **multiple wavetables** are crossfaded (morphing) for time-varying or modulated timbre.

So the sound is produced by **reading through a fixed waveform at a variable rate**. The rate (phase increment) sets the fundamental frequency; the **shape** of the stored waveform sets the **spectrum** (harmonic content). No separate filter is required for the basic tone; filters and modulation can be applied on top (e.g. subtractive + wavetable).

### Why wavetables?

- **Efficiency**: One table read + interpolation per sample can replace many oscillators (e.g. additive) for a fixed spectrum.
- **Flexibility**: Any single-cycle shape can be stored—recorded, drawn, or computed (Fourier, waveshaping).
- **Morphing**: Blending between tables (e.g. by position or LFO) gives smooth timbre changes (Serum, Vital, Ableton Wavetable style).

---

## 2. Mathematics at Play

### 2.1 Phase accumulator

In [wavetable synthesis](https://en.wikipedia.org/wiki/Wavetable_synthesis) [2][3], the oscillator is implemented by reading a table at a rate that sets pitch. Let the table have **N** samples (one period), sample rate **f_s**, and desired fundamental frequency **f_0**. One period in samples is \(N / f_0\) at rate \(f_s\), so we advance by one full table per period. So **phase increment per sample**:

\[
\Delta\phi = \frac{f_0 \cdot N}{f_s} \quad \text{(in "table samples per sample")}
\]

or, if phase is normalized to \([0, 1)\) (one cycle):

\[
\Delta\phi = \frac{f_0}{f_s}.
\]

Then each sample:

\[
\phi_{n+1} = (\phi_n + \Delta\phi) \bmod 1, \qquad \text{or} \qquad \phi_{n+1} = (\phi_n + \Delta\phi) \bmod N
\]

depending on whether phase is in \([0,1)\) or \([0,N)\). The **index** into the table is \(\phi \cdot N\) (or \(\phi\) if already in \([0,N)\)). So the **math that produces the sound** is: **phase integration** (accumulator) + **table lookup** (with optional interpolation).

### 2.2 Table lookup (no interpolation)

If \(\phi\) is in \([0, N)\) and we use **truncation**:

\[
\text{index} = \lfloor \phi \rfloor, \qquad y_n = \text{table}[\text{index}].
\]

This causes **quantization** and can sound gritty; doubling table size improves quality.

### 2.3 Linear interpolation

Let \(\phi = i + \mu\) with integer \(i\) and \(\mu \in [0, 1)\). Then:

\[
y_n = (1 - \mu) \cdot \text{table}[i] + \mu \cdot \text{table}[i+1].
\]

This is one multiply and two reads per sample and significantly reduces aliasing/quantization compared to truncation [4]. **Cubic** or **allpass** interpolation can improve further at higher CPU cost [3].

### 2.4 Frequency from phase increment

From \(\Delta\phi = f_0 / f_s\) we get:

\[
f_0 = \Delta\phi \cdot f_s.
\]

So in code: **phase increment = desired frequency / sample rate** (when phase is in \([0,1)\)). In SuperCollider, `Osc` and similar UGens hide this: you give frequency and buffer, and the UGen computes the increment and does the lookup.

### 2.5 Spectrum of the output

The **spectrum** of the output is the **Fourier series** of the stored waveform (one period). So the wavetable doesn't add new math to "what is the spectrum"—it's the spectrum of that periodic shape. The math specific to wavetable synthesis is **phase accumulation** and **interpolation**.

---

## 3. SuperCollider Implementation

### 3.1 Buffer + Osc (built-in wavetable oscillator)

SuperCollider’s [`Osc`](https://doc.sccode.org/Classes/Osc.html) [6] reads a **buffer** with a **phase** that advances by **frequency/sampleRate** in cycle units (phase 0–1). It uses interpolation (e.g. linear). So the buffer must hold one cycle (or the UGen will wrap).

```supercollider
// Allocate buffer and fill with one cycle of a saw (or use Signal.sawtooth, etc.)
(
var buf = Buffer.alloc(s, 4096, 1);
buf.loadCollection(Signal.sawtooth(4096).asWavetable);
SynthDef(\wavetable_osc, {
	arg out = 0, buf, freq = 440, amp = 0.3, gate = 1;
	var sig, env, phase;
	env = EnvGen.ar(Env.adsr(0.01, 0.2, 0.6, 0.4), gate, doneAction: 2);
	sig = Osc.ar(buf, freq);
	Out.ar(out, (sig * env * amp) ! 2);
}).add;
)
```

`Osc` implements the phase accumulator and lookup (with interpolation) internally. You just supply buffer and frequency.

### 3.2 Explicit phase accumulator: Phasor + BufRd

For full control (e.g. custom phase or multiple tables), use a **phasor** (ramp 0→1, then wrap) and **BufRd** with linear interpolation:

```supercollider
(
var buf = Buffer.alloc(s, 4096, 1);
buf.loadCollection(Signal.sawtooth(4096).asWavetable);

SynthDef(\wavetable_phasor, {
	arg out = 0, buf, freq = 440, amp = 0.3, gate = 1;
	var phase, sig, env, tableSize;
	tableSize = BufFrames.kr(buf);
	env = EnvGen.ar(Env.adsr(0.01, 0.2, 0.6, 0.4), gate, doneAction: 2);
	// Phasor: advance by (freq/sampleRate)*tableSize table-samples per sample → one cycle per period
	phase = Phasor.ar(0, freq * tableSize / SampleRate.ir, 0, tableSize);
	sig = BufRd.ar(1, buf, phase, 1, 2);  // 2 = linear interpolation
	Out.ar(out, (sig * env * amp) ! 2);
}).add;
)
```

- **Phasor** output is in \([0, \text{tableSize})\) here; `BufRd` with interpolation 2 does linear interpolation between samples. So the **math** is: phase += (freq/sr)*N per sample, then `y = linear_interp(table, phase)`.

### 3.3 Filling the buffer: different waveforms

```supercollider
// Saw
Signal.sawtooth(4096).asWavetable

// Square (e.g. -1 for first half, +1 for second)
Signal.fill(4096, { |i| if(i < 2048) { -1 } { 1 } }).asWavetable

// Sin (for testing)
Signal.sineFill(4096, [1], [0]).asWavetable
```

Load one of these into the buffer; then `Osc.ar(buf, freq)` or the Phasor/BufRd synth will play that shape at `freq`.

### 3.4 Wavetable morphing (two tables, crossfade)

Use two buffers and a **position** (0–1) to crossfade:

```supercollider
(
SynthDef(\wavetable_morph, {
	arg out = 0, buf1, buf2, freq = 440, amp = 0.3, gate = 1, pos = 0;
	var s1, s2, sig, env;
	env = EnvGen.ar(Env.adsr(0.01, 0.2, 0.6, 0.4), gate, doneAction: 2);
	s1 = Osc.ar(buf1, freq);
	s2 = Osc.ar(buf2, freq);
	sig = (s1 * (1 - pos)) + (s2 * pos);
	Out.ar(out, (sig * env * amp) ! 2);
}).add;
)
```

An LFO or envelope on `pos` gives time-varying timbre (wavetable morph).

### 3.5 Relation to phase increment formula

In `Phasor.ar(0, rate, 0, tableSize)` we want the phase to advance by **one full table per period** of the wave. One period = \(f_s / f_0\) samples. So per sample we should advance by **tableSize / (f_s / f_0) = tableSize * f_0 / f_s**. So:

\[
\text{rate} = \frac{f_0 \cdot \text{tableSize}}{f_s}.
\]

So the correct Phasor rate for "one cycle at freq" is **rate = freq × tableSize / SampleRate.ir** (phase in 0..tableSize). The **math** in code is: **phase += (freq / sr) × N** per sample, then read table at phase with interpolation.

---

## Summary

| Aspect | Content |
|--------|--------|
| **Sound production** | Stored single-cycle waveform is read at a rate set by a **phase accumulator**; interpolation between samples; optional morph between tables. |
| **Math** | Phase: \(\phi_{n+1} = (\phi_n + f_0/f_s \cdot N) \bmod N\); output: linear (or other) interpolation of table at \(\phi\); spectrum = Fourier content of table. |
| **SuperCollider** | `Osc.ar(buf, freq)` for simple use; or `Phasor.ar(0, freq*N/SampleRate.ir, 0, N)` + `BufRd.ar(1, buf, phase, 1, 2)` for explicit control; morph = crossfade two `Osc` outputs. |

---

## References

1. [The difference between subtractive, additive, FM, and wavetable synthesis](https://splice.com/blog/difference-between-synthesis-types/) (Splice).
2. [Wavetable synthesis](https://en.wikipedia.org/wiki/Wavetable_synthesis) (Wikipedia).
3. [Wavetable Synthesis](https://ccrma.stanford.edu/~bilbao/booktop/node9.html) (CCRMA/Stanford, Stefan Bilbao).
4. [Wavetable Interpolation](https://caml.music.mcgill.ca/~gary/307/week3/node9.html) (McGill CAML).
5. [Tutorial: Wavetable synthesis](https://docs.juce.com/master/tutorial_wavetable_synth.html) (JUCE).
6. [Osc – SuperCollider Help](https://doc.sccode.org/Classes/Osc.html) (SuperCollider documentation).
