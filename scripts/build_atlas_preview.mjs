#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const spec = JSON.parse(fs.readFileSync(path.join(root, "atlas/llm-atlas.json"), "utf8"));
const out = path.join(root, "LLM-ATLAS.svg");
const escape = (value) => String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&apos;" }[char]));
const colors = {
  external: ["#e0f2fe", "#0369a1", "#38bdf8"],
  cloud: ["#ede9fe", "#6d28d9", "#8b5cf6"],
  database: ["#dcfce7", "#047857", "#34d399"],
  backend: ["#dbeafe", "#1d4ed8", "#60a5fa"],
  messagebus: ["#fef3c7", "#b45309", "#f59e0b"],
  security: ["#ffe4e6", "#be123c", "#fb7185"],
  frontend: ["#f1f5f9", "#334155", "#94a3b8"]
};
const nodes = new Map(spec.components.map((node) => [node.id, node]));
const yShift = 105;

const lines = spec.connections.map((edge) => {
  const from = nodes.get(edge.from);
  const to = nodes.get(edge.to);
  let x1 = from.pos[0] + from.size[0] / 2;
  let y1 = from.pos[1] + yShift + from.size[1] / 2;
  let x2 = to.pos[0] + to.size[0] / 2;
  let y2 = to.pos[1] + yShift + to.size[1] / 2;
  if (from.pos[1] === to.pos[1]) {
    const direction = x2 > x1 ? 1 : -1;
    x1 += direction * from.size[0] / 2;
    x2 -= direction * to.size[0] / 2;
  } else {
    y1 += from.size[1] / 2;
    y2 -= to.size[1] / 2;
  }
  const stroke = edge.variant === "security" ? "#e11d48" : edge.variant === "dashed" ? "#7c3aed" : "#2563eb";
  const dash = edge.variant === "dashed" ? ' stroke-dasharray="8 7"' : "";
  const labelX = (x1 + x2) / 2;
  const labelY = (y1 + y2) / 2 - (from.pos[1] === to.pos[1] ? 8 : 0);
  return `<g class="edge"><path d="M ${x1} ${y1} L ${x2} ${y2}" fill="none" stroke="${stroke}" stroke-width="2.2"${dash} marker-end="url(#arrow)"/><text x="${labelX}" y="${labelY}" text-anchor="middle">${escape(edge.label || "")}</text></g>`;
}).join("\n");

const boxes = spec.components.map((node) => {
  const [fill, text, accent] = colors[node.type];
  const x = node.pos[0];
  const y = node.pos[1] + yShift;
  const source = node.sources?.[0]?.path ? `./${node.sources[0].path}` : "#";
  return `<a href="${escape(source)}" target="_top"><g class="node"><rect x="${x}" y="${y}" width="${node.size[0]}" height="${node.size[1]}" rx="14" fill="${fill}" stroke="${accent}" stroke-width="2"/><rect x="${x}" y="${y}" width="6" height="${node.size[1]}" rx="3" fill="${accent}"/><text class="label" x="${x + 18}" y="${y + 29}" fill="${text}">${escape(node.label)}</text><text class="sub" x="${x + 18}" y="${y + 52}" fill="${text}">${escape(node.sublabel)}</text></g></a>`;
}).join("\n");

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="850" viewBox="0 0 1800 850" role="img" aria-labelledby="title desc">
<title id="title">LLM Atlas 大模型技术全生命周期知识地图</title>
<desc id="desc">从历史基础，经过数据、训练、后训练、评测、推理、Agent 与生产系统，到当前阶段和未来前沿的知识树。</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f8fafc"/><stop offset="1" stop-color="#eef2ff"/></linearGradient>
  <filter id="shadow" x="-10%" y="-20%" width="120%" height="150%"><feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="#0f172a" flood-opacity=".10"/></filter>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#475569"/></marker>
  <style>
    text{font-family:Inter,"Noto Sans SC","PingFang SC",system-ui,sans-serif}.node{filter:url(#shadow)}.label{font-size:17px;font-weight:700}.sub{font-size:11px;opacity:.82}.edge text{font-size:11px;fill:#475569;paint-order:stroke;stroke:#f8fafc;stroke-width:5px;stroke-linejoin:round}.phase{font-size:15px;font-weight:700;letter-spacing:.08em}.hint{font-size:13px;fill:#64748b}.node:hover rect:first-child{stroke-width:4}
  </style>
</defs>
<rect width="1800" height="850" rx="24" fill="url(#bg)"/>
<text x="60" y="52" font-size="30" font-weight="800" fill="#0f172a">LLM Atlas · 大模型技术全生命周期</text>
<text x="60" y="80" class="hint">从哪里来 · 当下处于什么阶段 · 未来要去往何处　｜　点击节点进入知识页</text>
<text x="40" y="125" class="phase" fill="#0369a1">来源与基础</text>
<text x="40" y="345" class="phase" fill="#1d4ed8">训练、推理与行动</text>
<text x="40" y="565" class="phase" fill="#7c3aed">生产、现状与未来</text>
${lines}
${boxes}
<g transform="translate(60 755)"><rect width="1680" height="60" rx="14" fill="#ffffff" opacity=".82"/><circle cx="28" cy="30" r="7" fill="#38bdf8"/><text x="44" y="35" class="hint">历史解释能力来源</text><circle cx="260" cy="30" r="7" fill="#60a5fa"/><text x="276" y="35" class="hint">生命周期解释系统如何形成</text><circle cx="610" cy="30" r="7" fill="#fb7185"/><text x="626" y="35" class="hint">安全贯穿每一阶段</text><circle cx="875" cy="30" r="7" fill="#8b5cf6"/><text x="891" y="35" class="hint">现状以日期冻结，未来按证据分级</text><text x="1390" y="35" class="hint">快照 2026-09-30</text></g>
</svg>`;

fs.writeFileSync(out, svg);
console.log(`wrote ${path.relative(root, out)}`);

