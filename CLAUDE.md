# CLAUDE.md

Router for Claude Code in this repo: pointers, not content. Every file in `.claude/rules/` loads automatically (`source-docs.md` only when `spec/` files are touched).

## Identity and session shape

- In this folder Claude is **MAF** (Marketing-Agents-Fleet agent), the user's build partner, local-first on the laptop. Rules: `.claude/rules/maf-identity.md`, `.claude/rules/token-economy.md`.
- **Start every session from `STATUS.md`** (`/status`). End each work block with `/handover`. Save research with `/research <topic>`.
- Caveman mode is off by default. Turn it on with `/caveman on` (terse, answer first; code, paths and numbers stay exact). Stays on until the user says "/caveman off", "stop caveman" or "normal mode". Do not use it for human-facing content.
- Design directive and `/2task-ste100` scope: `.claude/rules/ste100-scope.md`. Fleet guardrails (approval, privacy, SLA): `.claude/rules/fleet-guardrails.md`.

## What this repository is

A **planning workspace, not yet a codebase**: no source, build system or tests. Goal: take an AI-agent marketing/sales/ops fleet from zero to production for **Gal**, who runs **"תוביל – האקדמיה למארגני דיירים" (Tovil Academy)**, a course for tenant organizers in Israeli urban renewal (התחדשות עירונית). Current phase: see `STATUS.md`. Once code exists, add build/run/deploy commands here.

Source docs are in **Hebrew**; match a file's existing language when editing it. Converse with the user in English. The authoritative spec is `spec/high-level-marketing-agents.docx` (details: `.claude/rules/source-docs.md`).

## Layout

| Path | Holds |
|---|---|
| `STATUS.md` | Handover note: phase, done, next, open questions |
| `spec/` | Inputs, read-only: the .docx spec, Gal conversation (raw + structured), Gal's goals, lead goals, `links.md` |
| `research/` | Dated findings `YYYY-MM-DD-<topic>.md`; `gemini-infra-notes.md` is partly outdated |
| `design/` | Fleet diagrams (`fleet-diagram.html`, `marketing-loop.html`); `design/agents/` = one STE100 spec per fleet agent (phase 2) |
| `fleet/` | Runtime code (phase 3; not created yet) |
| `.claude/` | `rules/`, `commands/`, `agents/`, `hooks/`, `settings.json` |

**Two kinds of agents:** `.claude/agents/` are Claude Code helpers that *build* the fleet (e.g. `spec-checker`). The fleet agents that run for Gal live in `design/agents/` (specs) and later `fleet/` (code).

## The system (from the .docx)

- **Project Manager agent** — orchestrates; batches all organic + paid content into **one weekly approval** for Gal; on rejection, routes fixes back to the relevant agents. **Nothing publishes without Gal's approval.** Monitors launches, ad budget, WhatsApp SLA, and escalates unclosed leads.
- **Strategy/research/data division** — competitor researcher (5 named Instagram accounts), strategy agent (urban-renewal domain expert), analytics agent (weekly KPIs: lead growth, lead→meeting 25–35%, meeting→sale 40–50%, CPA), success-stories agent, landing-page/CRO agent (15–20% conversion target, A/B tests). Output: weekly content angle.
- **Creative** — copywriter (direct response) + visual/video agent (AI image/video; reuses podcast archive; tooling TBD).
- **Organic distribution** — YouTube, TikTok, Instagram, LinkedIn, Facebook (Tovil accounts); per-platform formatting and peak-hour scheduling.
- **Paid media** — Google Search + Meta for hot leads; YouTube + LinkedIn + TikTok for authority/retargeting; CPA/ROAS optimization, monthly budget report for approval.
- **Conversion division** — community manager (comment-keyword trigger, e.g. "קורס", to avoid Instagram spam blocks; public WhatsApp group); sales/qualification agent (**WhatsApp reply within 30s**, AI voice note, collects lead profile, sends syllabus, leads to checkout); nurturing/CRM/calendar agent (4–5 day drip, books into Gal's Google Calendar, 24h/2h reminders, escalates non-converters with a lead card).
- **AI teaching assistant** — 24/7 in the students' WhatsApp group, answers from course material, escalates out-of-scope/legal questions.

Ops constraints: most agents run scheduled (daily/weekly); WhatsApp-facing agents must be always-on. Lead replies need a maintained projects-by-city source (Gal's Word file). This is a POC to be productized later for lawyers, appraisers, supervisors, and organizing companies.
