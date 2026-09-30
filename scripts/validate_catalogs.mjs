#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const names = ["models", "datasets", "benchmarks", "tools", "papers"];
const failures = [];
for (const name of names) {
  const file = path.join(root, "catalogs", `${name}.yml`);
  const text = fs.readFileSync(file, "utf8");
  if (!text.includes("schema_version: 1")) failures.push(`${name}: missing schema version`);
  if (!text.includes("last_verified:")) failures.push(`${name}: missing verification date`);
  if (!/https:\/\//.test(text)) failures.push(`${name}: no primary source links`);
}
if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}
console.log(`catalogs ok: ${names.length}`);

