#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const expected = [
  "00-navigation", "01-origins", "02-grails", "03-mature-technology-schools",
  "04-top-model-lifecycle", "05-intelligence-systems", "06-hands-on-practice",
  "07-production-engineering", "08-state-of-the-field", "09-future", "10-career", "11-reference"
];
const actual = fs.readdirSync(path.join(root, "knowledge"), {withFileTypes: true})
  .filter((entry) => entry.isDirectory()).map((entry) => entry.name).sort();
const failures = [];
if (JSON.stringify(actual) !== JSON.stringify(expected)) failures.push(`knowledge roots differ: ${actual.join(", ")}`);
for (const directory of expected) {
  if (!fs.existsSync(path.join(root, "knowledge", directory, "README.md"))) failures.push(`missing README: ${directory}`);
}
const required = ["labs", "catalogs", "evidence", "atlas", "book", "output/pdf", "scripts", ".github/workflows"];
for (const item of required) if (!fs.existsSync(path.join(root, item))) failures.push(`missing path: ${item}`);
if (failures.length) { console.error(failures.join("\n")); process.exit(1); }
const count = fs.readdirSync(path.join(root, "knowledge"), {recursive: true}).filter((item) => item.endsWith(".md")).length;
console.log(`structure ok: ${expected.length} domains, ${count} knowledge articles`);

