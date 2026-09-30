#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const base = path.join(root, "knowledge");
const files = fs.readdirSync(base, {recursive: true}).filter((item) => item.endsWith(".md"));
const failures = [];
const fields = ["title", "pillar", "audience", "last_verified", "evidence_level"];
for (const relative of files) {
  const text = fs.readFileSync(path.join(base, relative), "utf8");
  if (text.length < 1500) failures.push(`${relative}: fewer than 1500 characters`);
  if (!text.startsWith("---\n")) failures.push(`${relative}: missing YAML front matter`);
  for (const field of fields) if (!new RegExp(`^${field}:`, "m").test(text)) failures.push(`${relative}: missing ${field}`);
  for (const section of ["## 学习目标", "## 机制与技术骨架", "## 工程决策", "## 常见失效模式", "## 评测与验收", "## 延伸阅读"])
    if (!text.includes(section)) failures.push(`${relative}: missing section ${section}`);
}
if (failures.length) { console.error(failures.slice(0, 100).join("\n")); process.exit(1); }
console.log(`content ok: ${files.length} substantial articles, complete metadata and section contract`);

