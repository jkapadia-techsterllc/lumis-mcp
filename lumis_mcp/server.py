# Copyright (c) 2024-2026 Lumis AI. All rights reserved.
# Licensed under the Lumis AI Proprietary Software License. See LICENSE.
"""Lumis MCP Server — re-export for pip-installed package.

When installed via pip, the knowledge base lives alongside this file.
This module patches the BASE path and loads the real server logic.
"""

import importlib.util
import sys
from pathlib import Path

BASE = Path(__file__).parent
_repo_server = BASE.parent / "server.py"

if _repo_server.exists() and (BASE.parent / "knowledge").is_dir():
    spec = importlib.util.spec_from_file_location("_lumis_server", str(_repo_server))
    _mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_mod)
    mcp = _mod.mcp
else:
    sys.path.insert(0, str(BASE))
    spec = importlib.util.spec_from_file_location(
        "_lumis_server",
        str(BASE.parent / "server.py") if (BASE.parent / "server.py").exists() else str(BASE / "_server_stub.py"),
    )
    _mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_mod)
    mcp = _mod.mcp
