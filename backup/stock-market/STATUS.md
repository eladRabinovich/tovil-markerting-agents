# STATUS — Stock-Market Agent Fleet (TAF)

Handover note. A fresh session starts here. Keep it short; update at the end of each work block.

_Last updated: 2026-10-22 (evening)_

## Phase

1 of 4: **Base + infrastructure** → 2. agent design & data sources → 3. production (scheduled runs) → 4. operations.

## Done (2026-10-22)

- Folder structure copied from `~/Playground/tovil-markerting-agents` (`.claude/{agents,commands,rules,skills,hooks}`, `docs/`, `research/`, `CLAUDE.md`, `STATUS.md`, `.mcp.json`).
- `CLAUDE.md`: project router. Identity **TAF** (`docs/taf-identity.md`); token practices copied and adapted (`docs/token-economy-practices.md`).
- Sources saved: `finance-agents-post-raw.txt` (post transcript), `finance-agents-prompts-notion.md` (the three prompts, verbatim from Notion).
- Three subagents written from the prompts: `market-researcher`, `financial-modeler`, `earnings-analyzer` (`.claude/agents/`). Shared rules in `.claude/rules/finance-output.md`. Slash commands `/research`, `/model`, `/earnings`.
- `research/2026-10-22-anthropic-finance-plugins.md`: what Anthropic ships officially (10 finance agent plugins) and how it maps to our v0. **Updated after reading the repo source**: agent-by-agent comparison + decision proposal (don't install agent plugins; vendor `dcf-model` + `audit-xls` skills; patch our guardrails).
- **Smoke test done: `/research VST`** → `reports/VST/2026-10-22-market-researcher.md` (159 lines, ~25 sources, 34 links, 16×«לא אומת», 8×«הסקה», found a real wording change in the 8-K footnote on Cogentrix/Meta). Cost: ~66k subagent tokens, 45 tool calls, ~5.5 min. Weak spots reported by the agent: no full call transcripts (Benzinga 403, Insider Monkey paywall), conflicting analyst-target data across sites, EDGAR search returned only 8-Ks.
- Prompt fixes applied from the smoke test: fixed data-source order (EDGAR full-text search + Exhibit 99, IR page, fool.com transcripts; skip SA/Benzinga), MarketBeat as the single target-price source, search budget (25 searches / 30 fetches), untrusted-document guardrail and "find latest period first" rule added to `.claude/rules/finance-output.md`.

## Next

1. ~~Vendor skills~~ **Done 2026-10-22:** `.claude/skills/dcf-model/` (SKILL.md, TROUBLESHOOTING.md, scripts/validate_dcf.py, scripts/recalc.py copied from the xlsx skill) and `.claude/skills/audit-xls/`, Apache 2.0 notice + LICENSE file. MCP-first wording replaced with user files → EDGAR/MAYA → web. `financial-modeler` rewritten: skills line, source order, stop-for-approval checkpoints, audit + validate step. `openpyxl` installed (`pip3 --user`). **LibreOffice is not installed** → `recalc.py` cannot run; the agent is told to fall back to `validate_dcf.py` and say formulas were not recalculated. Install LibreOffice (`brew install --cask libreoffice`) before the first real model run.
2. ~~Re-run `/research VST`~~ **Done (v2, 2026-10-22)** → `reports/VST/2026-10-22-market-researcher-v2.md` (v1 kept for comparison). Fixes worked: both full call transcripts reached (fool.com Q2 + Q1), section 3 now has named speakers and 6 marked wording changes vs 1 in v1; «הסקה» 8→3, «לא אומת» 16→15, searches 16/25, fetches 26/30, ~64k tokens, ~6 min. MarketBeat as single target source worked (history back to April). Remaining gap: WebFetch returns a summary, not raw text, so quotes are "as returned by the tool"; 10-Q came back XBRL-only. **Fix added to the prompt:** download transcripts/filings with curl into `filings/<TICKER>/`, strip HTML, quote via grep from the local file; use the EDGAR index page for the primary 10-Q .htm. Not yet re-tested. Next test: a TASE name (e.g. TEVA) for the MAYA path.
3. Decide data sources: MAYA (TASE) fetcher; EDGAR helper (CIK lookup + latest 10-Q/8-K Exhibit 99); free price/consensus source.
4. Validate `financial-modeler` builds a real .xlsx with formulas only; run `validate_dcf.py` on it.
5. Earnings agent: borrow from official `earnings-analysis/references/workflow.md` (beat/miss table, dodged-questions extraction, QC checklist) — without rating/price-target output.

## Open questions

- Which markets first: TASE only, US only, or both? (Affects filings source and language of sources.)
- Does the user want a daily watchlist run (scheduled) or on-demand only for now?
- Broker / portfolio data: read-only access wanted later, or keep the fleet research-only?
- Which model per agent: Sonnet (default now) vs Opus for the modeler?
