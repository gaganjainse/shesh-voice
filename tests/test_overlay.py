"""Verification for the Shesh voice overlay (Newelle fork, verification-lit).

We cannot import the GTK application headless, but everything the overlay
owns is verifiable statically, and upstream drift is caught by applying the
patch context against the tracked source tree.
"""

from __future__ import annotations

import ast
import configparser
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "shesh-overlay"


def test_overlay_files_present() -> None:
    for name in ("branding.patch", "default-settings.ini", "shesh-mcp-servers.json", "README.md"):
        assert (OVERLAY / name).exists(), f"missing overlay file {name}"


def test_settings_ini_parses_and_is_sane() -> None:
    cfg = configparser.ConfigParser()
    cfg.read(OVERLAY / "default-settings.ini")
    assert cfg.sections(), "default-settings.ini has no sections"


def test_mcp_servers_json_valid_and_runnable() -> None:
    data = json.loads((OVERLAY / "shesh-mcp-servers.json").read_text())
    assert data, "empty mcp servers file"
    servers = data.get("mcpServers", data)
    assert isinstance(servers, dict) and servers, "expected mcpServers mapping"
    for name, spec in servers.items():
        assert isinstance(spec, dict), f"{name}: spec must be an object"
        assert "command" in spec, f"{name}: missing command"
        assert name.startswith("shesh"), f"{name}: server ids must be shesh-* (uniform naming)"


def test_branding_patch_applies_cleanly(tmp_path: Path) -> None:
    """Apply the overlay patch onto a scratch copy — guards upstream drift."""
    import shutil
    import subprocess

    patched_files = (
        "src/constants.py",
        "data/io.github.qwersyk.Newelle.appdata.xml.in",
        "data/io.github.qwersyk.Newelle.desktop.in",
    )
    for rel in patched_files:
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    proc = subprocess.run(
        ["git", "apply", "--stat", "-"], input=(OVERLAY / "branding.patch").read_bytes(),
        cwd=tmp_path, capture_output=True, timeout=60, check=False,
    )
    assert proc.returncode == 0, proc.stderr.decode()
    proc = subprocess.run(
        ["git", "apply", "-"], input=(OVERLAY / "branding.patch").read_bytes(),
        cwd=tmp_path, capture_output=True, timeout=60, check=False,
    )
    assert proc.returncode == 0, (
        "branding.patch no longer applies — rebase it against upstream:\n"
        + proc.stderr.decode()
    )
    assert 'DIR_NAME = "Shesh"' in (tmp_path / "src/constants.py").read_text()
    assert "Name=Shesh" in (tmp_path / "data/io.github.qwersyk.Newelle.desktop.in").read_text()
    assert "<name>Shesh</name>" in (tmp_path / "data/io.github.qwersyk.Newelle.appdata.xml.in").read_text()


def test_every_python_source_parses() -> None:
    """Static gate for the full fork: 181 files must all be valid Python.

    This is the fork's real regression net when rebasing upstream Newelle —
    a syntactic break is caught without needing GTK on CI.
    """
    files = sorted((ROOT / "src").rglob("*.py"))
    assert len(files) > 100, f"expected the full Newelle tree, found {len(files)} files"
    bad = []
    for f in files:
        try:
            ast.parse(f.read_text(encoding="utf-8", errors="replace"), filename=str(f))
        except SyntaxError as exc:
            bad.append(f"{f.relative_to(ROOT)}: {exc.msg} (line {exc.lineno})")
    assert not bad, "syntax errors:\n" + "\n".join(bad[:10])


def test_no_shesha_remnants_in_overlay() -> None:
    for f in OVERLAY.rglob("*"):
        if f.is_file():
            text = f.read_text(encoding="utf-8", errors="replace")
            assert "shesha" not in text.lower(), f"naming remnant in {f.name}"
    assert not (ROOT / "shesha-overlay").exists()


def test_readme_mentions_overlay_and_upstream_credit() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
    assert "shesh-overlay" in readme
    assert "Newelle" in readme  # upstream attribution must stay
