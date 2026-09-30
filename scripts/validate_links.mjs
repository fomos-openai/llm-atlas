#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const ignored = new Set(["LLM-ATLAS.html", "LLM-ATLAS.svg", "LLM-ATLAS.pdf"]);
const failures = [];

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(dir, entry.name);
    if (entry.name === ".git" || entry.name === "tmp") return [];
    return entry.isDirectory() ? walk(full) : [full];
  });
}

for (const file of walk(root).filter((item) => item.endsWith(".md"))) {
  const text = fs.readFileSync(file, "utf8");
  const pattern = /!?(?:\[[^\]]*\])\(([^)]+)\)/g;
  for (const match of text.matchAll(pattern)) {
    let target = match[1].trim().replace(/^<|>$/g, "").split("#")[0];
    if (!target || /^(?:https?:|mailto:|codex:)/i.test(target)) continue;
    target = decodeURIComponent(target);
    const resolved = path.resolve(path.dirname(file), target);
    if (!fs.existsSync(resolved) && !(path.dirname(file) === root && ignored.has(target.replace(/^\.\//, "")))) {
      failures.push(`${path.relative(root, file)} -> ${target}`);
    }
  }
}

if (failures.length) {
  console.error(`broken local links (${failures.length}):\n${failures.join("\n")}`);
  process.exit(1);
}
console.log("local markdown links ok");

