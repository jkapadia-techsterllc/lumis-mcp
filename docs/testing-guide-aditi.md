# Lumis MCP — Testing Guide

## Prerequisites

You need a Mac or Windows machine with internet access.

---

## Step 1: Create a Claude account

1. Go to **https://claude.ai** and sign up (use your Google account or email)
2. Subscribe to **Claude Pro** ($20/month) — this is required for MCP server support in Claude Desktop. You can cancel after testing.

## Step 2: Install Python

Check if you already have Python 3.10+:
- Open **Terminal** (Mac: Cmd+Space, type "Terminal")
- Type: `python3 --version`
- If it shows 3.10 or higher, skip to Step 3

If not installed:
1. Go to **https://python.org/downloads**
2. Download and install the latest version (3.12+)
3. Restart Terminal and verify with `python3 --version`

## Step 3: Install uv (Python package runner)

In Terminal, run:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close and reopen Terminal, then verify:
```bash
uvx --version
```

## Step 4: Install Claude Desktop

1. Go to **https://claude.ai/download**
2. Download and install the Claude Desktop app
3. Open it and sign in with your Claude account from Step 1

## Step 5: Configure Lumis MCP Server

1. In Claude Desktop, open **Settings**:
   - Mac: Claude menu → Settings (or Cmd+,)
   - Windows: File → Settings
2. Go to the **Developer** tab
3. Click **Edit Config**
4. This opens a JSON file. Replace its contents with:

```json
{
  "mcpServers": {
    "lumis": {
      "command": "uvx",
      "args": ["lumis-mcp"]
    }
  }
}
```

5. Save the file and **restart Claude Desktop** (Quit and reopen)

> **Note:** If you're using claude.ai (web app) instead of Claude Desktop, go to claude.ai → Settings → MCP Servers and add a new server with command `uvx` and args `lumis-mcp`. The web app handles MCP configuration differently than the desktop app.

## Step 6: Verify Lumis is connected

**Claude Desktop (native app):** When Claude Desktop restarts, you should see a small hammer/tools icon near the message input box. Click it — you should see 13 Lumis tools listed.

**claude.ai (web app):** If you're using claude.ai in a browser instead of the desktop app, there is no hammer icon. MCP tools still work — Claude will call them automatically when relevant. You'll see tool calls appear as collapsible sections in the response. If you've configured the MCP server correctly, the tools are connected even without a visible icon.

Either way, you should see these 13 Lumis tools:

- search_knowledge
- get_module_mapping
- get_gotchas
- traverse_decision_tree
- get_country_rules
- run_validation
- get_terminology
- get_agent_workflow
- assess_migration_readiness
- plan_multi_country_rollout
- compare_entities
- get_taxonomy
- plan_system_validation

If you don't see them, restart Claude Desktop one more time.

---

## Step 7: Warm-Up — Ask Some Natural Questions First

Before the formal tests, just have a conversation with Claude. These are questions a real user might ask when exploring Lumis for the first time. Ask them naturally — no special syntax needed.

**Getting started:**
> What is Lumis and what can it help me with?

**Explore what's in the knowledge base:**
> What life sciences CRM modules does Lumis know about?

**Ask a real-world question:**
> We're thinking about moving off our current CRM. What should we consider for sample management?

**Try a country-specific question:**
> What's different about running a pharma CRM in Germany vs the US?

**Ask about compliance:**
> What do I need to know about FDA 21 CFR Part 11 for a cloud CRM?

**Try a "help me decide" question:**
> Should we migrate all our CRM modules at once or do it in phases?

**Ask about common mistakes:**
> What are the most common things that go wrong in a life sciences CRM migration?

**Try a comparison:**
> How does consent management differ between Europe and Asia Pacific?

These should give you a feel for what Lumis knows and how Claude uses it. Then move on to the formal tests below.

---

## Step 8: Run the Formal Tests

Start a **new conversation** for each test. Copy-paste the prompt exactly. For each test, note:

- Did Claude show a tool call to Lumis? (you'll see a collapsible section showing the tool being called)
- Was the response relevant and structured?
- Any errors or empty results?
- Was it fast or slow?
- Any feedback on usefulness?

---

### Test 1 — Knowledge Search
**Prompt:**
> Search for sample management regulatory requirements in life sciences CRM

**Expected:** Returns knowledge entries about sample management compliance, FDA/PDMA rules, inventory tracking.

---

### Test 2 — Module Mapping
**Prompt:**
> What is the Salesforce Life Sciences Cloud equivalent of the legacy CRM call reporting module?

**Expected:** Returns the target module name, coverage level (full/partial/gap), and any known limitations.

---

### Test 3 — Gotchas
**Prompt:**
> What are the common pitfalls when migrating consent management to a new life sciences CRM?

**Expected:** Returns non-obvious issues, edge cases, and things that trip up migration teams.

---

### Test 4 — Decision Tree
**Prompt:**
> Help me choose between a big-bang migration and a phased migration for our CRM

**Expected:** Claude walks through a decision tree asking about your situation (number of countries, modules, risk tolerance) and gives a recommendation.

---

### Test 5 — Country Rules
**Prompt:**
> What are the regulatory rules for deploying a life sciences CRM in Japan?

**Expected:** Returns Japan-specific rules (APPI, PDMA, Transparency Guidelines), configuration requirements, and compliance notes.

---

### Test 6 — Validation
**Prompt:**
> We went live but users can't see account data. What could be wrong?

**Expected:** Returns potential validation issues — permission sets, sharing rules, data visibility settings, FLS — that commonly cause this symptom.

---

### Test 7 — Terminology
**Prompt:**
> What is the correct modern term for "call plan" in life sciences CRM?

**Expected:** Returns the correct terminology mapping, explaining the legacy vs. modern naming.

---

### Test 8 — Agent Workflow
**Prompt:**
> Show me the complete workflow for running a CRM migration

**Expected:** Returns the structured phases, steps, checklists, and milestones for an end-to-end migration.

---

### Test 9 — Migration Readiness Assessment
**Prompt:**
> Assess migration readiness for a mid-size pharma company: 500 sales reps across 12 countries, currently using a legacy CRM for call reporting, sample management, consent tracking, and medical inquiries

**Expected:** Returns a complexity score, module-by-module mapping, identified gaps and risks, and estimated timeline. This is the flagship tool.

---

### Test 10 — Multi-Country Rollout
**Prompt:**
> Plan a rollout across United States, Germany, Japan, and Brazil for a pharma CRM migration

**Expected:** Returns a wave-based rollout plan — which countries go in which wave, sequencing rationale, execution timeline, and risk warnings per country.

---

### Test 11 — Entity Comparison
**Prompt:**
> Compare GDPR and APPI regulations for life sciences CRM deployments

**Expected:** Side-by-side comparison of EU vs Japan privacy regulations, with implications for CRM configuration.

---

### Test 12 — Taxonomy
**Prompt:**
> Show me the complete Lumis knowledge taxonomy — what areas and categories are covered?

**Expected:** Returns the structured taxonomy tree — phases, areas, and knowledge categories across the entire knowledge base.

---

### Test 13 — System Validation Planning
**Prompt:**
> Plan a computer system validation for a cloud-based sample management system that needs to be FDA 21 CFR Part 11 compliant

**Expected:** Returns GAMP 5 classification, required validation deliverables (IQ/OQ/PQ), regulatory references, effort estimates, and gap areas.

---

## Bonus: Open-Ended Test

Try an unstructured question to see how Claude uses multiple Lumis tools together:

> We're a mid-size pharma moving from a legacy CRM to Salesforce. We have operations in the US, Germany, and Japan. Our biggest concerns are sample management compliance and consent tracking across different regulatory regimes. What should we know before starting?

**Expected:** Claude should combine multiple tools (knowledge search, country rules, gotchas, module mapping) to give a comprehensive answer.

---

## Reporting Results

Please share your findings in this format:

| Test # | Tool Called? | Response Quality (1-5) | Speed | Issues/Notes |
|--------|-------------|----------------------|-------|-------------|
| 1      | Yes/No      | 1-5                  | Fast/Slow | Any notes |
| 2      | ...         | ...                  | ...   | ...         |
| ...    | ...         | ...                  | ...   | ...         |

Plus any overall impressions:
- Was it easy to set up?
- Did the responses feel authoritative?
- Would this be useful in a real migration project?
- What's missing or could be better?

---

## Troubleshooting

**I don't see the hammer icon:**
- Make sure you're using the **Claude Desktop app**, not claude.ai in a browser. MCP tools only work with the hammer icon in the desktop app. On claude.ai (web), MCP tools work in the background without a visible icon — you'll see tool calls appear as collapsible sections in responses.
- Quit Claude Desktop completely (not just close the window) and reopen it.
- Check that the config file was saved correctly: on Mac, it's at `~/Library/Application Support/Claude/claude_desktop_config.json`.

**Tools show but Lumis returns errors:**
- Run `uvx lumis-mcp` in Terminal to test if the server starts. If it shows errors, try: `uv cache clean lumis-mcp` then restart Claude Desktop.
- If you recently updated, run `uv cache clean lumis-mcp` to force a fresh download of the latest version.

**Claude doesn't use Lumis tools:**
- Start your question with "Using Lumis," or mention "life sciences CRM" to help Claude recognize when to invoke the tools.
- In a new conversation, try: "What Lumis tools are available?" — Claude should list all 13.
- If using claude.ai (web), verify MCP is configured in Settings → MCP Servers.
