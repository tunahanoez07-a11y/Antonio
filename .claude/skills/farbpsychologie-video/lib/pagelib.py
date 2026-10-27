"""Writes a HyperFrames project for the Farbpsychologie format.

Layout on 1080x1920 (scaled 1.5x from the 720x1280 references):
  - colour title in quotes, Archivo Black, centred at y~450
  - word-by-word serif captions (Gelasio Bold) right below at y~560
  - the illustration stage: an SVG 1080x760 placed at top 600
  - small grey handle watermark at y~1450
"""
import html
import json
import os
import re

from figlib import defs, js_helpers

STAGE_TOP = 600
STAGE_H = 760
GROUP_MAX_WORDS = 7
DIM = "#5b5b5b"


def _defs_scoped(sid, accent):
    d = defs(accent)
    for name in ("glow-big", "glow", "beam", "aura", "warm"):
        d = d.replace(f'id="{name}"', f'id="{sid}-g-{name}"')
    return d


def _scope_urls(sid, markup):
    return re.sub(r"url\(#(glow-big|glow|beam|aura|warm)\)", lambda m: f"url(#{sid}-g-{m.group(1)})", markup)


def scene_html(sid, svg, js, accent):
    return f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    #{sid}-stage {{ position: absolute; left: 0; top: {STAGE_TOP}px; width: 1080px; height: {STAGE_H}px; overflow: visible; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920" data-layout-allow-overflow>
    <svg id="{sid}-stage" viewBox="0 0 1080 {STAGE_H}" xmlns="http://www.w3.org/2000/svg">
      {_defs_scoped(sid, accent)}
      {_scope_urls(sid, svg)}
    </svg>
  </div>
  <script>
    (() => {{
{js_helpers()}
{js}
    window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""


def group_words(words):
    groups, cur = [], []
    for w in words:
        cur.append(w)
        t = w["text"]
        if t.endswith((".", "!", "?")) or (t.endswith(",") and len(cur) >= 3) or len(cur) >= GROUP_MAX_WORDS:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


def captions_html(words, accent_words, total):
    """Each group is a clip; inside it words go invisible -> dim -> white,
    like the references (the next word already shows faintly)."""
    groups = group_words(words)
    lead = 0.28
    blocks, tweens = [], []
    for gi, g in enumerate(groups):
        start = max(0.0, g[0]["start"] - lead)
        end = groups[gi + 1][0]["start"] - lead if gi + 1 < len(groups) else total
        # a long pause empties the line, as in the references
        end = min(end, g[-1]["end"] + 1.4)
        spans = []
        for w in g:
            key = re.sub(r"[^\wäöüÄÖÜß-]", "", w["text"]).lower()
            acc = any(key == a or key.startswith(a + "-") for a in accent_words)
            spans.append(f'<span id="cap-{w["id"]}" class="w{" acc" if acc else ""}">{html.escape(w["text"])}</span>')
            on = w["start"]
            tweens.append(f'tl.fromTo("#cap-{w["id"]}", {{opacity:0}}, {{opacity:1,duration:0.14,ease:"power1.out"}}, {max(start, on - lead):.3f});')
            tweens.append(f'tl.to("#cap-{w["id"]}", {{color:{"accent" if acc else '"#ffffff"'},duration:0.08,ease:"none"}}, {on:.3f});')
        blocks.append(
            f'<div id="cap-g{gi}" class="clip grp" data-start="{start:.3f}" data-duration="{end-start:.3f}" '
            f'data-track-index="{gi % 2}">{" ".join(spans)}</div>')
    return f"""<template>
  <style>
    @font-face {{ font-family: "Gelasio"; font-weight: 700; src: url("assets/fonts/gelasio-700.woff2") format("woff2"); }}
    #root {{ position: absolute; inset: 0; }}
    .grp {{ position: absolute; left: 70px; right: 70px; top: 540px; text-align: center;
           font-family: "Gelasio", serif; font-weight: 700; font-size: 44px; line-height: 1.22;
           color: {DIM}; overflow: visible; }}
    .w {{ display: inline-block; opacity: 0; color: {DIM}; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
    {chr(10).join("    " + b for b in blocks)}
  </div>
  <script>
    (() => {{
    const tl = gsap.timeline({{ paused: true }});
    const accent = getComputedStyle(document.documentElement).getPropertyValue("--accent").trim() || "#F0251F";
    {chr(10).join("    " + t for t in tweens)}
    window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
"""


def index_html(title, accent, handle, total, scenes, voice="assets/voice.mp3", music=None, music_volume=0.12):
    vars_ = [
        {"id": "title", "type": "string", "label": "Titel", "default": title},
        {"id": "accent", "type": "color", "label": "Farbe", "default": accent},
        {"id": "handle", "type": "string", "label": "Handle", "default": handle},
    ]
    hosts = []
    for i, (sid, start, dur) in enumerate(scenes):
        hosts.append(
            f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
            f'data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="3" data-track-kind="graphics" '
            f'data-width="1080" data-height="1920"></div>')
    music_tag = ""
    if music:
        music_tag = (f'\n      <audio id="music" class="clip" src="{music}" data-start="0" data-duration="{total}" '
                     f'data-track-index="6" data-volume="{music_volume}" data-fade-out="1.5"></audio>')
    return f"""<!doctype html>
<html lang="de" data-resolution="portrait" data-composition-variables='{json.dumps(vars_, ensure_ascii=False)}'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      :root {{ --accent: {accent}; --bg: #000000; --font-title: "Archivo Black"; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: var(--bg); }}
      #root {{ position: relative; width: 1080px; height: 1920px; background: var(--bg); }}
      #title {{ position: absolute; left: 0; right: 0; top: 400px; text-align: center;
               font-family: var(--font-title); font-size: 76px; letter-spacing: 1px; color: var(--accent); }}
      #handle {{ position: absolute; left: 0; right: 0; top: 1438px; text-align: center;
                font-family: "Inter"; font-style: italic; font-size: 28px; color: #8d8d8d; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
      <div id="title" class="clip" data-start="0" data-duration="{total}" data-track-index="0" data-var-text="title">{html.escape(title)}</div>
      <div id="handle" class="clip" data-start="0" data-duration="{total}" data-track-index="1" data-var-text="handle" data-layout-allow-caption-zone>{html.escape(handle)}</div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{total}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920"></div>
{chr(10).join(hosts)}
      <audio id="voice" class="clip" src="{voice}" data-start="0" data-track-index="5" data-volume="1"></audio>{music_tag}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""


def write_project(root, title, accent, handle, total, words, accent_words, scenes, music=None):
    """scenes: list of (sid, start, dur, svg, js)."""
    os.makedirs(os.path.join(root, "compositions"), exist_ok=True)
    for sid, start, dur, svg, js in scenes:
        with open(os.path.join(root, "compositions", f"{sid}.html"), "w") as f:
            f.write(scene_html(sid, svg, js, accent))
    with open(os.path.join(root, "compositions", "captions.html"), "w") as f:
        f.write(captions_html(words, accent_words, total))
    with open(os.path.join(root, "index.html"), "w") as f:
        f.write(index_html(title, accent, handle, total, [(s, a, d) for s, a, d, _, _ in scenes], music=music))
