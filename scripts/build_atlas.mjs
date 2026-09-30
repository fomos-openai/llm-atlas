#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const cli = process.argv[2];
if (!cli) {
  console.error("usage: node scripts/build_atlas.mjs /absolute/path/to/archify/bin/archify.mjs");
  process.exit(2);
}
const result = spawnSync(process.execPath, [
  path.resolve(cli), "finalize", "architecture", "atlas/llm-atlas.json",
  "LLM-ATLAS.html", "--repo-root", root, "--quality", "showcase", "--json"
], { cwd: root, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
process.stdout.write(result.stdout || "");
process.stderr.write(result.stderr || "");
process.exit(result.status ?? 1);

