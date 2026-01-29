// Boot SuperCollider server and load Rhodes SynthDef.
// Run with: sclang bootstrap.scd
// Server will listen on default port 57120 for OSC.

(
var path = PathName(thisProcess.nowExecutingPath).pathOnly;
Server.default.waitForBoot {
	(path +/+ "rhodes_piano.scd").load;
	"Piano Practice: server booted, Rhodes loaded.".postln;
};
)
