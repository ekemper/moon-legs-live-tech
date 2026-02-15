// Subtractive synth with envelope-modulated cutoff — SynthDef + SC GUI
// Run: sclang Synth-Exploring/subtractive_synth_gui.scd
// Uses supernova + output only (like test_440_sine.scd). Set ~debugSynth = true for verbose logging.
//
// Sequencer uses square + filter (\square_filter_env); subtractive_env for Synth tab + MIDI.
(
var guiBuilt = false;
var test440NodeID = nil;
Server.supernova;
Server.default.options.numInputBusChannels = 0;
Server.default.options.inDevice = nil;
Server.default.options.outDevice = "Powerbeats Pro";
Server.default.options.sampleRate = 48000;
Server.default.options.blockSize = 256;
~debugSynth = ~debugSynth ?? { false };
~log = { |tag, msg| "[Synth] %: %".format(tag, msg).postln };
~logOptions = {
	var o = Server.default.options;
	~log.("OPTIONS", "out=% in=% rate=% inCh=% blockSize=%"
		.format(o.outDevice, o.inDevice, o.sampleRate, o.numInputBusChannels, o.blockSize));
};
~addTest440SynthDef = {
	SynthDef(\test440, { Out.ar(0, SinOsc.ar(440, 0, 0.3) ! 2) }).add;
};
~addSineEnvSynthDef = {
	SynthDef(\sine_env, {
		arg out = 0, freq = 440, amp = 0.3, gate = 1,
		    attack = 0.01, decay = 0.3, sustain = 0.5, release = 0.5;
		var sig, ampEnv;
		sig = SinOsc.ar(freq, 0, 1);
		ampEnv = EnvGen.ar(Env.adsr(attack, decay, sustain, release, curve: -4), gate, doneAction: 2);
		sig = LeakDC.ar(sig * ampEnv * amp);
		sig = Limiter.ar(sig, 0.95, 0.01);
		Out.ar(out, sig ! 2);
	}).add;
};
~addSquareFilterSynthDef = {
	SynthDef(\square_filter_env, {
		arg out = 0, freq = 440, amp = 0.3, gate = 1,
		    filterType = 0, cutoff = 2000, cutoffEnvAmt = 800, res = 0.08,
		    attack = 0.01, decay = 0.3, sustain = 0.5, release = 0.5,
		    filtAttack = 0.01, filtDecay = 0.4, filtEnvAmt = 800;
		var sig, ampEnv, filtEnv, cut;
		sig = LFPulse.ar(freq, 0.25, 0.5);
		sig = Lag.ar(sig, 0.008);
		ampEnv = EnvGen.ar(Env.adsr(attack, decay, sustain, release, curve: -4), gate, doneAction: 2);
		filtEnv = EnvGen.ar(Env.perc(filtAttack, filtDecay, 1, -4), gate) * filtEnvAmt;
		cut = (cutoff + filtEnv).clip(20, 20000);
		sig = Select.ar(filterType.clip(0, 1), [
			RLPF.ar(sig, cut, res.reciprocal.clip(0.01, 10)),
			MoogFF.ar(sig, cut, res * 4)
		]);
		sig = LeakDC.ar(sig * ampEnv * amp);
		sig = Limiter.ar(sig, 0.95, 0.01);
		Out.ar(out, sig ! 2);
	}).add;
};
~addSubtractiveSynthDef = {
	SynthDef(\subtractive_env, {
		arg out = 0, freq = 440, amp = 0.3, gate = 1,
		    oscType = 0, filterType = 0,
		    cutoff = 2000, cutoffEnvAmt = 800, res = 0.08,
		    attack = 0.01, decay = 0.3, sustain = 0.5, release = 0.5,
		    filtAttack = 0.01, filtDecay = 0.4, filtEnvAmt = 800;
		var sig, ampEnv, filtEnv, cut;
		// Safe phases at note-on; longer Lag softens onset for BT codecs
		sig = Select.ar(oscType.clip(0, 4), [
			LFSaw.ar(freq, 0.5),
			LFPulse.ar(freq, 0.25, 0.5),
			LFTri.ar(freq, 0),
			LFSaw.ar(freq, 0.5),
			WhiteNoise.ar()
		]);
		sig = Lag.ar(sig, 0.008);
		// Exponential-ish curve on amp envelope to avoid sharp transient at attack
		ampEnv = EnvGen.ar(Env.adsr(attack, decay, sustain, release, curve: -4), gate, doneAction: 2);
		filtEnv = EnvGen.ar(Env.perc(filtAttack, filtDecay, 1, -4), gate) * filtEnvAmt;
		cut = (cutoff + filtEnv).clip(20, 20000);
		sig = Select.ar(filterType.clip(0, 1), [
			RLPF.ar(sig, cut, res.reciprocal.clip(0.01, 10)),
			MoogFF.ar(sig, cut, res * 4)
		]);
		sig = LeakDC.ar(sig * ampEnv * amp);
		sig = Limiter.ar(sig, 0.95, 0.01);
		Out.ar(out, sig ! 2);
	}).add;
};
Server.default.doWhenBooted {
	~addTest440SynthDef.value;
	~addSineEnvSynthDef.value;
	~addSquareFilterSynthDef.value;
	~addSubtractiveSynthDef.value;
	Server.default.sync;
	~log.("BOOT", "SynthDefs test440, sine_env, square_filter_env, subtractive_env sent. Server sampleRate=%".format(Server.default.options.sampleRate));
	~log.("AUDIO", "post-boot: out=%, rate=%, inCh=%, blockSize=%".format(
		Server.default.options.outDevice, Server.default.options.sampleRate,
		Server.default.options.numInputBusChannels, Server.default.options.blockSize));
	~logOptions.value;
	if (guiBuilt.not, {
		var w, outDevices, deviceMenu, contentView, synthTab, seqTab, tabSynthBtn, tabSeqBtn;
		var oscMenu, filterMenu;
		var freqSpec, ampSpec, cutoffSpec, cutoffEnvSpec, resSpec;
		var attackSpec, decaySpec, sustainSpec, releaseSpec;
		var filtAttackSpec, filtDecaySpec, filtEnvAmtSpec;
		var freqVal = 440, ampVal = 0.25, cutoffVal = 2000, cutoffEnvVal = 800, resVal = 0.08;
		var attackVal = 0.01, decayVal = 0.3, sustainVal = 0.5, releaseVal = 0.5;
		var filtAttackVal = 0.01, filtDecayVal = 0.4, filtEnvAmtVal = 800;
		var oscTypeVal = 0, filterTypeVal = 0;
		var midiSynths, alesisIdx;
		var seqSteps, seqBpm, seqTask, seqStepBtns, stepDur, seqScale, seqFreqForStep, seqRunning;
		var seqSynthRef = Ref(nil);
		guiBuilt = true;

	freqSpec = ControlSpec(20, 2000, \exp, 1, 440, " Hz");
	ampSpec = ControlSpec(0, 1, \lin, 0.01, 0.25, "");
	cutoffSpec = ControlSpec(50, 16000, \exp, 10, 2000, " Hz");
	cutoffEnvSpec = ControlSpec(0, 12000, \lin, 50, 800, " Hz");
	resSpec = ControlSpec(0.01, 1, \lin, 0.01, 0.08, "");
	attackSpec = ControlSpec(0.001, 2, \exp, 0.001, 0.01, " s");
	decaySpec = ControlSpec(0.01, 2, \exp, 0.01, 0.3, " s");
	sustainSpec = ControlSpec(0, 1, \lin, 0.01, 0.5, "");
	releaseSpec = ControlSpec(0.01, 5, \exp, 0.01, 0.5, " s");
	filtAttackSpec = ControlSpec(0.001, 1, \exp, 0.001, 0.01, " s");
	filtDecaySpec = ControlSpec(0.01, 2, \exp, 0.01, 0.4, " s");
	filtEnvAmtSpec = ControlSpec(0, 12000, \lin, 100, 800, " Hz");

	w = Window("Synth + Sequencer", Rect(100, 100, 1620, 780)).front;
	w.view.decorator = FlowLayout(w.view.bounds, Point(8, 8), Point(6, 6));

	// Top row: Output, Sample rate (output only = supernova config)
	outDevices = ServerOptions.outDevices;
	StaticText(w.view, 48@18).string_("Output").font_(Font.default.bold_());
	deviceMenu = PopUpMenu(w.view, 180@22).items_(outDevices).action_({ |m|
		var name = outDevices[m.value];
		if (name.notNil and: { name != Server.default.options.outDevice }, {
			Server.default.options.outDevice_(name);
			Server.default.options.inDevice_(nil);
			Server.default.options.sampleRate_(48000);
			Server.default.options.blockSize_(256);
			Server.default.doWhenBooted({ ~addSineEnvSynthDef.value; ~addSquareFilterSynthDef.value; ~addSubtractiveSynthDef.value; ~log.("DEVICE", "SynthDef re-added"); });
			Server.default.reboot;
			~log.("DEVICE", "Output -> % @ 48000 Hz blockSize=256 (output only)".format(name));
		});
	});
	deviceMenu.value_((outDevices.indexOf(Server.default.options.outDevice) ? 0).max(0));
	StaticText(w.view, 24@18).string_("Rate").font_(Font.default.bold_());
	PopUpMenu(w.view, 120@22).items_(["Auto", "44100", "48000"]).value_(2).action_({ |m|
		var rate = [nil, 44100, 48000][m.value];
		if (rate != Server.default.options.sampleRate, {
			Server.default.options.sampleRate_(rate);
			if (Server.default.serverRunning, {
				Server.default.doWhenBooted({ ~addSineEnvSynthDef.value; ~addSquareFilterSynthDef.value; ~addSubtractiveSynthDef.value; ~log.("RATE", "SynthDef re-added"); });
				Server.default.reboot;
			}, { Server.default.boot });
			~log.("RATE", "Sample rate -> %".format(if(rate.isNil, "device default", rate.asString ++ " Hz")));
		});
	});
	StaticText(w.view, 24@18).string_(""); // gap
	Button(w.view, 52@22).states_([["440", Color.black, Color.green(0.7)]]).action_({
		test440NodeID !? { |id| Server.default.sendMsg(\n_free, id) };
		test440NodeID = Synth(\test440, [], Server.default).nodeID;
		~log.("AUDIO", "Test 440 Hz sine playing. Use Stop to free.");
	});
	Button(w.view, 36@22).states_([["Stop", Color.gray, Color.red(0.6)]]).action_({
		test440NodeID !? { |id| Server.default.sendMsg(\n_free, id) };
		test440NodeID = nil;
		~log.("AUDIO", "Test 440 stopped");
	});
	StaticText(w.view, 24@18).string_(""); // gap
	tabSynthBtn = Button(w.view, 72@22).states_([["Synth", Color.gray, Color.white], ["Synth", Color.black, Color.gray(0.85)]]).value_(1).action_({ |b|
		synthTab.visible = true; seqTab.visible = false;
		tabSeqBtn.value_(0); b.value_(1);
	});
	tabSeqBtn = Button(w.view, 80@22).states_([["Sequencer", Color.black, Color.gray(0.85)], ["Sequencer", Color.gray, Color.white]]).value_(0).action_({ |b|
		synthTab.visible = false; seqTab.visible = true;
		tabSynthBtn.value_(0); b.value_(1);
	});

	w.view.decorator.nextLine;
	contentView = CompositeView(w.view, 1620@746);
	contentView.background = Color.gray(0.95);

	// ---- Tab 1: Subtractive Synth ----
	synthTab = CompositeView(contentView, Rect(0, 0, 1620, 746));
	synthTab.decorator = FlowLayout(synthTab.bounds, Point(8, 8), Point(6, 6));
	StaticText(synthTab, 52@18).string_("Osc").font_(Font.default.bold_());
	oscMenu = PopUpMenu(synthTab, 100@22).items_(["Saw", "Pulse", "Triangle", "Saw LFO", "Noise"]).action_({ |m| oscTypeVal = m.value });
	StaticText(synthTab, 38@18).string_("Filter").font_(Font.default.bold_());
	filterMenu = PopUpMenu(synthTab, 72@22).items_(["RLPF", "MoogFF"]).action_({ |m| filterTypeVal = m.value });
	synthTab.decorator.nextLine;
	EZSlider(synthTab, 88@700, "Freq", freqSpec, { |ez| freqVal = ez.value }, layout: \vert);
	EZSlider(synthTab, 88@700, "Amp", ampSpec, { |ez| ampVal = ez.value }, layout: \vert);
	EZSlider(synthTab, 88@700, "Cutoff", cutoffSpec, { |ez| cutoffVal = ez.value }, layout: \vert);
	EZSlider(synthTab, 88@700, "Cutoff env", cutoffEnvSpec, { |ez| cutoffEnvVal = ez.value }, layout: \vert);
	EZSlider(synthTab, 88@700, "Resonance", resSpec, { |ez| resVal = ez.value }, layout: \vert);
	EZSlider(synthTab, 88@700, "Attack", attackSpec, { |ez| attackVal = ez.value }, layout: \vert);
	EZSlider(synthTab, 88@700, "Decay", decaySpec, { |ez| decayVal = ez.value }, layout: \vert);
	EZSlider(synthTab, 88@700, "Sustain", sustainSpec, { |ez| sustainVal = ez.value }, layout: \vert);
	EZSlider(synthTab, 88@700, "Release", releaseSpec, { |ez| releaseVal = ez.value }, layout: \vert);
	EZSlider(synthTab, 88@700, "Filt attack", filtAttackSpec, { |ez| filtAttackVal = ez.value }, layout: \vert);
	EZSlider(synthTab, 88@700, "Filt decay", filtDecaySpec, { |ez| filtDecayVal = ez.value }, layout: \vert);
	EZSlider(synthTab, 88@700, "Filt env", filtEnvAmtSpec, { |ez| filtEnvAmtVal = ez.value }, layout: \vert);

	// ---- Tab 2: Basic Sequencer ----
	seqTab = CompositeView(contentView, Rect(0, 0, 1620, 746));
	seqTab.visible = false;
	seqTab.decorator = FlowLayout(seqTab.bounds, Point(8, 8), Point(6, 6));
	seqSteps = Array.fill(16, false);
	seqBpm = 120;
	seqScale = [0, 2, 4, 5, 7, 9, 11, 12]; // C major scale degrees
	seqFreqForStep = { |stepIndex| (48 + seqScale.wrapAt(stepIndex) + (12 * stepIndex.div(8))).midicps };
	StaticText(seqTab, 400@24).string_("16 steps (C major). Toggle steps, set BPM, press Play.").font_(Font.default.bold_());
	seqTab.decorator.nextLine;
	seqStepBtns = 16.collect({ |i|
		Button(seqTab, 42@42).states_([
			["", Color.gray(0.7), Color.gray(0.9)],
			[(i+1).asString, Color.black, Color.green(0.6)]
		]).value_(if (seqSteps[i], { 1 }, { 0 })).action_({ |b|
			seqSteps[i] = (b.value == 1);
		});
	});
	seqTab.decorator.nextLine;
	StaticText(seqTab, 36@22).string_("BPM");
	NumberBox(seqTab, 56@22).value_(120).clipLo_(20).clipHi_(300).step_(1).action_({ |nb| seqBpm = nb.value.clip(20, 300) });
	Button(seqTab, 80@28).states_([["Play", Color.black, Color.green(0.6)]]).action_({
		~seqRunning = false;
		~seqTask !? { _.stop };
		seqSynthRef.value !? { _.set(\gate, 0) };
		~seqRunning = true;
		stepDur = 60 / (seqBpm * 4);
		~log.("SEQ", "Play BPM=% stepDur=% s".format(seqBpm, stepDur.round(0.001)));
		~seqTask = Task({
			while { ~seqRunning } {
				16.do({ |i|
					if (~seqRunning.not, { ^nil });
					if (seqSteps[i], {
						var syn;
						~log.("SYNTH", "sequencer step % freq=% Hz (square+filter)".format(i + 1, seqFreqForStep.(i).round(0.01)));
						seqSynthRef.value !? { _.set(\gate, 0) };
						syn = Synth(\square_filter_env, [
							\freq, seqFreqForStep.(i), \amp, ampVal * 0.8, \gate, 1,
							\filterType, filterTypeVal, \cutoff, cutoffVal, \cutoffEnvAmt, cutoffEnvVal, \res, resVal,
							\attack, attackVal, \decay, decayVal, \sustain, sustainVal, \release, releaseVal,
							\filtAttack, filtAttackVal, \filtDecay, filtDecayVal, \filtEnvAmt, filtEnvAmtVal
						]);
						seqSynthRef.value = syn;
						SystemClock.sched(stepDur * 0.85, { syn.set(\gate, 0); nil });
					});
					stepDur.wait;
				});
			};
		}).play(SystemClock);
	});
	Button(seqTab, 70@28).states_([["Stop", Color.white, Color.red(0.6)]]).action_({
		var s;
		~seqRunning = false;
		~seqTask !? { _.stop };
		~seqTask = nil;
		s = seqSynthRef.value;
		seqSynthRef.value = nil;
		s !? { _.set(\gate, 0) };
		~log.("SEQ", "Stop");
	});

	// ---- MIDI: Alesis keyboard as sole source ----
	midiSynths = IdentityDictionary.new;
	MIDIClient.init;
	alesisIdx = MIDIClient.sources.detectIndex({ |ep| ep.name.toLower.contains("alesis") });
	if (alesisIdx.notNil, {
		MIDIIn.connect(alesisIdx);
		~log.("MIDI", "Alesis connected: %".format(MIDIClient.sources[alesisIdx].name));
		MIDIdef.noteOn(\alesisOn, { |vel, noteNum, chan, src|
			var freq = noteNum.midicps, amp = (vel / 127) * ampVal;
			~log.("SYNTH", "MIDI note=% freq=% Hz".format(noteNum, freq.round(0.01)));
			midiSynths[noteNum] = Synth(\subtractive_env, [
				\freq, freq, \amp, amp, \gate, 1,
				\oscType, oscTypeVal, \filterType, filterTypeVal,
				\cutoff, cutoffVal, \cutoffEnvAmt, cutoffEnvVal, \res, resVal,
				\attack, attackVal, \decay, decayVal, \sustain, sustainVal, \release, releaseVal,
				\filtAttack, filtAttackVal, \filtDecay, filtDecayVal, \filtEnvAmt, filtEnvAmtVal
			]);
		}).permanent_(false);
		MIDIdef.noteOff(\alesisOff, { |vel, noteNum, chan, src|
			if (~debugSynth, { ~log.("MIDI", "off note=%".format(noteNum)) });
			if (midiSynths[noteNum].notNil, {
				midiSynths[noteNum].set(\gate, 0);
				midiSynths.removeAt(noteNum);
			});
		}).permanent_(false);
	}, {
		~log.("MIDI", "Alesis not found. Available: %".format(MIDIClient.sources.collect(_.name)));
	});

	w.onClose_({
		test440NodeID !? { |id| Server.default.sendMsg(\n_free, id) }; test440NodeID = nil;
		~log.("CLOSE", "Stopping sequencer, releasing synths, disconnecting MIDI");
		~seqRunning = false;
		~seqTask !? { _.stop };
		seqSynthRef.value !? { _.set(\gate, 0) };
		MIDIdef(\alesisOn).free;
		MIDIdef(\alesisOff).free;
		if (alesisIdx.notNil, { MIDIIn.disconnect(alesisIdx) });
		midiSynths.do({ |s| if (s.isPlaying, { s.set(\gate, 0) }) });
	});

	~log.("READY", "Synth + Sequencer. Use 440 button: if 440 sounds correct but subtractive/seq wrong, issue is subtractive SynthDef; if 440 also wrong, issue is session/config.");
	});
};

~log.("INIT", "output only, out=Powerbeats Pro rate=48000 blockSize=256 (supernova)");
~log.("AUDIO", "pre-boot: out=%, in=%, rate=%, inCh=%, blockSize=%".format(
	Server.default.options.outDevice, Server.default.options.inDevice,
	Server.default.options.sampleRate, Server.default.options.numInputBusChannels,
	Server.default.options.blockSize));
if (Server.default.serverRunning.not, { Server.default.boot }, { ~log.("AUDIO", "server already running, skip boot") });
)
