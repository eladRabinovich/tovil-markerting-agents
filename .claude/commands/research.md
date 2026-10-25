---
description: Research a topic for the fleet and save findings to research/
argument-hint: "<topic>"
---

Topic: $ARGUMENTS

1. Search `research/` with grep for earlier findings on the topic. Do not repeat them; build on them.
2. Use WebSearch in standard mode first. Use extended mode only for prices, recent changes or thin results. Send independent searches in one turn.
3. Save to `research/YYYY-MM-DD-<kebab-topic>.md` with these sections:
   - **Summary**: 5 bullets or fewer.
   - **Findings**: each with source URL and the date of the source.
   - **Unverified / caveats**.
   - **Impact on the fleet design**: which agent, cost or guardrail changes.
4. Add one line to "Done" in `STATUS.md`. If a finding changes a decision, update "Key findings" or "Next".

Reply with the file path and the summary bullets only.
