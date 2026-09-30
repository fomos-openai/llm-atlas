#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const knowledge = path.join(root, "knowledge");
const expected = [
  "00-start-here", "01-origins", "02-foundations", "03-data",
  "04-tokenization-and-representation", "05-model-architectures",
  "06-pretraining", "07-post-training", "08-reasoning-and-test-time-compute",
  "09-evaluation", "10-inference-and-efficiency", "11-context-and-knowledge",
  "12-agents-and-tool-use", "13-multimodal-and-generation",
  "14-safety-security-and-privacy", "15-production-lifecycle",
  "16-infrastructure-hardware-and-economics", "17-ecosystem-and-applications",
  "18-state-of-the-field", "19-future-frontiers", "20-reference"
];

const failures = [];
for (const dir of expected) {
  const full = path.join(knowledge, dir);
  if (!fs.existsSync(full) || !fs.statSync(full).isDirectory()) failures.push(`missing directory: knowledge/${dir}`);
  const readme = path.join(full, "README.md");
  if (!fs.existsSync(readme)) failures.push(`missing chapter index: knowledge/${dir}/README.md`);
}

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(dir, entry.name);
    return entry.isDirectory() ? walk(full) : [full];
  });
}

const markdown = walk(knowledge).filter((file) => file.endsWith(".md"));
for (const file of markdown) {
  const text = fs.readFileSync(file, "utf8").trim();
  if (text.length < 80) failures.push(`too little content: ${path.relative(root, file)}`);
  if (!text.startsWith("#")) failures.push(`missing heading: ${path.relative(root, file)}`);
}

const topLevel = fs.readdirSync(knowledge, { withFileTypes: true })
  .filter((entry) => entry.isDirectory()).map((entry) => entry.name).sort();
if (JSON.stringify(topLevel) !== JSON.stringify(expected)) {
  failures.push(`chapter set differs: ${topLevel.join(", ")}`);
}

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}
console.log(`structure ok: ${expected.length} chapters, ${markdown.length} markdown pages`);

