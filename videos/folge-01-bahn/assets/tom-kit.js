/* Tom-Kit: Figuren, Requisiten und Animations-Helfer im Stil der Referenzvideos.
   Deterministisch: keine Zufallswerte, alles hängt nur von der Timeline-Zeit ab. */
(function () {
  const INK = "#1E1E1E";
  const BAG = "#A8A29A";
  const CUP = "#5A3A22";
  const SLEEVE = "#C9A26B";

  function eyes(look, shut) {
    const dx = look === "right" ? 14 : look === "left" ? -14 : 0;
    const one = (cx) => {
      const lid = shut
        ? `<path d="M${cx - 19} 92 Q${cx} 100 ${cx + 19} 92" fill="none" stroke="${INK}" stroke-width="7" stroke-linecap="round"/>`
        : `<line x1="${cx - 18}" y1="79" x2="${cx + 16}" y2="79" stroke="${INK}" stroke-width="7" stroke-linecap="round"/>` +
          `<circle cx="${cx + dx * 0.4}" cy="89" r="8" fill="${INK}"/>`;
      return lid + `<path d="M${cx - 16} 107 Q${cx} 115 ${cx + 16} 107" fill="none" stroke="${BAG}" stroke-width="4.5" stroke-linecap="round"/>`;
    };
    return `<g class="tk-eyes-open">${one(92 + dx)}${one(148 + dx)}</g>` +
      `<g class="tk-eyes-shut" style="opacity:0">${eyesShut(dx)}</g>`;
  }
  function eyesShut(dx) {
    const one = (cx) =>
      `<path d="M${cx - 18} 90 Q${cx} 97 ${cx + 18} 90" fill="none" stroke="${INK}" stroke-width="7" stroke-linecap="round"/>` +
      `<path d="M${cx - 16} 107 Q${cx} 115 ${cx + 16} 107" fill="none" stroke="${BAG}" stroke-width="4.5" stroke-linecap="round"/>`;
    return one(92 + dx) + one(148 + dx);
  }
  function mouths(look, open) {
    const dx = look === "right" ? 10 : look === "left" ? -10 : 0;
    return `<line class="tk-mouth-closed" x1="${103 + dx}" y1="136" x2="${137 + dx}" y2="136" stroke="${INK}" stroke-width="7" stroke-linecap="round" style="opacity:${open ? 0 : 1}"/>` +
      `<ellipse class="tk-mouth-open" cx="${120 + dx}" cy="138" rx="15" ry="17" fill="${INK}" style="opacity:${open ? 1 : 0}"/>`;
  }
  function head(look, open, extra) {
    return `<circle cx="120" cy="95" r="78" fill="#fff" stroke="${INK}" stroke-width="10"/>` +
      eyes(look) + mouths(look, open) + (extra || "");
  }
  function cup(label) {
    return `<g class="tk-cup">
      <path class="tk-steam" d="M114 206 q-8 -12 0 -24 q8 -12 0 -24" fill="none" stroke="${BAG}" stroke-width="3" opacity=".7"/>
      <path class="tk-steam" d="M132 204 q-8 -10 0 -20 q8 -10 0 -20" fill="none" stroke="${BAG}" stroke-width="3" opacity=".5"/>
      <rect x="92" y="214" width="66" height="16" rx="5" fill="${INK}"/>
      <path d="M97 229 L153 229 L146 322 L104 322 Z" fill="${CUP}" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>
      <path d="M101 266 L149 266 L147 292 L103 292 Z" fill="${SLEEVE}"/>
      ${label ? `<text data-layout-ignore x="125" y="255" text-anchor="middle" font-family="Inter" font-weight="900" font-size="17" fill="#F2EEE6">${label}</text>` : ""}
    </g>`;
  }
  function legs(stride) {
    const s = stride || 0;
    return `<g class="tk-leg-l" style="transform-origin:120px 330px"><line x1="120" y1="330" x2="${94 - s}" y2="452" stroke="${INK}" stroke-width="10" stroke-linecap="round"/></g>` +
      `<g class="tk-leg-r" style="transform-origin:120px 330px"><line x1="120" y1="330" x2="${148 + s}" y2="452" stroke="${INK}" stroke-width="10" stroke-linecap="round"/></g>`;
  }

  // Tom: großer runder Kopf, müde Augen, hält immer seinen Kaffee ("TIM" steht drauf).
  function tom(o) {
    const look = o.look || "front";
    return `<svg viewBox="0 0 240 460" width="100%" style="overflow:visible;display:block">
      <line x1="120" y1="172" x2="120" y2="332" stroke="${INK}" stroke-width="10" stroke-linecap="round"/>
      ${legs(o.stride ? 10 : 0)}
      ${o.nocup ? "" : cup(o.label === undefined ? "TIM" : o.label)}
      ${o.nocup
        ? `<path d="M120 204 L92 300" stroke="${INK}" stroke-width="10" stroke-linecap="round" fill="none"/><path d="M120 204 L150 298" stroke="${INK}" stroke-width="10" stroke-linecap="round" fill="none"/>`
        : `<path d="M120 200 L82 250 L102 270" stroke="${INK}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"/>`}
      <g class="tk-head" style="transform-origin:120px 170px">${head(look, o.mouth === "open")}</g>
    </svg>`;
  }

  // Nebenfigur ohne Kaffee. hat: "conductor" | "cap" | "glasses" | undefined
  function guy(o) {
    const look = o.look || "front";
    const shrug = o.pose === "shrug";
    const arms = shrug
      ? `<path d="M120 206 L78 236 L60 190" stroke="${INK}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
         <path d="M120 206 L162 236 L180 190" stroke="${INK}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"/>`
      : `<path d="M120 204 L90 298" stroke="${INK}" stroke-width="10" stroke-linecap="round" fill="none"/>
         <path d="M120 204 L152 296" stroke="${INK}" stroke-width="10" stroke-linecap="round" fill="none"/>`;
    let extra = "";
    if (o.hat === "conductor") {
      extra = `<path d="M50 52 Q120 -6 190 52 L186 66 L54 66 Z" fill="#26355E" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/>
        <rect x="54" y="52" width="132" height="14" fill="#C8102E"/>
        <path d="M40 66 L200 66" stroke="${INK}" stroke-width="9" stroke-linecap="round"/>`;
    } else if (o.hat === "cap") {
      extra = `<path d="M54 56 Q120 0 186 56 Z" fill="${o.color || "#7A8FB3"}" stroke="${INK}" stroke-width="7"/><path d="M150 56 L214 60" stroke="${INK}" stroke-width="9" stroke-linecap="round"/>`;
    } else if (o.hat === "glasses") {
      extra = `<circle cx="92" cy="93" r="17" fill="none" stroke="${INK}" stroke-width="5"/><circle cx="148" cy="93" r="17" fill="none" stroke="${INK}" stroke-width="5"/><line x1="109" y1="93" x2="131" y2="93" stroke="${INK}" stroke-width="5"/>`;
    }
    const body = o.color && o.hat !== "cap"
      ? `<path d="M96 186 L144 186 L150 300 L90 300 Z" fill="${o.color}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>`
      : "";
    return `<svg viewBox="0 0 240 460" width="100%" style="overflow:visible;display:block">
      <line x1="120" y1="172" x2="120" y2="332" stroke="${INK}" stroke-width="10" stroke-linecap="round"/>
      ${legs(o.stride ? 10 : 0)}${body}${arms}
      <g class="tk-head" style="transform-origin:120px 170px">${head(look, o.mouth === "open", extra)}</g>
    </svg>`;
  }

  function train() {
    let windows = "";
    for (let i = 0; i < 9; i++) windows += `<rect x="${360 + i * 120}" y="70" width="88" height="56" rx="10" fill="#2E2E2E"/>`;
    return `<svg viewBox="0 0 1500 260" width="100%" style="display:block">
      <path d="M40 210 L40 120 Q60 40 200 34 L1480 34 L1480 210 Z" fill="#FFFFFF" stroke="${INK}" stroke-width="8" stroke-linejoin="round"/>
      <path d="M70 92 Q110 56 210 52 L250 52 L250 120 L60 120 Z" fill="#2E2E2E"/>
      ${windows}
      <rect x="44" y="150" width="1436" height="18" fill="#C8102E"/>
      <text x="300" y="196" font-family="Inter" font-weight="900" font-size="30" fill="${INK}">ICE</text>
      <circle cx="260" cy="226" r="20" fill="${INK}"/><circle cx="460" cy="226" r="20" fill="${INK}"/>
      <circle cx="1100" cy="226" r="20" fill="${INK}"/><circle cx="1300" cy="226" r="20" fill="${INK}"/>
    </svg>`;
  }

  function bike() {
    return `<svg viewBox="0 0 300 190" width="100%" style="display:block;overflow:visible">
      <circle cx="62" cy="128" r="54" fill="none" stroke="${INK}" stroke-width="8"/>
      <circle cx="238" cy="128" r="54" fill="none" stroke="${INK}" stroke-width="8"/>
      <path d="M62 128 L120 60 L210 60 L238 128 M120 60 L150 128 L210 60 M150 128 L62 128" fill="none" stroke="#3E7D4F" stroke-width="9" stroke-linejoin="round"/>
      <path d="M108 44 L140 44 M205 60 L200 30 L228 26" fill="none" stroke="${INK}" stroke-width="8" stroke-linecap="round"/>
    </svg>`;
  }

  function speaker() {
    return `<svg viewBox="0 0 200 160" width="100%" style="display:block;overflow:visible">
      <rect x="8" y="58" width="44" height="44" rx="6" fill="#9A9A9A" stroke="${INK}" stroke-width="7"/>
      <path d="M52 58 L130 14 L130 146 L52 102 Z" fill="#D9D4CB" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/>
      <path d="M150 50 Q170 80 150 110 M168 34 Q198 80 168 126" fill="none" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>
    </svg>`;
  }

  // Kanal-Stempel am Ende jeder Folge.
  function stamp(top, bottom) {
    return `<svg viewBox="0 0 400 400" width="100%" style="display:block">
      <defs>
        <path id="tk-arc-top" d="M52 200 A148 148 0 0 1 348 200"/>
        <path id="tk-arc-bot" d="M38 200 A162 162 0 0 0 362 200"/>
      </defs>
      <g fill="none" stroke="#D9473A">
        <circle cx="200" cy="200" r="186" stroke-width="10"/>
        <circle cx="200" cy="200" r="122" stroke-width="4"/>
      </g>
      <text font-family="Inter" font-weight="900" font-size="31" fill="#D9473A" letter-spacing="2"><textPath href="#tk-arc-top" startOffset="50%" text-anchor="middle">${top}</textPath></text>
      <text font-family="Inter" font-weight="900" font-size="30" fill="#D9473A" letter-spacing="4"><textPath href="#tk-arc-bot" startOffset="50%" text-anchor="middle">${bottom}</textPath></text>
      <g stroke="#D9473A" stroke-width="9" fill="none" stroke-linejoin="round">
        <rect x="160" y="140" width="80" height="18" rx="4"/>
        <path d="M166 158 L234 158 L226 266 L174 266 Z"/>
        <path d="M170 198 L230 198 M172 226 L228 226"/>
      </g>
      <text x="40" y="212" font-family="Inter" font-weight="900" font-size="34" fill="#D9473A">★</text>
      <text x="334" y="212" font-family="Inter" font-weight="900" font-size="34" fill="#D9473A">★</text>
    </svg>`;
  }

  function cupOnly(o) {
    return `<svg viewBox="86 150 78 178" width="100%" style="display:block;overflow:visible">${cup(o.label === undefined ? "TIM" : o.label)}</svg>`;
  }

  const builders = { tom, guy, train, bike, speaker, cup: cupOnly };

  // Füllt alle .tk-Platzhalter in einer Szene mit ihrer Zeichnung.
  function mount(root) {
    root.querySelectorAll(".tk").forEach((el) => {
      const d = el.dataset;
      if (d.kind === "stamp") { el.innerHTML = stamp(d.top || "DOPPELTER STRESSO", d.bottom || "WIE IMMER"); return; }
      const b = builders[d.kind];
      if (b) el.innerHTML = b({ look: d.look, mouth: d.mouth, hat: d.hat, color: d.color, pose: d.pose, label: d.label, nocup: d.nocup === "1", stride: d.stride === "1" });
    });
  }

  function clipWindow(el) {
    const shot = el.closest(".clip");
    if (!shot) return [0, 1e9];
    const s = parseFloat(shot.dataset.start || "0");
    return [s, s + parseFloat(shot.dataset.duration || "0")];
  }

  // Mund auf/zu im Takt der Voiceover-Wörter (globale Zeiten) für jedes Tom mit data-talk.
  function lipSync(tl, root, sceneStart) {
    const words = (window.TOM_WORDS || []).filter((w) => w.type === "word" && !/^\[/.test(w.text));
    root.querySelectorAll('.tk[data-kind="tom"][data-talk]').forEach((el) => {
      const [s, e] = clipWindow(el);
      const from = el.dataset.talkFrom ? parseFloat(el.dataset.talkFrom) : s;
      const to = el.dataset.talkTo ? parseFloat(el.dataset.talkTo) : e;
      const open = el.querySelector(".tk-mouth-open");
      const closed = el.querySelector(".tk-mouth-closed");
      words.forEach((w) => {
        const t = w.start - sceneStart;
        if (t < from || t >= to - 0.05) return;
        const len = Math.max(0.1, Math.min(0.22, (w.end - w.start) * 0.7));
        tl.set(open, { opacity: 1 }, t);
        tl.set(closed, { opacity: 0 }, t);
        tl.set(open, { opacity: 0 }, t + len);
        tl.set(closed, { opacity: 1 }, t + len);
      });
    });
  }

  // Blinzeln in festem Rhythmus.
  function blink(tl, root) {
    root.querySelectorAll('.tk[data-kind="tom"], .tk[data-kind="guy"]').forEach((el, i) => {
      const [s, e] = clipWindow(el);
      const openEyes = el.querySelector(".tk-eyes-open");
      const shut = el.querySelector(".tk-eyes-shut");
      if (el.dataset.eyes === "shut") { tl.set(openEyes, { opacity: 0 }, s); tl.set(shut, { opacity: 1 }, s); return; }
      for (let t = s + 0.9 + (i % 3) * 0.37; t < e - 0.2; t += 2.7) {
        tl.set(openEyes, { opacity: 0 }, t); tl.set(shut, { opacity: 1 }, t);
        tl.set(openEyes, { opacity: 1 }, t + 0.12); tl.set(shut, { opacity: 0 }, t + 0.12);
      }
    });
  }

  // Lauf-/Geh-Zyklus der Beine (data-walk = Dauer eines Schritts in s).
  function walk(tl, root) {
    root.querySelectorAll(".tk[data-walk]").forEach((el, i) => {
      const [s, e] = clipWindow(el);
      const step = parseFloat(el.dataset.walk);
      const amp = parseFloat(el.dataset.amp || "16");
      const l = el.querySelector(".tk-leg-l"), r = el.querySelector(".tk-leg-r");
      const n = Math.max(1, Math.floor((e - s) / step));
      const off = (i % 2) * step * 0.5;
      tl.fromTo(l, { rotation: -amp, svgOrigin: "120 330" }, { rotation: amp, duration: step, ease: "sine.inOut", yoyo: true, repeat: n - 1 }, s + off);
      tl.fromTo(r, { rotation: amp, svgOrigin: "120 330" }, { rotation: -amp, duration: step, ease: "sine.inOut", yoyo: true, repeat: n - 1 }, s + off);
      const head = el.querySelector(".tk-head");
      if (head) tl.fromTo(head, { y: 0 }, { y: -6, duration: step / 2, ease: "sine.inOut", yoyo: true, repeat: n * 2 - 1 }, s + off);
    });
  }

  // Standard-Shot-Bewegung: leichter Push-in der Kamera + Pop-ins für [data-pop="delay"].
  function shots(tl, root) {
    root.querySelectorAll(".shot").forEach((shot) => {
      const s = parseFloat(shot.dataset.start), d = parseFloat(shot.dataset.duration);
      const cam = shot.querySelector(".cam");
      const zoom = parseFloat(shot.dataset.zoom || "1.04");
      if (cam) tl.fromTo(cam, { scale: 1 }, { scale: zoom, duration: d, ease: "none" }, s);
      shot.querySelectorAll("[data-pop]").forEach((el) => {
        const at = s + parseFloat(el.dataset.pop || "0");
        tl.fromTo(el, { scale: 0.82, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.22, ease: "back.out(2.2)" }, at);
      });
      shot.querySelectorAll("[data-slam]").forEach((el) => {
        const at = s + parseFloat(el.dataset.slam || "0");
        tl.fromTo(el, { scale: 2.2, opacity: 0, rotation: -18 }, { scale: 1, opacity: 1, rotation: -12, duration: 0.18, ease: "power4.in" }, at);
      });
    });
  }

  // Alles in einem Aufruf: zeichnen + animieren.
  function setup(tl, root, sceneStart) {
    mount(root);
    shots(tl, root);
    lipSync(tl, root, sceneStart);
    blink(tl, root);
    walk(tl, root);
  }

  window.TomKit = { mount, lipSync, blink, walk, shots, setup, svg: { tom, guy, train, bike, speaker, stamp } };
})();
