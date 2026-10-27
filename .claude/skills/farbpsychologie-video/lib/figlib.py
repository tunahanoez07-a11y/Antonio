"""Figure + prop library for the Farbpsychologie TikTok format.

Draws the reference look as static SVG markup: cream faceless-ish figures with
a few dark face strokes, warm brown furniture and props, grey floor shadows,
on black. Every movable part is a <g> whose transform attribute has the fixed
shape "translate(x,y) rotate(a)" (root: "translate(x,y) rotate(a) scale(s)"),
so GSAP's attr plugin can tween between poses (see JS_HELPERS).

Joint angles are degrees; 0 means the limb hangs straight down. Positive turns
clockwise on screen, so a positive angle swings the limb's end towards -x.
Figure-left limbs (``_l``) are on the viewer's left.
"""

CREAM = "#F6E3C6"
CREAM_D = "#E9CFA9"   # second figure tone (crowds, background people)
LINE = "#3b2a20"      # face strokes
BROWN = "#A9643A"     # furniture
BROWN_D = "#7A4527"
BROWN_L = "#C9875A"
SHADOW = "#2c2c2c"
FLOOR = "#3a3a3a"
HAIR = "#6b3f24"
HAIR_D = "#3a2418"

# base offsets of every joint inside its parent group
RIG = {
    "torso": (0, 0), "head": (0, -100),
    "ua_l": (-25, -86), "la_l": (0, 44), "ua_r": (25, -86), "la_r": (0, 44),
    "ul_l": (-12, 0), "ll_l": (0, 55), "ul_r": (12, 0), "ll_r": (0, 55),
}
PELVIS_Y = -110

MOUTHS = {
    "smile": "M-11,-24 Q0,-15 11,-24",
    "grin": "M-14,-26 Q0,-6 14,-26",
    "flat": "M-8,-21 Q0,-21 8,-21",
    "frown": "M-10,-17 Q0,-27 10,-17",
    "open": "M-7,-22 Q0,-8 7,-22",
    "shout": "M-10,-24 Q0,-2 10,-24",
}
BROWS = {
    "none": "M-16,-53 L-6,-53 M6,-53 L16,-53",
    "angry": "M-17,-57 L-5,-50 M5,-50 L17,-57",
    "sad": "M-17,-50 L-5,-56 M5,-56 L17,-50",
    "up": "M-17,-56 L-5,-58 M5,-58 L17,-56",
}


def _f(v):
    return f"{v:g}"


def jt(name, angle):
    bx, by = RIG[name]
    return f"translate({_f(bx)},{_f(by)}) rotate({_f(angle)})"


def pelvis_t(dy=0, rot=0):
    return f"translate(0,{_f(PELVIS_Y + dy)}) rotate({_f(rot)})"


def root_t(x, y, rot=0, s=1):
    return f"translate({_f(x)},{_f(y)}) rotate({_f(rot)}) scale({_f(s)})"


DEFAULT_POSE = {
    "torso": 0, "head": 0,
    "ua_l": 8, "la_l": 4, "ua_r": -8, "la_r": -4,
    "ul_l": 3, "ll_l": 0, "ul_r": -3, "ll_r": 0,
    "pelvis": (0, 0),
}


def hair_svg(kind, color=HAIR):
    """Hair drawn in head space (head circle centre at 0,-36, r=34)."""
    if kind == "bob":
        return (f'<path d="M-38,-30 Q-42,-78 0,-74 Q42,-78 38,-30 L36,-8 Q30,-2 26,-10 '
                f'L26,-46 Q0,-60 -26,-46 L-26,-10 Q-30,-2 -36,-8 Z" fill="{color}"/>')
    if kind == "pony":
        return (f'<path d="M-35,-40 Q-34,-74 0,-72 Q34,-74 35,-40 Q20,-58 -35,-40 Z" fill="{color}"/>'
                f'<path d="M30,-56 Q60,-40 46,-6 Q40,4 36,-4 Q46,-30 26,-48 Z" fill="{color}"/>')
    if kind == "short":
        return f'<path d="M-35,-38 Q-36,-74 0,-73 Q36,-74 35,-38 Q28,-56 0,-56 Q-28,-56 -35,-38 Z" fill="{color}"/>'
    if kind == "bald":
        return ""
    if kind == "glasses":
        return (f'<circle cx="-12" cy="-40" r="9" fill="none" stroke="{LINE}" stroke-width="3"/>'
                f'<circle cx="12" cy="-40" r="9" fill="none" stroke="{LINE}" stroke-width="3"/>'
                f'<path d="M-3,-40 L3,-40" stroke="{LINE}" stroke-width="3"/>')
    return ""


def fig(fid, x, y, s=1.0, pose=None, skin=CREAM, shirt=None, pants=None,
        hair=None, hair_color=HAIR, dress=None, mouth="smile", brow="none",
        brow_on=False, blush=False, rot=0, hand_r="", hand_l="", head_extra="",
        back="", face=True):
    """One rigged figure. ``hand_r``/``hand_l`` is SVG drawn in the lower-arm
    group at the hand (0,44 points down the forearm); ``back`` is drawn behind
    the torso in torso space (capes, backpacks)."""
    p = dict(DEFAULT_POSE)
    p.update(pose or {})
    body = shirt or skin
    arm_top = shirt or skin
    leg = pants or skin
    pv = p["pelvis"] if isinstance(p["pelvis"], (tuple, list)) else (p["pelvis"], 0)

    def leg_svg(side):
        return (f'<g id="{fid}-ul_{side}" transform="{jt("ul_"+side, p["ul_"+side])}">'
                f'<line x1="0" y1="0" x2="0" y2="55" stroke="{leg}" stroke-width="25" stroke-linecap="round"/>'
                f'<g id="{fid}-ll_{side}" transform="{jt("ll_"+side, p["ll_"+side])}">'
                f'<line x1="0" y1="0" x2="0" y2="53" stroke="{skin if pants is None else leg}" stroke-width="23" stroke-linecap="round"/>'
                f'</g></g>')

    def arm_svg(side, extra):
        return (f'<g id="{fid}-ua_{side}" transform="{jt("ua_"+side, p["ua_"+side])}">'
                f'<line x1="0" y1="0" x2="0" y2="44" stroke="{arm_top}" stroke-width="20" stroke-linecap="round"/>'
                f'<g id="{fid}-la_{side}" transform="{jt("la_"+side, p["la_"+side])}">'
                f'<line x1="0" y1="0" x2="0" y2="40" stroke="{skin}" stroke-width="18" stroke-linecap="round"/>'
                f'<circle cx="0" cy="44" r="11" fill="{skin}"/>{extra}'
                f'</g></g>')

    back_svg = f'<g id="{fid}-torsob" transform="{jt("torso", p["torso"])}">{back}</g>' if back else ""
    torso_path = "M-26,4 L-29,-78 Q-29,-104 0,-104 Q29,-104 29,-78 L26,4 Q0,14 -26,4 Z"
    skirt = ""
    if dress:
        skirt = f'<path d="M-26,-30 L-44,40 Q0,52 44,40 L26,-30 Z" fill="{dress}"/>'
        body = dress
    face_svg = ""
    if face:
        face_svg = (
            f'<g id="{fid}-eyes" transform="translate(0,-40) scale(1,1)">'
            f'<ellipse cx="-11" cy="0" rx="3.6" ry="4.4" fill="{LINE}"/>'
            f'<ellipse cx="11" cy="0" rx="3.6" ry="4.4" fill="{LINE}"/></g>'
            f'<path id="{fid}-brow" d="{BROWS[brow]}" stroke="{LINE}" stroke-width="3.2" '
            f'stroke-linecap="round" fill="none" opacity="{1 if brow_on else 0}"/>'
            f'<path id="{fid}-mouth" d="{MOUTHS[mouth]}" stroke="{LINE}" stroke-width="3.4" '
            f'stroke-linecap="round" fill="none"/>'
        )
        if blush:
            face_svg += (f'<ellipse cx="-20" cy="-26" rx="6" ry="3.5" fill="#E8907A" opacity=".7"/>'
                         f'<ellipse cx="20" cy="-26" rx="6" ry="3.5" fill="#E8907A" opacity=".7"/>')
    head_svg = (f'<g id="{fid}-head" transform="{jt("head", p["head"])}">'
                f'<rect x="-9" y="-10" width="18" height="16" rx="6" fill="{skin}"/>'
                f'<circle cx="0" cy="-36" r="34" fill="{skin}"/>'
                f'{hair_svg(hair, hair_color) if hair else ""}{face_svg}{head_extra}</g>')
    return (
        f'<g id="{fid}" transform="{root_t(x, y, rot, s)}">'
        f'<g id="{fid}-pelvis" transform="{pelvis_t(*pv)}">'
        f'{back_svg}{leg_svg("l")}{leg_svg("r")}'
        f'<g id="{fid}-torso" transform="{jt("torso", p["torso"])}">'
        f'{skirt}<path d="{torso_path}" fill="{body}"/>'
        f'{head_svg}{arm_svg("l", hand_l)}{arm_svg("r", hand_r)}'
        f'</g></g></g>'
    )


# ---------------------------------------------------------------- props

def shadow(sid, x, y, w=150, h=18, color=SHADOW, opacity=1):
    return (f'<ellipse id="{sid}" cx="{_f(x)}" cy="{_f(y)}" rx="{_f(w/2)}" ry="{_f(h)}" '
            f'fill="{color}" opacity="{opacity}"/>')


def floor(y, h=170, color=FLOOR, x=0, w=1080):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>'


def sofa(x, y, w=380, color=BROWN):
    """Sofa standing on y, centred on x."""
    l = x - w / 2
    return (f'<g><rect x="{l}" y="{y-150}" width="{w}" height="95" rx="22" fill="{BROWN_D}"/>'
            f'<rect x="{l-28}" y="{y-110}" width="56" height="95" rx="20" fill="{color}"/>'
            f'<rect x="{l+w-28}" y="{y-110}" width="56" height="95" rx="20" fill="{color}"/>'
            f'<rect x="{l+10}" y="{y-75}" width="{w-20}" height="55" rx="14" fill="{color}"/>'
            f'<rect x="{l-10}" y="{y-20}" width="12" height="20" fill="{BROWN_D}"/>'
            f'<rect x="{l+w-2}" y="{y-20}" width="12" height="20" fill="{BROWN_D}"/></g>')


def table(x, y, w=420, h=150, top=BROWN):
    l = x - w / 2
    return (f'<g><rect x="{l}" y="{y-h}" width="{w}" height="22" rx="6" fill="{top}"/>'
            f'<rect x="{l+28}" y="{y-h+20}" width="16" height="{h-20}" fill="{BROWN_D}"/>'
            f'<rect x="{l+w-44}" y="{y-h+20}" width="16" height="{h-20}" fill="{BROWN_D}"/></g>')


def chair(x, y, facing=1):
    """Side-view chair; facing=1 means the seat opens to the right."""
    bx = x - 40 * facing
    return (f'<g><rect x="{min(bx, bx+12*facing)-6}" y="{y-200}" width="12" height="200" fill="{BROWN}"/>'
            f'<rect x="{x-45}" y="{y-95}" width="90" height="14" rx="4" fill="{BROWN}"/>'
            f'<rect x="{x+33*facing-6}" y="{y-85}" width="12" height="85" fill="{BROWN}"/></g>')


def lamp(x, y_top=0, drop=90, color=BROWN_L):
    return (f'<g><line x1="{x}" y1="{y_top}" x2="{x}" y2="{y_top+drop}" stroke="{color}" stroke-width="3"/>'
            f'<path d="M{x-26},{y_top+drop+26} Q{x},{y_top+drop-14} {x+26},{y_top+drop+26} Z" fill="{color}"/>'
            f'<ellipse cx="{x}" cy="{y_top+drop+28}" rx="10" ry="5" fill="#FFE7B0"/></g>')


def tree(x, y, h=260, color=BROWN_L, kind="round"):
    if kind == "pine":
        return (f'<g><rect x="{x-7}" y="{y-40}" width="14" height="40" fill="{BROWN_D}"/>'
                f'<path d="M{x},{y-h} L{x+55},{y-h*0.55} L{x+28},{y-h*0.55} L{x+70},{y-40} '
                f'L{x-70},{y-40} L{x-28},{y-h*0.55} L{x-55},{y-h*0.55} Z" fill="{color}"/></g>')
    return (f'<g><rect x="{x-8}" y="{y-h*0.45}" width="16" height="{h*0.45}" fill="{BROWN_D}"/>'
            f'<ellipse cx="{x}" cy="{y-h*0.62}" rx="{h*0.22}" ry="{h*0.38}" fill="{color}"/></g>')


def heart_path(cx, cy, s=1.0):
    def p(x, y):
        return f"{_f(cx + x * s)},{_f(cy + y * s)}"
    return (f"M{p(0,40)} C{p(-95,-25)} {p(-60,-105)} {p(0,-55)} "
            f"C{p(60,-105)} {p(95,-25)} {p(0,40)} Z")


def neon_heart(hid, cx, cy, s=1.0, color="#FF2D55"):
    d = heart_path(cx, cy, s)
    return (f'<g id="{hid}">'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{26*s}" opacity=".25" filter="url(#glow-big)"/>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{10*s}" filter="url(#glow)"/>'
            f'<path d="{d}" fill="none" stroke="#FFD6DE" stroke-width="{3.5*s}"/></g>')


def thought(tid, x, y, w=170, h=120, inner="", dots_dir=-1):
    """Cloud bubble centred at x,y; the trailing dots run down-left (dots_dir=-1)
    or down-right (1)."""
    rx, ry = w / 2, h / 2
    puffs = "".join(
        f'<circle cx="{_f(x + rx*0.62*c)}" cy="{_f(y + ry*0.55*sn)}" r="{_f(ry*0.62)}" fill="#F7F1E8"/>'
        for c, sn in ((-1, 0), (1, 0), (-0.45, -0.75), (0.45, -0.75), (-0.45, 0.7), (0.45, 0.7)))
    dots = (f'<circle cx="{_f(x + dots_dir*rx*0.75)}" cy="{_f(y + ry*1.05)}" r="11" fill="#F7F1E8"/>'
            f'<circle cx="{_f(x + dots_dir*rx*1.0)}" cy="{_f(y + ry*1.45)}" r="7" fill="#F7F1E8"/>')
    return (f'<g id="{tid}">{dots}{puffs}<ellipse cx="{x}" cy="{y}" rx="{_f(rx*0.85)}" ry="{_f(ry*0.8)}" '
            f'fill="#F7F1E8"/>{inner}</g>')


def bouquet(color="#D9322B"):
    """Held in a hand group: stems run up from the hand (0,44)."""
    flowers = "".join(
        f'<circle cx="{dx}" cy="{dy}" r="13" fill="{color}"/><circle cx="{dx}" cy="{dy}" r="5" fill="#8E1C17"/>'
        for dx, dy in ((-18, -22), (0, -34), (18, -22), (-8, -8), (10, -6)))
    return (f'<g transform="translate(0,44) rotate(180)">'
            f'<path d="M-6,0 L-14,-40 M0,0 L0,-50 M6,0 L14,-40" stroke="#5E7A3A" stroke-width="4"/>'
            f'<g transform="translate(0,-38)">{flowers}</g></g>')


def glass(color="#E8A33A"):
    return (f'<g transform="translate(0,44) rotate(180)">'
            f'<path d="M-11,-6 L-13,-42 L13,-42 L11,-6 Z" fill="#FFF3DA" opacity=".9"/>'
            f'<path d="M-11,-8 L-12,-28 L12,-28 L11,-8 Z" fill="{color}"/></g>')


def bottle(color, fill_id=None, level=1.0):
    """Bottle in a hand, neck pointing along the forearm direction (+y)."""
    lid = f' id="{fill_id}"' if fill_id else ""
    return (f'<g transform="translate(0,40)">'
            f'<rect x="-15" y="-30" width="30" height="62" rx="9" fill="#F1F4F7" opacity=".9"/>'
            f'<rect{lid} x="-13" y="{_f(-28 + 58*(1-level))}" width="26" height="{_f(58*level)}" rx="7" fill="{color}"/>'
            f'<rect x="-7" y="30" width="14" height="16" rx="3" fill="#F1F4F7"/>'
            f'<rect x="-8" y="44" width="16" height="6" rx="2" fill="{color}"/></g>')


def speech_zigzag(sid, x, y, w=210, h=120, color="#E2231A", text="#@!", flip=False):
    sx = -1 if flip else 1
    tail = f"M{x - 30*sx},{y + h/2 - 6} L{x - 75*sx},{y + h/2 + 45} L{x - 5*sx},{y + h/2 - 6} Z"
    pts = []
    n = 14
    import math
    for i in range(n * 2):
        a = math.pi * 2 * i / (n * 2)
        r = 1.0 if i % 2 == 0 else 0.78
        pts.append(f"{_f(x + math.cos(a)*w/2*r)},{_f(y + math.sin(a)*h/2*r)}")
    return (f'<g id="{sid}"><path d="{tail}" fill="{color}"/><path d="M{" L".join(pts)} Z" fill="{color}"/>'
            f'<text x="{x}" y="{y+16}" text-anchor="middle" font-family="Archivo Black" font-size="44" '
            f'fill="#fff">{text}</text></g>')


def broken_heart(cx, cy, s=1.0, color="#D9322B"):
    d = heart_path(cx, cy, s)
    crack = (f"M{_f(cx)},{_f(cy-55*s)} L{_f(cx-12*s)},{_f(cy-25*s)} L{_f(cx+10*s)},{_f(cy-5*s)} "
             f"L{_f(cx-6*s)},{_f(cy+25*s)}")
    return (f'<g><path d="{d}" fill="{color}"/>'
            f'<path d="{crack}" stroke="#F7F1E8" stroke-width="{6*s}" fill="none" stroke-linejoin="round"/></g>')


def spotlight(lid, x, y_top, y_floor, w_top=60, w_floor=360, opacity=0.22):
    return (f'<g id="{lid}"><path d="M{x-w_top/2},{y_top} L{x+w_top/2},{y_top} L{x+w_floor/2},{y_floor} '
            f'L{x-w_floor/2},{y_floor} Z" fill="url(#beam)" opacity="{opacity}"/>'
            f'<ellipse cx="{x}" cy="{y_floor}" rx="{w_floor/2}" ry="26" fill="#9a9a9a" opacity="{opacity*1.4}"/></g>')


def clock(cid, x, y, r=62):
    ticks = "".join(
        f'<line x1="0" y1="{-r+8}" x2="0" y2="{-r+18}" stroke="{LINE}" stroke-width="4" transform="rotate({a})"/>'
        for a in range(0, 360, 30))
    return (f'<g transform="translate({x},{y})"><circle r="{r+8}" fill="{BROWN}"/><circle r="{r}" fill="#F7F1E8"/>'
            f'{ticks}<g id="{cid}-h" transform="translate(0,0) rotate(60)"><line x1="0" y1="0" x2="0" y2="{-r*0.5}" '
            f'stroke="{LINE}" stroke-width="7" stroke-linecap="round"/></g>'
            f'<g id="{cid}-m" transform="translate(0,0) rotate(0)"><line x1="0" y1="0" x2="0" y2="{-r*0.8}" '
            f'stroke="#D9322B" stroke-width="5" stroke-linecap="round"/></g><circle r="6" fill="{LINE}"/></g>')


def snail(sid, x, y, s=1.0):
    return (f'<g id="{sid}" transform="{root_t(x, y, 0, s)}">'
            f'<path d="M-60,0 Q-70,-14 -52,-16 L40,-16 Q60,-16 62,-40 L70,-62 M62,-40 L52,-64" '
            f'stroke="{CREAM}" stroke-width="14" stroke-linecap="round" fill="none"/>'
            f'<path d="M-60,0 L48,0 Q66,-2 62,-30 L-50,-12 Z" fill="{CREAM}"/>'
            f'<circle cx="-5" cy="-42" r="40" fill="{BROWN}"/>'
            f'<path d="M-5,-42 m-24,0 a24,24 0 1,1 24,24 a16,16 0 1,1 -14,-18 a8,8 0 1,1 10,8" '
            f'stroke="{BROWN_D}" stroke-width="6" fill="none"/></g>')


def boulder(bid=""):
    i = f' id="{bid}"' if bid else ""
    return (f'<g{i}><path d="M-80,-10 Q-100,-110 -20,-140 Q60,-160 95,-90 Q120,-20 60,10 Q-40,30 -80,-10 Z" '
            f'fill="{BROWN}"/><path d="M-40,-90 Q-10,-110 30,-100 M20,-40 Q50,-50 70,-30" stroke="{BROWN_D}" '
            f'stroke-width="6" fill="none" stroke-linecap="round"/></g>')


def mask_disc(skin="#FBEFD9"):
    return (f'<g><circle cx="0" cy="0" r="48" fill="{skin}" stroke="{BROWN_L}" stroke-width="4"/>'
            f'<path d="M-20,-10 Q-14,-18 -8,-10 M8,-10 Q14,-18 20,-10" stroke="{LINE}" stroke-width="4" '
            f'fill="none" stroke-linecap="round"/>'
            f'<path d="M-24,8 Q0,36 24,8" stroke="{LINE}" stroke-width="5" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="-28" cy="10" rx="7" ry="4" fill="#E8907A" opacity=".7"/>'
            f'<ellipse cx="28" cy="10" rx="7" ry="4" fill="#E8907A" opacity=".7"/></g>')


def defs(accent):
    """Shared SVG defs: glows and the spotlight beam gradient."""
    return (
        '<defs>'
        '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        '<filter id="glow-big" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="22"/></filter>'
        '<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".9"/>'
        '<stop offset="1" stop-color="#ffffff" stop-opacity=".25"/></linearGradient>'
        f'<radialGradient id="aura"><stop offset="0" stop-color="{accent}" stop-opacity=".95"/>'
        f'<stop offset=".45" stop-color="{accent}" stop-opacity=".45"/>'
        f'<stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="warm"><stop offset="0" stop-color="#FFE3A3" stop-opacity=".95"/>'
        '<stop offset=".5" stop-color="#FFB25B" stop-opacity=".35"/><stop offset="1" stop-color="#FF8A3D" stop-opacity="0"/></radialGradient>'
        '</defs>'
    )


# JS helpers embedded in every scene. `P(id, pose, t, d, ease)` tweens a
# figure to a pose; keys: root [x,y,rot,s], pelvis [dy,rot], any joint angle,
# mouth / brow (names from MOUTHS / BROWS), eyes (vertical scale, 1 = open).
JS_HELPERS = r"""
const RIG = __RIG__, PELVIS_Y = __PY__, MOUTHS = __MOUTHS__, BROWS = __BROWS__;
const tl = gsap.timeline({ paused: true });
function jointT(k, v) {
  if (k === "pelvis") { const d = Array.isArray(v) ? v : [v, 0]; return `translate(0,${PELVIS_Y + d[0]}) rotate(${d[1]})`; }
  const b = RIG[k]; return `translate(${b[0]},${b[1]}) rotate(${v})`;
}
function P(id, pose, t, d = 0.35, ease = "power2.inOut") {
  for (const k in pose) {
    const v = pose[k]; let sel = `#${id}-${k}`, vars;
    if (k === "root") { sel = `#${id}`; vars = { attr: { transform: `translate(${v[0]},${v[1]}) rotate(${v[2] || 0}) scale(${v[3] || 1})` } }; }
    else if (k === "mouth") vars = { attr: { d: MOUTHS[v] } };
    else if (k === "brow") vars = { attr: { d: BROWS[v] }, opacity: v === "none" ? 0 : 1 };
    else if (k === "eyes") vars = { attr: { transform: `translate(0,-40) scale(1,${v})` } };
    else { vars = { attr: { transform: jointT(k, v) } }; if (k === "torso") sel = `#${id}-torso, #${id}-torsob`; }
    if (d === 0) tl.set(sel, vars, t); else tl.to(sel, { ...vars, duration: d, ease }, t);
  }
}
function blink(id, t) { P(id, { eyes: 0.1 }, t, 0.06, "none"); P(id, { eyes: 1 }, t + 0.09, 0.08, "none"); }
function T(sel, t, vars, d = 0.35, ease = "power2.inOut") {
  if (d === 0) tl.set(sel, vars, t); else tl.to(sel, { ...vars, duration: d, ease }, t);
}
// hard cut between shots inside a scene
function cut(hideSel, showSel, t) { if (hideSel) tl.set(hideSel, { opacity: 0 }, t); if (showSel) tl.set(showSel, { opacity: 1 }, t); }
// walk/run cycle from (x0) to (x1) between t0 and t1; s = figure scale
function walk(id, x0, x1, y, s, t0, t1, step = 0.32, amp = 26, lean = 4) {
  T(`#${id}`, t0, { attr: { transform: `translate(${x0},${y}) rotate(0) scale(${s})` } }, 0);
  tl.to(`#${id}`, { attr: { transform: `translate(${x1},${y}) rotate(0) scale(${s})` }, duration: t1 - t0, ease: "none" }, t0);
  P(id, { torso: lean }, t0, 0.2);
  let k = 0;
  for (let t = t0; t < t1 - 0.01; t += step, k++) {
    const a = k % 2 ? amp : -amp, d = Math.min(step, t1 - t);
    P(id, { ul_l: a, ll_l: a > 0 ? 0 : -amp * 0.9, ul_r: -a, ll_r: -a > 0 ? 0 : -amp * 0.9,
            ua_l: -a * 0.8, la_l: -10, ua_r: a * 0.8, la_r: -10, pelvis: [k % 2 ? -4 : 0, 0] }, t, d, "sine.inOut");
  }
}
"""


def js_helpers():
    import json
    return (JS_HELPERS.replace("__RIG__", json.dumps({k: list(v) for k, v in RIG.items()}))
            .replace("__PY__", str(PELVIS_Y)).replace("__MOUTHS__", json.dumps(MOUTHS))
            .replace("__BROWS__", json.dumps(BROWS)))
