"""Builds the HyperFrames project for "ROT" (Farbpsychologie format).

Run: python3 build.py   (rewrites index.html and compositions/)
Scene times come from assets/transcript.json (ElevenLabs Scribe word timings).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", ".claude", "skills", "farbpsychologie-video", "lib"))

from figlib import *  # noqa: E402,F401
from pagelib import write_project  # noqa: E402

TITLE = '"ROT"'
ACCENT = "#F0251F"
RED = "#E2231A"
HANDLE = "@deinhandle"
TOTAL = 65.0
GROUND = 600
S = 1.7

words = json.load(open(os.path.join(HERE, "assets", "transcript.json")))

scenes = []


def scene(sid, start, end, svg, js):
    scenes.append((sid, start, end - start, svg, js))


# ------------------------------------------------------------ s01 hook
# 0.00 Wenn Rot deine Lieblingsfarbe ist, | 2.35 sagt die Psychologie einiges über dich.
svg = (
    '<g id="s01-a">'
    + shadow("s01-sh1", 540, GROUND, 190)
    + fig("s01-f1", 540, GROUND, S,
          pose={"ua_r": -160, "la_r": -95, "head": -14, "ua_l": 10, "la_l": 6},
          hand_r=f'<g transform="rotate(90)">{bottle(RED, "s01-liq", 1.0)}</g>', mouth="open")
    + '<g id="s01-drops">'
    + "".join(f'<circle id="s01-d{i}" cx="{556+i*6}" cy="{GROUND-395}" r="7" fill="{RED}" opacity="0"/>' for i in range(3))
    + '</g></g>'
    '<g id="s01-b" opacity="0">'
    + shadow("s01-sh2", 540, GROUND, 200)
    + fig("s01-f2", 540, GROUND, S, skin="#E0312B",
          pose={"ua_l": 150, "la_l": 20, "ua_r": -14, "la_r": -4},
          hand_r=f'<g transform="rotate(180)">{bottle(RED, None, 0.0)}</g>', mouth="grin")
    + '</g>'
)
js = """
// drinking
P("s01-f1", {head: -24, ua_r: -168}, 0.0, 0.5);
tl.to("#s01-liq", {attr: {y: 26, height: 4}, duration: 1.9, ease: "sine.inOut"}, 0.2);
for (let i = 0; i < 3; i++) {
  tl.fromTo(`#s01-d${i}`, {opacity: 0, attr: {cy: 205}}, {opacity: 1, attr: {cy: 300}, duration: 0.45, ease: "power1.in"}, 0.5 + i * 0.45);
  tl.to(`#s01-d${i}`, {opacity: 0, duration: 0.1}, 0.95 + i * 0.45);
}
P("s01-f1", {pelvis: [-3, 0]}, 0.6, 0.3); P("s01-f1", {pelvis: [0, 0]}, 0.9, 0.3);
P("s01-f1", {pelvis: [-3, 0]}, 1.3, 0.3); P("s01-f1", {pelvis: [0, 0]}, 1.6, 0.3);
cut("#s01-a", "#s01-b", 2.35);
// turned red: wave + bounce
for (let k = 0; k < 6; k++) P("s01-f2", {la_l: k % 2 ? 25 : -25, ua_l: k % 2 ? 150 : 140}, 2.4 + k * 0.33, 0.33, "sine.inOut");
for (let k = 0; k < 4; k++) { P("s01-f2", {pelvis: [-10, 0], root: [540, 590, 0, 1.7]}, 2.5 + k * 0.9, 0.22, "power2.out"); P("s01-f2", {pelvis: [0, 0], root: [540, 600, 0, 1.7]}, 2.72 + k * 0.9, 0.25, "power2.in"); }
blink("s01-f2", 3.6); blink("s01-f2", 5.4);
P("s01-f2", {head: 8}, 4.4, 0.4); P("s01-f2", {head: -4}, 5.6, 0.5);
"""
scene("s01", 0.0, 6.4, svg, js)

# ------------------------------------------------------------ s02 mutig / leidenschaftlich
# 6.64 Menschen, die Rot lieben, gelten oft als mutig, | 9.74 leidenschaftlich und voller Energie.
cape = f'<path id="s02-cape" d="M-24,-96 Q-62,0 -70,92 L40,96 Q30,0 24,-96 Z" fill="{RED}"/>'
svg = (
    '<g id="s02-a">'
    + "".join(f'<path id="s02-wind{i}" d="M{80+i*40},{180+i*90} q60,-18 120,0 t120,0" stroke="#bdbdbd" stroke-width="5" fill="none" stroke-linecap="round" opacity="0"/>' for i in range(3))
    + f'<path d="M330,{GROUND+10} L380,{GROUND-120} L470,{GROUND-150} L640,{GROUND-140} L720,{GROUND-90} L760,{GROUND+10} Z" fill="{BROWN}"/>'
    + f'<path d="M380,{GROUND-120} L470,{GROUND-150} L640,{GROUND-140} L720,{GROUND-90} L700,{GROUND-80} L470,{GROUND-128} Z" fill="{BROWN_L}"/>'
    + fig("s02-h", 545, GROUND - 138, 1.55, shirt=RED, back=cape,
          pose={"ua_l": 38, "la_l": -115, "ua_r": -38, "la_r": 115, "ul_l": 8, "ul_r": -8, "head": -6}, mouth="smile")
    + '</g>'
    '<g id="s02-b" opacity="0">'
    + '<circle id="s02-aura" cx="540" cy="330" r="300" fill="url(#aura)" opacity=".0"/>'
    + "".join(f'<circle id="s02-p{i}" cx="540" cy="330" r="{6+i%3*3}" fill="{["#FF5A3C", "#FFB04A", RED][i%3]}" opacity="0"/>' for i in range(14))
    + shadow("s02-sh", 540, GROUND, 170)
    + fig("s02-j", 540, GROUND, S, shirt=RED,
          pose={"ua_l": 30, "la_l": 20, "ua_r": -30, "la_r": -20}, mouth="grin")
    + '</g>'
)
js = """
// cape + wind
for (let k = 0; k < 6; k++) T("#s02-cape", k * 0.5, {attr: {d: k % 2 ? "M-24,-96 Q-62,0 -70,92 L40,96 Q30,0 24,-96 Z" : "M-24,-96 Q-90,-10 -118,70 L20,96 Q30,0 24,-96 Z"}}, 0.5, "sine.inOut");
for (let i = 0; i < 3; i++) tl.fromTo(`#s02-wind${i}`, {opacity: 0, x: -120}, {opacity: 0.8, x: 160, duration: 1.4, ease: "none"}, 0.2 + i * 0.6);
P("s02-h", {head: 6}, 0.9, 0.6); blink("s02-h", 1.8); P("s02-h", {torso: -3}, 2.0, 0.6);
cut("#s02-a", "#s02-b", 3.1);
// energy jumps
T("#s02-aura", 3.1, {opacity: 0.85}, 0.4, "power2.out");
for (let k = 0; k < 4; k++) {
  const t = 3.2 + k * 0.75;
  P("s02-j", {pelvis: [14, 0], ua_l: 40, ua_r: -40}, t, 0.15, "power2.in");
  P("s02-j", {root: [540, 530, 0, 1.7], pelvis: [0, 0], ua_l: 150, la_l: -10, ua_r: -150, la_r: 10, ul_l: 28, ul_r: -28}, t + 0.15, 0.25, "power2.out");
  P("s02-j", {root: [540, 600, 0, 1.7], ua_l: 30, la_l: 20, ua_r: -30, la_r: -20, ul_l: 3, ul_r: -3}, t + 0.42, 0.25, "power2.in");
  T("#s02-aura", t + 0.2, {attr: {r: 330}}, 0.2, "power2.out"); T("#s02-aura", t + 0.45, {attr: {r: 290}}, 0.3);
}
for (let i = 0; i < 14; i++) {
  const a = i / 14 * Math.PI * 2, r = 260 + (i % 4) * 40;
  tl.fromTo(`#s02-p${i}`, {opacity: 0, attr: {cx: 540, cy: 330}}, {opacity: 1, attr: {cx: 540 + Math.cos(a) * r, cy: 330 + Math.sin(a) * r * 0.8}, duration: 1.2, ease: "power2.out"}, 3.3 + (i % 5) * 0.5);
  tl.to(`#s02-p${i}`, {opacity: 0, duration: 0.3}, 4.5 + (i % 5) * 0.5);
}
"""
scene("s02", 6.4, 12.7, svg, js)

# ------------------------------------------------------------ s03 direkt
# 13.00 Du gehst Dinge lieber direkt an, | 14.76 statt ewig darüber nachzudenken.
svg = (
    '<g id="s03-a">' + floor(GROUND - 10, 160)
    + f'<rect x="545" y="{GROUND-95}" width="110" height="95" rx="8" fill="{BROWN}"/>'
    + f'<rect x="545" y="{GROUND-95}" width="110" height="18" rx="6" fill="{BROWN_L}"/>'
    + "".join(f'<line id="s03-ml{i}" x1="0" y1="{GROUND-260+i*40}" x2="90" y2="{GROUND-260+i*40}" stroke="#bdbdbd" stroke-width="5" stroke-linecap="round" opacity="0"/>' for i in range(3))
    + fig("s03-r", -120, GROUND, S, shirt=RED, mouth="grin")
    + '</g>'
    '<g id="s03-b" opacity="0">'
    + '<line x1="540" y1="70" x2="540" y2="640" stroke="#e8e8e8" stroke-width="5"/>'
    + shadow("s03-sh1", 270, GROUND, 170)
    + fig("s03-t", 270, GROUND, S, pose={"ua_l": 150, "la_l": -120, "head": -6}, mouth="flat", brow="sad", brow_on=True)
    + thought("s03-tb", 395, 150, 170, 120, inner=''.join(
        f'<circle id="s03-dot{i}" cx="{355+i*40}" cy="150" r="11" fill="{LINE}" opacity=".25"/>' for i in range(3)), dots_dir=-1)
    + f'<path d="M770,{GROUND-45} L770,{GROUND} L970,{GROUND} L970,{GROUND-45} Z" fill="{BROWN}"/>'
    + shadow("s03-sh2", 870, GROUND - 45, 150, 14)
    + fig("s03-w", 870, GROUND - 45, 1.4, shirt=RED, mouth="grin",
          pose={"ua_l": 150, "la_l": 10, "ua_r": -20, "la_r": -10},
          hand_l=f'<g transform="translate(0,44) rotate(180)"><line x1="0" y1="0" x2="0" y2="-110" stroke="{BROWN_D}" stroke-width="7"/>'
                 f'<path id="s03-flag" d="M0,-110 L75,-92 L0,-72 Z" fill="{RED}"/></g>')
    + '</g>'
)
js = """
walk("s03-r", -120, 470, 600, 1.7, 0.0, 0.85, 0.17, 42, 10);
for (let i = 0; i < 3; i++) { tl.fromTo(`#s03-ml${i}`, {opacity: 0, x: 0}, {opacity: 0.8, x: 300, duration: 0.5, ease: "none"}, 0.2 + i * 0.08); tl.to(`#s03-ml${i}`, {opacity: 0, duration: 0.15}, 0.75 + i * 0.08); }
P("s03-r", {root: [610, 420, 8, 1.7], ul_l: -70, ll_l: 90, ul_r: -40, ll_r: 70, ua_l: -60, ua_r: 120}, 0.85, 0.28, "power2.out");
P("s03-r", {root: [760, 600, 0, 1.7], ul_l: 3, ll_l: 0, ul_r: -3, ll_r: 0, ua_l: 8, ua_r: -8}, 1.13, 0.24, "power2.in");
walk("s03-r", 760, 1250, 600, 1.7, 1.37, 1.95, 0.17, 42, 10);
cut("#s03-a", "#s03-b", 1.95);
for (let k = 0; k < 9; k++) T(`#s03-dot${k % 3}`, 2.0 + k * 0.3, {opacity: 1}, 0.12), T(`#s03-dot${k % 3}`, 2.15 + k * 0.3, {opacity: 0.25}, 0.15);
for (let k = 0; k < 5; k++) P("s03-t", {la_l: k % 2 ? -120 : -100}, 2.0 + k * 0.4, 0.2, "sine.inOut");
for (let k = 0; k < 6; k++) T("#s03-flag", 2.0 + k * 0.45, {attr: {d: k % 2 ? "M0,-110 L75,-92 L0,-72 Z" : "M0,-110 Q35,-110 75,-86 Q35,-84 0,-72 Z"}}, 0.45, "sine.inOut");
for (let k = 0; k < 3; k++) { P("s03-w", {root: [870, 520, 0, 1.4]}, 2.2 + k * 0.8, 0.2, "power2.out"); P("s03-w", {root: [870, 555, 0, 1.4]}, 2.4 + k * 0.8, 0.22, "power2.in"); }
blink("s03-t", 3.4);
"""
scene("s03", 12.7, 17.6, svg, js)

# ------------------------------------------------------------ s04 Liebe
# 17.84 Und wenn du jemanden liebst, | 19.44 dann mit ganzem Herzen, nicht nur halb.
svg = (
    '<g id="s04-a">'
    + shadow("s04-sh1", 400, GROUND, 190) + shadow("s04-sh2", 720, GROUND, 150)
    + fig("s04-m", 400, GROUND, S, hair="short", hair_color=HAIR_D,
          pose={"pelvis": (55, 0), "ul_l": -95, "ll_l": 95, "ul_r": 0, "ll_r": 92, "ua_r": -78, "la_r": -12, "ua_l": 12, "head": 6},
          hand_r=bouquet(), mouth="smile")
    + fig("s04-w", 720, GROUND, S, hair="bob", dress=BROWN_L, blush=True,
          pose={"ua_l": 22, "la_l": -150, "ua_r": -22, "la_r": 150}, mouth="open")
    + '</g>'
    '<g id="s04-b" opacity="0">'
    + f'<rect x="0" y="{GROUND-20}" width="1080" height="140" fill="{BROWN_L}"/>'
    + tree(90, GROUND - 10, 330, BROWN) + tree(200, GROUND - 10, 250, BROWN_L) + tree(960, GROUND - 10, 360, BROWN, "pine") + tree(850, GROUND - 10, 240, BROWN)
    + neon_heart("s04-heart", 540, 330, 2.4)
    + "".join(f'<path id="s04-mh{i}" d="{heart_path(0, 0, 0.18)}" fill="#FF5A7A" opacity="0" transform="translate({380+i*110},{GROUND-60})"/>' for i in range(4))
    + shadow("s04-sh3", 540, GROUND, 330, 22, "#7a4527")
    + fig("s04-m2", 455, GROUND, S, hair="short", hair_color=HAIR_D, pose={"ua_r": -32, "la_r": -18}, mouth="grin")
    + fig("s04-w2", 625, GROUND, S, hair="bob", dress=RED, blush=True, pose={"ua_l": 32, "la_l": 18}, mouth="grin")
    + '</g>'
)
js = """
P("s04-m", {la_r: -22}, 0.2, 0.5); P("s04-w", {head: -6}, 0.3, 0.5); P("s04-w", {head: 6}, 0.9, 0.5);
blink("s04-w", 1.2);
cut("#s04-a", "#s04-b", 1.75);
tl.fromTo("#s04-heart", {opacity: 0}, {opacity: 1, duration: 0.08}, 1.8);
tl.to("#s04-heart", {opacity: 0.3, duration: 0.06}, 1.95); tl.to("#s04-heart", {opacity: 1, duration: 0.06}, 2.05);
for (let k = 0; k < 5; k++) { tl.to("#s04-heart", {opacity: 0.75, duration: 0.3, ease: "sine.inOut"}, 2.4 + k * 0.6); tl.to("#s04-heart", {opacity: 1, duration: 0.3, ease: "sine.inOut"}, 2.7 + k * 0.6); }
for (let i = 0; i < 4; i++) { const x = 380 + i * 110; tl.fromTo(`#s04-mh${i}`, {opacity: 0, attr: {transform: `translate(${x},540)`}}, {opacity: 0.9, attr: {transform: `translate(${x + (i % 2 ? 30 : -30)},260)`}, duration: 1.8, ease: "sine.out"}, 2.2 + i * 0.45); tl.to(`#s04-mh${i}`, {opacity: 0, duration: 0.4}, 3.6 + i * 0.45); }
P("s04-m2", {head: 10}, 2.3, 0.5); P("s04-w2", {head: -10}, 2.4, 0.5); blink("s04-m2", 3.3); blink("s04-w2", 3.9);
P("s04-m2", {head: 4}, 4.2, 0.6); P("s04-w2", {head: -4}, 4.3, 0.6);
"""
scene("s04", 17.6, 22.7, svg, js)

# ------------------------------------------------------------ s05 Runde
# 22.94 Oft bist du die Person, | 24.26 die eine ganze Runde mitreißt | 26.66 und die Stimmung hebt.
friends = [("s05-a", 205, "bob", HAIR), ("s05-b", 345, "short", HAIR_D), ("s05-c", 735, "pony", HAIR_D), ("s05-d", 875, "short", HAIR)]
svg = (
    floor(GROUND - 20, 170) + lamp(220, 40) + lamp(540, 40, 70) + lamp(860, 40)
    + "".join(fig(fid, x, GROUND + 70, 1.5, skin=CREAM_D if i % 2 else CREAM, hair=h, hair_color=hc, mouth="smile",
                  pose={"ua_l": 15, "la_l": -60, "ua_r": -15, "la_r": 60},
                  hand_r=glass() if i in (0, 2) else "", hand_l=glass() if i in (1, 3) else "")
              for i, (fid, x, h, hc) in enumerate(friends))
    + fig("s05-h", 540, GROUND - 20, 1.65, shirt=RED, mouth="grin", pose={"ua_r": -150, "la_r": -15, "ua_l": 20}, hand_r=glass())
    + table(540, GROUND, 860, 175)
    + f'<path d="M110,{GROUND-157} L970,{GROUND-157} L960,{GROUND+85} L120,{GROUND+85} Z" fill="{BROWN_L}"/>'
    + f'<rect x="110" y="{GROUND-175}" width="860" height="22" rx="6" fill="{BROWN}"/>'
    + "".join(f'<rect x="{x}" y="{GROUND-200}" width="22" height="26" rx="4" fill="#FFF3DA" opacity=".85"/>' for x in (300, 470, 610, 780))
    + "".join(f'<rect id="s05-cf{i}" x="{180+i*55}" y="60" width="12" height="20" rx="3" fill="{["#FF5A3C", "#FFB04A", RED, "#F6E3C6"][i%4]}" opacity="0"/>' for i in range(14))
)
js = """
P("s05-h", {la_r: 10, ua_r: -160}, 0.3, 0.5); P("s05-h", {head: -8}, 0.6, 0.4); P("s05-h", {head: 8}, 1.4, 0.5);
const ids = ["s05-a", "s05-b", "s05-c", "s05-d"];
ids.forEach((id, i) => { P(id, {head: i % 2 ? 6 : -6}, 0.4 + i * 0.25, 0.5); blink(id, 1.2 + i * 0.37); });
// mitreißt: everyone joins in
ids.forEach((id, i) => {
  const t = 2.7 + i * 0.12, up = i % 2 ? {ua_l: 160, la_l: 10, ua_r: -40, la_r: 60} : {ua_r: -160, la_r: -10, ua_l: 40, la_l: -60};
  P(id, {...up, mouth: "grin"}, t, 0.3, "back.out(2)");
  for (let k = 0; k < 4; k++) P(id, {pelvis: [k % 2 ? 0 : -8, 0], head: k % 2 ? -5 : 5}, t + 0.35 + k * 0.32, 0.3, "sine.inOut");
});
for (let k = 0; k < 6; k++) P("s05-h", {pelvis: [k % 2 ? 0 : -10, 0], ua_l: k % 2 ? 20 : 150, la_l: k % 2 ? 0 : 20}, 2.7 + k * 0.4, 0.35, "sine.inOut");
for (let i = 0; i < 14; i++) { tl.fromTo(`#s05-cf${i}`, {opacity: 0, y: 0, rotation: 0}, {opacity: 1, y: 380 + (i % 3) * 60, rotation: 200 + i * 30, duration: 1.1, ease: "power1.in"}, 4.2 + (i % 4) * 0.12); tl.to(`#s05-cf${i}`, {opacity: 0, duration: 0.1}, 5.3 + (i % 4) * 0.12); }
"""
scene("s05", 22.7, 28.45, svg, js)

# ------------------------------------------------------------ s06 zur Stelle
# 28.70 Und wenn jemand, der dir wichtig ist, | 31.28 unfair behandelt wird, | 33.12 bist du sofort zur Stelle.
svg = (
    shadow("s06-sh0", 240, GROUND, 140)
    + fig("s06-v", 240, GROUND, 1.3, hair="pony", pose={"ua_l": 165, "la_l": -95, "ua_r": -165, "la_r": 95, "pelvis": (8, 0)},
          mouth="frown", brow="sad", brow_on=True)
    + '<circle id="s06-tear" cx="258" cy="430" r="7" fill="#8ec5ff" opacity="0"/>'
    + shadow("s06-sh1", 720, GROUND, 170) + shadow("s06-sh2", 900, GROUND, 170)
    + fig("s06-b1", 720, GROUND, 1.8, skin=CREAM_D, hair="short", hair_color=HAIR_D, pose={"ua_l": 95, "la_l": 0}, mouth="shout", brow="angry", brow_on=True)
    + fig("s06-b2", 900, GROUND, 1.75, skin=CREAM_D, pose={"ua_l": 92, "la_l": 5, "ua_r": -20}, mouth="shout", brow="angry", brow_on=True)
    + speech_zigzag("s06-sp", 820, 120, 150, 90, "#8d8d8d", "!!").replace('<g id="s06-sp">', '<g id="s06-sp" opacity="0">')
    + shadow("s06-sh3", -150, GROUND, 170)
    + fig("s06-h", -150, GROUND, 1.75, shirt=RED, mouth="flat", brow="angry", brow_on=True)
)
js = """
for (let k = 0; k < 8; k++) P("s06-v", {root: [k % 2 ? 242 : 238, 600, 0, 1.3]}, 0.2 + k * 0.12, 0.12, "none");
P("s06-b1", {la_l: -20}, 0.4, 0.2); P("s06-b1", {la_l: 0}, 0.6, 0.2);
T("#s06-sp", 2.8, {opacity: 1}, 0.1);
P("s06-b1", {root: [670, 600, 0, 1.8]}, 2.8, 0.4); P("s06-b2", {root: [850, 600, 0, 1.75]}, 2.9, 0.4);
tl.to("#s06-sh1", {attr: {cx: 670}, duration: 0.4}, 2.8); tl.to("#s06-sh2", {attr: {cx: 850}, duration: 0.4}, 2.9);
tl.fromTo("#s06-tear", {opacity: 0, attr: {cy: 430}}, {opacity: 1, attr: {cy: 520}, duration: 0.8, ease: "power1.in"}, 3.2);
tl.to("#s06-tear", {opacity: 0, duration: 0.1}, 4.0);
for (let k = 0; k < 6; k++) P("s06-b2", {la_l: k % 2 ? 5 : -25}, 3.3 + k * 0.18, 0.18, "sine.inOut");
// hero runs in
walk("s06-h", -150, 500, 600, 1.75, 4.45, 5.05, 0.15, 42, 10);
tl.to("#s06-sh3", {attr: {cx: 500}, duration: 0.6, ease: "none"}, 4.45);
P("s06-h", {torso: 0, ul_l: 8, ll_l: 0, ul_r: -8, ll_r: 0, ua_l: 80, la_l: 0, ua_r: -80, la_r: 0, pelvis: [0, 0]}, 5.05, 0.2, "back.out(2)");
T("#s06-sp", 5.2, {opacity: 0}, 0.1);
P("s06-b1", {root: [800, 600, -6, 1.8], mouth: "open", brow: "up", ua_l: 20, la_l: -120}, 5.25, 0.35, "power2.out");
P("s06-b2", {root: [960, 600, -5, 1.75], mouth: "open", brow: "up", ua_l: 20, la_l: -120}, 5.3, 0.35, "power2.out");
tl.to("#s06-sh1", {attr: {cx: 800}, duration: 0.35}, 5.25); tl.to("#s06-sh2", {attr: {cx: 960}, duration: 0.35}, 5.3);
P("s06-v", {ua_l: 20, la_l: 10, ua_r: -20, la_r: -10, pelvis: [0, 0], mouth: "smile", brow: "none"}, 5.7, 0.4);
P("s06-h", {head: -8}, 6.1, 0.4); blink("s06-h", 6.6);
"""
scene("s06", 28.45, 35.7, svg, js)

# ------------------------------------------------------------ s07 andere Seite
# 35.94 Aber es gibt auch eine andere Seite.
svg = (
    '<g id="s07-shadew" opacity="0">' + fig("s07-shade", 640, GROUND - 20, 2.3, skin="#3a1714", face=False, pose={"ua_l": 20, "ua_r": -20}) + '</g>'
    + spotlight("s07-spot", 520, -30, GROUND, 70, 380, 0.24)
    + fig("s07-h", 520, GROUND, S, shirt=RED, mouth="smile")
)
js = """
const fl = [[0.35, 0.05], [0.42, 0.24], [0.55, 0.04], [0.6, 0.2], [0.9, 0.03], [1.0, 0.14], [1.4, 0.07]];
fl.forEach(([t, o]) => tl.set("#s07-spot", {opacity: o / 0.24}, t));
tl.to("#s07-shadew", {opacity: 0.85, duration: 1.4, ease: "power1.inOut"}, 0.5);
P("s07-h", {mouth: "flat"}, 0.6, 0.3); P("s07-h", {mouth: "frown", eyes: 0.55, head: 7}, 1.3, 0.5);
P("s07-h", {ua_l: 4, ua_r: -4}, 1.3, 0.6);
P("s07-shade", {head: -6}, 1.6, 0.8);
"""
scene("s07", 35.7, 38.4, svg, js)

# ------------------------------------------------------------ s08 ungeduldig
# 38.64 Rot-Liebhaber werden schnell ungeduldig, | 41.22 wenn etwas zu langsam geht.
svg = (
    clock("s08-clk", 860, 170, 62)
    + "".join(f'<circle id="s08-st{i}" cx="{300+i*28}" cy="150" r="{16+i*4}" fill="#cfcfcf" opacity="0"/>' for i in range(3))
    + shadow("s08-sh", 300, GROUND, 170)
    + fig("s08-h", 300, GROUND, S, shirt=RED, mouth="flat",
          pose={"ua_l": 12, "la_l": -98, "ua_r": -12, "la_r": 98})
    + shadow("s08-sn-sh", 700, GROUND, 140, 12)
    + snail("s08-sn", 690, GROUND, 1.1)
)
js = """
for (let k = 0; k < 10; k++) T("#s08-clk-m", 0.1 + k * 0.5, {attr: {transform: `translate(0,0) rotate(${(k + 1) * 6})`}}, 0.08, "power3.out");
tl.to("#s08-sn", {attr: {transform: "translate(780,600) rotate(0) scale(1.1)"}, duration: 5.2, ease: "none"}, 0);
tl.to("#s08-sn-sh", {attr: {cx: 790}, duration: 5.2, ease: "none"}, 0);
for (let k = 0; k < 16; k++) P("s08-h", {ul_r: k % 2 ? -3 : -12, ll_r: k % 2 ? 0 : 28}, 0.2 + k * 0.3, 0.15, "power1.inOut");
P("s08-h", {head: 12}, 0.4, 0.4); blink("s08-h", 1.2);
P("s08-h", {brow: "angry", mouth: "frown", head: 0}, 2.0, 0.3);
for (let i = 0; i < 3; i++) { tl.fromTo(`#s08-st${i}`, {opacity: 0, y: 30, scale: 0.6, transformOrigin: "50% 50%"}, {opacity: 0.8, y: -40, scale: 1.1, duration: 0.7, ease: "power1.out"}, 2.3 + i * 0.25 + 0); tl.to(`#s08-st${i}`, {opacity: 0, duration: 0.3}, 3.0 + i * 0.25); }
for (let i = 0; i < 3; i++) { tl.fromTo(`#s08-st${i}`, {opacity: 0, y: 30, scale: 0.6}, {opacity: 0.8, y: -40, scale: 1.1, duration: 0.7, ease: "power1.out"}, 3.8 + i * 0.25); tl.to(`#s08-st${i}`, {opacity: 0, duration: 0.3}, 4.5 + i * 0.25); }
P("s08-h", {head: 14, eyes: 0.6}, 3.4, 0.4);
"""
scene("s08", 38.4, 43.6, svg, js)

# ------------------------------------------------------------ s09 Streit
# 43.86 Manchmal sagst du im Streit Dinge, | 45.74 die du später bereust.
svg = (
    '<g id="s09-a">'
    + shadow("s09-sh1", 340, GROUND, 170) + shadow("s09-sh2", 760, GROUND, 160)
    + fig("s09-h", 340, GROUND, S, shirt=RED, mouth="shout", brow="angry", brow_on=True, pose={"ua_r": -70, "la_r": -40, "ua_l": 30})
    + fig("s09-o", 760, GROUND, S, skin=CREAM_D, hair="bob", hair_color=HAIR_D, mouth="frown", brow="sad", brow_on=True, pose={"torso": 6, "ua_l": 25, "la_l": -120})
    + speech_zigzag("s09-sp", 470, 130, 230, 130, RED, "#@!")
    + '</g>'
    '<g id="s09-b" opacity="0">'
    + floor(GROUND - 10, 160)
    + f'<g transform="translate(540,{GROUND}) scale(1.9)">{sofa(0, 0, 300)}</g>'
    + fig("s09-s", 540, GROUND, S, shirt=RED, mouth="frown", brow="sad", brow_on=True,
          pose={"pelvis": (22, 0), "ul_l": 38, "ll_l": -38, "ul_r": -38, "ll_r": 38, "ua_l": 120, "la_l": 127, "ua_r": -120, "la_r": -127})
    + thought("s09-tb", 800, 150, 190, 130, inner=broken_heart(800, 150, 0.55), dots_dir=-1)
    + '</g>'
)
js = """
for (let k = 0; k < 6; k++) P("s09-h", {la_r: k % 2 ? -40 : -5, pelvis: [k % 2 ? 0 : -6, 0]}, 0.1 + k * 0.28, 0.25, "sine.inOut");
for (let k = 0; k < 6; k++) T("#s09-sp", 0.1 + k * 0.14, {x: k % 2 ? 4 : -4}, 0.07, "none");
P("s09-o", {torso: 12, root: [790, 600, 0, 1.7]}, 0.6, 0.5);
cut("#s09-a", "#s09-b", 2.05);
tl.fromTo("#s09-tb", {opacity: 0}, {opacity: 1, duration: 0.3}, 2.5);
for (let k = 0; k < 4; k++) P("s09-s", {torso: k % 2 ? 0 : 3}, 2.2 + k * 0.5, 0.5, "sine.inOut");
"""
scene("s09", 43.6, 47.8, svg, js)

# ------------------------------------------------------------ s10 stark wirken
# 48.04 Und weil du nach außen so stark wirkst, | 50.96 fragt kaum jemand, wie es dir wirklich geht.
crowd = [("s10-c0", "bob"), ("s10-c1", "short"), ("s10-c2", "pony"), ("s10-c3", None), ("s10-c4", "short")]
svg = (
    '<g id="s10-a">'
    + shadow("s10-sh", 540, GROUND, 180)
    + fig("s10-h", 540, GROUND, S, shirt=RED, mouth="frown", brow="sad", brow_on=True,
          pose={"ua_r": -160, "la_r": -97, "ua_l": 10},
          hand_r=f'<g transform="translate(0,44) rotate(-103) scale(1.05)">{mask_disc()}</g>')
    + '<circle id="s10-tear" cx="560" cy="345" r="7" fill="#8ec5ff" opacity="0"/>'
    + '</g>'
    '<g id="s10-b" opacity="0">'
    + floor(GROUND - 10, 160) + lamp(200, 40) + lamp(540, 40, 60) + lamp(880, 40)
    + '<ellipse cx="540" cy="600" rx="140" ry="22" fill="#8a8a8a" opacity=".45"/>'
)
svg += (
    fig("s10-h2", 540, GROUND, 1.6, shirt=RED, mouth="frown", brow="sad", brow_on=True)
    + "".join(fig(cid, -200 - i * 230, GROUND + 60, 1.5, skin=CREAM_D if i % 2 else CREAM, hair=h, hair_color=HAIR_D if i % 2 else HAIR, mouth="grin")
              for i, (cid, h) in enumerate(crowd))
    + '</g>'
)
js = """
P("s10-h", {head: -5}, 0.3, 0.6); P("s10-h", {head: 5}, 1.2, 0.6);
P("s10-h", {ua_r: -30, la_r: -15}, 2.0, 0.5, "power2.inOut");
tl.fromTo("#s10-tear", {opacity: 0, attr: {cy: 345}}, {opacity: 1, attr: {cy: 420}, duration: 0.55, ease: "power1.in"}, 2.4);
tl.to("#s10-tear", {opacity: 0, duration: 0.1}, 3.0);
cut("#s10-a", "#s10-b", 3.0);
const cr = ["s10-c0", "s10-c1", "s10-c2", "s10-c3", "s10-c4"];
cr.forEach((id, i) => walk(id, -150 - i * 200, 1250 - i * 40, 660, 1.5, 3.0, 6.4, 0.3 + (i % 3) * 0.03, 26, 4));
P("s10-h2", {head: -6}, 3.6, 0.6); P("s10-h2", {head: 6}, 4.6, 0.8); blink("s10-h2", 5.5);
"""
scene("s10", 47.8, 54.2, svg, js)

# ------------------------------------------------------------ s11 tragen
# 54.46 Vielleicht trägst du mehr mit dir herum, | 56.54 als du zeigst.
rock = f'<g transform="translate(-6,-40) scale(0.95)">{boulder()}</g>'
svg = (
    floor(GROUND - 10, 160)
    + "".join(f'<circle id="s11-dust{i}" cx="0" cy="{GROUND-10}" r="{10+i*3}" fill="#6b6b6b" opacity="0"/>' for i in range(4))
    + fig("s11-h", 180, GROUND, S, shirt=RED, mouth="frown", brow="sad", brow_on=True, back=rock, pose={"torso": 10})
    + '<circle id="s11-sweat" cx="0" cy="0" r="7" fill="#8ec5ff" opacity="0"/>'
)
js = """
walk("s11-h", 180, 600, 600, 1.7, 0.0, 2.7, 0.45, 18, 12);
for (let i = 0; i < 4; i++) { const x = 230 + i * 100; tl.fromTo(`#s11-dust${i}`, {opacity: 0, attr: {cx: x}}, {opacity: 0.6, attr: {cx: x - 30}, duration: 0.4}, 0.4 + i * 0.6); tl.to(`#s11-dust${i}`, {opacity: 0, duration: 0.4}, 0.8 + i * 0.6); }
tl.fromTo("#s11-sweat", {opacity: 0, attr: {cx: 400, cy: 260}}, {opacity: 1, attr: {cx: 420, cy: 330}, duration: 0.7}, 1.2);
tl.to("#s11-sweat", {opacity: 0, duration: 0.2}, 1.9);
P("s11-h", {ul_l: 3, ll_l: 0, ul_r: -3, ll_r: 0, ua_l: 8, la_l: 4, ua_r: -8, la_r: -4, pelvis: [0, 0], torso: 6}, 2.7, 0.3);
P("s11-h", {mouth: "smile", brow: "none", head: -8}, 2.85, 0.35, "back.out(2)");
blink("s11-h", 3.5);
"""
scene("s11", 54.2, 58.3, svg, js)

# ------------------------------------------------------------ s12 heller brennen
# 58.48 Im Grunde brennst du einfach heller als andere, | 61.58 und nicht jeder kann mit dieser Wärme umgehen.
rays = "".join(
    f'<path d="M-14,-150 L0,-330 L14,-150 Z" fill="{["#FF8A3D", "#FFB25B"][i%2]}" opacity=".55" transform="rotate({i*30})"/>' for i in range(12))
others = [("s12-o0", 130, "bob"), ("s12-o1", 280, "short"), ("s12-o2", 800, "pony"), ("s12-o3", 950, None)]
svg = (
    '<circle id="s12-warm" cx="540" cy="330" r="330" fill="url(#warm)" opacity=".6"/>'
    + f'<g id="s12-rays" transform="translate(540,330) rotate(0)" opacity="0">{rays}</g>'
    + '<circle id="s12-aura" cx="540" cy="360" r="230" fill="url(#aura)" opacity=".7"/>'
    + "".join(f'<circle id="s12-e{i}" cx="{420+i*24}" cy="560" r="{5+i%3*2}" fill="{["#FFB25B", "#FF5A3C"][i%2]}" opacity="0"/>' for i in range(10))
    + "".join(shadow(f"{oid}-sh", x, GROUND, 140) + fig(oid, x, GROUND, 1.45, skin=CREAM_D, hair=h, hair_color=HAIR_D, mouth="smile",
                                                         pose={"head": 8 if x < 540 else -8})
              for oid, x, h in others)
    + shadow("s12-sh", 540, GROUND, 190, 20, "#5a2a1a")
    + fig("s12-h", 540, GROUND, 1.75, shirt=RED, mouth="grin", blush=True, pose={"ua_l": 40, "la_l": 10, "ua_r": -40, "la_r": -10})
)
js = """
tl.to("#s12-rays", {attr: {transform: "translate(540,330) rotate(45)"}, duration: 6.7, ease: "none"}, 0);
T("#s12-rays", 0.6, {opacity: 1}, 0.6);
T("#s12-warm", 1.4, {opacity: 1, attr: {r: 400}}, 0.6, "power2.out");
T("#s12-aura", 1.4, {opacity: 1, attr: {r: 280}}, 0.6, "power2.out");
for (let k = 0; k < 5; k++) { T("#s12-aura", 2.1 + k * 0.9, {attr: {r: 300}}, 0.45, "sine.inOut"); T("#s12-aura", 2.55 + k * 0.9, {attr: {r: 270}}, 0.45, "sine.inOut"); }
for (let i = 0; i < 10; i++) { const x = 420 + i * 24; tl.fromTo(`#s12-e${i}`, {opacity: 0, attr: {cy: 560, cx: x}}, {opacity: 1, attr: {cy: 120, cx: x + (i % 2 ? 40 : -40)}, duration: 2.2, ease: "sine.out"}, 0.3 + (i % 5) * 0.55 + (i > 4 ? 2.6 : 0)); tl.to(`#s12-e${i}`, {opacity: 0, duration: 0.4}, 2.2 + (i % 5) * 0.55 + (i > 4 ? 2.6 : 0)); }
P("s12-h", {ua_l: 120, la_l: 20, ua_r: -120, la_r: -20}, 1.4, 0.5, "back.out(1.6)");
P("s12-h", {head: -5}, 2.3, 0.5); blink("s12-h", 2.9);
// the others shield their eyes and back off
[["s12-o0", 130, 60], ["s12-o1", 280, 210], ["s12-o2", 800, 870], ["s12-o3", 950, 1020]].forEach(([id, x, x2], i) => {
  const left = x < 540, t = 3.25 + i * 0.12;
  const arm = left ? {ua_r: -160, la_r: -100, ua_l: 12} : {ua_l: 160, la_l: 100, ua_r: -12};
  P(id, {...arm, mouth: "open", brow: "up", torso: left ? -6 : 6}, t, 0.35, "power2.out");
  P(id, {root: [x2, 600, 0, 1.45]}, t + 0.3, 0.6, "power2.out");
  tl.to(`#${id}-sh`, {attr: {cx: x2}, duration: 0.6, ease: "power2.out"}, t + 0.3);
});
P("s12-h", {head: 5}, 4.6, 0.6); P("s12-h", {head: 0}, 5.6, 0.6); blink("s12-h", 5.9);
"""
scene("s12", 58.3, 65.0, svg, js)

write_project(HERE, TITLE, ACCENT, HANDLE, TOTAL, words, ["rot"], scenes)
print("built", len(scenes), "scenes")
