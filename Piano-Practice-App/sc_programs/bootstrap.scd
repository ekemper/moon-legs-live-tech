// Boot SuperCollider server and load Rhodes SynthDef.
// Run with: sclang bootstrap.scd
// Server listens on default port 57110 for OSC.
// bindAddress "0.0.0.0" so Docker backend (host.docker.internal) can reach scsynth.
// Keep sclang running so the server stays up; Ctrl+C to quit.
//
// Audio output: scsynth uses the system default at boot. To use Bluetooth headphones,
// set them as system output before starting, or restart sclang after switching.
// To force a device: Server.default.options.outDevice_("Device Name"); (before waitForBoot)
// List devices: ServerOptions.outDevices;

(
var path = PathName(thisProcess.nowExecutingPath).pathOnly;
Server.default.options.bindAddress = "0.0.0.0";
// No input needed (Rhodes only); avoids sample-rate mismatch with output device (e.g. Bose QC45).
Server.default.options.numInputBusChannels = 0;
// Match output device sample rate (Bose QC45 / macOS often 44100; set to 44100 to match driver).
Server.default.options.sampleRate = 44100;
// Slightly larger buffer to reduce dropouts/glitches (default can be too small for Bluetooth).
Server.default.options.hardwareBufferSize = 512;
Server.default.waitForBoot {
	(path +/+ "rhodes_piano.scd").load;
	"Piano Practice: server booted, Rhodes loaded.".postln;
};
// Keep interpreter alive (inf.wait must run inside a Routine)
{ inf.wait }.fork;
)
