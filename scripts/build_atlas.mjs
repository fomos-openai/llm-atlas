#!/usr/bin/env node
import {spawnSync} from "node:child_process";
import {readFileSync, writeFileSync} from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const cli = process.argv[2] || process.env.ARCHIFY_CLI;
if (!cli) {
  console.error("usage: node scripts/build_atlas.mjs /absolute/path/to/archify/bin/archify.mjs");
  process.exit(2);
}
const result = spawnSync(process.execPath, [
  path.resolve(cli), "finalize", "architecture", "atlas/llm-atlas-v2.json",
  "LLM-ATLAS.html", "--repo-root", root, "--quality", "showcase",
  "--out-dir", "atlas/evidence/finalize", "--json"
], {cwd: root, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"]});
process.stdout.write(result.stdout || "");
process.stderr.write(result.stderr || "");
if ((result.status ?? 1) !== 0) process.exit(result.status ?? 1);

// README needs a static fallback in addition to Archify's interactive HTML.
// Reuse the exact validated SVG scene and its authored CSS so the preview
// cannot drift into a second, independently maintained map.
const html = readFileSync(path.join(root, "LLM-ATLAS.html"), "utf8");
const styleBlocks = [...html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)].map((match) => match[1]);
const svgMatch = html.match(/<svg\s[^>]*data-quality-profile="showcase"[\s\S]*?<\/svg>/);
if (!svgMatch || styleBlocks.length === 0) {
  console.error("Archify output did not contain the expected showcase SVG and styles");
  process.exit(1);
}
let svg = svgMatch[0]
  .replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ')
  .replace("<defs>", `<defs>\n<style><![CDATA[\n${styleBlocks.join("\n")}\n]]></style>`);
writeFileSync(path.join(root, "LLM-ATLAS.svg"), `${svg}\n`, "utf8");
console.log("static preview: LLM-ATLAS.svg");
