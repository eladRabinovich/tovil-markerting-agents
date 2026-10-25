# Design directive and /2task-ste100 scope

When designing the fleet (system prompts, workflow mapping, tool schemas) act as a **Senior AI Multi-Agent Systems Architect**. Use the custom skill `/2task-ste100` (ASD-STE100 Simplified Technical English) for all backend text that an agent or system must parse.

**Apply `/2task-ste100` to (and say so explicitly when designing these):**
- **Agent-to-agent communication**: every handoff (e.g. Strategy Agent / Data Manager insights and briefs to Copywriter and Designer) is formatted via `/2task-ste100` for zero ambiguity.
- **System prompts and rules**: all of them, especially the Project Manager Agent's approval loops, budget controls, and launch-monitoring rules. This includes fleet agent specs in `design/agents/` and Claude Code helpers in `.claude/agents/`.
- **Tool descriptions and schemas (function calling)**: e.g. the WhatsApp Agent pulling data from the Projects Word document by the user's city. This prevents LLM hallucinations.

**Never apply `/2task-ste100` to human-facing content:**
- Copywriter Agent creative output.
- WhatsApp Agent conversational replies (text and voice messages to leads).
- Distribution Agent social posts and newsletters.
