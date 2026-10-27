#!/usr/bin/env python3
"""Fügt Kunstpausen nach Pointen in den Voiceover ein und verschiebt die Wort-Timings.
Aufruf: python3 add_pauses.py [quelle.mp3]  (Standard: assets/voiceover-raw.mp3)
Eingabe: assets/voiceover-raw.mp3 + assets/words-raw.json. Ausgabe: assets/voiceover.mp3 + assets/words.json.
PAUSES = [(Schnittpunkt im Original in s, Pausenlänge in s), ...] – Schnittpunkt in die Lücke zwischen zwei Wörter legen."""
import json, subprocess, sys
PAUSES = [(10.64, 0.7), (22.98, 0.6), (25.455, 0.8), (34.16, 1.0), (39.07, 0.6), (44.98, 0.9), (48.48, 0.8)]
src = sys.argv[1] if len(sys.argv) > 1 else "assets/voiceover-raw.mp3"  # z. B. assets/voiceover-flat.mp3
out = "assets/voiceover.mp3"
cuts = [0.0] + [p for p, _ in PAUSES] + [None]
parts, filt = [], []
for i in range(len(cuts) - 1):
    a, b = cuts[i], cuts[i + 1]
    trim = f"atrim=start={a}" + (f":end={b}" if b is not None else "")
    filt.append(f"[0:a]{trim},asetpts=PTS-STARTPTS[s{i}]")
    parts.append(f"[s{i}]")
    if i < len(PAUSES):
        filt.append(f"anullsrc=r=44100:cl=mono,atrim=duration={PAUSES[i][1]}[p{i}]")
        parts.append(f"[p{i}]")
filt.append("".join(parts) + f"concat=n={len(parts)}:v=0:a=1[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", ";".join(filt), "-map", "[out]", "-ac", "1", "-ar", "44100", "-b:a", "192k", out], check=True)
data = json.load(open("assets/words-raw.json"))
for w in data["words"]:
    shift = sum(d for p, d in PAUSES if w["start"] >= p)
    w["start"] = round(w["start"] + shift, 3); w["end"] = round(w["end"] + shift, 3)
json.dump(data, open("assets/words.json", "w"), ensure_ascii=False)
print("Pausen gesamt:", sum(d for _, d in PAUSES), "s; letztes Wort endet bei", data["words"][-1]["end"])
