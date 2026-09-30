# Atlas 构建说明

`llm-atlas.json` 是 Archify architecture schema 的 typed JSON 源；根目录 `LLM-ATLAS.html` 是经 Archify showcase profile 验证的独立交互制品，`LLM-ATLAS.svg` 是 README 预览。

重建：

```bash
node scripts/build_atlas.mjs /absolute/path/to/archify/bin/archify.mjs
```

修改知识树拓扑时应同步修改 JSON，并保留 Archify 的 finalize summary 与 artifact receipt。历史大改版放入 `snapshots/`。

