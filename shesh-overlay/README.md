# Shesh Voice overlay

This is a fork of [Newelle](https://github.com/qwersyk/Newelle) rebranded as
**Shesh Voice** — the voice/chat frontend for the Shesh agent ecosystem.

## What changes vs upstream

We keep upstream core untouched (for easy rebasing) and layer:

1. **Branding** — app display name "Shesh" (see `branding.patch`).
2. **Default MCP servers** — `shesh-mcp-servers.json` wires Newelle's MCP
   integration to the local Shesh components:
   system, shell, files, skills, memory, mind, harness, orchestrator,
   audit, phone, backup.
3. **Default model** — points at local Ollama (`phi4-mini`) so it works offline.

## Install

After installing the fork, copy the config:

```bash
mkdir -p ~/.config/Shesh
cp shesh-overlay/shesh-mcp-servers.json ~/.config/Shesh/mcp-servers.json
```

The fork is kept in sync with upstream; do not edit core files here unless
necessary — prefer extension/overlay changes.
