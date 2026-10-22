---
name: token-economy-practices
description: "How TAF works with the user without wasting tokens — bounded output, slices, batching, short replies, lean subagents"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 6b0cda9e-6de4-4bec-a8c2-02ce1813ec80
  modified: 2026-10-19T19:25:41.889Z
---

The user asked (2026-10-19) that TAF ([[taf-identity]]) always work by these rules, distilled from Lulu's token-economy guide. Cost model: every turn resends the whole context (cached ≈0.1×, fresh output ≈5×), so the only levers are a smaller context and fewer turns.

**Reading and output**
1. Bound every output before running it: `| head -40`, `| tail -20`, `--stat`, `-q`, `LIMIT 20`. Unknown size → `wc -l` first.
2. Read slices: `grep -n -A5`, `sed -n 'a,bp'`, Read with offset/limit. Whole file only when rewriting most of it. Company filings (PDF/XLSX): extract to text once, then grep/sed slices; never dump a whole filing.
3. Never re-read what I just wrote or what hasn't changed; verify with a targeted grep or a test.
4. Aggregate at the source (`grep -c`, `jq`, SQL `COUNT/GROUP BY`); scripts print the answer, not the data.
5. Never `cat` lockfiles, logs, generated JSON, CSVs; exclude `node_modules .venv dist .git` from find/grep. No `-v`/`--verbose`; installs with `-q`/`--silent`. Tests: `pytest -q -x 2>&1 | tail -20`.
6. Never paste tool output back into a heredoc or prompt; reference the file. Secrets never enter the context (print key names/lengths only) — relevant for broker, market-data and LLM API keys.

**Turns and replies**
7. All independent calls in one message; sequence only real dependencies.
8. Two strikes: after two failures of the same approach, stop and report what failed.
9. Say less: one line per step, result first, point with `path:line`, never restate a diff/file/plan already on disk.
10. Think at the task's level; heavy reasoning only for design/debugging.

**Subagents, tools, session shape**
11. A subagent costs a whole session. Spawn only for parallel or dump-heavy work, narrow brief, "return conclusions, not file contents"; then wait, don't duplicate. Cheap models (haiku/sonnet) for mechanical search.
12. Load tool schemas one at a time (`ToolSearch select:<name>`); invoke a skill only when its trigger matches. WebSearch standard first; WebFetch with a question, not "give me the page".
13. State on disk early: keep a handover/status note (e.g. `STATUS.md` in the project) updated so a fresh session starts from it instead of resuming a heavy one.
14. Always-loaded files (CLAUDE.md, MEMORY.md) are routers: pointers, not content; prune what stops mattering.
15. Suggest `/compact <what to keep>` when half the window is finished work, `/clear` between unrelated tasks.

**Why:** the user wants the same results for fewer tokens; long sessions pay for their past every turn.
**How to apply:** every session in this project, every tool call and reply. Copied from the Tovil project on 2026-10-22; measure a `/context` baseline here on the first working session.
