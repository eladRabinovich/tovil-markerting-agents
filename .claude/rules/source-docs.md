---
paths:
  - "spec/**"
  - "research/gemini-infra-notes.md"
---

# Source documents (same conversation, different fidelity)

- `spec/high-level-marketing-agents.docx`: **the most complete and authoritative spec**. Much broader than the two conversation files. Read slices only: `textutil -convert txt -stdout spec/high-level-marketing-agents.docx | grep -n -A5 <term>`.
- `spec/conversation-raw.txt`: prose transcript of the user's conversation with Gal (Speaker 1 = Gal, Speaker 2 = the user).
- `spec/conversation-structured.md`: structured input → action → output per agent, plus ops notes (scheduled vs 24/7, $20–100/mo compute estimate).
- `spec/gal-goals.md`: Gal's own words on the academy's purpose.
- `spec/goal-leads.md`: the strategic goal: leads → students → students who create projects.
- `spec/links.md`: Tovil site and related links.
- `research/gemini-infra-notes.md`: Gemini's first-pass infra/sprint proposal (Hebrew), built from the transcripts, not the .docx. Outdated: models, WhatsApp pricing, AWS free tier, Midjourney API. Verify before relying on it.

Transcription errors in the two conversation files: "גיא" = Gal, "טובין" = Tovil.

Files in `spec/` are inputs. Do not edit them unless the user asks.
