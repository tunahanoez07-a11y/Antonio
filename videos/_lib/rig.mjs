// Shared drawing rig for the "Ein Leben ohne …" series.
// Everything returns SVG/HTML strings; scenes are generated into compositions/*.html.

export const C = {
  line: "#4a4752",
  skin: "#f4f3f6",
  skinShade: "#d5d3dc",
  eye: "#2b2930",
  mouth: "#5b3b44",
  shirt: "#6e86b3",
  pants: "#7d8a55",
  shoe: "#6e4c35",
  title: "#7a6f8e",
  card: "#6e6878",
};

export const defs = `
<defs>
  <radialGradient id="headGrad" cx="0.62" cy="0.32" r="0.8">
    <stop offset="0" stop-color="#fdfdfe"/>
    <stop offset="0.55" stop-color="${C.skin}"/>
    <stop offset="1" stop-color="${C.skinShade}"/>
  </radialGradient>
  <linearGradient id="floorShade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#000" stop-opacity="0.06"/>
    <stop offset="1" stop-color="#000" stop-opacity="0"/>
  </linearGradient>
</defs>`;

// A two-segment limb drawn as an outlined white tube.
const tube = (d, w = 15) =>
  `<path d="${d}" fill="none" stroke="${C.line}" stroke-width="${w + 7}" stroke-linecap="round" stroke-linejoin="round"/>` +
  `<path d="${d}" fill="none" stroke="${C.skin}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;

const hand = (x, y) =>
  `<circle cx="${x}" cy="${y}" r="11" fill="${C.skin}" stroke="${C.line}" stroke-width="3.5"/>`;

/**
 * A character standing with its feet at (x, y).
 * opts: id, x, y, s (scale), shirt, pants, hair ("none"|"long"|"bun"|"bob"), hairColor,
 *       glasses, tie, holding ("letter"), torsoOnly (skip legs, for characters behind counters)
 * Animatable parts (ids): -body, -armR, -foreR, -eyes, -brows, -m0 (closed), -m1 (open)
 */
export function person(o) {
  const id = o.id;
  const s = o.s ?? 1;
  const shirt = o.shirt ?? C.shirt;
  const pants = o.pants ?? C.pants;
  const hairColor = o.hairColor ?? "#d9b77e";

  const legs = o.torsoOnly
    ? ""
    : `<path d="M-26,-385 L-38,-12" stroke="${C.line}" stroke-width="44" stroke-linecap="round"/>
       <path d="M26,-385 L38,-12" stroke="${C.line}" stroke-width="44" stroke-linecap="round"/>
       <path d="M-26,-385 L-38,-12" stroke="${pants}" stroke-width="37" stroke-linecap="round"/>
       <path d="M26,-385 L38,-12" stroke="${pants}" stroke-width="37" stroke-linecap="round"/>
       <path d="M-60,-370 L60,-370 L58,-330 L-58,-330 Z" fill="${pants}" stroke="${C.line}" stroke-width="4"/>
       <ellipse cx="-48" cy="-6" rx="38" ry="15" fill="${C.shoe}" stroke="${C.line}" stroke-width="4"/>
       <ellipse cx="48" cy="-6" rx="38" ry="15" fill="${C.shoe}" stroke="${C.line}" stroke-width="4"/>`;

  // Left arm (viewer's left). "letter" bends it up to hold a sheet in front of the chest.
  const armL =
    o.holding === "letter"
      ? tube("M-68,-620 L-100,-470 L-30,-505") +
        hand(-30, -505) +
        `<g transform="rotate(-8 -20 -560)"><rect x="-85" y="-610" width="120" height="88" rx="4" fill="#fffdf6" stroke="${C.line}" stroke-width="4"/>
         <path d="M-70,-590 H15 M-70,-574 H5 M-70,-558 H20" stroke="#b9b3c4" stroke-width="5" stroke-linecap="round"/></g>`
      : tube("M-68,-620 L-95,-470 L-100,-330") + hand(-100, -330);

  // Right arm in two nested groups so it can scratch the head (rotate -armR at the shoulder, -foreR at the elbow).
  const armR = `<g id="${id}-armR">${tube("M68,-620 L95,-470")}
      <g id="${id}-foreR">${tube("M95,-470 L100,-330")}${hand(100, -330)}</g></g>`;

  const shirtPath = `<path d="M-70,-640 Q0,-656 70,-640 L98,-560 L72,-546 L62,-598 L60,-368 L-60,-368 L-62,-598 L-72,-546 L-98,-560 Z"
      fill="${shirt}" stroke="${C.line}" stroke-width="4.5" stroke-linejoin="round"/>`;
  const tie = o.tie
    ? `<path d="M0,-640 L-11,-626 L-6,-520 L0,-505 L6,-520 L11,-626 Z" fill="${o.tie}" stroke="${C.line}" stroke-width="3"/>`
    : "";

  const hairBack = {
    long: `<path d="M-128,-800 Q-130,-930 0,-918 Q130,-930 128,-800 L140,-610 Q0,-585 -140,-610 Z" fill="${hairColor}" stroke="${C.line}" stroke-width="4.5"/>`,
    bob: `<path d="M-130,-790 Q-132,-930 0,-920 Q132,-930 130,-790 L132,-700 Q0,-680 -132,-700 Z" fill="${hairColor}" stroke="${C.line}" stroke-width="4.5"/>`,
    bun: `<circle cx="0" cy="-925" r="45" fill="${hairColor}" stroke="${C.line}" stroke-width="4.5"/>`,
  }[o.hair] ?? "";
  const hairFront = {
    long: `<path d="M-112,-830 Q-60,-935 0,-905 Q60,-935 112,-830 Q60,-880 0,-872 Q-55,-880 -112,-830 Z" fill="${hairColor}" stroke="${C.line}" stroke-width="4"/>`,
    bob: `<path d="M-114,-825 Q-60,-940 0,-908 Q60,-940 114,-825 Q50,-870 0,-865 Q-50,-870 -114,-825 Z" fill="${hairColor}" stroke="${C.line}" stroke-width="4"/>`,
    bun: `<path d="M-110,-835 Q0,-930 110,-835 Q55,-875 0,-872 Q-55,-875 -110,-835 Z" fill="${hairColor}" stroke="${C.line}" stroke-width="4"/>`,
  }[o.hair] ?? "";

  const glasses = o.glasses
    ? `<g fill="none" stroke="${C.line}" stroke-width="4"><circle cx="-36" cy="-798" r="20"/><circle cx="26" cy="-798" r="20"/><path d="M-16,-800 Q-5,-806 6,-800"/></g>`
    : "";

  const head = `
    <path d="M0,-645 L0,-690" stroke="${C.line}" stroke-width="26" stroke-linecap="round"/>
    <path d="M0,-645 L0,-690" stroke="${C.skin}" stroke-width="19" stroke-linecap="round"/>
    ${hairBack}
    <circle cx="0" cy="-790" r="115" fill="url(#headGrad)" stroke="${C.line}" stroke-width="5"/>
    ${hairFront}
    <g id="${id}-eyes"><circle cx="-36" cy="-798" r="7.5" fill="${C.eye}"/><circle cx="26" cy="-798" r="7.5" fill="${C.eye}"/></g>
    ${glasses}
    <g id="${id}-brows" opacity="0" fill="none" stroke="${C.line}" stroke-width="5" stroke-linecap="round">
      <path d="M-52,-832 Q-38,-842 -22,-836"/><path d="M12,-848 Q28,-850 42,-838"/></g>
    <path id="${id}-m0" d="M-14,-748 Q-2,-744 12,-749" fill="none" stroke="${C.line}" stroke-width="4.5" stroke-linecap="round"/>
    <ellipse id="${id}-m1" cx="-2" cy="-746" rx="13" ry="10" fill="${C.mouth}" stroke="${C.line}" stroke-width="3.5" opacity="0"/>`;

  return `<g transform="translate(${o.x} ${o.y}) scale(${s})"><g id="${id}-body">
    <ellipse cx="0" cy="0" rx="120" ry="16" fill="#000" opacity="0.08"/>
    ${legs}${armL}${shirtPath}${tie}${armR}${head}</g></g>`;
}

// ---- timeline helpers (emitted as JS source inside a scene's <script>) ----

// Mouth flaps over speech intervals: [[start, end], ...] in scene-local seconds.
export function talk(id, spans, rate = 0.09) {
  const lines = [];
  for (const [a, b] of spans) {
    let open = true;
    for (let t = a; t < b - 0.02; t += rate) {
      lines.push(`tl.set("#${id}-m1",{opacity:${open ? 1 : 0}},${t.toFixed(2)});`);
      lines.push(`tl.set("#${id}-m0",{opacity:${open ? 0 : 1}},${t.toFixed(2)});`);
      open = !open;
    }
    lines.push(`tl.set("#${id}-m1",{opacity:0},${b.toFixed(2)});`);
    lines.push(`tl.set("#${id}-m0",{opacity:1},${b.toFixed(2)});`);
  }
  return lines.join("\n");
}

export function blink(id, at) {
  return `tl.set("#${id}-eyes",{scaleY:1,transformOrigin:"50% 50%"},0);\n` + at
    .map(
      (t) =>
        `tl.to("#${id}-eyes",{scaleY:0.1,transformOrigin:"50% 50%",duration:0.06,ease:"none"},${t});` +
        `tl.to("#${id}-eyes",{scaleY:1,transformOrigin:"50% 50%",duration:0.08,ease:"none"},${(t + 0.1).toFixed(2)});`,
    )
    .join("\n");
}

// The "Hä?" take: anticipation, arm up to the head, brows up, mouth open, scratching, settle.
export function hae(id, at, len = 0.75) {
  const up = (at - 0.25).toFixed(2);
  return `
tl.fromTo("#${id}-armR",{rotation:0},{rotation:-129,svgOrigin:"68 -620",duration:0.28,ease:"back.out(1.6)"},${up});
tl.fromTo("#${id}-foreR",{rotation:0},{rotation:-95,svgOrigin:"95 -470",duration:0.28,ease:"back.out(1.6)"},${up});
tl.fromTo("#${id}-foreR",{rotation:-95},{rotation:-82,svgOrigin:"95 -470",duration:0.12,ease:"sine.inOut",yoyo:true,repeat:5,immediateRender:false},${(at + 0.05).toFixed(2)});
tl.fromTo("#${id}-brows",{opacity:0},{opacity:1,duration:0.08},${up});
tl.fromTo("#${id}-body",{y:0},{y:6,duration:0.12,ease:"power2.out",yoyo:true,repeat:1},${up});
tl.set("#${id}-m1",{opacity:1,scaleX:0.8,scaleY:1.2,transformOrigin:"50% 50%"},${at.toFixed(2)});
tl.set("#${id}-m0",{opacity:0},${at.toFixed(2)});
tl.set("#${id}-m1",{opacity:0},${(at + len).toFixed(2)});
tl.set("#${id}-m0",{opacity:1},${(at + len).toFixed(2)});`;
}

// Breathing idle so a held character never freezes.
export function idle(id, dur, phase = 0) {
  return `tl.fromTo("#${id}-body",{scaleY:1},{scaleY:1.008,transformOrigin:"50% 100%",duration:1.1,ease:"sine.inOut",yoyo:true,repeat:${Math.max(1, Math.floor(dur / 1.1))}},${phase});`;
}

// Wraps one scene: a 1080×1920 SVG inside a camera div that slowly pushes in.
export function scene({ id, dur, svg, overlays = "", script, push = 1.04, origin = "50% 60%", css = "" }) {
  return `<template>
  <style>
    #root { position: absolute; inset: 0; overflow: hidden; background: #e9e1ef; font-family: "Nunito", sans-serif; }
    #${id}-cam { position: absolute; inset: 0; }
    #${id}-cam svg { position: absolute; inset: 0; width: 100%; height: 100%; }
    ${css}
  </style>
  <div id="root" data-composition-id="${id}" data-width="1080" data-height="1920">
    <div id="${id}-cam"><svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">${defs}${svg}</svg></div>
    ${overlays}
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.fromTo("#${id}-cam",{scale:1},{scale:${push},transformOrigin:"${origin}",duration:${dur},ease:"none"},0);
    ${script}
    window.__timelines["${id}"] = tl;
  </script>
</template>
`;
}
