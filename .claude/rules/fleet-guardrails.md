# Fleet guardrails

Hard constraints for every fleet design, prompt, tool and line of fleet code. Sources: the .docx spec and `research/`. If a design breaks a guardrail, stop and tell the user.

1. **Approval gate.** No agent publishes content or launches paid media without Gal's approval. The Project Manager agent sends one weekly approval batch.
2. **Budget gate.** Ad budget changes need Gal's approval (monthly budget report).
3. **AI disclosure.** Every bot conversation (sales, nurturing, teaching assistant) opens with a statement that the speaker is an AI.
4. **Privacy (Israeli Privacy Protection Law, Amendment 13).** Show a full collection notice before the bot collects lead profile data. Collect only the fields that the spec lists.
5. **WhatsApp SLA.** The sales agent replies to a new lead within 30 seconds. WhatsApp-facing agents run always-on; other agents run on a schedule.
6. **Escalation.** Bots escalate legal questions and questions outside the course material to a human. Do not let a bot give legal advice.
7. **Secrets.** API keys and tokens live in `.env` (not in git). Never print a secret; check key names or lengths only.
8. **Cost.** Default the bot model to the cheapest model that passes the Hebrew quality test. WhatsApp fees are a main cost; design short conversations.
