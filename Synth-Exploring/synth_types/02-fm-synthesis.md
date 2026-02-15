# FM (Frequency Modulation) Synthesis: Deep Dive

FM synthesis is one of the four most popular software synthesis methods [1]. It was invented by [John Chowning](https://ccrma.stanford.edu/~jos/rbeats/Sinusoidal_Frequency_Modulation_FM.html) [2] and became the basis of the Yamaha DX-7 and many digital sound chips (see also Chowning’s original paper [3]). This document covers how the sound is produced, the mathematics (phase modulation, Bessel functions, sidebands), and implementation in SuperCollider.

---

## 1. How the Sound Is Produced

### What is actually modulated

Strictly speaking, we modulate **phase**, not frequency. The oscillator’s **instantaneous phase** is varied by a modulating signal. Because instantaneous frequency is the derivative of phase, varying phase over time is equivalent to varying frequency over time—hence the name “FM” in music tech [2].

### Signal flow

1. **Carrier oscillator** — A sinusoid at the **carrier** frequency \(f_c\) (pitch we hear).
2. **Modulator oscillator** — A sinusoid at the **modulator** frequency \(f_m\). Its **amplitude** (modulation depth) is the FM index \(\beta\).
3. **Modulation** — The modulator’s **output** (scaled by \(\beta\)) is **added into the phase** of the carrier. So the carrier’s phase becomes \(\omega_c t + \beta \sin(\omega_m t)\).
4. **Output** — One (or more) such phase-modulated sinusoids are summed and shaped with envelopes.

So the sound is produced by a **single (or few) oscillators** whose phase is driven by another oscillator. No explicit filter is required; the **spectrum is determined by the modulation index and the ratio \(f_m/f_c\)**. Integer ratios yield harmonic spectra (e.g. bells, electric piano); non-integer ratios yield inharmonic spectra (e.g. metallic, percussion).

### Why it’s powerful

- **One carrier + one modulator** can produce many sidebands (partials).
- **Index \(\beta\)** controls brightness: larger \(\beta\) → more and stronger sidebands.
- **Ratio \(f_m/f_c\)** controls harmonic vs inharmonic and timbre (e.g. 1:1 = simple, 2:1 or 15:1 = richer or metallic).

---

## 2. Mathematics at Play

### 2.1 Phase modulation (FM) equation

General form for one sinusoid modulating the phase of another:

\[
x(t) = A_c \cos\bigl[ \omega_c t + \phi_c + A_m \sin(\omega_m t + \phi_m) \bigr]
\]

- \(\omega_c = 2\pi f_c\): carrier angular frequency  
- \(\omega_m = 2\pi f_m\): modulator angular frequency  
- \(A_m\): modulator amplitude in **phase** (radians). In FM synthesis this is usually written as the **FM index** \(\beta\).

With zero phase offsets and unit carrier amplitude:

\[
x(t) = \cos\bigl[ \omega_c t + \beta \sin(\omega_m t) \bigr].
\]

So the **instantaneous phase** is \(\theta(t) = \omega_c t + \beta \sin(\omega_m t)\); the **instantaneous frequency** is:

\[
\frac{d\theta}{dt} = \omega_c + \beta \omega_m \cos(\omega_m t),
\]

i.e. it varies between \(\omega_c - \beta\omega_m\) and \(\omega_c + \beta\omega_m\). So \(\beta\) (and \(f_m\)) set how far and how fast the frequency deviates.

### 2.2 Bessel expansion: spectrum of sinusoidal FM

Using the generating function for **Bessel functions of the first kind** \(J_k(\beta)\) [4][5]:

\[
e^{j\beta\sin(\omega_m t)} = \sum_{k=-\infty}^{\infty} J_k(\beta) \, e^{jk\omega_m t},
\]

we can write:

\[
e^{j[\omega_c t + \beta\sin(\omega_m t)]} = e^{j\omega_c t} \sum_{k=-\infty}^{\infty} J_k(\beta) \, e^{jk\omega_m t}
= \sum_{k=-\infty}^{\infty} J_k(\beta) \, e^{j(\omega_c + k\omega_m)t}.
\]

Taking the real part gives the **FM spectrum**:

\[
x(t) = \sum_{k=-\infty}^{\infty} J_k(\beta) \cos\bigl[ (\omega_c + k\omega_m) t \bigr].
\]

So sinusoidal FM produces **sidebands** at \(\omega_c + k\omega_m\) for all integers \(k\), with **amplitude** \(J_k(\beta)\).

- **Carrier** = \(k=0\): amplitude \(J_0(\beta)\).
- **Sidebands** = \(k = \pm1, \pm2, \ldots\): amplitudes \(J_k(\beta)\). For real \(\beta\), \(J_{-k}(\beta) = (-1)^k J_k(\beta)\), so the spectrum is symmetric in magnitude.

### 2.3 Role of the FM index \(\beta\)

- \(\beta = 0\): \(J_0(0)=1\), \(J_k(0)=0\) for \(k\ne 0\) → only the carrier; no sidebands.
- \(\beta\) small: carrier dominates, a few small sidebands.
- \(\beta\) large: carrier weakens, many sidebands grow → **brighter**, more complex spectrum.

So the **math that produces the sound** is: phase = \(\omega_c t + \beta\sin(\omega_m t)\), and the **resulting spectrum** is entirely determined by \(\beta\) and the sideband spacing \(\omega_m\), via Bessel amplitudes \(J_k(\beta)\).

### 2.4 Harmonic vs inharmonic spectra

- If \(f_m = f_c\) (ratio 1:1), sidebands are at \(f_c + k f_c\) → **harmonic** (integer multiples of \(f_c\)).
- If \(f_m = 2f_c\), sidebands are still at multiples of \(f_c\) → harmonic.
- If \(f_m/f_c\) is non-integer (e.g. 1.5, 2.7), sidebands are **inharmonic** (bells, metallic tones).

Cascade (modulator → carrier → further modulators) gives even more control; the DX-7 uses **algorithms** that are combinations of such operators [1][3].

---

## 3. SuperCollider Implementation

### 3.1 Core idea: phase input to SinOsc

In SuperCollider, **phase modulation** is done by feeding the modulator’s **output** (scaled) into the **phase** of the carrier. `SinOsc.ar(freq, phase)` uses `phase` in radians.

\[
\text{phase} = \omega_c t + \beta \sin(\omega_m t).
\]

So: **phase = (carrier phase) + (modulator output × index)**. The server’s `SinOsc` integrates `freq` into phase internally; we add the extra term.

### 3.2 Single modulator–carrier pair

```supercollider
// FM index β in radians; modulator output in [-1,1], so multiply by 2π*index for radians
(
SynthDef(\fm_basic, {
	arg out = 0, freq = 440, amp = 0.3, gate = 1,
	    modRatio = 1, modIndex = 2;  // modIndex = β
	var carFreq, modFreq, modPhase, carPhase, sig, env;
	env = EnvGen.ar(Env.adsr(0.01, 0.2, 0.6, 0.4), gate, doneAction: 2);
	modFreq = freq * modRatio;
	modPhase = SinOsc.ar(modFreq) * modIndex * 2pi;  // β * 2π ≈ index in “phase units”
	carPhase = modPhase;  // carrier phase = 0 + modulator contribution
	sig = SinOsc.ar(freq, carPhase);
	sig = sig * env * amp;
	Out.ar(out, sig ! 2);
}).add;
)
```

Here `modIndex` plays the role of \(\beta\); scaling by `2pi` converts a typical “index” knob (e.g. 0–4) into a phase deviation in radians. For a purer \(\beta\) in radians, use `modPhase = SinOsc.ar(modFreq) * modIndex` and keep `modIndex` in 0..5 or so.

### 3.3 DX-7 style: modulator in phase of carrier (explicit)

```supercollider
(
SynthDef(\fm_dx7style, {
	arg out = 0, note = 60, amp = 0.3, gate = 1,
	    modRatio = 2, modIndex = 3;
	var fc, fm, mod, sig, env;
	fc = note.midicps;
	fm = fc * modRatio;
	env = EnvGen.ar(Env.adsr(0.01, 0.3, 0.6, 0.3), gate, doneAction: 2);
	mod = SinOsc.ar(fm) * modIndex * 2pi;
	sig = SinOsc.ar(fc, mod);
	sig = sig * env * amp;
	Out.ar(out, sig ! 2);
}).add;
)
```

### 3.4 Your project’s Rhodes (nested FM)

The Rhodes in `sc_programs/rhodes_piano.scd` uses **nested FM**: one SinOsc modulates the phase of another, and that result can modulate further. For example:

- `osc4 = SinOsc.ar(freq*0.5) * 2pi * ... * modIndex * env4 * vel` → modulator.
- `osc3 = SinOsc.ar(freq, osc4) * env3 * vel` → carrier at `freq` with phase = `osc4`.

So the **phase** of the carrier is the **output** of the modulator (scaled). That is exactly \(x(t) = \cos[\omega_c t + \beta \sin(\omega_m t)]\) with time-varying \(\beta\) (envelope) and multiple such pairs summed. The same Bessel/sideband math applies to each pair; the sum gives the rich Rhodes tone.

### 3.5 Bell-like FM (inharmonic)

Use a non-integer mod ratio and moderate index:

```supercollider
SynthDef(\fm_bell, {
	arg out = 0, freq = 440, amp = 0.2, gate = 1, modIndex = 5;
	var mod, sig, env;
	env = EnvGen.ar(Env.perc(0.001, 2), gate, doneAction: 2);
	mod = SinOsc.ar(freq * 2.7) * modIndex * 2pi;  // inharmonic ratio
	sig = SinOsc.ar(freq, mod);
	sig = sig * env * amp;
	Out.ar(out, sig ! 2);
}).add;
```

---

## Summary

| Aspect | Content |
|--------|--------|
| **Sound production** | Modulator sinusoid is added into the **phase** of the carrier; one or more such phase-modulated oscillators, shaped by envelopes. |
| **Math** | Phase = \(\omega_c t + \beta\sin(\omega_m t)\); spectrum = \(\sum_k J_k(\beta)\cos[(\omega_c+k\omega_m)t]\); Bessel \(J_k(\beta)\) set sideband amplitudes; \(\beta\) controls brightness. |
| **SuperCollider** | `SinOsc.ar(fc, SinOsc.ar(fm) * index * 2pi)`; nested FM = multiple such stages (as in the Rhodes). |

---

## References

1. [The difference between subtractive, additive, FM, and wavetable synthesis](https://splice.com/blog/difference-between-synthesis-types/) (Splice).
2. [Sinusoidal Frequency Modulation (FM)](https://ccrma.stanford.edu/~jos/rbeats/Sinusoidal_Frequency_Modulation_FM.html) (CCRMA/Stanford, Julius O. Smith III).
3. [John Chowning, “The Synthesis of Complex Audio Spectra by Means of Frequency Modulation”](https://ccrma.stanford.edu/sites/default/files/user/jc/fm_synthesis_paper.pdf) (Stanford/CCRMA, PDF).
4. [Bessel Functions](https://ccrma.stanford.edu/~jos/rbeats/Bessel_Functions.html) (CCRMA/Stanford, JOS).
5. [FM Spectra](https://ccrma.stanford.edu/~jos/rbeats/FM_Spectra.html) (CCRMA/Stanford, JOS).
