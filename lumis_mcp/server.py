# Copyright (c) 2024-2026 Lumis AI. All rights reserved.
# Licensed under the Lumis AI Proprietary Software License. See LICENSE.
"""Lumis MCP Server — re-export for pip-installed package.

When installed via pip, the knowledge base and server implementation live
alongside this file (copied by hatch force-include). This module detects
the environment and loads the real server logic from the right location.
"""

import importlib.util
import sys
from pathlib import Path

BASE = Path(__file__).parent
_repo_server = BASE.parent / "server.py"

if _repo_server.exists() and (BASE.parent / "knowledge").is_dir():
    # Running from a repo checkout — load the repo-root server.py directly
    spec = importlib.util.spec_from_file_location("_lumis_server", str(_repo_server))
    _mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_mod)
    mcp = _mod.mcp
else:
    # pip-installed — load _server_impl.py bundled by hatch force-include
    _impl = BASE / "_server_impl.py"
    if not _impl.exists():
        raise FileNotFoundError(
            f"Lumis server implementation not found at {_impl}. "
            "Reinstall with: pip install --force-reinstall lumis-mcp"
        )
    sys.path.insert(0, str(BASE))
    spec = importlib.util.spec_from_file_location("_lumis_server", str(_impl))
    _mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_mod)
    mcp = _mod.mcp
