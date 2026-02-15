// Minimal test: pure 440 Hz sine. Run this block in sclang; tone starts when server is ready.
// Stop: ~test440.free   or Cmd+.
// Output only. Supernova avoids macOS opening an input device (fixes BT/16k mismatch).
(
var opts = Server.default.options;
var outDeviceName = "Powerbeats Pro";
var sampleRateHz = 48000;
Server.supernova;
opts.numInputBusChannels = 0;
opts.inDevice = nil;
opts.outDevice = outDeviceName;
opts.sampleRate = sampleRateHz;
opts.blockSize = 256;
"Output only: % | % Hz (supernova)".format(outDeviceName, sampleRateHz).postln;

Server.default.doWhenBooted {
	"Server booted. Check post for 'SC_AudioDriver: sample rate = %'.".format(sampleRateHz).postln;
	SynthDef(\test440, { Out.ar(0, SinOsc.ar(440, 0, 0.3) ! 2) }).add;
	Server.default.sync;
	SystemClock.sched(0.3, {
		~test440 = Synth(\test440);
		"Playing 440 Hz. Stop: ~test440.free".postln;
		nil
	});
};
if (Server.default.serverRunning, { Server.default.reboot }, { Server.default.boot });
)
