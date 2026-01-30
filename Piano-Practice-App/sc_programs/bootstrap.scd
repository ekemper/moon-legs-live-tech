// Boot SuperCollider server and load Rhodes SynthDef.
// Run with: sclang bootstrap.scd
// Server listens on default port 57110 for OSC.
// bindAddress "0.0.0.0" so Docker backend (host.docker.internal) can reach scsynth.
// Keep sclang running so the server stays up; Ctrl+C to quit.

(
var path = PathName(thisProcess.nowExecutingPath).pathOnly;
Server.default.options.bindAddress = "0.0.0.0";
Server.default.waitForBoot {
	(path +/+ "rhodes_piano.scd").load;
	"Piano Practice: server booted, Rhodes loaded.".postln;
};
// Keep interpreter alive (inf.wait must run inside a Routine)
{ inf.wait }.fork;
)
