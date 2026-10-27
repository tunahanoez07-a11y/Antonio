---
name: farbpsychologie-video
description: Erstellt deutsche TikTok-Videos (9:16, ca. 65 s) im Format „Wenn [Farbe] deine Lieblingsfarbe ist, sagt die Psychologie …" – schwarzer Hintergrund, Farbtitel in Anführungszeichen, Wort-für-Wort-Untertitel in Serifenschrift, cremefarbene Strichfiguren mit warmen Braun-Requisiten, komplett in Code mit HyperFrames gebaut. Verwenden, wenn der Creator ein neues Video dieser Nische will (andere Farbe, anderes Thema derselben Machart) oder ein bestehendes ändern möchte.
---

# Farbpsychologie-Videos (Deutsch, HyperFrames)

Alles entsteht im Code: Stimme von ElevenLabs, Wort-Timings von ElevenLabs Scribe, Figuren und Requisiten als SVG, Bewegung mit GSAP, gerendert mit HyperFrames. Videos sind **immer auf Deutsch**.

Vor dem Bauen den HyperFrames-Skill laden (`/hyperframes:hyperframes`), den Vertrag dort einhalten. CLI aus dem Plugin starten:

```bash
HF="node /root/.claude/plugins/cache/hyperframes/hyperframes/<version>/skills/hyperframes/scripts/plugin-cli.mjs"
```

## Das Format (aus den Referenzen von @CortexVault abgeleitet)

**Aufbau des Skripts** (~140–150 Wörter für 65 s):
1. Hook: „Wenn [Farbe] deine Lieblingsfarbe ist, sagt die Psychologie …"
2. „Menschen, die [Farbe] lieben, gelten oft als …" + 4–5 positive Eigenschaften, je ein Satz, direkt mit „du" angesprochen.
3. Wendepunkt: „Aber es gibt auch eine andere Seite."
4. 3–4 Schattenseiten (Overthinking, Gefühle verstecken, Ungeduld, …).
5. Schluss: „Im Grunde …" – ein warmer, zusammenfassender Satz. Kein Call-to-Action.
Weich formulieren („oft", „vielleicht", „manchmal"), damit sich jeder wiedererkennt. Geschlechtsneutral formulieren („die Person", „sofort zur Stelle").

**Look** (1080×1920, Referenz ×1,5):
- Schwarzer Hintergrund. Titel `"FARBE"` in Archivo Black, 76 px, Farbe der Folge, bei y≈400.
- Untertitel bei y≈540: Gelasio Bold 44 px (Georgia-ähnlich, `assets/fonts/gelasio-700.woff2`). Die ganze Phrase ist gesetzt, unsichtbare Wörter halten ihren Platz; ein Wort taucht 0,28 s vor dem Sprechen grau auf (#5b5b5b) und wird beim Sprechen weiß. Der Farbname leuchtet in der Akzentfarbe.
- Bühne: SVG 1080×760 ab y=600, Boden bei SVG-y 600. Figuren skaliert ~1,7.
- Figuren cremefarben (#F6E3C6, Nebenfiguren #E9CFA9), runde Köpfe, Punktaugen, Strichmund; die Hauptfigur trägt die Akzentfarbe (Shirt/Kleid/Umhang). Möbel und Natur in Braun-Tönen, graue Bodenschatten, gelegentlich ein grauer Bodenstreifen, Hängelampen oben.
- Harte Schnitte alle 2–4 s, ein Bild pro Satzteil. Wiederkehrende Motive: Farbe trinken (Hook), Neon-Herz, Sofa mit Denkblase, Tischrunde, Antrag mit Blumen, Spotlight, Menge vs. allein.
- Handle unten klein, grau, kursiv bei y≈1438 (Variable `handle`).

## Ablauf für ein neues Video

1. **Farbe + Skript** auf Deutsch schreiben (Struktur oben). Wenn der Creator nichts vorgibt: Farbe selbst wählen, die noch nicht dran war (siehe `videos/`).
2. **Projekt anlegen:** `$HF init videos/<farbe> --example blank --resolution portrait --non-interactive --skip-skills --skill hyperframes`. Dann aus einem bestehenden Video kopieren: `assets/vendor/gsap.min.js` (der CDN ist in der Sandbox gesperrt, deshalb lokal) und `assets/fonts/gelasio-700.woff2`.
3. **Stimme:** ElevenLabs `creative_generate_speech`, Modell `eleven_multilingual_v2`, Stimme „Clay – Deep Thoughtful Storyteller" (`ed7QNPkbQjEAYxYSuzmM`) oder nach Wunsch. Die Variante nehmen, deren Länge ≤ Zielänge ist; nach `assets/voice.mp3` laden.
4. **Wort-Timings:** lokales Whisper kann HuggingFace nicht erreichen. Stattdessen: `creative_create_asset_upload` → PUT der MP3 → `creative_finalize_asset_upload` (mit flow_id) → `creative_transcribe_audio` (`eleven_scribe_v1`). Wörter als `assets/transcript.json` speichern: `[{"id":"w0","text":"Wenn","start":0.1,"end":0.24}, …]`. Schreibweisen aus dem Skript übernehmen (z. B. „Rot-Liebhaber").
5. **Szenen planen:** pro Satz eine Szene (Schnitt am ersten Wort), innerhalb einer Szene bei Bedarf 2 Einstellungen mit `cut()`. Zeiten aus den Wort-Timings.
6. **`build.py`** im Projekt schreiben (Vorlage: `videos/rot/build.py`): importiert `lib/figlib.py` (Figuren + Requisiten) und `lib/pagelib.py` (schreibt `index.html`, `compositions/sNN.html`, `compositions/captions.html`). `python3 build.py` erzeugt das Projekt neu – nie die HTML-Dateien von Hand ändern, sondern `build.py`.
7. **Prüfen:** `$HF check` (Fehler beheben), `$HF snapshot --at <je Einstellung eine Zeit> --no-end -o <dir>` und die Bilder ansehen: Figuren dürfen die Untertitel nicht berühren (Bühne oberhalb SVG-y≈90 frei lassen), Posen müssen lesbar sein.
8. **Rendern:** `$HF render -o renders/<farbe>-farbpsychologie.mp4 -f 30`.

## Figuren-Rig (lib/figlib.py)

`fig(id, x, y, s, pose=…, shirt=…, dress=…, hair="bob|pony|short", mouth=…, brow=…, hand_r=…, hand_l=…, back=…)`.
Gelenkwinkel in Grad, 0 = hängt gerade nach unten, positiv = im Uhrzeigersinn (Ende wandert nach links). Gelenke: `torso head ua_l la_l ua_r la_r ul_l ll_l ul_r ll_r`, dazu `pelvis: (dy, rot)` (positives dy = tiefer, z. B. Knien 55, Sitzen 22).
Bewährte Posen: Arm hoch `ua_l 150 / ua_r -150`; Arme verschränkt `ua_l 12, la_l -98, ua_r -12, la_r 98`; Fäuste in die Hüften `ua_l 38, la_l -115`; Hand vors Gesicht `ua_r -160, la_r -97`; Hände an den Kopf `ua_l 120, la_l 127, ua_r -120, la_r -127`; Knien `pelvis 55, ul_l -95, ll_l 95, ul_r 0, ll_r 92`; Zeigen nach links `ua_l 95`.

In JS (in jeder Szene vorhanden): `P(id, {…pose, root:[x,y,rot,s], mouth, brow, eyes}, t, dauer, ease)`, `blink(id, t)`, `walk(id, x0, x1, y, s, t0, t1, schritt, amplitude, neigung)`, `T(selector, t, vars, dauer)`, `cut(ausblenden, einblenden, t)`. Münder: `smile grin flat frown open shout`; Brauen: `none angry sad up`.
Requisiten: `sofa table chair lamp tree floor shadow neon_heart thought bouquet glass bottle speech_zigzag broken_heart spotlight clock snail boulder mask_disc`.

Regeln: Startzustände stehen im Markup (keine `tl.set(…, 0)` zum Verstecken – stattdessen `opacity="0"` im SVG). Zwei Tweens auf dieselbe Eigenschaft dürfen sich nicht überlappen. Kein `Math.random()`.

## Ton

Nur Sprecherstimme. Musik kann der eingeschränkte ElevenLabs-Connector nicht erzeugen; wenn der Creator eine Musikdatei liefert, als `<audio id="music">` mit Lautstärke ~0,12 einbauen (`write_project(..., music="assets/music.mp3")`).
