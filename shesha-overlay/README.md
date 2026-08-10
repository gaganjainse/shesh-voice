# Shesha Voice overlay

This is a fork of [Newelle](https://github.com/qwersyk/Newelle) rebranded as
**Shesha Voice** — the voice/chat frontend for the Shesha agent ecosystem.

## What changes vs upstream

We keep upstream core untouched (for easy rebasing) and layer:

1. **Branding** — app display name "Shesha" (see `branding.patch`).
2. **Default MCP servers** — `shesha-mcp-servers.json` wires Newelle's MCP
   integration to the local Shesha components:
   system, shell, files, skills, memory, mind, harness, orchestrator,
   audit, phone, backup.
3. **Default model** — points at local Ollama (`phi4-mini`) so it works offline.

## Install

After installing the fork, copy the config:

```bash
mkdir -p ~/.config/Shesha
cp shesha-overlay/shesha-mcp-servers.json ~/.config/Shesha/mcp-servers.json
```

The fork is kept in sync with upstream; do not edit core files here unless
necessary — prefer extension/overlay changes.
