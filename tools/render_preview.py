"""Rendert ein Vorschau-Video im Stil der Referenzen (schwarzer Rahmen, Farbtitel,
Karaoke-Untertitel, flache Figuren) aus Voiceover + Szenenliste.

Aufruf: python3 render_preview.py voiceover.mp3 out.mp4
"""
import json
import math
import random
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
SS = 2  # Supersampling der Szene
BAND_Y, BAND_H = 700, 608  # Animationsstreifen (16:9)
BW, BH = W * SS, BAND_H * SS
ZOOM = 1.2  # Figuren größer wirken lassen

BLACK = (0, 0, 0)
CREAM = (242, 223, 196)
CREAM_D = (222, 199, 168)
BROWN = (140, 84, 48)
BROWN_D = (104, 60, 34)
COPPER = (184, 115, 62)
GREY = (52, 52, 52)
GREY_L = (90, 90, 90)
ACCENT = (224, 33, 63)  # Granatrot Januar
TEXT_DIM = (58, 58, 58)
WHITE = (255, 255, 255)

F_TITLE = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
F_SUB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_WM = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"

TITLE = '"JANUAR"'
KEYWORD = "januar"
WATERMARK = "@DEINNAME"

# (Untertitel, Szenenfunktion) - Text muss exakt dem Voiceover entsprechen
SCENES = [
    ("Wenn du im Januar geboren bist …", "drink"),
    ("heißt es, dass du ehrgeiziger bist als die meisten.", "race"),
    ("Menschen, die im Januar geboren sind, gelten als", "standout"),
    ("diszipliniert,", "alarm"),
    ("zielstrebig", "stairs"),
    ("und erstaunlich ruhig unter Druck.", "meditate_chaos"),
    ("Während andere noch überlegen,", "confused"),
    ("hast du längst einen Plan.", "board"),
    ("Du redest nicht groß über deine Ziele.", "zip"),
    ("Du arbeitest still daran,", "desk"),
    ("bis alle staunen.", "trophy"),
    ("Und du bist loyaler, als viele denken.", "loyal_split"),
    ("Wenn du jemanden in dein Leben lässt,", "door"),
    ("dann richtig.", "sofa_blanket"),
    ("Aber es gibt eine Schattenseite.", "shadow"),
    ("Du kannst ziemlich streng mit dir selbst sein.", "redpen"),
    ("Ein kleiner Fehler,", "small_x"),
    ("und du denkst tagelang darüber nach.", "overthink"),
    ("Du zeigst selten, wenn es dir schlecht geht,", "mask"),
    ("weil du nicht willst, dass sich jemand Sorgen macht.", "wave_off"),
    ("Und manchmal wirkst du kalt,", "cold"),
    ("obwohl in dir eigentlich ganz viel los ist.", "inner_storm"),
    ("Im Grunde bist du der Mensch, auf den sich alle verlassen,", "bridge"),
    ("während du selbst manchmal vergisst,", "alone_sofa"),
    ("dass du dich auch anlehnen darfst.", "lean"),
    ("Wenn du im Januar geboren bist, schreib „Januar“ in die Kommentare.", "crowd"),
]


# ---------------------------------------------------------------- Timing

def audio_duration(path):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(out)


def speech_segments(path, dur):
    """Sprachabschnitte über silencedetect."""
    log = subprocess.run(
        ["ffmpeg", "-i", path, "-af", "silencedetect=noise=-35dB:d=0.18", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    sil = []
    start = None
    for line in log.splitlines():
        if "silence_start" in line:
            start = float(line.split("silence_start:")[1].split()[0])
        elif "silence_end" in line and start is not None:
            sil.append((max(0.0, start), float(line.split("silence_end:")[1].split()[0])))
            start = None
    if start is not None:
        sil.append((start, dur))
    segs, t = [], 0.0
    for a, b in sil:
        if a > t:
            segs.append((t, a))
        t = b
    if t < dur:
        segs.append((t, dur))
    return [s for s in segs if s[1] - s[0] > 0.05]


def word_timings(words, segs):
    """Verteilt Wörter proportional zur Zeichenzahl über die reine Sprechzeit."""
    weights = [len(w) + 2 for w in words]
    total_w = sum(weights)
    speech = sum(b - a for a, b in segs)

    def speech_to_real(x):
        for a, b in segs:
            if x <= b - a:
                return a + x
            x -= b - a
        return segs[-1][1]

    times, acc = [], 0.0
    for w in weights:
        times.append(speech_to_real(acc / total_w * speech))
        acc += w
    return times


# ---------------------------------------------------------------- Zeichnen

def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def ground(d, x, y, w=260):
    d.ellipse([x - w // 2, y - 18, x + w // 2, y + 18], fill=GREY)


def floor(d, y=None, color=GREY):
    y = y if y is not None else int(BH * 0.86)
    d.rectangle([0, y, BW, BH], fill=color)


def limb(d, p1, p2, width, color):
    d.line([p1, p2], fill=color, width=width)
    r = width // 2
    for p in (p1, p2):
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=color)


def polar(p, ang, length):
    a = math.radians(ang)
    return (p[0] + math.sin(a) * length, p[1] + math.cos(a) * length)


def figure(d, x, y, s=1.0, body=CREAM, shirt=None, arms=(20, -20), legs=(8, -8),
           sit=False, head_dy=0, face=None, hair=None, scarf=None, hat=None, lean=0):
    """Flache Figur. (x, y) = Fußpunkt. Winkel in Grad, 0 = nach unten."""
    lw = int(30 * s)
    hip = (x + lean * 0.3, y - 160 * s) if not sit else (x, y - 110 * s)
    neck = (hip[0] + lean, hip[1] - 150 * s)
    # Beine
    for i, a in enumerate(legs):
        if sit:
            knee = (hip[0] + (60 if i == 0 else 50) * s, hip[1] + 6 * s)
            foot = (knee[0] + 8 * s, knee[1] + 104 * s)
            limb(d, hip, knee, lw, body)
            limb(d, knee, foot, lw, body)
        else:
            limb(d, hip, polar(hip, a, 160 * s), lw, body)
    # Rumpf
    torso_col = shirt or body
    d.rounded_rectangle([min(neck[0], hip[0]) - 40 * s, neck[1] - 8 * s,
                         max(neck[0], hip[0]) + 40 * s, hip[1] + 20 * s],
                        radius=int(36 * s), fill=torso_col)
    if scarf:
        d.rounded_rectangle([neck[0] - 44 * s, neck[1] - 14 * s, neck[0] + 44 * s, neck[1] + 16 * s],
                            radius=int(14 * s), fill=scarf)
    # Arme
    sh = (neck[0], neck[1] + 20 * s)
    for a in arms:
        elbow = polar(sh, a, 75 * s)
        hand = polar(elbow, a * 1.15, 75 * s)
        limb(d, sh, elbow, int(26 * s), body)
        limb(d, elbow, hand, int(26 * s), body)
    # Kopf
    hr = 52 * s
    hc = (neck[0] + lean * 0.2, neck[1] - hr - 6 * s + head_dy)
    d.ellipse([hc[0] - hr, hc[1] - hr, hc[0] + hr, hc[1] + hr], fill=body)
    if hair:
        d.pieslice([hc[0] - hr, hc[1] - hr, hc[0] + hr, hc[1] + hr], 180, 360, fill=hair)
    if hat:
        d.polygon([(hc[0] - 30 * s, hc[1] - hr + 10 * s), (hc[0] + 30 * s, hc[1] - hr + 10 * s),
                   (hc[0], hc[1] - hr - 70 * s)], fill=hat)
    if face:
        ink = BROWN_D
        ex = 18 * s
        ey = hc[1] - 6 * s
        if face == "happy":
            for sx in (-ex, ex):
                d.arc([hc[0] + sx - 9 * s, ey - 9 * s, hc[0] + sx + 9 * s, ey + 9 * s], 200, 340, fill=ink, width=int(5 * s))
            d.chord([hc[0] - 24 * s, hc[1] + 6 * s, hc[0] + 24 * s, hc[1] + 34 * s], 0, 180, fill=ink)
        elif face == "sad":
            for sx in (-ex, ex):
                d.ellipse([hc[0] + sx - 5 * s, ey - 5 * s, hc[0] + sx + 5 * s, ey + 5 * s], fill=ink)
            d.arc([hc[0] - 18 * s, hc[1] + 16 * s, hc[0] + 18 * s, hc[1] + 40 * s], 200, 340, fill=ink, width=int(5 * s))
        elif face == "shock":
            for sx in (-ex, ex):
                d.ellipse([hc[0] + sx - 7 * s, ey - 7 * s, hc[0] + sx + 7 * s, ey + 7 * s], fill=ink)
            d.ellipse([hc[0] - 10 * s, hc[1] + 14 * s, hc[0] + 10 * s, hc[1] + 36 * s], fill=ink)
        elif face == "calm":
            for sx in (-ex, ex):
                d.arc([hc[0] + sx - 9 * s, ey - 4 * s, hc[0] + sx + 9 * s, ey + 10 * s], 20, 160, fill=ink, width=int(5 * s))
        elif face == "neutral":
            for sx in (-ex, ex):
                d.ellipse([hc[0] + sx - 5 * s, ey - 5 * s, hc[0] + sx + 5 * s, ey + 5 * s], fill=ink)
            d.line([hc[0] - 12 * s, hc[1] + 24 * s, hc[0] + 12 * s, hc[1] + 24 * s], fill=ink, width=int(5 * s))
    return hc, hr


def sofa(d, x, y, w=620, color=BROWN):
    d.rounded_rectangle([x - w // 2, y - 230, x + w // 2, y - 90], radius=40, fill=color)
    d.rounded_rectangle([x - w // 2 - 40, y - 160, x - w // 2 + 50, y - 20], radius=30, fill=COPPER)
    d.rounded_rectangle([x + w // 2 - 50, y - 160, x + w // 2 + 40, y - 20], radius=30, fill=COPPER)
    d.rounded_rectangle([x - w // 2 + 20, y - 110, x + w // 2 - 20, y - 30], radius=20, fill=COPPER)
    d.rectangle([x - w // 2 - 20, y - 30, x - w // 2, y], fill=BROWN_D)
    d.rectangle([x + w // 2, y - 30, x + w // 2 + 20, y], fill=BROWN_D)


def table(d, x, y, w=420, h=170):
    d.rectangle([x - w // 2, y - h, x + w // 2, y - h + 26], fill=BROWN)
    d.rectangle([x - w // 2 + 20, y - h, x - w // 2 + 44, y], fill=BROWN_D)
    d.rectangle([x + w // 2 - 44, y - h, x + w // 2 - 20, y], fill=BROWN_D)


def chair(d, x, y, facing=1):
    d.rectangle([x - 50, y - 110, x + 50, y - 90], fill=BROWN)
    bx = x - 50 * facing
    d.rectangle([min(bx, bx - 18 * facing), y - 250, max(bx, bx - 18 * facing), y], fill=BROWN_D)
    d.rectangle([x + 34 * facing - 9, y - 100, x + 34 * facing + 9, y], fill=BROWN_D)


def star(d, cx, cy, r, color, rot=0.0):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        a = math.radians(i * 36 - 90) + rot
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.polygon(pts, fill=color)


def heart(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r * 0.8, cx, cy + r * 0.2], fill=color)
    d.ellipse([cx, cy - r * 0.8, cx + r, cy + r * 0.2], fill=color)
    d.polygon([(cx - r * 0.97, cy - r * 0.15), (cx + r * 0.97, cy - r * 0.15), (cx, cy + r * 1.05)], fill=color)


def bubble(d, cx, cy, rw, rh, color=(235, 235, 235)):
    for dx, dy, k in [(-0.55, 0.1, 0.55), (0.55, 0.1, 0.55), (0, -0.35, 0.6), (-0.3, -0.25, 0.5),
                      (0.3, -0.25, 0.5), (0, 0.25, 0.6)]:
        d.ellipse([cx + dx * rw - k * rw, cy + dy * rh - k * rh, cx + dx * rw + k * rw, cy + dy * rh + k * rh],
                  fill=color)
    return color


def _add(a, b):
    from PIL import ImageChops
    return ImageChops.add(a, b)


def xmark(d, cx, cy, r, color, w=22):
    d.line([cx - r, cy - r, cx + r, cy + r], fill=color, width=w)
    d.line([cx - r, cy + r, cx + r, cy - r], fill=color, width=w)


def snowflake(d, cx, cy, r, color, rot):
    for k in range(3):
        a = rot + k * math.pi / 3
        d.line([cx - math.cos(a) * r, cy - math.sin(a) * r, cx + math.cos(a) * r, cy + math.sin(a) * r],
               fill=color, width=max(4, int(r / 4)))


# ---------------------------------------------------------------- Szenen
# Jede Szene bekommt (img, d, p, t): p = Fortschritt 0..1, t = Sekunden seit Szenenstart

GY = int(BH * 0.86)  # Bodenlinie
CX = BW // 2


def bob(t, amp=6, f=2.0):
    return math.sin(t * f * math.pi) * amp


def sc_drink(img, d, p, t):
    ground(d, CX, GY, 420)
    fill = ease(p * 1.3)
    figure(d, CX, GY, 1.5, arms=(160, 25), shirt=None)
    # Rot läuft von oben über den Körper
    top = GY - 560
    level = top + fill * 560
    mask = Image.new("L", (BW, BH), 0)
    md = ImageDraw.Draw(mask)
    figure(md, CX, GY, 1.5, body=255, arms=(160, 25))
    md.rectangle([0, level, BW, BH], fill=0)
    img.paste(Image.new("RGB", (BW, BH), ACCENT), (0, 0), mask)
    # Flasche
    bx, by = CX + 40, GY - 690
    d.rounded_rectangle([bx, by - 30, bx + 150, by + 40], radius=20, fill=BROWN)
    d.rectangle([bx - 40, by - 10, bx, by + 20], fill=BROWN_D)
    for i in range(8):
        ph = (t * 1.6 + i / 8) % 1
        d.ellipse([CX - 120 + i * 30 - 10, GY - 600 + ph * 520 - 10, CX - 120 + i * 30 + 10, GY - 600 + ph * 520 + 10],
                  fill=ACCENT)


def sc_race(img, d, p, t):
    floor(d)
    for i, x in enumerate([BW * 0.15, BW * 0.27, BW * 0.39]):
        figure(d, x + p * 60, GY, 0.9, arms=(30 + bob(t, 20, 1.5), -30), legs=(10 + bob(t, 12, 1.5), -10), face="sad")
    lead = BW * 0.55 + ease(p) * BW * 0.25
    sw = 40 * math.sin(t * 9)
    figure(d, lead, GY, 1.0, shirt=ACCENT, arms=(60 + sw, -60 - sw), legs=(35 * math.sin(t * 9), -35 * math.sin(t * 9)),
           face="happy", lean=30)


def sc_standout(img, d, p, t):
    floor(d)
    xs = [BW * k for k in (0.12, 0.26, 0.4, 0.6, 0.74, 0.88)]
    for x in xs:
        chair(d, x, GY)
        figure(d, x - 10, GY, 0.85, sit=True, arms=(40, 30))
    rise = ease(p * 1.6)
    y = GY - 60 * (1 - rise)
    figure(d, CX, y, 1.0, shirt=CREAM_D, arms=(170 * rise + 20, -20), face="happy")
    d.polygon([(CX - 12, y - 300), (CX + 12, y - 300), (CX + 18, y - 190), (CX, y - 170), (CX - 18, y - 190)], fill=ACCENT)


def sc_alarm(img, d, p, t):
    floor(d)
    # Bett
    d.rounded_rectangle([BW * 0.1, GY - 170, BW * 0.45, GY - 80], radius=20, fill=BROWN)
    d.rectangle([BW * 0.1, GY - 300, BW * 0.12, GY], fill=BROWN_D)
    cx, cy = BW * 0.52, GY - 150
    shake = math.sin(t * 50) * 8 if p < 0.4 else 0
    d.ellipse([cx - 60 + shake, cy - 60, cx + 60 + shake, cy + 60], fill=ACCENT)
    d.ellipse([cx - 44 + shake, cy - 44, cx + 44 + shake, cy + 44], fill=CREAM)
    d.line([cx + shake, cy, cx + shake, cy - 32], fill=BROWN_D, width=8)
    d.line([cx + shake, cy, cx + shake + 24, cy], fill=BROWN_D, width=8)
    if p < 0.4:
        for k in (-1, 1):
            d.arc([cx - 100, cy - 100, cx + 100, cy + 100], 200 if k < 0 else -20, 250 if k < 0 else 30, fill=ACCENT, width=8)
        figure(d, BW * 0.28, GY - 60, 0.8, sit=True, arms=(120, 60), face="shock")
    else:
        # Liegestütze
        up = (math.sin(t * 8) + 1) / 2
        px, py = BW * 0.75, GY - 40 - up * 40
        limb(d, (px - 170, GY - 10), (px + 60, py - 60), 30, CREAM)
        d.rounded_rectangle([px - 120, py - 110 + 20, px + 90, py - 30], radius=36, fill=CREAM)
        d.ellipse([px + 80, py - 140, px + 170, py - 50], fill=CREAM)
        limb(d, (px + 50, py - 60), (px + 60, GY - 10), 26, CREAM)


def sc_stairs(img, d, p, t):
    floor(d)
    steps = 7
    x0, y0, sw, sh = BW * 0.28, GY, 150, 95
    for i in range(steps):
        d.rectangle([x0 + i * sw, y0 - (i + 1) * sh, x0 + (i + 1) * sw + 8, y0 - i * sh], fill=COPPER)
    star(d, x0 + steps * sw + 40, y0 - steps * sh - 110, 70, ACCENT, rot=t * 0.8)
    k = ease(p) * (steps - 1)
    i = int(k)
    fx = x0 + (k + 0.5) * sw
    fy = y0 - (i + 1) * sh
    figure(d, fx, fy, 0.75, arms=(150 + bob(t, 20, 3), -30), legs=(25 * math.sin(t * 8), -25 * math.sin(t * 8)))
    for j in range(5):
        figure(d, BW * 0.05 + j * 90 + bob(t + j, 10, 1), GY, 0.55, arms=(80, 60), legs=(60, 80), lean=40)


def sc_meditate_chaos(img, d, p, t):
    ground(d, CX, GY, 520)
    d.ellipse([CX - 220, GY - 60, CX + 220, GY + 10], fill=ACCENT)
    # Lotus
    d.ellipse([CX - 190, GY - 120, CX + 190, GY - 20], fill=CREAM)
    d.rounded_rectangle([CX - 80, GY - 360, CX + 80, GY - 90], radius=60, fill=CREAM)
    limb(d, (CX - 60, GY - 300), (CX - 150, GY - 120), 26, CREAM)
    limb(d, (CX + 60, GY - 300), (CX + 150, GY - 120), 26, CREAM)
    d.ellipse([CX - 70, GY - 500, CX + 70, GY - 360], fill=CREAM)
    for sx in (-24, 24):
        d.arc([CX + sx - 12, GY - 440, CX + sx + 12, GY - 424], 20, 160, fill=BROWN_D, width=6)
    rnd = random.Random(3)
    for k in range(12):
        a = rnd.random() * math.tau + t * (0.8 + rnd.random())
        r = 420 + rnd.random() * 200
        x, y = CX + math.cos(a) * r * 1.4, GY - 300 + math.sin(a) * r * 0.5
        kind = k % 3
        if kind == 0:
            d.rectangle([x - 40, y - 50, x + 40, y + 50], fill=CREAM_D)
        elif kind == 1:
            d.rounded_rectangle([x - 26, y - 48, x + 26, y + 48], radius=10, fill=BROWN_D)
        else:
            d.ellipse([x - 30, y - 30, x + 30, y + 30], fill=COPPER)


def sc_confused(img, d, p, t):
    floor(d)
    for k, x in enumerate((BW * 0.25, BW * 0.5, BW * 0.75)):
        hc, hr = figure(d, x, GY, 0.95, arms=(170 + bob(t + k, 15, 2), -15), face="neutral")
        qy = hc[1] - hr - 90 + bob(t + k, 12, 1.5)
        f = ImageFont.truetype(F_TITLE, 120)
        d.text((hc[0], qy), "?", font=f, fill=ACCENT, anchor="mm")


def sc_board(img, d, p, t):
    floor(d)
    bx, by = BW * 0.45, GY - 560
    d.rectangle([bx, by, bx + 700, by + 420], fill=BROWN)
    d.rectangle([bx + 20, by + 20, bx + 680, by + 400], fill=(70, 46, 30))
    n = min(4, int(ease(p * 1.4) * 4) + 1)
    pts = [(bx + 80, by + 330), (bx + 240, by + 240), (bx + 380, by + 280), (bx + 520, by + 140), (bx + 630, by + 70)]
    d.line(pts[:n + 1], fill=ACCENT, width=16)
    tip = pts[n]
    d.polygon([(tip[0] + 30, tip[1] - 30), (tip[0] - 30, tip[1] - 10), (tip[0] + 10, tip[1] + 30)], fill=ACCENT)
    for i in range(4):
        d.rectangle([bx + 80 + i * 70, by + 380 - (i + 1) * 40, bx + 120 + i * 70, by + 380], fill=CREAM_D)
    figure(d, BW * 0.3, GY, 1.0, arms=(150 + bob(t, 10, 2), -20), face="happy", lean=10)


def sc_zip(img, d, p, t):
    floor(d)
    table(d, BW * 0.3, GY, 300, 200)
    table(d, BW * 0.72, GY, 300, 200)
    for x in (BW * 0.14, BW * 0.86):
        chair(d, x, GY, 1 if x < CX else -1)
    hc, hr = figure(d, BW * 0.14 + 10, GY, 0.85, sit=True, arms=(110 + bob(t, 30, 4), 40), face="happy")
    figure(d, BW * 0.86 - 10, GY, 0.85, sit=True, arms=(-110 - bob(t, 30, 4), -40), face="happy")
    chair(d, CX, GY)
    hc, hr = figure(d, CX, GY, 0.95, sit=True, arms=(160, 30))
    mx, my = hc[0], hc[1] + 22
    zl = ease(p * 1.5)
    d.line([mx - 34, my, mx - 34 + 68 * zl, my], fill=ACCENT, width=10)
    d.rectangle([mx - 40 + 68 * zl, my - 10, mx - 22 + 68 * zl, my + 14], fill=ACCENT)
    f = ImageFont.truetype(F_TITLE, 60)
    for k, x in enumerate((BW * 0.2, BW * 0.8)):
        if math.sin(t * 6 + k) > 0:
            d.text((x, GY - 520), "~", font=f, fill=GREY_L, anchor="mm")


def sc_desk(img, d, p, t):
    floor(d)
    dx = CX + 60
    table(d, dx, GY, 520, 210)
    # Lampe
    lx, ly = dx + 170, GY - 210
    d.line([lx, ly, lx - 30, ly - 160], fill=BROWN_D, width=12)
    d.polygon([(lx - 90, ly - 150), (lx + 10, ly - 190), (lx - 10, ly - 110)], fill=ACCENT)
    img.paste(_add(img, _lightcone(lx - 40, ly - 130)), (0, 0))
    chair(d, dx - 230, GY)
    figure(d, dx - 220, GY, 0.95, sit=True, arms=(110 + bob(t, 12, 4), 120 - bob(t, 12, 4)), lean=30)
    h = int(ease(p) * 8)
    for i in range(h):
        d.rectangle([dx + 20, GY - 236 - i * 12, dx + 130, GY - 226 - i * 12], fill=CREAM if i % 2 else CREAM_D)


def _lightcone(x, y):
    layer = Image.new("RGB", (BW, BH), BLACK)
    ImageDraw.Draw(layer).polygon([(x, y), (x - 260, y + 260), (x + 120, y + 260)], fill=(90, 20, 28))
    return layer.filter(ImageFilter.GaussianBlur(30))


def sc_trophy(img, d, p, t):
    floor(d)
    for k, x in enumerate((BW * 0.15, BW * 0.3, BW * 0.7, BW * 0.85)):
        figure(d, x, GY, 0.85, arms=(150, -150) if p > 0.3 else (20, -20), face="shock" if p > 0.3 else "neutral")
    up = ease(p * 2)
    hc, hr = figure(d, CX, GY, 1.05, arms=(180 * up + 10, -180 * up - 10), face="happy")
    tx, ty = CX, hc[1] - hr - 60 - up * 40
    d.chord([tx - 70, ty - 80, tx + 70, ty + 40], 0, 180, fill=ACCENT)
    d.rectangle([tx - 70, ty - 80, tx + 70, ty - 20], fill=ACCENT)
    d.rectangle([tx - 12, ty + 40, tx + 12, ty + 80], fill=ACCENT)
    d.rectangle([tx - 50, ty + 80, tx + 50, ty + 100], fill=ACCENT)
    if p > 0.3:
        star(d, tx - 120, ty - 60, 22, CREAM, t * 3)
        star(d, tx + 120, ty - 90, 18, CREAM, -t * 3)


def sc_loyal_split(img, d, p, t):
    third = BW // 3
    for k in range(3):
        cx = third * k + third // 2
        ground(d, cx, GY, 300)
        if k == 0:
            figure(d, cx - 50, GY, 0.8, arms=(-120, -90), face="happy")
            figure(d, cx + 50, GY, 0.8, arms=(120, 90), face="happy", hair=BROWN_D)
        elif k == 1:
            rise = ease(p * 1.5)
            figure(d, cx - 70, GY, 0.8, arms=(-130, 20), face="happy")
            figure(d, cx + 60, GY - 0, 0.8, sit=rise < 0.6, arms=(140, -20), face="happy", hair=BROWN_D)
        else:
            figure(d, cx - 50, GY, 0.8, arms=(-170, 20), face="happy")
            figure(d, cx + 50, GY, 0.8, arms=(20, 20), face="happy", hair=BROWN_D)
            d.chord([cx - 170, GY - 560, cx + 170, GY - 400], 180, 360, fill=COPPER)
            d.line([cx, GY - 480, cx, GY - 330], fill=BROWN_D, width=8)
        s = 1 + 0.15 * math.sin(t * 5 + k)
        heart(d, cx, GY - 640, 36 * s, ACCENT)
        if k:
            d.line([third * k, BH * 0.12, third * k, BH], fill=CREAM, width=6)


def sc_door(img, d, p, t):
    floor(d)
    dx = BW * 0.58
    d.rectangle([dx - 150, GY - 500, dx + 150, GY], fill=BROWN_D)
    open_ = ease(p * 1.5)
    d.rectangle([dx - 130, GY - 480, dx + 130, GY], fill=(120, 18, 36))
    img.paste(_add(img, _doorglow(dx, GY - 240, open_)), (0, 0))
    d = ImageDraw.Draw(img)
    pw = 260 * (1 - open_ * 0.8)
    d.polygon([(dx - 130, GY - 480), (dx - 130 + pw, GY - 470 + 20 * open_), (dx - 130 + pw, GY - 10 * open_),
               (dx - 130, GY)], fill=BROWN)
    figure(d, dx + 230, GY, 0.95, arms=(-80, -20), face="happy")
    figure(d, BW * 0.2 + open_ * 120, GY, 0.95, arms=(20, -20), face="happy", hair=BROWN_D,
           legs=(15 * math.sin(t * 7), -15 * math.sin(t * 7)))
    return d


def _doorglow(x, y, k):
    layer = Image.new("RGB", (BW, BH), BLACK)
    ImageDraw.Draw(layer).ellipse([x - 200, y - 260, x + 200, y + 260], fill=tuple(int(c * 0.6 * k) for c in ACCENT))
    return layer.filter(ImageFilter.GaussianBlur(60))


def sc_sofa_blanket(img, d, p, t):
    floor(d)
    sofa(d, CX, GY)
    figure(d, CX - 90, GY - 30, 0.9, sit=True, arms=(60, 20), face="happy", head_dy=bob(t, 6, 3))
    figure(d, CX + 90, GY - 30, 0.9, sit=True, arms=(-60, -20), face="happy", hair=BROWN_D, head_dy=bob(t + 0.3, 6, 3))
    d.rounded_rectangle([CX - 210, GY - 210, CX + 210, GY - 40], radius=40, fill=ACCENT)


def sc_shadow(img, d, p, t):
    cone = Image.new("RGB", (BW, BH), BLACK)
    ImageDraw.Draw(cone).polygon([(CX - 60, 0), (CX + 60, 0), (CX + 300, GY), (CX - 300, GY)], fill=(70, 70, 70))
    img.paste(_add(img, cone.filter(ImageFilter.GaussianBlur(20))), (0, 0))
    d = ImageDraw.Draw(img)
    grow = ease(p * 1.3)
    sh = Image.new("L", (BW, BH), 0)
    sd = ImageDraw.Draw(sh)
    sxs = 0.9 + grow * 0.9
    figure(sd, CX + 260, GY, sxs, body=255, arms=(40, -40))
    img.paste(Image.new("RGB", (BW, BH), (110, 14, 30)), (0, 0), sh)
    d = ImageDraw.Draw(img)
    d.ellipse([CX - 180, GY - 20, CX + 180, GY + 20], fill=GREY)
    figure(d, CX, GY, 0.9, arms=(15, -15), face="neutral")
    return d


def sc_redpen(img, d, p, t):
    floor(d)
    table(d, CX + 80, GY, 520, 210)
    d.polygon([(CX - 60, GY - 222), (CX + 220, GY - 222), (CX + 200, GY - 250), (CX - 40, GY - 250)], fill=CREAM)
    rnd = random.Random(1)
    n = int(ease(p) * 14)
    for i in range(n):
        x = CX - 30 + rnd.random() * 220
        d.line([x, GY - 248, x + 40, GY - 226], fill=ACCENT, width=6)
    chair(d, CX - 250, GY)
    figure(d, CX - 240, GY, 0.95, sit=True, arms=(115 + 25 * math.sin(t * 14), 110), face="sad", lean=30)
    px = CX - 20 + 30 * math.sin(t * 14)
    d.line([px, GY - 250, px - 40, GY - 330], fill=ACCENT, width=14)


def sc_small_x(img, d, p, t):
    floor(d)
    d.rectangle([BW * 0.15, BH * 0.15, BW * 0.85, GY], fill=(26, 26, 26))
    s = 0.4 + 0.6 * ease(p * 2)
    xmark(d, BW * 0.62, GY - 380, 26 * s, ACCENT, 10)
    figure(d, BW * 0.38, GY, 1.05, arms=(60, -150), face="shock", lean=-10)


def sc_overthink(img, d, p, t):
    floor(d)
    sofa(d, BW * 0.38, GY, 560)
    figure(d, BW * 0.38, GY - 30, 0.95, sit=True, arms=(150, 40), face="sad")
    bubble(d, BW * 0.52, GY - 700, 130, 100)
    xmark(d, BW * 0.52, GY - 710, 40 + 6 * math.sin(t * 8), ACCENT, 14)
    # Kalender
    cx, cy = BW * 0.8, GY - 520
    d.rectangle([cx - 120, cy - 130, cx + 120, cy + 130], fill=CREAM)
    d.rectangle([cx - 120, cy - 130, cx + 120, cy - 80], fill=ACCENT)
    f = ImageFont.truetype(F_TITLE, 110)
    d.text((cx, cy + 30), str(1 + int(t * 6) % 31), font=f, fill=BROWN_D, anchor="mm")


def sc_mask(img, d, p, t):
    ground(d, CX, GY, 360)
    hc, hr = figure(d, CX, GY, 1.2, arms=(150, -20), face="sad")
    lower = ease((p - 0.45) * 2.5)
    mx, my = hc[0] + 10 + lower * 140, hc[1] + lower * 160
    d.ellipse([mx - 72, my - 72, mx + 72, my + 72], fill=ACCENT)
    for sx in (-24, 24):
        d.ellipse([mx + sx - 9, my - 25, mx + sx + 9, my - 7], fill=BLACK)
    d.arc([mx - 40, my - 20, mx + 40, my + 40], 20, 160, fill=BLACK, width=10)


def sc_wave_off(img, d, p, t):
    floor(d)
    figure(d, BW * 0.4, GY, 1.0, arms=(170 + 25 * math.sin(t * 10), -15), face="happy")
    figure(d, BW * 0.62, GY, 1.0, shirt=ACCENT, arms=(-80, -20), face="sad", hair=BROWN_D)


def sc_cold(img, d, p, t):
    floor(d)
    rnd = random.Random(7)
    for k in range(18):
        x = rnd.random() * BW
        y = (rnd.random() * BH + t * (80 + rnd.random() * 60)) % (GY)
        snowflake(d, x, y, 14 + rnd.random() * 12, ACCENT, t + k)
    figure(d, CX, GY, 1.05, arms=(10, -10), face="neutral")
    off = ease(p) * 120
    figure(d, BW * 0.22 - off, GY, 0.9, arms=(-60, 60), face="sad", lean=-15 + math.sin(t * 30) * 3)
    figure(d, BW * 0.78 + off, GY, 0.9, arms=(-60, 60), face="sad", hair=BROWN_D, lean=15 + math.sin(t * 30) * 3)


def sc_inner_storm(img, d, p, t):
    ground(d, CX, GY, 380)
    figure(d, CX, GY, 1.3, arms=(25, -25), face="calm")
    k = ease(p * 1.5)
    layer = Image.new("RGB", (BW, BH), BLACK)
    ld = ImageDraw.Draw(layer)
    cy = GY - 300
    for i in range(16):
        a = t * 2.5 + i * math.tau / 16
        r = 30 + (i % 4) * 18
        x, y = CX + math.cos(a) * r * k, cy + math.sin(a) * r * 1.4 * k
        if i % 3 == 0:
            heart(ld, x, y, 14, ACCENT)
        else:
            ld.ellipse([x - 9, y - 9, x + 9, y + 9], fill=ACCENT)
    img.paste(_add(img, layer.filter(ImageFilter.GaussianBlur(12))), (0, 0))
    img.paste(_add(img, layer), (0, 0))


def sc_bridge(img, d, p, t):
    floor(d)
    by = GY - 380
    d.rectangle([BW * 0.08, by, BW * 0.92, by + 40], fill=BROWN)
    for i in range(12):
        d.line([BW * 0.08 + i * 80, by, BW * 0.08 + i * 80, by + 40], fill=BROWN_D, width=4)
    figure(d, CX, GY, 1.0, shirt=ACCENT, arms=(175, -175), face="sad", head_dy=6)
    for k in range(5):
        x = (BW * 0.1 + (k * 200 + t * 120)) % (BW * 0.8) + BW * 0.1
        figure(d, x, by, 0.55, arms=(30, -30), legs=(20 * math.sin(t * 8 + k), -20 * math.sin(t * 8 + k)), face="happy")


def sc_alone_sofa(img, d, p, t):
    floor(d)
    sofa(d, CX, GY)
    figure(d, CX, GY - 30, 0.95, sit=True, arms=(40, 30), face="sad", head_dy=14, lean=12)


def sc_lean(img, d, p, t):
    floor(d)
    sofa(d, CX, GY)
    k = ease(p * 1.4)
    figure(d, CX - 80, GY - 30, 0.95, sit=True, arms=(40, 30), face="calm", lean=20 * k, head_dy=10 * k)
    arrive = ease(p * 3)
    figure(d, CX + 100 + (1 - arrive) * 400, GY - 30, 0.95, sit=arrive > 0.95, scarf=ACCENT, arms=(-70 * k, -20),
           face="happy", hair=BROWN_D)


def sc_crowd(img, d, p, t):
    rnd = random.Random(5)
    for row in range(2):
        for i in range(9):
            x = BW * (0.06 + i * 0.11) + (row * 50)
            jump = abs(math.sin(t * 5 + i * 0.7 + row)) * 40
            figure(d, x, GY - row * 30 - jump, 0.7 - row * 0.05,
                   arms=(160 + rnd.random() * 20, -160 - rnd.random() * 20), face="happy",
                   hat=ACCENT if (i + row) % 3 == 0 else None)
    for k in range(40):
        x = rnd.random() * BW
        y = (rnd.random() * BH + t * 260) % BH
        c = ACCENT if k % 2 else CREAM
        d.rectangle([x, y, x + 14, y + 22], fill=c)


SCENE_FUNCS = {k[3:]: v for k, v in globals().items() if k.startswith("sc_")}


# ---------------------------------------------------------------- Text

def norm(w):
    return "".join(ch for ch in w.lower() if ch.isalpha())


def layout_lines(words, font, maxw, draw):
    lines, cur = [], []
    for i, w in enumerate(words):
        test = " ".join(words[j] for j in cur + [i])
        if cur and draw.textlength(test, font=font) > maxw:
            lines.append(cur)
            cur = [i]
        else:
            cur.append(i)
    if cur:
        lines.append(cur)
    return lines


def main():
    audio, out = sys.argv[1], sys.argv[2]
    dur = audio_duration(audio)
    segs = speech_segments(audio, dur)

    scene_words = [s[0].split() for s in SCENES]
    flat = [w for ws in scene_words for w in ws]
    times = word_timings(flat, segs)
    starts, idx = [], 0
    for ws in scene_words:
        starts.append(times[idx])
        idx += len(ws)
    starts[0] = 0.0
    total = dur + 0.6
    ends = starts[1:] + [total]

    f_title = ImageFont.truetype(F_TITLE, 76)
    f_sub = ImageFont.truetype(F_SUB, 50)
    f_wm = ImageFont.truetype(F_WM, 30)

    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
         "-i", "-", "-i", audio, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
         "-af", "apad", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out],
        stdin=subprocess.PIPE)

    nframes = int(total * FPS)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    for fi in range(nframes):
        tt = fi / FPS
        si = max(i for i in range(len(starts)) if starts[i] <= tt)
        st, en = starts[si], ends[si]
        p = (tt - st) / max(0.01, en - st)

        frame = Image.new("RGB", (W, H), BLACK)
        band = Image.new("RGB", (BW, BH), BLACK)
        bd = ImageDraw.Draw(band)
        SCENE_FUNCS[SCENES[si][1]](band, bd, p, tt - st)
        cw, ch = int(BW / ZOOM), int(BH / ZOOM)
        cx0, cy0 = (BW - cw) // 2, int((BH - ch) * 0.7)
        band = band.crop((cx0, cy0, cx0 + cw, cy0 + ch))
        frame.paste(band.resize((W, BAND_H), Image.LANCZOS), (0, BAND_Y))

        fd = ImageDraw.Draw(frame)
        fd.text((W / 2, 455), TITLE, font=f_title, fill=ACCENT, anchor="mm")

        words = scene_words[si]
        base = sum(len(w) for w in scene_words[:si])
        lines = layout_lines(words, f_sub, W - 120, probe)
        y = 560 if len(lines) == 1 else 540
        for li, line in enumerate(lines[:3]):
            text = " ".join(words[i] for i in line)
            x = W / 2 - fd.textlength(text, font=f_sub) / 2
            for i in line:
                w = words[i]
                spoken = times[base + i] <= tt + 0.02
                if norm(w) == KEYWORD:
                    col = ACCENT if spoken else (70, 14, 24)
                else:
                    col = WHITE if spoken else TEXT_DIM
                fd.text((x, y + li * 60), w, font=f_sub, fill=col, anchor="lm")
                x += fd.textlength(w + " ", font=f_sub)

        fd.text((W / 2, 1400), WATERMARK, font=f_wm, fill=(120, 120, 120), anchor="mm")
        ff.stdin.write(frame.tobytes())
        if fi % 300 == 0:
            print(f"frame {fi}/{nframes}", flush=True)
    ff.stdin.close()
    ff.wait()
    json.dump({"starts": starts, "duration": dur}, open(out + ".timing.json", "w"), indent=1)


if __name__ == "__main__":
    main()
