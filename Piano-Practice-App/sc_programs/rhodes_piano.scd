// FM Rhodes - from sccode.org 1-522 / snappizz, Gist by mbutz
// Args: note (MIDI), gate, vel (0-1), amp
(
SynthDef(\rhodes, {
 |
 out_bus = 0, note = 60, amp = 0.3, gate = 1, pan = 0,
 vel = 0.8, modIndex = 0.2, mix = 0.2, lfoSpeed = 0.4, lfoDepth = 0.1
 |
 var freq = note.midicps;
 var env1, env2, env3, env4;
 var osc1, osc2, osc3, osc4, snd;

 lfoSpeed = lfoSpeed * 12;
 freq = freq * 2;

 env1 = EnvGen.ar(Env.adsr(0.001, 1.25, 0.0, 0.04, curve: \lin));
 env2 = EnvGen.ar(Env.adsr(0.001, 1.00, 0.0, 0.04, curve: \lin));
 env3 = EnvGen.ar(Env.adsr(0.001, 1.50, 0.0, 0.04, curve: \lin));
 env4 = EnvGen.ar(Env.adsr(0.001, 1.50, 0.0, 0.04, curve: \lin));

 osc4 = SinOsc.ar(freq * 0.5) * 2pi * 2 * 0.535887 * modIndex * env4 * vel;
 osc3 = SinOsc.ar(freq, osc4) * env3 * vel;
 osc2 = SinOsc.ar(freq * 15) * 2pi * 0.108819 * env2 * vel;
 osc1 = SinOsc.ar(freq, osc2) * env1 * vel;
 snd = Mix((osc3 * (1 - mix)) + (osc1 * mix));
 snd = snd * (SinOsc.ar(lfoSpeed) * lfoDepth + 1);
 snd = snd * EnvGen.ar(Env.asr(0, 1, 0.1), gate, doneAction: 2);
 snd = Pan2.ar(snd, pan, amp);
 Out.ar(out_bus, snd);
}).add;
)
