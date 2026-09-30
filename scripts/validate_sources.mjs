#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const failures = [];
function walk(directory) {
  return fs.readdirSync(directory, {withFileTypes: true}).flatMap((entry) => {
    const full = path.join(directory, entry.name);
    if ([".git", "tmp", ".venv"].includes(entry.name)) return [];
    return entry.isDirectory() ? walk(full) : [full];
  });
}
for (const file of walk(root).filter((item) => item.endsWith(".md"))) {
  const text = fs.readFileSync(file, "utf8");
  for (const match of text.matchAll(/!?(?:\[[^\]]*\])\(([^)]+)\)/g)) {
    const raw = match[1].trim().replace(/^<|>$/g, "");
    if (!raw || /^(https?:|mailto:)/i.test(raw)) continue;
    const target = decodeURIComponent(raw.split("#")[0]);
    if (!target) continue;
    if (!fs.existsSync(path.resolve(path.dirname(file), target))) failures.push(`${path.relative(root, file)} -> ${target}`);
  }
  if (file.includes(`${path.sep}knowledge${path.sep}`) && !/https:\/\//.test(text)) failures.push(`${path.relative(root, file)}: no primary source link`);
}
if (failures.length) { console.error(failures.join("\n")); process.exit(1); }
console.log("sources ok: local links resolve and every knowledge article has external evidence");

