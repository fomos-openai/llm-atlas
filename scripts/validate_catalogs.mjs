#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const names = ["models", "datasets", "benchmarks", "frameworks", "hardware", "papers"];
const failures = [];
for (const name of names) {
  const file = path.join(root, "catalogs", `${name}.yml`);
  if (!fs.existsSync(file)) { failures.push(`missing ${name}.yml`); continue; }
  const text = fs.readFileSync(file, "utf8");
  if (!text.includes("schema_version: 2")) failures.push(`${name}: schema_version must be 2`);
  if (!text.includes("last_verified: 2026-10-01")) failures.push(`${name}: stale verification date`);
  if (!text.includes("source: https://")) failures.push(`${name}: no source URLs`);
}
if (failures.length) { console.error(failures.join("\n")); process.exit(1); }
console.log(`catalogs ok: ${names.length} versioned catalogs`);

