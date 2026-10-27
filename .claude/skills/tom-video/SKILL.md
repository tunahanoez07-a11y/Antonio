---
name: tom-video
description: Erstellt ein komplettes TikTok-Video (9:16, deutsch) mit der Strichmännchen-Figur Tom im Stil der Referenz-Creator – Skript, deutsche Stimme (ElevenLabs), Karaoke-Untertitel, Animation und Render mit HyperFrames. Verwenden, wenn der User ein neues Tom-Video, eine neue Folge oder ein Video zu einem Thema in dieser Nische möchte.
---

# Tom-Video (HyperFrames)

Jedes Video ist **auf Deutsch**, wird **komplett im Code** mit HyperFrames gebaut und sieht aus wie die Referenzvideos (siehe `STYLE_GUIDE.md` im Repo-Root). Hauptfigur ist **Tom**. Folge 1 (`videos/folge-01-bahn/`) ist die Referenz-Implementierung: im Zweifel dort nachsehen und kopieren.

Vor dem Bauen den HyperFrames-Skill lesen (`/hyperframes`, Contract + `references/types/vertical.md`, `references/captions.md`).

## Format

- 1080×1920, 30 fps. Länge nach Vorgabe des Users (Standard ~60 s). Die Root-`data-duration` = Wunschlänge; der Voiceover endet ~2–3 s vorher, der Rest ist das Outro.
- **Hook in Sekunde 0**: Tom steht schon im Bild, der erste Satz nennt die Situation.
- Neuer Shot alle **1–3 s**, im Takt der Sätze. Wechsel zwischen Tom-Totale, Tom-Close-up/Extrem-Close-up und UI-Vollbild (Karte, Handy, Anzeige).
- Text-Inhalte zwischen y=560 und y=1330, Untertitel bei y≈430 (oberes Drittel), unter 1330 nur Figuren und Deko.

## Figur & Running Gags

- **Tom**: großer runder Kopf, dicke schwarze Kontur, müde Augen mit grauen Augenringen, hält **immer** einen braunen To-go-Becher. Auf dem Becher steht **„TIM“** – niemand schreibt seinen Namen richtig. Den Gag in jeder Folge mindestens einmal ausspielen (Becher, Ticket, Überweisung, E-Mail, Durchsage).
- Erzählstil: Ich-Erzähler, trocken, resigniert, kurze Sätze, konkrete Zahlen als Pointen.
- Outro: resignierter Schlusssatz („Naja.“), Tom geht nach rechts aus dem Bild, dann knallt der Kanal-Stempel **„DOPPELTER STRESSO – WIE IMMER“** rein (`data-kind="stamp"`).
- Nebenfiguren: `guy` mit `data-hat="conductor|cap|glasses|hair"` (`hair` = lange Haare + Dutt, Farbe über `data-hair`), `data-color` für Kleidung, `data-pose="shrug"`.
- Gesichter: `data-mouth="open|smile"` (z. B. Lächeln aufs Passfoto), `data-eyes="shut"` (Seufzer). Becher einzeln: `data-kind="cup" data-label="KAI"`.

## Dramaturgie (für ~60 s, ca. 120–130 Wörter Sprechtext)

1. **Hook** (0–3 s): Situation in einem Satz.
2. **Setup** (3–15 s): Ausgangslage + erster kleiner Widerspruch.
3. **Eskalation** (15–45 s): 5–8 Beats, jeder absurder, mit konkreten Zahlen (+5 → +15 → +40, 6 Seiten, 7,40 €).
4. **Twist** (45–55 s): das System schlägt zurück, meist mit dem TIM-Gag.
5. **Outro** (letzte 5–7 s): Schlusssatz, Abgang, Stempel.

## Workflow

### 1. Skript
Thema vom User (sonst einen deutschen Alltagsfrust vorschlagen: Bürokratie, Behörden, Bahn, Vermieter, Paketdienst, Arzttermin, Steuererklärung …). Skript auf Deutsch schreiben, Zahlen ausschreiben („sieben Euro vierzig“), damit die Stimme sie richtig spricht. Vor dem Seufzer `[sighs]` einfügen.

### 2. Stimme (ElevenLabs-Connector) – lustlos wie die Referenz
Ziel (gemessen an den Referenzvideos): tiefe Stimme ~106 Hz, sehr flache Melodie (~1,9 Halbtöne Streuung), wenig Dynamik. Siehe `STYLE_GUIDE.md` Abschnitt 9.
- `creative_create_flow` → `creative_generate_speech` mit `model_id: eleven_v4`, Stimme **Clay** `voice_id: ed7QNPkbQjEAYxYSuzmM`, **`generations_count: 1`** (User-Wunsch: nur ein Take). Skript beginnt mit **`[tired] [bored]`**; Seufzer als `[sighs]`. Zahlen/Uhrzeiten in Ziffern schreiben („14:32 Uhr“, „8 und 18 Uhr“) – v4 spricht sie richtig und die Untertitel zeigen Ziffern. Kosten ~700 Credits pro Minute; dem User am Ende nennen. (Folge 1–2 nutzten noch Dennis `bGkjVHUyQ9rRhorWJufM` – zu hell/melodisch.)
- Status pollen, `content_url` per `curl` nach `assets/voiceover-raw.mp3` laden.
- **Melodie glätten (kostenlos):** `pip install praat-parselmouth` (falls nötig), dann
  `python3 ../../.claude/skills/tom-video/tools/flatten_voice.py assets/voiceover-raw.mp3 assets/voiceover-flat.mp3 --keep 0.55 --target 106`
  – PSOLA, Dauer bleibt exakt gleich. Prüfen: `python3 ../../.claude/skills/tom-video/tools/voicestats.py assets/voiceover-flat.mp3`.
- Wort-Timings: `creative_transcribe_audio` (`eleven_scribe_v1`, `connect_from` = die TTS-Node-ID aus dem Generate-Ergebnis) → `words_download_url` nach `assets/words-raw.json` laden. Tags wie `[tired]` tauchen als Wörter auf – `build_captions.py` filtert sie.
- **Länge anpassen:** `PAUSES` in `add_pauses.py` setzen (Kunstpausen 0,5–1,0 s direkt nach Pointen, Schnittpunkte in Wortlücken) und `python3 add_pauses.py assets/voiceover-flat.mp3` → schreibt `assets/voiceover.mp3` + `assets/words.json`. Ohne Pausen: `PAUSES = []`.
- Hinweis: Lokale Transkription (whisper) und Kokoro-TTS funktionieren hier nicht (HuggingFace gesperrt, Kokoro kann kein Deutsch).

### 3. Projekt anlegen
```bash
cd videos && npx hyperframes init folge-XX-thema && cd folge-XX-thema
cp -r ../../.claude/skills/tom-video/template/. .
```
Das Template bringt `assets/tom-kit.js`, `assets/gsap.min.js` (lokal, weil das CDN hier blockiert ist), Marker-Schrift, Sound-Effekte, `build_captions.py`, ein `index.html`-Gerüst und eine Beispielszene mit.

### 4. Untertitel
```bash
python3 build_captions.py .
```
Erzeugt `assets/words.js` (für Lippen-Sync) und `compositions/captions.html` (Karaoke: Wort erscheint orange, wird schwarz, sobald das nächste kommt; max. 3 Wörter pro Gruppe).

### 5. Shotliste → Szenen
- Shotliste aus den Wort-Timings ableiten: jeder Shot beginnt auf einem Wort, Pointen-Elemente poppen **genau auf ihrem Wort** auf.
- 5–7 Szenen-Dateien in `compositions/` (je ~8–12 s), jede mit 3–5 Shots. Szenen-Host-IDs in `index.html` = `data-composition-id` der Szene = Timeline-Key.
- Shot-Aufbau (siehe `template/compositions/szene-beispiel.html`):
  ```html
  <div id="sX-a" class="shot clip" data-start="0" data-duration="2.0" data-track-index="0">
    <div class="cam"> … Inhalte absolut positioniert … </div>
  </div>
  ```
  Am Ende des Scripts: `TomKit.setup(tl, root, SZENEN_START_GLOBAL);` – das zeichnet alle `.tk`-Figuren, macht den Kamera-Push-in, Pop-ins (`data-pop="0.4"` = Sekunden ab Shot-Start), Stempel-Slams (`data-slam`), Lippen-Sync (`data-talk`, optional `data-talk-from`/`data-talk-to` in Szenenzeit), Blinzeln und Laufzyklen (`data-walk="0.2" data-amp="28"`).
- Figurgrößen (Tom, `width`): Totale 240–300 px, Halbtotale 420 px (left 330, top 760, Boden bei 1562), Close-up 640–760 px, Extrem-Close-up 1000–1100 px (left −10, top 640).
- UI-Bausteine aus `index.html`: `.card` + `.card-head` (+ `.dot`) + `.card-body`, `.pill`, `.chip`, `.sign`, `.board`, `.bubble`, `.marker` (Handschrift), `.ground`. Handy-Mockup siehe Folge 1 (`#s1-phone`).
- Weitere Kit-Elemente: `data-kind="train|bike|speaker|cup|stamp"`. Deko-Wackeln: `data-wobble="10"` (z. B. Stinkwolken `.stink`, Gedankenblasen).
- Ideen aus den Referenzen (STYLE_GUIDE Abschnitt 8): Mindmap-Shot, steigernde Requisite über die Folge (z. B. Stinkwolken 1 → 2 → 3), Anzeigen/Akkus als Pointe, Callbacks auf frühere Folgen (Ausweis „TIM“ aus Folge 2).

### 6. Sound
Bundled SFX (`assets/sfx/`): `pop` (UI erscheint), `ping` (Bestätigung/Betrag), `notification` (Nachricht/Durchsage), `error` (schlechte Nachricht), `whoosh-short` (Bewegung), `impact-bass-1` (Stempel). Lautstärke 0.25–0.4, als `<audio class="clip" id=…>` in `index.html`. Keine Musik (wie Referenzen).

### 7. Prüfen & Rendern
```bash
npx hyperframes check --json      # alle errors beheben
npx hyperframes snapshot --at …   # mind. ein Frame pro Shot ansehen
npx hyperframes render --quality delivery --output out/tom-folge-XX.mp4
```
Bekannte, akzeptierte Warnungen: Kontrast des orangen Karaoke-Worts (Referenz-Look), `timeline_track_too_dense` für die Untertitel.
Typische Fehler: Beine drehen sich falsch → Rotation im SVG immer mit `svgOrigin` (macht das Kit); ein per `fromTo` eingeblendetes Element braucht `opacity: 1` auch in den Ziel-Werten; gestapelte Karten brauchen `data-layout-allow-overlap`.

### 8. Abliefern
MP4 nach `videos/folge-XX-thema/out/` rendern, committen (ohne `.hyperframes/`), pushen und dem User das Video schicken.
