#!/usr/bin/env python3
# Copyright (c) 2024-2026 Lumis AI. All rights reserved.
# Licensed under the Lumis AI Proprietary Software License. See LICENSE.
"""Lumis MCP Server — Life Sciences Intelligence across the pharma value chain."""

import json
import os
from pathlib import Path

import yaml
try:
    from mcp.server.fastmcp import FastMCP
except (ModuleNotFoundError, ImportError):
    from mcp.server.mcpserver import MCPServer as FastMCP

BASE = Path(__file__).parent
KNOWLEDGE = BASE / "knowledge"
FOUNDATION = KNOWLEDGE / "_foundation"
META = KNOWLEDGE / "_meta"
AGENTS = BASE / "agents"

mcp = FastMCP(
    "lumis",
    instructions=(
        "Lumis provides expert-level intelligence for life sciences implementations "
        "across the pharma value chain — from drug discovery through clinical development "
        "to commercialization (CRM, safety/PV, regulated content, market access). "
        "Use ONLY the knowledge returned by these tools to answer questions. "
        "Do not improvise or guess. If the knowledge base does not cover a topic, say so. "
        "Always cite the source entry for every factual claim."
    ),
)


def _load_taxonomy() -> dict:
    """Load the value chain taxonomy registry."""
    path = META / "value-chain.json"
    if path.exists():
        with open(path) as fh:
            return json.load(fh)
    return {}


def _load_dir(folder: Path) -> list[dict]:
    """Load all JSON and YAML files from a directory."""
    entries: list[dict] = []
    if not folder.exists():
        return entries
    for f in sorted(folder.iterdir()):
        if f.suffix == ".json":
            with open(f) as fh:
                data = json.load(fh)
                if isinstance(data, list):
                    entries.extend(data)
                else:
                    entries.append(data)
        elif f.suffix in (".yaml", ".yml"):
            with open(f) as fh:
                data = yaml.safe_load(fh)
                if isinstance(data, dict) and "rules" in data:
                    entries.extend(data["rules"])
                elif isinstance(data, list):
                    entries.extend(data)
                else:
                    entries.append(data)
    return entries


def _resolve_paths(phase: str, area: str, category: str) -> list[Path]:
    """Resolve knowledge paths for a phase/area/category query.

    Foundation knowledge is always included. Phase and area narrow the scope.
    """
    paths: list[Path] = []

    # Foundation always included
    if category == "all":
        for subdir in FOUNDATION.iterdir():
            if subdir.is_dir():
                paths.append(subdir)
    else:
        foundation_path = FOUNDATION / category
        if foundation_path.exists():
            paths.append(foundation_path)

    # If phase is "all" or "foundation", we scan everything (or just foundation)
    if phase == "foundation":
        return paths

    # Scope to phase/area
    if phase == "all":
        for phase_dir in KNOWLEDGE.iterdir():
            if phase_dir.is_dir() and not phase_dir.name.startswith("_"):
                if area == "all":
                    for area_dir in phase_dir.iterdir():
                        if area_dir.is_dir():
                            if category == "all":
                                for cat_dir in area_dir.iterdir():
                                    if cat_dir.is_dir():
                                        paths.append(cat_dir)
                            else:
                                cat_path = area_dir / category
                                if cat_path.exists():
                                    paths.append(cat_path)
                else:
                    area_dir = phase_dir / area
                    if area_dir.exists():
                        if category == "all":
                            for cat_dir in area_dir.iterdir():
                                if cat_dir.is_dir():
                                    paths.append(cat_dir)
                        else:
                            cat_path = area_dir / category
                            if cat_path.exists():
                                paths.append(cat_path)
    else:
        phase_dir = KNOWLEDGE / phase
        if phase_dir.exists():
            if area == "all":
                for area_dir in phase_dir.iterdir():
                    if area_dir.is_dir():
                        if category == "all":
                            for cat_dir in area_dir.iterdir():
                                if cat_dir.is_dir():
                                    paths.append(cat_dir)
                        else:
                            cat_path = area_dir / category
                            if cat_path.exists():
                                paths.append(cat_path)
            else:
                area_dir = phase_dir / area
                if area_dir.exists():
                    if category == "all":
                        for cat_dir in area_dir.iterdir():
                            if cat_dir.is_dir():
                                paths.append(cat_dir)
                    else:
                        cat_path = area_dir / category
                        if cat_path.exists():
                            paths.append(cat_path)

    return paths


def _load_scoped(phase: str = "all", area: str = "all", category: str = "all") -> list[dict]:
    """Load knowledge entries scoped by phase, area, and category."""
    entries: list[dict] = []
    for path in _resolve_paths(phase, area, category):
        entries.extend(_load_dir(path))
    return entries


def _search(entries: list[dict], query: str, limit: int = 5) -> list[dict]:
    """Simple keyword search — returns entries whose text contains query terms."""
    query_terms = query.lower().split()
    scored = []
    for entry in entries:
        text = json.dumps(entry).lower()
        score = sum(1 for term in query_terms if term in text)
        if score > 0:
            scored.append((score, entry))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [e for _, e in scored[:limit]]


# ─── Tools ─────────────────────────────────────────────

@mcp.tool()
def get_taxonomy() -> str:
    """Get the Lumis value chain taxonomy — phases, areas, and available knowledge categories.

    Call this first to understand what domains Lumis covers and how knowledge is organized.
    """
    taxonomy = _load_taxonomy()
    phases = taxonomy.get("phases", [])
    summary = []
    for phase in phases:
        areas = phase.get("areas", [])
        area_names = [f"{a['name']} ({a['status']})" for a in areas]
        summary.append({
            "phase": phase["name"],
            "id": phase["id"],
            "status": phase["status"],
            "areas": area_names,
        })
    return json.dumps({
        "taxonomy": summary,
        "foundation": taxonomy.get("foundation", {}),
        "usage": "Pass phase and area IDs to other tools to scope your queries. Foundation knowledge is always included.",
    })


@mcp.tool()
def search_knowledge(
    query: str,
    phase: str = "all",
    area: str = "all",
    category: str = "all",
    limit: int = 5,
) -> str:
    """Search the Lumis knowledge base across the life sciences value chain.

    Foundation knowledge (org strategy, regulatory, terminology) is always included.
    Use phase and area to narrow scope.

    Args:
        query: Natural language search query
        phase: Value chain phase — 'discovery', 'clinical', 'commercialization', 'foundation', or 'all'
        area: Area within phase — e.g. 'crm', 'safety-pv', 'regulated-content', 'market-access', or 'all'
        category: Knowledge category — 'modules', 'decision-trees', 'gotchas', 'country-rules',
                  'validation-rules', 'terminology', 'org-strategy', or 'all'
        limit: Maximum results to return (default 5)
    """
    entries = _load_scoped(phase, area, category)

    if not entries:
        return json.dumps({
            "results": [],
            "note": f"No knowledge found for phase={phase}, area={area}, category={category}.",
        })

    results = _search(entries, query, limit)
    return json.dumps({
        "results": results,
        "total_entries": len(entries),
        "scope": {"phase": phase, "area": area, "category": category},
        "query": query,
    })


@mcp.tool()
def get_module_mapping(source_module: str, area: str = "crm") -> str:
    """Get the target platform equivalent for a source module.

    Args:
        source_module: The source module name (e.g. 'CLM', 'Legacy Events', 'AE Reporting')
        area: Which area to search — 'crm', 'safety-pv', 'regulated-content', etc. (default 'crm')
    """
    entries = _load_scoped(phase="commercialization", area=area, category="modules")
    results = _search(entries, source_module, limit=3)
    if not results:
        return json.dumps({
            "error": f"No mapping found for '{source_module}' in {area}",
            "suggestion": "Try search_knowledge with broader terms or a different area.",
        })
    return json.dumps({"mappings": results})


@mcp.tool()
def get_gotchas(
    module: str = "",
    country: str = "",
    phase: str = "all",
    area: str = "all",
) -> str:
    """Get non-obvious pitfalls and gotchas for a module, country, or domain area.

    Args:
        module: Filter by module name (optional)
        country: Filter by country (optional)
        phase: Value chain phase filter (default 'all')
        area: Area filter — 'crm', 'safety-pv', etc. (default 'all')
    """
    entries = _load_scoped(phase, area, category="gotchas")
    query = f"{module} {country}".strip()
    if not query:
        return json.dumps({"gotchas": entries[:10], "total": len(entries)})
    results = _search(entries, query, limit=10)
    return json.dumps({"gotchas": results, "query": query})


@mcp.tool()
def traverse_decision_tree(
    tree_name: str,
    inputs: str,
    phase: str = "all",
    area: str = "all",
) -> str:
    """Walk a decision tree given user inputs to produce a recommendation.

    Args:
        tree_name: Name of the decision tree (e.g. 'module-selection', 'migration-path', 'org-strategy')
        inputs: JSON string of input parameters for the tree
        phase: Value chain phase filter (default 'all')
        area: Area filter (default 'all')
    """
    entries = _load_scoped(phase, area, category="decision-trees")
    results = _search(entries, tree_name, limit=1)
    if not results:
        return json.dumps({"error": f"Decision tree '{tree_name}' not found."})

    tree = results[0]
    try:
        user_inputs = json.loads(inputs) if isinstance(inputs, str) else inputs
    except json.JSONDecodeError:
        user_inputs = {"raw": inputs}

    return json.dumps({
        "tree": tree.get("name", tree_name),
        "inputs": user_inputs,
        "nodes": tree.get("nodes", []),
        "recommendation": tree.get("default_recommendation", "Follow the decision nodes with your specific inputs."),
        "citation": tree.get("citation", {}),
    })


@mcp.tool()
def get_country_rules(
    country: str,
    module: str = "",
    phase: str = "all",
    area: str = "all",
) -> str:
    """Get regulatory and configuration rules for a specific country.

    Foundation rules (GDPR, APPI, data residency) are always included.
    Use area to add domain-specific rules (e.g. 'safety-pv' for adverse event reporting timelines).

    Args:
        country: Country name or code (e.g. 'Germany', 'DE', 'Japan')
        module: Optional module filter (e.g. 'Sample Management', 'AE Reporting')
        phase: Value chain phase filter (default 'all')
        area: Area filter (default 'all')
    """
    entries = _load_scoped(phase, area, category="country-rules")
    query = f"{country} {module}".strip()
    results = _search(entries, query, limit=10)
    return json.dumps({"country": country, "rules": results})


@mcp.tool()
def run_validation(
    rule_id: str = "",
    symptom: str = "",
    area: str = "crm",
) -> str:
    """Run a validation rule or find rules matching a reported symptom.

    Args:
        rule_id: Specific rule ID to run (optional)
        symptom: User-reported problem to match against rules (optional)
        area: Area to validate — 'crm', 'safety-pv', etc. (default 'crm')
    """
    entries = _load_scoped(phase="commercialization", area=area, category="validation-rules")
    query = rule_id or symptom
    if not query:
        return json.dumps({"rules": entries[:5], "total": len(entries), "note": "Provide a rule_id or symptom to filter."})
    results = _search(entries, query, limit=5)
    return json.dumps({"matched_rules": results, "query": query})


@mcp.tool()
def get_terminology(term: str = "") -> str:
    """Look up correct vs incorrect terminology to avoid hallucinations.

    Args:
        term: Term to look up (e.g. 'CLM', 'Approved Email', 'ICSR', 'CIOMS')
    """
    entries = _load_scoped(phase="foundation", category="terminology")
    if not term:
        return json.dumps({"terminology": entries, "total": len(entries)})
    results = _search(entries, term, limit=5)
    return json.dumps({"terminology": results, "query": term})


@mcp.tool()
def get_agent_workflow(agent: str) -> str:
    """Get the workflow, phases, and checklists for a specific Lumis agent.

    Args:
        agent: Agent name — 'migration', 'implementation', 'audit', or 'operations'
    """
    workflow = _load_agent(agent)
    if not workflow:
        available = [d.name for d in AGENTS.iterdir() if d.is_dir() and (d / "workflow.json").exists()]
        return json.dumps({"error": f"Agent '{agent}' not found.", "available": available})
    return json.dumps(workflow)


def _load_agent(agent_name: str) -> dict | None:
    """Load an agent's workflow definition."""
    path = AGENTS / agent_name / "workflow.json"
    if path.exists():
        with open(path) as fh:
            return json.load(fh)
    return None


@mcp.tool()
def assess_migration_readiness(
    source_platform: str,
    modules_in_use: str,
    country_count: int,
    user_count: int,
    area: str = "crm",
) -> str:
    """Run a migration readiness assessment for any commercialization area.

    Args:
        source_platform: Current platform (e.g. 'Legacy CRM', 'Argus Safety', 'Veeva Vault')
        modules_in_use: Comma-separated list of modules currently in use
        country_count: Number of countries in scope
        user_count: Approximate number of users
        area: Commercialization area — 'crm', 'safety-pv', 'regulated-content' (default 'crm')
    """
    modules = [m.strip() for m in modules_in_use.split(",")]
    module_entries = _load_scoped(phase="commercialization", area=area, category="modules")
    gotcha_entries = _load_scoped(phase="commercialization", area=area, category="gotchas")

    mapped = []
    gaps = []
    for mod in modules:
        results = _search(module_entries, mod, limit=1)
        if results:
            entry = results[0]
            mapped.append({
                "source": mod,
                "target": entry.get("target_module", "See mapping"),
                "coverage": entry.get("coverage", "Unknown"),
                "gaps": entry.get("gaps", []),
            })
            gaps.extend(entry.get("gaps", []))
        else:
            gaps.append(f"No mapping found for {mod}")

    relevant_gotchas = _search(gotcha_entries, " ".join(modules), limit=5)
    complexity = min(10, 2 + len(modules) + (country_count // 5) + (1 if user_count > 1000 else 0))

    return json.dumps({
        "assessment": {
            "source_platform": source_platform,
            "area": area,
            "complexity_score": f"{complexity}/10",
            "modules_assessed": len(modules),
            "module_mappings": mapped,
            "top_gaps": gaps[:5],
            "top_risks": [g.get("title", g) if isinstance(g, dict) else g for g in relevant_gotchas[:5]],
            "estimated_timeline": f"{6 + country_count}–{12 + country_count * 2} months",
            "recommendation": "Unlock the full migration blueprint with a Lumis subscription.",
        },
        "citation": {"source": "Lumis Migration Readiness Assessment v1"},
    })


@mcp.tool()
def plan_multi_country_rollout(
    country_count: int,
    modules: str,
    regions: str,
    includes_us: bool = False,
    includes_japan: bool = False,
    area: str = "crm",
) -> str:
    """Plan a wave-based multi-country rollout for any commercialization area.

    Args:
        country_count: Total countries in scope
        modules: Comma-separated list of modules to deploy
        regions: Comma-separated regions in scope (e.g. 'EU, Americas, APAC, LATAM')
        includes_us: Whether the US is in scope (adds regulatory complexity)
        includes_japan: Whether Japan is in scope (requires standalone wave)
        area: Commercialization area — 'crm', 'safety-pv', 'regulated-content' (default 'crm')
    """
    mod_list = [m.strip() for m in modules.split(",")]
    region_list = [r.strip().upper() for r in regions.split(",")]
    region_count = len(region_list)

    if country_count <= 5 and region_count == 1:
        wave_count = 1
    elif country_count <= 15:
        wave_count = 2 if not (includes_us and includes_japan) else 3
    elif country_count <= 30:
        wave_count = 3 if not (includes_us and includes_japan) else 4
    elif country_count <= 50:
        wave_count = 4 if not (includes_us and includes_japan) else 5
    else:
        wave_count = 5

    base_months_per_wave = 7
    module_adder = max(0, (len(mod_list) - 3)) * 1
    gap_months = 3
    total_months = (wave_count * (base_months_per_wave + module_adder)) + ((wave_count - 1) * gap_months)

    clustering = _search(_load_scoped(phase="all", category="country-rules"), "country clustering regional", limit=2)
    sequencing = _search(_load_scoped(phase="all", category="country-rules"), "wave sequencing rules", limit=1)
    timeline = _search(_load_scoped(phase="commercialization", area=area, category="modules"), "wave execution timeline sprint", limit=2)
    anti_patterns = _search(_load_scoped(phase="all", category="country-rules"), "anti-patterns rollout planning", limit=1)
    tree = _search(_load_scoped(phase="all", category="decision-trees"), "multi-country rollout planner", limit=1)

    complexity = min(10, 2 + len(mod_list) + (country_count // 10) + (2 if includes_us else 0) + (2 if includes_japan else 0))

    plan = {
        "rollout_plan": {
            "country_count": country_count,
            "modules": mod_list,
            "regions": region_list,
            "area": area,
            "includes_us": includes_us,
            "includes_japan": includes_japan,
            "complexity_score": f"{complexity}/10",
            "recommended_waves": wave_count,
            "estimated_duration_months": f"{total_months - 4}–{total_months + 4}",
            "key_rules": [
                "Japan is ALWAYS a standalone wave" if includes_japan else None,
                "US must NOT be Wave 1 — defer to Wave 2+" if includes_us else None,
                "Never combine US and Japan in the same wave" if includes_us and includes_japan else None,
                "LATAM should be the last wave" if "LATAM" in region_list else None,
                f"Minimum 3-month gap between waves",
                f"Sub-wave spacing: minimum 6 weeks apart for {country_count}+ country programs" if country_count > 10 else None,
                "Pilot 3-5 diverse countries in Wave 1 sub-wave 1a",
            ],
            "regional_clusters": clustering,
            "sequencing_guidance": sequencing,
            "wave_execution_template": timeline,
            "anti_patterns_to_avoid": anti_patterns,
            "decision_tree": tree[0] if tree else None,
        },
        "citation": {"source": "Lumis Multi-Country Rollout Planner v1"},
    }
    plan["rollout_plan"]["key_rules"] = [r for r in plan["rollout_plan"]["key_rules"] if r]
    return json.dumps(plan)


@mcp.tool()
def compare_entities(
    entity_a: str,
    entity_b: str,
    dimension: str = "",
    phase: str = "all",
    area: str = "all",
) -> str:
    """Compare two entities side-by-side — countries, modules, regulatory frameworks, or any knowledge base entries.

    Args:
        entity_a: First entity to compare (e.g. 'Germany', 'CLM', 'Argus')
        entity_b: Second entity to compare (e.g. 'France', 'Events', 'Vault Safety')
        dimension: Optional focus dimension (e.g. 'sample rules', 'field mapping', 'regulatory')
        phase: Value chain phase filter (default 'all')
        area: Area filter (default 'all')
    """
    all_entries = _load_scoped(phase, area)

    query_a = f"{entity_a} {dimension}".strip()
    query_b = f"{entity_b} {dimension}".strip()

    results_a = _search(all_entries, query_a, limit=5)
    results_b = _search(all_entries, query_b, limit=5)

    shared_query = f"{entity_a} {entity_b} {dimension}".strip()
    shared_results = _search(all_entries, shared_query, limit=3)

    return json.dumps({
        "comparison": {
            "entity_a": entity_a,
            "entity_b": entity_b,
            "dimension": dimension or "all",
            "scope": {"phase": phase, "area": area},
            "entity_a_findings": results_a,
            "entity_b_findings": results_b,
            "cross_references": shared_results,
            "instruction": "Compare the findings above. Highlight differences, similarities, and which entity is more complex or restrictive for the given dimension.",
        },
        "citation": {"source": "Lumis Comparison Engine v1"},
    })


@mcp.tool()
def plan_system_validation(
    system_name: str,
    system_type: str,
    platform: str = "",
    regulatory_geography: str = "US",
    gxp_context: str = "",
    modules_in_use: str = "",
    has_mobile: bool = False,
    has_integrations: bool = False,
    has_custom_code: bool = False,
    user_count: int = 0,
    country_count: int = 1,
) -> str:
    """Plan a computer system validation (CSV/CSA) for a life sciences system.

    Returns applicable regulations, methodology recommendation, GAMP classification,
    deliverables list, effort estimate, gap assessment areas, and decision tree guidance.

    This tool supports planning for 21 CFR Part 11, EU Annex 11, GAMP 5, and related
    regulatory requirements across CRM, clinical, safety, and manufacturing systems.

    Args:
        system_name: Name of the system being validated (e.g. 'Salesforce CRM', 'Veeva Vault', 'SAP QM')
        system_type: Type of system — 'saas', 'cots', 'configured', 'custom', 'hybrid'
        platform: Platform vendor if applicable (e.g. 'Salesforce', 'Veeva', 'SAP', 'Oracle')
        regulatory_geography: Jurisdiction — 'US', 'EU', 'Japan', 'Global', 'WHO' (default 'US')
        gxp_context: GxP context — 'GMP', 'GCP', 'GLP', 'GPvP', 'GDP', or comma-separated combo
        modules_in_use: Comma-separated modules (e.g. 'Sample Management, Events, Consent')
        has_mobile: Whether mobile/offline is in scope (adds validation complexity)
        has_integrations: Whether system integrations are in scope
        has_custom_code: Whether custom code (e.g. Apex, custom middleware) exists
        user_count: Approximate number of users
        country_count: Number of countries in scope
    """
    validation_entries = _load_dir(FOUNDATION / "validation")

    gxp_list = [g.strip() for g in gxp_context.split(",") if g.strip()] if gxp_context else []
    mod_list = [m.strip() for m in modules_in_use.split(",") if m.strip()] if modules_in_use else []

    # --- GAMP classification ---
    if system_type in ("custom",):
        gamp_category = "Category 5 — Custom Application"
    elif system_type in ("cots",):
        gamp_category = "Category 3 — Non-Configured Product (COTS)"
    elif has_custom_code:
        gamp_category = "Category 4 (configured) + Category 5 (custom code components)"
    else:
        gamp_category = "Category 4 — Configured Product"

    # --- Applicable regulations ---
    regulations = ["21 CFR Part 11 (Electronic Records / Electronic Signatures)"]
    if regulatory_geography in ("EU", "Global"):
        regulations.append("EU Annex 11 (Computerised Systems)")
    if regulatory_geography in ("Japan", "Global"):
        regulations.append("Japan MHLW ERES Guidelines")
    if "GMP" in gxp_list:
        regulations.extend(["21 CFR Parts 210/211 (cGMP)", "EU GMP Volume 4"])
    if "GCP" in gxp_list:
        regulations.extend(["ICH E6(R2) (Good Clinical Practice)", "EU CTR 536/2014"])
    if "GLP" in gxp_list:
        regulations.append("21 CFR Part 58 (Good Laboratory Practice)")
    if "GPvP" in gxp_list:
        regulations.extend(["ICH E2B(R3)", "EU GVP Module I"])
    if "GDP" in gxp_list:
        regulations.append("EU GDP Guidelines (2013/C 343/01)")
    regulations.append("ISPE GAMP 5 Second Edition (2022)")

    # --- Methodology recommendation ---
    geo = regulatory_geography.upper()
    if geo == "US":
        methodology = "CSA (Computer Software Assurance) — FDA's risk-based approach"
        methodology_detail = "FDA actively encourages CSA. Use risk-based tiered testing: scripted for high-risk, unscripted for medium-risk, verification for low-risk."
    elif geo == "EU":
        methodology = "Hybrid CSV/CSA — CSA risk tiers with Annex 11-compliant documentation"
        methodology_detail = "Apply CSA risk assessment to determine testing depth, but maintain formal validation documentation for GMP-critical functions per EU Annex 11 expectations."
    elif geo == "JAPAN":
        methodology = "Traditional CSV — PMDA expects comprehensive documentation"
        methodology_detail = "PMDA currently expects traditional CSV with comprehensive validation documentation. CSA is not yet widely accepted by PMDA inspectors."
    elif geo == "GLOBAL":
        methodology = "Hybrid CSV/CSA (Global) — strictest-jurisdiction documentation"
        methodology_detail = "Use CSA risk assessment to drive testing depth, but maintain CSV-style documentation for all GxP-critical functions to satisfy FDA, EMA, and PMDA expectations."
    else:
        methodology = "Traditional CSV per GAMP 5"
        methodology_detail = "Default to traditional CSV for jurisdictions where CSA acceptance is uncertain."

    # --- Deliverables ---
    deliverables = [
        "Validation Plan (VP)",
        "User Requirements Specification (URS)",
        "Functional Risk Assessment (FRA)",
        "Traceability Matrix (RTM)",
        "IQ Protocol & Report (Installation Qualification)",
        "OQ Protocol & Report (Operational Qualification)",
        "PQ Protocol & Report (Performance Qualification / UAT)",
        "Validation Summary Report (VSR)",
        "Vendor Assessment Report",
    ]
    if has_mobile:
        deliverables.extend([
            "Mobile Validation Addendum (offline sync, timestamp integrity, signature capture)",
            "Real-Device Test Protocol",
        ])
    if has_integrations:
        deliverables.append("Integration Validation Protocol (per integration point)")
    if has_custom_code:
        deliverables.extend([
            "Design Specification (for custom code)",
            "Code Review Documentation",
            "Unit Test Documentation",
        ])
    if country_count > 1:
        deliverables.append("Multi-Country Regulatory Matrix")
    if system_type in ("cots", "saas"):
        deliverables.extend([
            "System Configuration Documentation",
            "Release Assessment Procedure (vendor release impact evaluation)",
            "Periodic Review Schedule (annual at minimum)",
            "System Retirement Plan (data archival and decommissioning)",
        ])

    # --- Effort estimate ---
    if len(mod_list) <= 10 and country_count == 1:
        effort_range = "2–3 months"
        team_size = "2–3 people"
        complexity = "Small"
    elif len(mod_list) <= 20 and country_count <= 15:
        effort_range = "4–6 months"
        team_size = "3–5 people"
        complexity = "Medium"
    else:
        effort_range = "6–12 months"
        team_size = "5–8 people"
        complexity = "Large"

    if has_mobile:
        effort_range += " (+1–2 months for mobile validation)"
    if has_integrations:
        effort_range += " (+1–2 weeks per integration point)"

    # --- Gap assessment areas ---
    gap_areas = [
        "Access Controls (Part 11.10(d), Annex 11 §12)",
        "Audit Trail (Part 11.10(e), Annex 11 §9)",
        "Electronic Signatures (Part 11.50/70/100/200)",
        "Data Integrity (ALCOA+ principles)",
        "Change Control (Part 11.10(k)(2), Annex 11 §10)",
        "Training (Part 11.10(i), Annex 11 §2)",
        "Periodic Review (Annex 11 §11)",
        "Backup & Recovery",
    ]

    platform_specific_gaps = []
    platform_part11_mapping = None
    if platform.lower() in ("salesforce", "sfdc"):
        platform_specific_gaps = [
            "Field History Tracking limited to 20 fields per object — plan custom audit trail for additional fields",
            "Setup Audit Trail retains only 180 days — implement external archival for regulatory retention",
            "No native 'reason for change' capture — requires custom Lightning component",
            "Salesforce does NOT provide Part 11 compliance certification — customer responsibility",
            "Shield Event Monitoring recommended for comprehensive audit coverage",
        ]
        platform_part11_mapping = {
            "§11.10(a) Validation": {
                "platform_provides": "Audit logs, NTP-synchronized timestamps, change-history tracking on platform metadata",
                "customer_must": "Validate your specific configuration, custom code, and business processes — platform validation ≠ system validation",
            },
            "§11.10(b) Copies": {
                "platform_provides": "Reporting, CSV/PDF/XML export, locked reports for immutable copies",
                "customer_must": "Ensure exports include all GxP-critical fields plus audit trail data; verify export completeness",
            },
            "§11.10(c) Protection": {
                "platform_provides": "Secure multitenant database, backup and DR, customer-controlled record deletion policies",
                "customer_must": "Implement data retention/disposition policies and document deletion controls for GxP records",
            },
            "§11.10(d) Access": {
                "platform_provides": "Unique user sign-in, role-based profiles, login history logging, account lockout after failed attempts",
                "customer_must": "Establish access review SOPs (at least annual), document role assignments, ensure no shared accounts",
            },
            "§11.10(e) Audit Trails": {
                "platform_provides": "Field History Tracking (20-field limit per object!), Setup Audit Trail (180-day retention!), creation/edit timestamps",
                "customer_must": "Implement custom audit trail or Salesforce Shield for full field coverage beyond 20-field limit; archive Setup Audit Trail beyond 180 days",
            },
            "§11.10(f) Operational Checks": {
                "platform_provides": "Workflow rules and approval processes enforce sequence of operations",
                "customer_must": "Design and validate workflow sequences for GxP-critical processes; document sequence enforcement logic",
            },
            "§11.10(g) Authority": {
                "platform_provides": "Encrypted passwords, password complexity/aging/recycling policies, account lockout, idle session timeout, SSO/SAML",
                "customer_must": "Configure and document password policies; implement written security policy enforcement; enable MFA for GxP users",
            },
            "§11.10(h) Device Checks": {
                "platform_provides": "Session ID + client ID tracking, IP range restrictions (Login IP Ranges), trusted IP ranges",
                "customer_must": "Configure IP restrictions for GxP environments; document trusted network policies",
            },
            "§11.10(i) Training": {
                "platform_provides": "Salesforce offers platform training (Trailhead, certification)",
                "customer_must": "Maintain training records for all GxP system users; re-train on system updates; document training on e-signature legal significance",
            },
            "§11.10(j) Policies": {
                "platform_provides": "N/A — this is entirely a customer responsibility",
                "customer_must": "Establish and maintain admin and end-user policies covering electronic record and signature accountability",
            },
            "§11.10(k) Documentation": {
                "platform_provides": "Salesforce maintains platform documentation with revision/change control",
                "customer_must": "Maintain customer-specific system documentation (SOPs, configuration docs, validation deliverables) under change control",
            },
            "§11.30 Open Systems": {
                "platform_provides": "HTTPS encryption, authentication, session management — Salesforce is typically a CLOSED system per §11.3",
                "customer_must": "Assess whether premier support login-as access makes the system 'open'; if so, apply additional §11.30 controls (encryption, digital signatures, integrity checks)",
            },
            "§11.50 Signatures": {
                "platform_provides": "Signer name, date/time, and meaning can be displayed; AppExchange components for digital signatures",
                "customer_must": "Implement e-signature capture (via AppExchange or custom) with signer name, date/time, meaning; ensure signatures are bound to their records per §11.70",
            },
            "§11.100 General": {
                "platform_provides": "Unique user IDs, password-based authentication",
                "customer_must": "Certify to FDA that electronic signatures are legally binding equivalents of handwritten signatures (one-time letter)",
            },
        }

    # --- Revalidation triggers ---
    revalidation_triggers = [
        "Major vendor version upgrades (e.g. Salesforce seasonal releases affecting GxP functions)",
        "Major infrastructure changes (e.g. data center migration, cloud region change)",
        "GxP scope changes (e.g. system re-categorized as GxP, new GxP modules added)",
        "Regulatory changes (e.g. new FDA guidance, updated EU Annex 11 requirements)",
        "Significant configuration changes (e.g. new objects, workflows, integrations affecting GxP functions)",
        "Retrospective validation needs (e.g. existing system newly classified as GxP)",
    ]

    # --- Risk assessment framework (inline) ---
    risk_assessment = {
        "approach": "two-tier",
        "tier_1_system_level": {
            "purpose": "Classify the overall system as Direct Impact, Indirect Impact, or No Impact",
            "severity_factors": ["GxP Impact", "Business Impact", "Compliance Impact", "System Scope"],
            "probability_factors": ["Complexity", "Product Maturity"],
            "override_rule": "High GxP impact automatically results in High overall severity regardless of other factors",
        },
        "tier_2_requirement_level": {
            "purpose": "Assess each functional requirement/sub-process individually to determine testing intensity",
            "severity_factors": ["GxP Impact", "Compliance Impact", "Business Impact", "Probability of Avoiding Detection"],
            "probability_factors": ["Complexity", "Component Maturity"],
            "detectability_note": "Adds FMEA-style detectability dimension not present in Tier 1 — a fault with no error trapping escalates to High even if other factors are moderate",
        },
        "risk_matrix_3x3": {
            "Low_Low": "Low", "Low_Med": "Low", "Low_High": "Medium",
            "Med_Low": "Low", "Med_Med": "Medium", "Med_High": "High",
            "High_Low": "Medium", "High_Med": "High", "High_High": "High",
        },
        "risk_to_testing": {
            "High": "Full IQ/OQ/PQ — every requirement traced and tested with prescriptive expected results, boundary and negative testing",
            "Medium": "OQ/PQ — key functions tested with representative data, negative testing on critical paths only",
            "Low": "PQ or verification — golden path testing with spot checks on configuration",
        },
        "mitigation_table_required": True,
        "mitigation_columns": ["Risk #", "Identified Hazard", "Pre-Mitigation Severity", "System Design Controls", "Procedural Controls", "Other Controls", "Residual Risk", "Document Traceability"],
    }

    # --- Record retention ---
    record_retention = "Validation deliverables must be retained for at least product life + 10 years per regulatory expectations. Store in a document repository with change control."

    # --- Search for relevant knowledge ---
    reg_results = _search(validation_entries, f"regulation {regulatory_geography} {' '.join(gxp_list)}", limit=3)
    method_results = _search(validation_entries, f"{methodology} GAMP validation lifecycle", limit=2)
    planning_results = _search(validation_entries, "validation plan deliverables URS traceability", limit=2)
    risk_results = _search(validation_entries, "risk assessment severity probability mitigation", limit=2)
    faq_results = _search(validation_entries, f"{platform} {system_type} validation", limit=3)

    plan = {
        "validation_plan": {
            "system": system_name,
            "system_type": system_type,
            "platform": platform or "Not specified",
            "gamp_classification": gamp_category,
            "regulatory_geography": regulatory_geography,
            "gxp_context": gxp_list or ["Not specified — recommend conducting Initial Risk Assessment"],
            "applicable_regulations": regulations,
            "methodology": {
                "recommendation": methodology,
                "detail": methodology_detail,
            },
            "deliverables": deliverables,
            "effort_estimate": {
                "complexity": complexity,
                "duration": effort_range,
                "team_size": team_size,
                "csa_discount": "CSA reduces effort 30–50% for medium/low-risk functions vs traditional CSV",
            },
            "gap_assessment_areas": gap_areas,
            "platform_specific_gaps": platform_specific_gaps or None,
            "risk_assessment_framework": risk_assessment,
            "platform_part11_mapping": platform_part11_mapping,
            "record_retention": record_retention,
            "revalidation_triggers": revalidation_triggers,
            "scope_flags": {
                "mobile_offline": has_mobile,
                "integrations": has_integrations,
                "custom_code": has_custom_code,
                "multi_country": country_count > 1,
                "modules_count": len(mod_list),
                "user_count": user_count,
                "country_count": country_count,
            },
            "key_recommendations": [
                "Start validation planning at the BEGINNING of the implementation — not at the end",
                "Embed the validation team in the project from Day 1",
                "QA must be independent of the project delivery team",
                "Use risk assessment to drive testing depth — not one-size-fits-all scripted testing",
                "Plan for vendor release assessments — Salesforce releases 3x/year" if platform.lower() in ("salesforce", "sfdc") else "Plan for vendor release impact assessments",
                "Include periodic review (annual) in your validation lifecycle from the start",
            ],
        },
        "supporting_knowledge": {
            "applicable_regulations": reg_results,
            "methodology_guidance": method_results,
            "planning_templates": planning_results,
            "risk_assessment_guidance": risk_results,
            "relevant_faq": faq_results,
        },
        "next_steps": [
            "1. Conduct Initial Risk Assessment (IRA) to confirm GxP classification",
            "2. Perform Vendor Assessment of the platform vendor",
            "3. Write the Validation Plan (VP) for this specific system",
            "4. Develop User Requirements Specification (URS) with business SMEs",
            "5. Conduct Functional Risk Assessment (FRA) to classify each function by GxP risk",
            "6. Use 'search_knowledge' with query='gap assessment' for the Part 11/Annex 11 checklist",
            "7. Use 'traverse_decision_tree' with tree_name='system-validation-scope' to walk the scoping decision tree",
        ],
        "citation": {"source": "Lumis System Validation Planner v1"},
    }

    return json.dumps(plan)


if __name__ == "__main__":
    mcp.run()
