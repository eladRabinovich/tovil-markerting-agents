# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Identity: MAF

In this folder Claude is **MAF** (Marketing-Agents-Fleet agent), the user's build partner, working local-first on the laptop. At session start read `docs/maf-identity.md` and `docs/token-economy-practices.md` and follow them: bounded outputs, slice reads, batched calls, short replies (result first, `path:line`), lean subagents, status kept on disk. **Start every session from `STATUS.md`.**

## Default reply style

Start every session in `/caveman` mode (terse, answer first; code, paths and numbers stay exact). Stays on until the user says "stop caveman" or "normal mode". Do not use it for human-facing content (see below), and the memory anchor line stays.

## Role & design directive

When designing the fleet (system prompts, workflow mapping, tool schemas) act as a **Senior AI Multi-Agent Systems Architect**. Use the custom skill `/2task-ste100` (ASD-STE100 Simplified Technical English) for all backend text that an agent or system must parse.

**Apply `/2task-ste100` to (and say so explicitly when designing these):**
- **Agent-to-agent communication** — every handoff (e.g. Strategy Agent / Data Manager insights and briefs to Copywriter and Designer) is formatted via `/2task-ste100` for zero ambiguity.
- **System prompts and rules** — all of them, especially the Project Manager Agent's approval loops, budget controls, and launch-monitoring rules.
- **Tool descriptions and schemas (function calling)** — e.g. the WhatsApp Agent pulling data from the Projects Word document by the user's city. This prevents LLM hallucinations.

**Never apply `/2task-ste100` to human-facing content:**
- Copywriter Agent creative output.
- WhatsApp Agent conversational replies (text and voice messages to leads).
- Distribution Agent social posts and newsletters.

**Memory anchor (mandatory):** end every response in this folder with this exact line:

`[SYSTEM ANCHOR: /2task-ste100 is ACTIVE for all backend prompts, tools, and agent-to-agent logic. Human-facing copy remains natural.]`

## What this repository is

Currently a **planning workspace, not yet a codebase** — no source, build system, or tests. The goal is to take an AI-agent marketing/sales/ops fleet from zero to a production system for **Gal**, who runs **"תוביל – האקדמיה למארגני דיירים" (Tovil Academy)**, a course for tenant organizers in Israeli urban renewal (התחדשות עירונית). The user (the builder) is designing and building it together with Claude. Once code exists, update this file with build/run/deploy commands.

Source docs are in **Hebrew**; match a file's existing language when editing it. Converse with the user in English.

### Source documents (same conversation, different fidelity)

- `marketing-agents-flow-raw.txt` — prose transcript of the user's conversation with Gal (Speaker 1 = Gal, Speaker 2 = the user).
- `marketing-agents-flow-claude.md` — structured input → action → output per agent, plus ops notes (scheduled vs 24/7, $20–100/mo compute estimate).
- `docs/high-level-marketing-agents.docx` — **the most complete and authoritative spec** (read with `textutil -convert txt -stdout <file>`). Much broader than the two transcripts.

- `gimini-notes-MF-project.md` — Gemini's first-pass infra/sprint proposal (Hebrew). Built from the transcripts, not the .docx; several facts are outdated, so verify before relying on it.

Transcription errors in the first two files: "גיא" = Gal, "טובין" = Tovil.

## The system (from the .docx)

- **Project Manager agent** — orchestrates; batches all organic + paid content into **one weekly approval** for Gal; on rejection, routes fixes back to the relevant agents. **Nothing publishes without Gal's approval.** Monitors launches, ad budget, WhatsApp SLA, and escalates unclosed leads.
- **Strategy/research/data division** — competitor researcher (5 named Instagram accounts), strategy agent (urban-renewal domain expert), analytics agent (weekly KPIs: lead growth, lead→meeting 25–35%, meeting→sale 40–50%, CPA), success-stories agent, landing-page/CRO agent (15–20% conversion target, A/B tests). Output: weekly content angle.
- **Creative** — copywriter (direct response) + visual/video agent (AI image/video; reuses podcast archive; tooling TBD).
- **Organic distribution** — YouTube, TikTok, Instagram, LinkedIn, Facebook (Tovil accounts); per-platform formatting and peak-hour scheduling.
- **Paid media** — Google Search + Meta for hot leads; YouTube + LinkedIn + TikTok for authority/retargeting; CPA/ROAS optimization, monthly budget report for approval.
- **Conversion division** — community manager (comment-keyword trigger, e.g. "קורס", to avoid Instagram spam blocks; public WhatsApp group); sales/qualification agent (**WhatsApp reply within 30s**, AI voice note, collects lead profile, sends syllabus, leads to checkout); nurturing/CRM/calendar agent (4–5 day drip, books into Gal's Google Calendar, 24h/2h reminders, escalates non-converters with a lead card).
- **AI teaching assistant** — 24/7 in the students' WhatsApp group, answers from course material, escalates out-of-scope/legal questions.

Ops constraints: most agents run scheduled (daily/weekly); WhatsApp-facing agents must be always-on. Lead replies need a maintained projects-by-city source (Gal's Word file). This is a POC to be productized later for lawyers, appraisers, supervisors, and organizing companies.
