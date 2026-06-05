#!/usr/bin/env python3
"""Verify Claude and Codex plugin manifests stay aligned."""

from __future__ import annotations

import json
import logging
import re
import sys
from pathlib import Path
from typing import Any


LOGGER = logging.getLogger("verify-plugin-manifests")
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class ManifestError(ValueError):
    """Raised when a plugin manifest is missing required content."""


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from disk.

    Args:
        path: Manifest path to read.

    Returns:
        Parsed JSON object.

    Raises:
        ManifestError: If the file cannot be read, parsed, or is not an object.
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ManifestError(f"unable to read {path}: {exc}") from exc

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ManifestError(f"{path} is not valid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise ManifestError(f"{path} must contain a JSON object")
    return payload


def require_string(payload: dict[str, Any], key: str, label: str) -> str:
    """Return a required non-empty string field.

    Args:
        payload: Manifest object.
        key: Field name to read.
        label: Human-readable manifest label for errors.

    Returns:
        Field value.

    Raises:
        ManifestError: If the field is missing or not a non-empty string.
    """
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{label} field '{key}' must be a non-empty string")
    return value


def validate_common_manifest(payload: dict[str, Any], label: str) -> None:
    """Validate fields shared by Claude and Codex manifests.

    Args:
        payload: Manifest object.
        label: Human-readable manifest label for errors.

    Returns:
        None.

    Raises:
        ManifestError: If a shared required field is invalid.
    """
    name = require_string(payload, "name", label)
    version = require_string(payload, "version", label)
    require_string(payload, "description", label)

    author = payload.get("author")
    if not isinstance(author, dict):
        raise ManifestError(f"{label} field 'author' must be an object")
    require_string(author, "name", f"{label} author")

    if name != "human-training":
        raise ManifestError(f"{label} name must be 'human-training', got '{name}'")
    if SEMVER_RE.fullmatch(version) is None:
        raise ManifestError(f"{label} version must use strict semver, got '{version}'")


def validate_codex_manifest(payload: dict[str, Any], repo_root: Path) -> None:
    """Validate Codex-specific manifest fields.

    Args:
        payload: Codex manifest object.
        repo_root: Repository root for path checks.

    Returns:
        None.

    Raises:
        ManifestError: If Codex-specific fields are invalid.
    """
    skills_path = require_string(payload, "skills", "Codex manifest")
    if skills_path != "./skills/":
        raise ManifestError("Codex manifest field 'skills' must be './skills/'")
    if not (repo_root / "skills").is_dir():
        raise ManifestError("Codex manifest points at missing skills directory")

    interface = payload.get("interface")
    if not isinstance(interface, dict):
        raise ManifestError("Codex manifest field 'interface' must be an object")
    for key in (
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
    ):
        require_string(interface, key, "Codex manifest interface")


def verify(repo_root: Path) -> None:
    """Verify both plugin manifests.

    Args:
        repo_root: Repository root.

    Returns:
        None.

    Raises:
        ManifestError: If any manifest invariant fails.
    """
    claude = load_json(repo_root / ".claude-plugin" / "plugin.json")
    codex = load_json(repo_root / ".codex-plugin" / "plugin.json")

    validate_common_manifest(claude, "Claude manifest")
    validate_common_manifest(codex, "Codex manifest")
    validate_codex_manifest(codex, repo_root)

    claude_version = require_string(claude, "version", "Claude manifest")
    codex_version = require_string(codex, "version", "Codex manifest")
    if claude_version != codex_version:
        raise ManifestError(
            "plugin manifest versions must match: "
            f"Claude={claude_version}, Codex={codex_version}"
        )


def main(argv: list[str]) -> int:
    """Run manifest verification.

    Args:
        argv: Command-line arguments.

    Returns:
        Process exit code.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    repo_root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parents[1]

    LOGGER.info("Verifying plugin manifests in %s", repo_root)
    try:
        verify(repo_root)
    except ManifestError as exc:
        LOGGER.error("%s", exc)
        return 1

    LOGGER.info("Plugin manifests are valid and version-aligned.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
