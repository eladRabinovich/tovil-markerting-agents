# STATUS — Tovil Agent Fleet (MAF)

Handover note. A fresh session starts here. Keep it short; update at the end of each work block.

_Last updated: 2026-10-25_

## Phase

1 of 4: **Infrastructure research** → 2. agent design & business logic → 3. production deploy → 4. operations.

## Done

- 2026-10-25 repo restructure: `spec/` (inputs), `research/`, `design/`, `.claude/` (rules, commands `/status` `/handover` `/research`, helper agent `spec-checker`, hook `block-secrets.sh`, `settings.json`). `CLAUDE.md` is now a router. Unrelated `backup/` moved to `~/Playground/_backup/`.
- `CLAUDE.md`: project router. The .docx (`spec/high-level-marketing-agents.docx`) is the authoritative spec; transcription errors "גיא" = Gal, "טובין" = Tovil.
- Reviewed `research/gemini-infra-notes.md`. Keep its sprint skeleton (content brain → approval/publish → WhatsApp → ops), batch vs real-time split, local-first approach and self-hosted n8n. Outdated: models, WhatsApp pricing, AWS free tier, Midjourney API. Missing: about half the .docx agents.
- `design/fleet-diagram.html` v0.1: target-flow diagram, data-driven (edit `LANES`/`NODES`/`EDGES`). All agents marked `planned`.
- `design/marketing-loop.html`: weekly content loop diagram (monospace style). The 4-reviewer gate is MAF's proposal.
- Deep research round 2 → `research/2026-10-20-costs-access-deep-research.md` (LLM/media/TTS prices, Meta/TikTok/YouTube access).
- Deep research round 1 → `research/2026-10-19-infra-deep-research.md` (12 verified findings; big gaps listed under "Caveats").

## Key findings (round 1)

- Hosting is cheap; **LLM tokens + WhatsApp fees are the real costs.** One always-on VM (warm webhook, no cold start) + agents run sequentially on one scheduler.
- Oracle Always Free is now **2 OCPU / 12 GB** (halved Jun 2026); reclaim risk if idle under 20% for 7 days. AWS free tier = credits only.
- Claude Agent SDK needs a container/VM (~1 GiB per concurrent agent); not Workers.
- WhatsApp Israel (since 2026-10-01): service msgs $0.0053 after 1,000 free/number/month; marketing templates $0.0353. Drip design drives cost.
- **WhatsApp Groups API: max 8 participants + Official Business Account.** The teaching assistant inside the student group is not feasible on the official API as specified.
- LinkedIn Page posting: Community Management API requires legal-entity vetting (lead time). A third-party scheduler avoids it.
- Privacy (Amendment 13): full collection notice for lead profile data; draft PPA guidance requires AI disclosure, so bots should open with one.

## Key findings (round 2)

- LLM: Haiku 5.5 $0.10/$0.50 per MTok (cache hit $0.01); Sonnet 5.5 $2/$10; Opus 5.5 $4/$20; Batch API -50%. gpt-6-luna has the same price as Haiku.
- Media: images about $1–2/mo (FLUX / Nano Banana); Veo 3.1 video $0.05–0.40/s (Fast 1080p about $0.96 per 8s clip); Hebrew TTS free (Google Chirp 3 HD, he-IL, 1M chars/mo). WhatsApp voice notes must be mono OGG/Opus with `voice:true`.
- AI cost about $8 / $30 / $250 per month (low/expected/high). The high case is Sonnet running the bot, so use Haiku.
- **WhatsApp fees likely exceed AI costs:** about 15k bot msgs/mo ≈ $74, plus drip marketing templates ($0.035 each). Levers: shorter chats, email for the drip.
- Blockers: Meta Business Verification + App Review; TikTok audit (2–6 wks, private-only until then, inbox/draft workaround). YouTube uploads have their own 100/day quota.
- Still unverified: orchestration, VPS prices, unofficial-WhatsApp ban risk, Hebrew quality, schedulers, ads APIs.

## Next

1. User to confirm the proposed stack (see "Key findings (round 2)").
2. Gal: start Meta Business Verification, a WhatsApp Business number and a TikTok developer app/audit now. These set the launch date.
3. Local Hebrew quality test: Haiku 5.5 vs Sonnet 5.5 on a sales-bot script and a post (unverified by research).
4. Sprint 1 (local): competitor → strategy → copywriter chain producing one post.

## Open questions

- Teaching assistant redesign for Gal: 1:1 bot chat, ≤8-person groups, or a human-moderated group with a bot DM? (Official API can't serve a big group.)
- Is Tovil a registered legal entity with its own domain email? (Needed for LinkedIn and Meta verification.)
- How does Gal want to approve the weekly batch: WhatsApp, Telegram, or a web page?
- Which accounts and credentials can Gal provide (Meta Business, Google Ads, TikTok, LinkedIn)?
- Visual/video generation tools: TBD.
