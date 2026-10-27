# Copyright (c) 2024-2026 Lumis AI. All rights reserved.
# Licensed under the Lumis AI Proprietary Software License. See LICENSE.
"""Lumis MCP Server — Life Sciences CRM Migration Intelligence."""

__version__ = "1.0.3"

import importlib.resources
import sys
from pathlib import Path


def _resolve_base() -> Path:
    """Resolve the base directory for knowledge, agents, and prompts.

    When pip-installed, the data is bundled inside the lumis_mcp package via
    hatch force-include. When running from a repo checkout, the data is at the
    repo root (one directory up from this file).
    """
    pkg_knowledge = Path(__file__).parent / "knowledge"
    if pkg_knowledge.is_dir():
        return Path(__file__).parent

    repo_root = Path(__file__).parent.parent
    if (repo_root / "knowledge").is_dir():
        return repo_root

    return Path(__file__).parent


def main():
    """Entry point for `lumis-mcp` console script and `uvx lumis-mcp`."""
    base = _resolve_base()

    sys.path.insert(0, str(base))

    if (base / "server.py").exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("server", str(base / "server.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.mcp.run()
    else:
        from lumis_mcp.server import mcp
        mcp.run()
