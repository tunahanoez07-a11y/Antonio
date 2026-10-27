// Generates compositions/*.html for "Ein Leben ohne Bürokratie".
// Run: node build.mjs   (then edit the generated files in Studio if you like)
import { writeFileSync, mkdirSync } from "node:fs";
import { person, scene, talk, blink, hae, idle, C } from "../_lib/rig.mjs";

mkdirSync(new URL("./compositions/", import.meta.url), { recursive: true });
const out = (name, html) => writeFileSync(new URL(`./compositions/${name}.html`, import.meta.url), html);

const T = (x, y, size, text, o = {}) =>
  `<text class="t" x="${x}" y="${y}" font-size="${size}" font-weight="${o.w ?? 700}" fill="${o.fill ?? C.line}" text-anchor="${o.a ?? "middle"}"${o.ls ? ` letter-spacing="${o.ls}"` : ""}>${text}</text>`;
const css = `.t { font-family: "Nunito", sans-serif; }`;

const room = (wall, floor, horizon = 1380) => `
  <rect width="1080" height="1920" fill="${wall}"/>
  <rect y="${horizon}" width="1080" height="${1920 - horizon}" fill="${floor}"/>
  <rect y="${horizon}" width="1080" height="60" fill="url(#floorShade)"/>
  <path d="M0,${horizon} H1080" stroke="${C.line}" stroke-width="3" opacity="0.35"/>`;

// Protagonist and recurring officials
const hero = (id, x, y, s = 1, extra = {}) => person({ id, x, y, s, ...extra });
const official = (id, x, y, s = 1, extra = {}) =>
  person({ id, x, y, s, shirt: "#a3a8b4", pants: "#5f636e", tie: "#c98b8b", glasses: true, ...extra });

// ---------- 1 · Intro (0–2.6) ----------
out(
  "intro",
  scene({
    id: "intro",
    dur: 2.6,
    css: css + `#intro-title{position:absolute;left:0;right:0;top:215px;text-align:center;font-family:"Nunito",sans-serif;font-weight:600;font-size:66px;color:${C.title};letter-spacing:-0.5px;}`,
    svg: `
    <defs><linearGradient id="introSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6dcf0"/><stop offset="1" stop-color="#f6dccd"/></linearGradient></defs>
    <rect width="1080" height="1920" fill="url(#introSky)"/>
    <rect x="110" y="640" width="860" height="780" fill="#cfd8e8" stroke="${C.line}" stroke-width="4"/>
    <path d="M80,640 L540,470 L1000,640 Z" fill="#bcc7db" stroke="${C.line}" stroke-width="4" stroke-linejoin="round"/>
    <rect x="300" y="680" width="480" height="90" rx="10" fill="#f7f3fa" stroke="${C.line}" stroke-width="4"/>
    ${T(540, 742, 54, "BÜRGERAMT", { ls: 6, fill: "#6d6680" })}
    ${[180, 330, 690, 840].map((x) => `<rect x="${x}" y="800" width="60" height="600" fill="#e3e9f3" stroke="${C.line}" stroke-width="4"/>`).join("")}
    ${[180, 330, 690, 840].map((x) => `<rect x="${x - 12}" y="790" width="84" height="22" fill="#e3e9f3" stroke="${C.line}" stroke-width="4"/>`).join("")}
    <rect x="450" y="1060" width="180" height="360" rx="8" fill="#a7b4cc" stroke="${C.line}" stroke-width="4"/>
    <rect y="1420" width="1080" height="500" fill="#cfc6d2"/>
    <path d="M0,1420 H1080" stroke="${C.line}" stroke-width="3" opacity="0.35"/>
    <path d="M330,1420 L190,1920 M750,1420 L890,1920" stroke="#bdb3c2" stroke-width="5"/>
    ${hero("p0", 540, 1760, 0.9)}`,
    overlays: `<div id="intro-title">Ein Leben ohne Bürokratie</div>`,
    script: `${idle("p0", 2.6)}\n${blink("p0", [1.3])}`,
  }),
);

// ---------- 2 · Bürgeramt (2.6–8.2) ----------
out(
  "amt",
  scene({
    id: "amt",
    dur: 5.6,
    css,
    svg: `
    ${room("#e8def0", "#d8cfd9", 1360)}
    <rect x="80" y="330" width="250" height="170" rx="14" fill="#3e3b48" stroke="${C.line}" stroke-width="4"/>
    ${T(205, 378, 30, "IHRE NUMMER", { fill: "#cfc7dc", w: 800, ls: 2 })}
    ${T(205, 465, 84, "001", { fill: "#8ee0a8", w: 900 })}
    <rect x="560" y="330" width="420" height="96" rx="10" fill="#f8f4fb" stroke="${C.line}" stroke-width="4"/>
    ${T(770, 395, 46, "SCHALTER 1", { fill: "#6d6680", w: 800, ls: 3 })}
    <rect x="600" y="520" width="150" height="190" fill="#f3eef7" stroke="${C.line}" stroke-width="4"/>
    <path d="M620,560 H730 M620,590 H710 M620,620 H725" stroke="#c8c0d3" stroke-width="6" stroke-linecap="round"/>
    ${official("be", 790, 1560, 1.0, { torsoOnly: true })}
    <rect x="430" y="1150" width="700" height="60" fill="#efd6b4" stroke="${C.line}" stroke-width="4"/>
    <rect x="450" y="1210" width="660" height="330" fill="#e4c39c" stroke="${C.line}" stroke-width="4"/>
    <path d="M450,1300 H1110" stroke="${C.line}" stroke-width="3" opacity="0.25"/>
    <g id="amt-card"><rect x="640" y="1118" width="150" height="40" rx="6" fill="#f2c9d6" stroke="${C.line}" stroke-width="4"/>
      <circle cx="668" cy="1138" r="11" fill="#fff" stroke="${C.line}" stroke-width="3"/><path d="M690,1132 H770 M690,1146 H750" stroke="${C.line}" stroke-width="4" stroke-linecap="round" opacity="0.6"/></g>
    ${hero("pa", 250, 1760, 1.08)}`,
    script: `
${idle("pa", 5.6)}
${idle("be", 5.6, 0.4)}
${talk("be", [[0.3, 1.47], [1.8, 2.71], [3.02, 4.47]])}
${blink("be", [1.6, 4.9])}
${blink("pa", [0.9, 3.5])}
tl.fromTo("#amt-card",{x:0,opacity:0},{x:0,opacity:1,duration:0.15},3.0);
tl.fromTo("#amt-card",{x:0},{x:-250,duration:0.55,ease:"power3.out",immediateRender:false},3.2);
${hae("pa", 4.6)}`,
  }),
);

// ---------- 3 · Steuerbescheid (8.2–13.8) ----------
out(
  "steuer",
  scene({
    id: "steuer",
    dur: 5.6,
    css:
      css +
      `#st-dim{position:absolute;inset:0;background:rgba(60,52,70,.35);opacity:0}
       #st-letter{position:absolute;left:150px;top:470px;width:780px;padding:56px 60px;background:#fffdf7;border:5px solid ${C.line};border-radius:14px;font-family:"Nunito",sans-serif;color:${C.line};opacity:0;box-shadow:0 14px 0 rgba(0,0,0,.08)}
       #st-letter .h{font-weight:900;font-size:40px;letter-spacing:4px;color:#7a7290}
       #st-letter .b{font-size:44px;font-weight:700;line-height:1.3;margin-top:34px}
       #st-letter .sum{margin-top:40px;font-size:96px;font-weight:900;color:#4f9e6e}
       #st-letter .l{margin-top:6px;font-size:32px;font-weight:700;color:#8b8499}`,
    svg: `
    <rect width="1080" height="1920" fill="#d6e6f2"/>
    <rect x="0" y="420" width="1080" height="1000" fill="#f6eac4" stroke="${C.line}" stroke-width="4"/>
    <path d="M-20,430 L540,250 L1100,430" fill="#e7b9a6" stroke="${C.line}" stroke-width="4" stroke-linejoin="round"/>
    <rect x="80" y="760" width="230" height="660" rx="6" fill="#d9a77a" stroke="${C.line}" stroke-width="4"/>
    <circle cx="275" cy="1100" r="12" fill="#f3d9a8" stroke="${C.line}" stroke-width="3"/>
    <rect x="700" y="640" width="260" height="230" fill="#cfe3ee" stroke="${C.line}" stroke-width="4"/>
    <path d="M830,640 V870 M700,755 H960" stroke="${C.line}" stroke-width="4"/>
    <rect y="1420" width="1080" height="500" fill="#cfc8cc"/>
    <rect x="0" y="1620" width="1080" height="300" fill="#a9c79a"/>
    <path d="M0,1420 H1080" stroke="${C.line}" stroke-width="3" opacity="0.35"/>
    <rect x="880" y="1180" width="22" height="440" fill="#8597b8" stroke="${C.line}" stroke-width="4"/>
    <path d="M800,1080 H960 V1190 H800 Z" fill="#9db0d2" stroke="${C.line}" stroke-width="4"/>
    <path d="M800,1080 Q880,1020 960,1080" fill="#9db0d2" stroke="${C.line}" stroke-width="4"/>
    <rect x="955" y="1060" width="12" height="60" fill="#e08a8a" stroke="${C.line}" stroke-width="3"/>
    ${hero("ps", 540, 1700, 1.08, { holding: "letter" })}`,
    overlays: `<div id="st-dim"></div>
    <div id="st-letter"><div class="h">FINANZAMT</div>
      <div class="b">Ihre Steuererklärung haben wir bereits für Sie erledigt.</div>
      <div class="sum">+ 800,00 €</div><div class="l">Erstattung · kein Antrag nötig</div></div>`,
    script: `
${idle("ps", 5.6)}
${blink("ps", [0.6, 4.3])}
tl.fromTo("#st-dim",{opacity:0},{opacity:1,duration:0.2},0.9);
tl.fromTo("#st-letter",{opacity:0,scale:0.86,rotation:-3},{opacity:1,scale:1,rotation:-1.5,duration:0.35,ease:"back.out(1.7)"},0.9);
tl.fromTo("#st-letter .sum",{scale:0.6,opacity:0},{scale:1,opacity:1,transformOrigin:"0% 50%",duration:0.3,ease:"back.out(2.2)"},2.75);
tl.to("#st-letter",{opacity:0,scale:0.92,duration:0.2,ease:"power2.in"},4.25);
tl.to("#st-dim",{opacity:0,duration:0.2},4.25);
${hae("ps", 4.7, 0.65)}`,
  }),
);

// ---------- 4 · CTA (13.8–18.2) ----------
out(
  "cta",
  scene({
    id: "cta",
    dur: 4.4,
    push: 1.03,
    css:
      css +
      `#cta-pill{position:absolute;left:90px;top:300px;width:820px;padding:30px 0;border-radius:999px;background:#fe2c55;color:#fff;text-align:center;font-family:"Nunito",sans-serif;font-weight:900;font-size:62px;opacity:0;box-shadow:0 10px 0 rgba(0,0,0,.12)}
       #cta-sub{position:absolute;left:0;right:0;top:450px;text-align:center;font-family:"Nunito",sans-serif;font-weight:800;font-size:40px;color:${C.line};opacity:0}
       #cta-arrow{position:absolute;left:820px;top:520px;width:200px;height:420px;opacity:0}`,
    svg: `
    ${room("#e6e0f1", "#d6cfdb", 1380)}
    <rect x="90" y="560" width="200" height="250" fill="#f3eef7" stroke="${C.line}" stroke-width="4"/>
    ${T(190, 640, 30, "AKTEN", { fill: "#8b8499", w: 800, ls: 3 })}
    <path d="M115,680 H265 M115,720 H245 M115,760 H260" stroke="#c8c0d3" stroke-width="7" stroke-linecap="round"/>
    <circle cx="880" cy="650" r="80" fill="#f8f4fb" stroke="${C.line}" stroke-width="4"/>
    <path d="M880,650 V598 M880,650 L915,668" stroke="${C.line}" stroke-width="6" stroke-linecap="round"/>
    ${official("be2", 540, 1700, 1.12, { torsoOnly: true })}
    <rect x="40" y="1230" width="1000" height="56" fill="#efd6b4" stroke="${C.line}" stroke-width="4"/>
    <rect x="70" y="1286" width="940" height="320" fill="#e4c39c" stroke="${C.line}" stroke-width="4"/>
    <g transform="rotate(-4 420 1180)"><rect x="300" y="1105" width="300" height="190" rx="4" fill="#fffdf7" stroke="${C.line}" stroke-width="4"/>
      ${T(450, 1148, 30, "ANTRAG AUF", { w: 900, fill: "#6d6680", ls: 2 })}${T(450, 1186, 32, "TEIL 2", { w: 900, fill: "#6d6680", ls: 3 })}
      <path d="M330,1278 H570" stroke="#c8c0d3" stroke-width="5" stroke-linecap="round"/></g>
    <g id="cta-mark" opacity="0" data-layout-allow-overlap><g transform="rotate(-10 455 1240)"><rect x="325" y="1206" width="260" height="70" rx="8" fill="none" stroke="#d64561" stroke-width="7"/>
      ${T(455, 1257, 40, "GENEHMIGT", { w: 900, fill: "#d64561", ls: 2 })}</g></g>
    <g id="cta-stamp"><rect x="410" y="1050" width="90" height="34" rx="6" fill="#d64561" stroke="${C.line}" stroke-width="4"/>
      <rect x="440" y="960" width="30" height="92" rx="8" fill="#b9875d" stroke="${C.line}" stroke-width="4"/>
      <circle cx="455" cy="950" r="30" fill="#b9875d" stroke="${C.line}" stroke-width="4"/></g>`,
    overlays: `<div id="cta-pill">FOLGEN für Teil 2</div>
    <div id="cta-sub">sonst brauchst du einen Antrag</div>
    <svg id="cta-arrow" viewBox="0 0 200 420"><path d="M40,10 C150,80 160,260 120,380" fill="none" stroke="#fe2c55" stroke-width="16" stroke-linecap="round"/>
      <path d="M75,345 L118,395 L160,340" fill="none" stroke="#fe2c55" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    script: `
${idle("be2", 4.4)}
${talk("be2", [[0.3, 1.09], [1.36, 3.98]])}
${blink("be2", [1.15, 3.2])}
tl.fromTo("#cta-stamp",{y:-1200,opacity:1},{y:-120,duration:0.35,ease:"power2.out"},0.75);
tl.to("#cta-stamp",{y:175,duration:0.12,ease:"power4.in"},1.33);
tl.fromTo("#cta-mark",{opacity:0,scale:1.4},{opacity:1,scale:1,svgOrigin:"455 1240",duration:0.12,ease:"power3.out"},1.45);
tl.to("#cta-stamp",{y:-1200,duration:0.4,ease:"power2.in"},1.62);
tl.fromTo("#cta-cam",{x:0},{x:-10,duration:0.05,yoyo:true,repeat:3,ease:"none",immediateRender:false},1.45);
tl.fromTo("#cta-pill",{opacity:0,y:-40,scale:0.9},{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(2)"},1.9);
tl.fromTo("#cta-sub",{opacity:0,y:20},{opacity:1,y:0,duration:0.3,ease:"power2.out"},2.2);
tl.fromTo("#cta-arrow",{opacity:0,y:-30},{opacity:1,y:0,duration:0.3,ease:"power2.out"},2.35);
tl.to("#cta-arrow",{y:24,duration:0.35,ease:"sine.inOut",yoyo:true,repeat:3},2.7);
tl.to("#cta-pill",{scale:1.05,duration:0.3,ease:"sine.inOut",yoyo:true,repeat:3},2.7);`,
  }),
);

// ---------- 5 · Arztpraxis (18.2–23.4) ----------
out(
  "arzt",
  scene({
    id: "arzt",
    dur: 5.2,
    css,
    svg: `
    ${room("#dcece4", "#cfd9d4", 1380)}
    <rect x="50" y="300" width="540" height="110" rx="12" fill="#f8fbf9" stroke="${C.line}" stroke-width="4"/>
    ${T(320, 372, 44, "PRAXIS DR. SOFORT", { fill: "#3f6e5c", w: 900, ls: 1 })}
    <rect x="620" y="300" width="380" height="150" rx="12" fill="#3e3b48" stroke="${C.line}" stroke-width="4"/>
    ${T(810, 352, 30, "WARTEZEIT", { fill: "#cfc7dc", w: 800, ls: 3 })}
    ${T(810, 425, 64, "0 MIN.", { fill: "#8ee0a8", w: 900 })}
    <rect x="60" y="560" width="250" height="800" rx="6" fill="#bfd9cd" stroke="${C.line}" stroke-width="4"/>
    ${T(185, 650, 30, "BEHANDLUNG", { fill: "#2f5a4a", w: 800, ls: 1 })}
    ${[0, 1, 2].map((i) => `<g transform="translate(${80 + i * 120} 1450)"><rect x="0" y="0" width="100" height="22" rx="6" fill="#9fc4b3" stroke="${C.line}" stroke-width="4"/><rect x="0" y="-110" width="100" height="22" rx="6" fill="#9fc4b3" stroke="${C.line}" stroke-width="4" transform="rotate(-4 0 -110)"/><path d="M10,22 V110 M90,22 V110" stroke="${C.line}" stroke-width="6"/><path d="M8,-88 V0 M92,-92 V0" stroke="${C.line}" stroke-width="5"/></g>`).join("")}
    ${person({ id: "mfa", x: 800, y: 1560, s: 0.98, shirt: "#9fd0bd", pants: "#7aa596", hair: "bun", hairColor: "#9a6b4a", torsoOnly: true })}
    <rect x="560" y="1170" width="520" height="56" fill="#f4f7f5" stroke="${C.line}" stroke-width="4"/>
    <rect x="580" y="1226" width="500" height="330" fill="#e5ece8" stroke="${C.line}" stroke-width="4"/>
    <path d="M610,1300 H1060" stroke="${C.line}" stroke-width="3" opacity="0.25"/>
    <path d="M760,1170 v-50 h40 v50" fill="#f0a8b8" stroke="${C.line}" stroke-width="4"/>
    ${hero("pz", 420, 1780, 1.08)}`,
    script: `
${idle("pz", 5.2)}
${idle("mfa", 5.2, 0.5)}
${talk("mfa", [[0.3, 1.12], [1.34, 4.05]])}
${blink("mfa", [1.2, 3.1])}
${blink("pz", [0.7, 2.8])}
${hae("pz", 4.2)}`,
  }),
);

// ---------- 6 · Zeitsprung (23.4–25.0) ----------
out(
  "card",
  scene({
    id: "card",
    dur: 1.6,
    push: 1.0,
    css:
      css +
      `#card-t{position:absolute;left:0;right:0;top:860px;text-align:center;font-family:"Nunito",sans-serif;font-weight:800;font-size:76px;color:${C.card}}`,
    svg: `<rect width="1080" height="1920" fill="#e2d6ea"/><rect y="1500" width="1080" height="420" fill="#d6cbd8"/>`,
    overlays: `<div id="card-t">1 Woche später…</div>`,
    script: `tl.fromTo("#card-t",{opacity:0,y:12},{opacity:1,y:0,duration:0.3,ease:"power2.out"},0.05);`,
  }),
);

// ---------- 7 · Museum (25.0–30.0) ----------
out(
  "museum",
  scene({
    id: "museum",
    dur: 5.0,
    push: 1.07,
    origin: "60% 55%",
    css,
    svg: `
    ${room("#e9dfe6", "#d9cdd3", 1400)}
    <path d="M330,0 L180,1400 H700 L560,0 Z" fill="#fff6dc" opacity="0.45"/>
    <rect x="80" y="300" width="380" height="110" rx="12" fill="#f8f4f6" stroke="${C.line}" stroke-width="4"/>
    ${T(270, 372, 46, "MUSEUM", { fill: "#8a6f80", w: 900, ls: 8 })}
    <rect x="300" y="1050" width="290" height="360" fill="#e7dde4" stroke="${C.line}" stroke-width="4"/>
    <rect x="280" y="1020" width="330" height="40" fill="#f2eaf0" stroke="${C.line}" stroke-width="4"/>
    <rect x="300" y="720" width="290" height="300" fill="#e8f3f8" opacity="0.55" stroke="${C.line}" stroke-width="4"/>
    <path d="M330,750 L380,720 M330,800 L420,740" stroke="#fff" stroke-width="6" opacity="0.8"/>
    <g transform="translate(445 960)">
      <rect x="-110" y="-70" width="220" height="80" rx="10" fill="#dcd6cf" stroke="${C.line}" stroke-width="4"/>
      <path d="M-80,-70 L-60,-120 H60 L80,-70" fill="#cfc8c0" stroke="${C.line}" stroke-width="4"/>
      <rect x="-50" y="-128" width="100" height="16" fill="#fffdf7" stroke="${C.line}" stroke-width="3"/>
      <rect x="20" y="-55" width="70" height="26" rx="4" fill="#9ab0a2" stroke="${C.line}" stroke-width="3"/>
      ${[0, 1, 2].map((r) => [0, 1, 2].map((c) => `<rect x="${-90 + c * 30}" y="${-55 + r * 18}" width="20" height="11" rx="3" fill="#f2efe9" stroke="${C.line}" stroke-width="2"/>`).join("")).join("")}
    </g>
    <rect x="330" y="1180" width="230" height="90" rx="6" fill="#fffdf7" stroke="${C.line}" stroke-width="4"/>
    ${T(445, 1220, 28, "FAXGERÄT", { w: 900, fill: "#6d6680", ls: 2 })}
    ${T(445, 1258, 30, "1985 – 2025", { w: 700, fill: "#8b8499" })}
    ${official("be3", 170, 1700, 0.98)}
    ${hero("pm", 810, 1760, 1.08)}`,
    script: `
${idle("pm", 5.0)}
${idle("be3", 5.0, 0.3)}
${talk("be3", [[0.4, 1.54], [1.93, 3.22]])}
${blink("be3", [1.7])}
${blink("pm", [0.9, 2.4])}
${hae("pm", 3.6, 0.65)}`,
  }),
);

console.log("scenes written");
