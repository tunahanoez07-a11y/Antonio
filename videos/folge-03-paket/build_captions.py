#!/usr/bin/env python3
"""Baut aus assets/words.json (ElevenLabs Scribe) die Karaoke-Untertitel und assets/words.js.

Aufruf: python3 build_captions.py [projektordner]
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
OFFSET = 0.0      # Verschiebung des Voiceovers in der Timeline
MAX_WORDS = 3     # Wörter pro Gruppe (Referenz: 1–4)
HOLD = 0.35       # Nachlauf nach dem letzten Wort einer Pause

data = json.loads((ROOT / "assets/words.json").read_text())
words = [w for w in data["words"] if w.get("type") == "word" and not w["text"].startswith("[")]
for w in words:
    w["start"] = round(w["start"] + OFFSET, 3)
    w["end"] = round(w["end"] + OFFSET, 3)

(ROOT / "assets/words.js").write_text("window.TOM_WORDS = " + json.dumps(words, ensure_ascii=False) + ";\n")

# Gruppen: Bruch nach Satzzeichen, nach MAX_WORDS oder bei Pausen >= 0.35 s
groups, cur = [], []
for i, w in enumerate(words):
    cur.append(w)
    nxt = words[i + 1] if i + 1 < len(words) else None
    end_punct = re.search(r"[.,:?!]$", w["text"])
    pause = nxt is None or nxt["start"] - w["end"] >= 0.35
    if end_punct or pause or len(cur) >= MAX_WORDS:
        groups.append(cur)
        cur = []

duration = round(words[-1]["end"] + 1.0, 2)
items, script = [], []
for gi, g in enumerate(groups):
    start = max(0.1, g[0]["start"] - 0.02) if gi == 0 else g[0]["start"]
    nxt = groups[gi + 1][0]["start"] if gi + 1 < len(groups) else None
    end = g[-1]["end"] + HOLD
    if nxt is not None:
        end = min(end, nxt) if nxt - g[-1]["end"] < 0.6 else end
        end = min(end, nxt)
    gid = f"cap-{gi}"
    spans = []
    for wi, w in enumerate(g):
        wid = f"{gid}-w{wi}"
        spans.append(f'<span id="{wid}" class="cw">{html.escape(w["text"])}</span>')
        script.append(f'  word("#{wid}", {w["start"]:.3f}, {g[wi + 1]["start"] if wi + 1 < len(g) else "null"});')
    items.append(
        f'    <div id="{gid}" class="cap clip" data-start="{start:.3f}" data-duration="{end - start:.3f}" data-track-index="1">'
        f'<div class="cap-line">{" ".join(spans)}</div></div>'
    )

doc = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    #root .cap {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; overflow: visible; }}
    #root .cap-line {{
      position: absolute; left: 0; right: 0; top: 430px; padding: 0 70px;
      text-align: center; font-family: Inter, sans-serif; font-weight: 900; font-size: 70px;
      line-height: 1.12; letter-spacing: -0.01em; color: #1E1E1E;
    }}
    #root .cw {{ display: inline-block; opacity: 0; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(items)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const ORANGE = "#E39B22", INK = "#1E1E1E";
    function word(sel, t, next) {{
      tl.fromTo(sel, {{ opacity: 0, y: 10, color: ORANGE }}, {{ opacity: 1, y: 0, color: ORANGE, duration: 0.08, ease: "power2.out" }}, t);
      if (next !== null) tl.set(sel, {{ color: INK }}, next);
    }}
{chr(10).join(script)}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""
(ROOT / "compositions/captions.html").write_text(doc)
print(f"{len(words)} Wörter, {len(groups)} Gruppen, Sprechdauer bis {words[-1]['end']}s")
