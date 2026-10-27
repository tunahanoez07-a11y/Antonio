#!/usr/bin/env python3
"""Macht den Voiceover lustloser: Satzmelodie per PSOLA (Praat) zusammendrücken und leicht absenken.

Aufruf: python3 flatten_voice.py in.mp3 out.mp3 [--keep 0.6] [--target 106]
  --keep    Anteil der Melodie, der bleibt (1.0 = unverändert, 0.6 = 40 % flacher)
  --target  Ziel-Grundton in Hz (Referenz-Creator: ~106 Hz)
Dauer und Timing bleiben exakt gleich, Wort-Timings müssen nicht neu erzeugt werden.
"""
import argparse, os, subprocess, tempfile
import numpy as np
import parselmouth
from parselmouth.praat import call

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("dst")
ap.add_argument("--keep", type=float, default=0.6)
ap.add_argument("--target", type=float, default=106.0)
a = ap.parse_args()

with tempfile.TemporaryDirectory() as tmp:
    wav = os.path.join(tmp, "in.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.src, "-ac", "1", "-ar", "44100", wav], check=True)
    snd = parselmouth.Sound(wav)
    manip = call(snd, "To Manipulation", 0.01, 65, 300)
    tier = call(manip, "Extract pitch tier")
    n = call(tier, "Get number of points")
    times = [call(tier, "Get time from index", i + 1) for i in range(n)]
    vals = np.array([call(tier, "Get value at index", i + 1) for i in range(n)])
    med = float(np.median(vals))
    new = a.target * (vals / med) ** a.keep
    call(tier, "Remove points between", 0, snd.duration)
    for t, v in zip(times, new):
        call(tier, "Add point", t, float(v))
    call([manip, tier], "Replace pitch tier")
    out = call(manip, "Get resynthesis (overlap-add)")
    ow = os.path.join(tmp, "out.wav")
    out.save(ow, "WAV")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", ow, "-ac", "1", "-ar", "44100", "-b:a", "192k", a.dst], check=True)
print(f"Median {med:.0f} Hz -> {a.target:.0f} Hz, Melodie x{a.keep}")
