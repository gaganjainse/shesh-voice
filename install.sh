#!/usr/bin/env bash
set -euo pipefail

APPID="io.github.qwersyk.Newelle"
BUNDLENAME="newelle.flatpak"

cat <<'EOF'
shesh-voice installation entrypoint

The Shesh ecosystem consumes this repository as the native voice frontend. The
old default behavior silently installed the Flatpak build, which contradicts
that contract because Flatpak sandboxing restricts localhost MCP, microphone
wake-word access, and filesystem integration.

Use the separate `flatpak` mode only when you explicitly want a Flatpak build.
EOF

case "${1:-}" in
  flatpak)
    command -v flatpak-builder >/dev/null 2>&1 || {
      printf 'ERROR: flatpak-builder is required for Flatpak builds.\n' >&2
      exit 1
    }
    flatpak-builder --install --user --force-clean flatpak-app "${APPID}.json"
    ;;
  bundle)
    command -v flatpak-builder >/dev/null 2>&1 || {
      printf 'ERROR: flatpak-builder is required for Flatpak builds.\n' >&2
      exit 1
    }
    flatpak-builder --install --user --force-clean flatpak-app "${APPID}.json"
    flatpak build-bundle ~/.local/share/flatpak/repo "$BUNDLENAME" "$APPID"
    ;;
  ""|help|-h|--help)
    printf '\nUsage:\n'
    printf '  %s flatpak    Build/install the explicit Flatpak variant.\n' "$0"
    printf '  %s bundle     Build the Flatpak variant and create %s.\n' "$0" "$BUNDLENAME"
    printf '\nFor the normal Shesh installation, use the shesh-ecosystem installer.\n\n'
    ;;
  *)
    printf 'ERROR: unknown mode %q. Use %s --help.\n' "$1" "$0" >&2
    exit 2
    ;;
esac
