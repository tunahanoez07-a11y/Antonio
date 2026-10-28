# Serie: Geburtsmonate

Gleiche Formel wie die Farb-Referenzen (@CortexVault), übertragen auf Geburtsmonate.
Jeder Monat bekommt **eine Akzentfarbe** (seinen Geburtsstein). Die Farbe übernimmt die Rolle,
die in den Referenzen die Lieblingsfarbe hatte: im Titel, im Monatswort der Untertitel und als einziger Farbakzent in den Animationen.

| Monat | Geburtsstein | Akzentfarbe | Hex |
|---|---|---|---|
| Januar | Granat | Granatrot | `#E0213F` |
| Februar | Amethyst | Violett | `#A63CF0` |
| März | Aquamarin | Hellaqua | `#4FD8E0` |
| April | Diamant | Eisweiß-Glitzer | `#E8F4FF` |
| Mai | Smaragd | Smaragdgrün | `#1FD67A` |
| Juni | Perle | Perlrosa | `#F3D6E4` |
| Juli | Rubin | Rubinrot | `#FF1F4B` |
| August | Peridot | Limettengrün | `#B6E83A` |
| September | Saphir | Saphirblau | `#2F6BFF` |
| Oktober | Opal | Opal-Pink | `#FF7AC8` |
| November | Topas | Goldorange | `#FFA62B` |
| Dezember | Türkis | Türkis | `#20D3C2` |

## Fixes Layout (jedes Video)
- 1080×1920 (9:16), 30 fps, Länge 60–75 s
- Hintergrund komplett schwarz `#000000`
- **Titel** oben bei ~23 % Bildhöhe: `"JANUAR"`, Arial Black / Montserrat Black, Akzentfarbe, bleibt stehen
- **Untertitel** bei ~31 %: weiß, fette Serifenschrift (Georgia Bold / Playfair), zentriert, max. 2 Zeilen,
  Wort-für-Wort-Karaoke (kommende Wörter dunkelgrau `#3A3A3A`, aktives Wort weiß),
  das Monatswort immer in der Akzentfarbe
- **Animation**: 16:9-Streifen, mittig bei ~35–65 % Bildhöhe
- **Wasserzeichen** `@DEINNAME` klein, grau, kursiv, bei ~75 %
- Szenenwechsel alle 2–3 s (harter Schnitt)

## Fixe Dramaturgie
1. Hook: „Wenn du im [Monat] geboren bist …“ (Figur trinkt die Akzentfarbe und färbt sich ein)
2. „Es heißt, dass du …“: 2–3 Stärken
3. „Menschen, die im [Monat] geboren sind, gelten als …“: soziale Seite
4. Twist: „Aber es gibt eine Schattenseite …“: 2–3 Schwächen
5. „Im Grunde bist du …“: emotionale Zusammenfassung
6. CTA: „Wenn du im [Monat] geboren bist, schreib ‚[Monat]‘ in die Kommentare.“

## Veo-Basis-Prompt (vor jeden Szenen-Prompt setzen)
```
Flat 2D vector animation, minimalist explainer style. Pure black background.
Simple faceless cream-beige human figures (#F2DFC4) with round heads and smooth limbs,
standing on a soft dark-grey shadow ellipse. Props and furniture in warm brown and copper tones only.
The ONLY saturated color in the scene is {AKZENTFARBE} ({HEX}), used on {ELEMENT}.
Smooth, simple, slightly bouncy character motion, static camera, no text, no letters, no logos, 16:9.
```
