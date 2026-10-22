# Costs & platform access deep research (round 2) — Tovil Agent Fleet

_Generated 2026-10-20 by the deep-research workflow (run wf_00b27e6e-957, resumed after a credit-balance failure). Claims were adversarially verified (3 votes each)._

## Question

Follow-up research (round 2), as of late October 2026, for a small Israeli online course academy ("Tovil", tenant-organizer training in urban renewal) building a low-budget (~$20–100/month infra target) fleet of ~12 AI agents on one always-on VM. Answer with current, verified facts: (1) Realistic monthly cost of current LLM APIs (Anthropic Claude Haiku/Sonnet/Opus current generation, OpenAI, Google Gemini — per-token prices, prompt-caching discounts, batch API discounts) for this workload: ~1 social post/day (research + strategy + copywriting + review), a weekly analytics report, and a WhatsApp sales bot handling ~20–50 leads/day with ~10–20 turns each; and which models produce good Hebrew. (2) Official-API prices for AI image generation (e.g. OpenAI gpt-image, Google Imagen/Gemini image, Flux via fal/Replicate) and AI video generation (Google Veo, OpenAI Sora API, Runway, Kling, Luma) per image / per second of video, for ~7 images and ~2–4 short videos per week. (3) Hebrew text-to-speech options with API pricing and quality (ElevenLabs, Google Cloud TTS, Azure, OpenAI TTS) for short WhatsApp voice notes, and how to send voice notes via WhatsApp Cloud API (OGG/Opus). (4) Platform access requirements and review lead times for a small Israeli business: Meta app review / business verification for Instagram & Facebook Page publishing and comment management (current permission names), Instagram Business Discovery API capabilities and limits for monitoring 5 competitor accounts vs Apify-style scraping and its ToS risk, TikTok Content Posting API audit (and whether unaudited apps can only post privately), YouTube Data API v3 upload quota and audit, Google Ads API developer token Basic/Standard access, Meta Marketing API access, TikTok and LinkedIn Ads APIs; and whether third-party schedulers (Buffer, Publer, Metricool, Ayrshare) are a cheaper shortcut. (5) Compare orchestration options for this setup on one small VM: self-hosted n8n (Community Edition license limits, RAM needs), CrewAI, LangGraph, Claude Agent SDK, Inngest/Trigger.dev self-hosted, and plain cron + Python; which best supports a weekly human-approval loop and a 24/7 WhatsApp webhook. (6) Current monthly prices for small VPS/containers: Hetzner CX/CAX (post-2025 price changes), Fly.io, Railway, Render, DigitalOcean, and free tiers of Supabase and Neon Postgres. (7) Ban risk of unofficial WhatsApp libraries (Baileys, whatsapp-web.js, WAHA) for a business number, and compliant designs for a course-student community assistant given the official Groups API 8-participant cap. Deliver a cost table (low/expected/high per month) and a recommendation.

## Summary

The checks covered 23 claims. The verified parts fit Tovil's $20–100/month target as long as the always-on WhatsApp bot runs on a cheap tier. Claude Haiku 5.5 ($0.10/$0.50 per MTok, cache hits at $0.01) and OpenAI gpt-6-luna (also $0.10/$0.50, cached $0.01) both make the bot cost roughly $2–10/month at 200–1,000 turns/day. Running the bot on a mid-tier model (Sonnet 5.5 or gpt-6.1-sol at $2/$10) would cost about $35–170/month, and the bot is the biggest cost variable. Media is cheap. About 30 images/month cost under $1 on fal FLUX, or about $2 on Nano Banana 2. Video depends on tier: about 12–16 Veo 3.1 clips of 8 seconds cost roughly $5 (Lite 720p), $12–15 (Fast 1080p) or $40–50 (Standard). Hebrew voice notes cost $0 inside Google Chirp 3 HD's 1M-character free tier, and on WhatsApp they must be mono OGG/Opus sent with voice:true. The main platform blockers are Meta Business Verification plus App Review for Advanced Access, and the TikTok audit (unaudited Direct Post is private-only). YouTube is easier than before: uploads have their own 100/day bucket, and the docs now say unverified projects are not locked to private, though that change is unannounced and needs a test. These research areas were not verified and remain open: Hebrew model quality, Sora/Runway/Kling/Luma pricing, ElevenLabs/Azure/OpenAI TTS, Google Ads/LinkedIn/TikTok Ads API access, third-party schedulers, orchestration frameworks, VPS prices and the ban risk of unofficial WhatsApp libraries. The recommendation is Haiku 5.5 (or gpt-6-luna) with prompt caching for the bot, Sonnet 5.5 with Batch for the daily content pipeline and weekly report, Opus 5.5 only for the weekly strategy pass, FLUX or Nano Banana for images, Veo 3.1 Fast for video and Chirp 3 HD for voice. Start Meta Business Verification and the TikTok audit right away because they set the launch timeline. Cost table (USD/month, LLM + media + TTS only; VPS and WhatsApp messaging fees not verified and excluded): LOW about $8 (Haiku bot at 200 turns/day about $2, Sonnet content with Batch/caching about $4, FLUX images about $0.10, Veo Lite 8 clips about $3, TTS $0). EXPECTED about $30 (Haiku bot at 500 turns/day about $5, Sonnet content plus weekly Opus strategy about $10, analytics about $1, Nano Banana 2 images about $2, Veo Fast 1080p 12 clips about $12, TTS $0). HIGH about $250+ (Sonnet bot at 1,000 turns/day about $170, Opus-heavy content about $25, Veo Standard 16 clips about $51, images about $2.50, TTS about $5).

## Findings (ranked)

### 1. [high] (vote 3-0 (x3))

Claude current-generation list prices per MTok are: Opus 5.5 $4 input / $20 output, Sonnet 5.5 $2/$10, Haiku 5.5 $0.10/$0.50 (prompts up to 100K tokens; above that the whole request is billed at $0.50/$2.50). Prompt caching: a 5-minute write costs 1.25x base input and a 1-hour write 2x. A cache hit costs 0.05x on Opus and Sonnet 5.5 ($0.20 and $0.10) and 0.1x on other models (Haiku 5.5 $0.01). The Batch API is 50% off input and output (Opus $2/$10, Sonnet $1/$5, Haiku $0.05/$0.25) and stacks with the caching multipliers. Fast mode cannot be batched, Managed Agents sessions have no batch mode, and US-only inference (inference_geo) costs 1.1x.

**Evidence:** Merged claims 0, 1 and 2, all voted 3-0 and checked live on 2026-10-20 against Anthropic's own pricing page, including the footnote on 0.05x cache hits and the FAQ on how discounts stack. The Claude API skill's model table (cached 2026-09-25) separately confirms the Opus and Sonnet 5.5 prices. It does not list Haiku 5.5, which suggests Haiku 5.5 is newer than that cache.

**Sources:** https://platform.claude.com/docs/en/about-claude/pricing

### 2. [high] (vote 3-0 (x3))

OpenAI's current GPT-6 family, standard tier, short context, per 1M tokens: gpt-6-astra (top) $10 input / $50 output / $1.00 cached; gpt-6.1-sol (mid) $2 / $10 / $0.10 cached; gpt-6-luna (cheapest current-gen) $0.10 / $0.50 / $0.01 cached. Batch halves these (astra $5/$25). Cached input also has a write fee (luna $0.125 for 30-minute, $0.25 for 12-hour; sol $2.50/$5.00). Long-context prompts (over about 272K tokens) cost more. gpt-6-luna has the same price as Haiku 5.5, so it is an equally cheap option for the WhatsApp bot. The previous-gen gpt-5-nano is cheaper still at $0.05 input.

**Evidence:** Merged claims 3, 4 and 5, all voted 3-0 and checked live against OpenAI's pricing page on 2026-10-20. A secondary source (eesel.ai, Oct 11 2026) agrees on the gpt-6-luna price.

**Sources:** https://developers.openai.com/api/docs/pricing

### 3. [high] (vote 3-0 (x2))

Gemini paid-tier prices: Gemini 3.8 Flash is $0.75 input / $3.75 output per 1M (thinking tokens included) through Dec 31, 2026, then doubles to $1.50/$7.50 on Jan 1, 2027. Cache reads go from $0.075 to $0.15. Batch and Flex are 50% off ($0.375/$1.875 now). Gemini 3.5 Flash-Lite is $0.30 input / $2.50 output, with $0.03 cached input plus $1.00 per 1M tokens per hour of cache storage. Any cost model that runs into 2027 should use the doubled 3.8 Flash prices, which makes it more expensive than Haiku 5.5 or gpt-6-luna for the bot.

**Evidence:** Merged claims 6 and 7, both voted 3-0 and checked against Google's official pricing page (fetched twice on 2026-10-20).

**Sources:** https://ai.google.dev/gemini-api/docs/pricing

### 4. [high] (vote 3-0, 3-0, 2-1)

Image generation is a rounding error at about 30 images/month. fal.ai bills FLUX per megapixel: FLUX.1 [schnell] $0.003/MP, FLUX 2 $0.012/MP, FLUX.1 [dev] $0.025/MP, so a month costs about $0.09–$0.75. FLUX.2 [pro] is about $0.03 for the first MP (about $0.90/month). Google's official API charges $0.067 per 1K image for Nano Banana 2 ($0.034 on batch) and $0.0336 for Nano Banana 2.1, about $1–2/month. fal resells Nano Banana at about $0.04 and Nano Banana 2 at $0.08 per 1K image, with 2K costing 1.5x and 4K 2x.

**Evidence:** Merged claims 8 (image part, 2-1), 9 (3-0) and 10 (3-0), all taken from first-party vendor pricing pages fetched on 2026-10-20.

**Sources:** https://fal.ai/pricing, https://fal.ai/models/fal-ai/flux-2-pro, https://fal.ai/models/fal-ai/nano-banana-2, https://ai.google.dev/gemini-api/docs/pricing

### 5. [medium] (vote 2-1)

Veo 3.1 video on the Gemini API is priced per second: Standard $0.40 (720p/1080p, $0.60 at 4K), Fast $0.10 (720p) / $0.12 (1080p) / $0.30 (4K), Lite $0.05 (720p) / $0.08 (1080p). An 8-second 1080p clip is about $0.96 on Fast, about $0.64 on Lite and $3.20 on Standard. That puts 8–16 clips/month at roughly $3–51 depending on tier. The models are still marked -preview, so prices may change.

**Evidence:** Claim 8 was voted 2-1. The verifier fetched the primary page and matched every figure, but the split vote and the preview status lower confidence. A competing Kling-on-fal price claim was refuted 0-3 because of internal inconsistency, so no non-Google video price was verified.

**Sources:** https://ai.google.dev/gemini-api/docs/pricing

### 6. [high] (vote 3-0)

Hebrew TTS: Google Cloud TTS Chirp 3 HD voices support he-IL. The first 1M characters per month are free, then $30 per 1M characters. A 300-character voice note costs about $0.009, so about 1,000 notes/month (0.3M characters) fall inside the free tier and cost $0. Billing must be enabled, and the free tier is per billing account per month.

**Evidence:** Claim 12 was voted 3-0. The verifier read the live pricing table (its free-usage column) and the Chirp 3 HD locale list. A separate claim about Gemini TTS per-token pricing was refuted 0-3.

**Sources:** https://cloud.google.com/text-to-speech/pricing, https://cloud.google.com/text-to-speech/docs/chirp3-hd

### 7. [high] (vote 3-0 (x3))

Sending a native WhatsApp voice note through the Cloud API uses the normal audio payload ({type:'audio', audio:{id, voice:true}}). The file must be audio/ogg encoded with Opus, mono. If the format is anything else, or voice is omitted or false, it arrives as a regular audio message. AAC, AMR, MP3 and M4A are allowed only as basic audio. The size limit is 16 MB, and files of 512 KB or less are recommended so the play icon shows. So the TTS pipeline needs to transcode to mono OGG/Opus (for example with ffmpeg -c:a libopus -ac 1).

**Evidence:** Merged claims 11, 13 and 14, all voted 3-0. Meta's own docs and a Meta BSP (360dialog) agree. The detail that the voice flag is ignored for other formats comes from 360dialog, whose page still says Beta.

**Sources:** https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/audio-messages, https://docs.360dialog.com/docs/messaging/media/voice-message-beta-program

### 8. [high] (vote 3-0, 3-0, 2-1, 3-0)

Meta permissions for the fleet. Instagram publishing: instagram_business_content_publish, which depends on instagram_business_basic (Instagram Login path), or instagram_content_publish plus instagram_basic, pages_read_engagement and pages_show_list (Facebook Login path). Instagram comment-keyword bot: instagram_business_manage_comments (or instagram_manage_comments) plus the comments webhook. Sending a DM or private reply also needs instagram_business_manage_messages. Facebook Page: pages_manage_posts to publish, pages_manage_engagement (which depends on pages_read_user_content) to moderate comments, pages_read_engagement to read, and publish_video for video. The old business_* scopes were deprecated on Jan 27, 2025. Business Verification is required for any Advanced Access request, and App Review is required for data you don't own or manage. In practice that means App Review for production Advanced Access.

**Evidence:** Merged claims 15, 16, 18 (all 3-0) and 17 (2-1), checked against Meta's primary docs on 2026-10-20. The verifiers noted that the permissions page has copy errors (the manage_comments description was copied from content_publish). The Comment Moderation doc fills that gap.

**Sources:** https://developers.facebook.com/docs/permissions, https://developers.facebook.com/docs/instagram-platform/comment-moderation, https://developers.facebook.com/docs/graph-api/overview/access-levels, https://developers.facebook.com/documentation/pages-api/posts

### 9. [high] (vote 3-0 (x2))

TikTok Content Posting API: everything an unaudited client posts through Direct Post is limited to private (SELF_ONLY) viewing, with the error unaudited_client_can_only_post_to_private_accounts. Posting publicly requires passing an audit for ToS compliance, which also checks UX and integration. Third-party write-ups put the audit at about 2–6 weeks. The Upload (inbox/draft) flow, where Gal would finish publishing by hand in the app, is a workaround until the audit passes.

**Evidence:** Merged claims 19 and 20, both voted 3-0, word-for-word from TikTok's docs. The 2–6 week audit time is secondary (bundle.social, Aug 2026; blotato).

**Sources:** https://developers.tiktok.com/doc/content-posting-api-reference-direct-post

### 10. [medium] (vote 3-0 (x2))

YouTube Data API v3: videos.insert now uses its own 'Video Uploads' quota bucket, at 1 unit per call and 100 calls/day, separate from the 10,000 general units (granular quota from June 1, 2026). That is far more than 2–4 videos/week. The videos.insert doc also now says 'Videos uploaded from unverified API projects are not restricted to private viewing mode,' which reverses the 2020 private lock. That wording changed between July and October 2026 with no changelog entry, and third-party guides still describe the old lock.

**Evidence:** Claim 21 (quota) was voted 3-0 with high confidence and is backed by the Overview page. Claim 22 (no private lock) was voted 3-0 but rated medium confidence: Wayback copies up to 2026-07-10 still show the old rule, and the revision history never announced the reversal. The quota part is high confidence; the private-lock reversal needs a test upload.

**Sources:** https://developers.google.cn/youtube/v3/docs/videos/insert, https://developers.google.com/youtube/v3/getting-started, https://developers.google.com/youtube/v3/revision_history

## Caveats

Coverage gaps: no claim survived verification for sub-questions 5 (orchestration: n8n CE limits/RAM, CrewAI, LangGraph, Claude Agent SDK, Inngest/Trigger.dev), 6 (Hetzner/Fly/Railway/Render/DO prices, Supabase/Neon free tiers) and 7 (ban risk of Baileys/whatsapp-web.js/WAHA, and community-assistant designs under the 8-participant Groups API cap). Several parts of 1–4 were also not verified: Hebrew output quality of any model, Sora/Runway/Kling/Luma pricing (the Kling claim was refuted 0-3), ElevenLabs/Azure/OpenAI TTS pricing and Hebrew quality (Gemini TTS claim refuted 0-3), Instagram Business Discovery limits vs Apify scraping, Google Ads developer token tiers, Meta Marketing/TikTok/LinkedIn Ads API access, and scheduler pricing (Buffer/Publer/Metricool/Ayrshare). Any recommendation in those areas comes from prior knowledge, not this research round. The cost table leaves out VPS hosting and WhatsApp Cloud API per-message/template fees, both unverified. Time sensitivity: Gemini 3.8 Flash promotional prices double on Jan 1, 2027. Veo 3.1 models are -preview. Haiku 5.5 appears to be newer than late September 2026. The YouTube private-lock reversal is an unannounced doc change. Modeling assumptions: about 8K input tokens per bot turn (mostly cached, about 1K uncached), about 300 output tokens, 200–1,000 turns/day, and about 4 Sonnet calls/day for the content pipeline. Cache writes (1.25x, with a 5-minute TTL) will raise bot costs a little when conversations are sparse, and real token counts for Hebrew may be higher than for English.

## Open questions

- Which low-cost model (Haiku 5.5, gpt-6-luna, Gemini 3.5 Flash-Lite) writes natural, sales-grade Hebrew and handles Hebrew tokenization efficiently? This needs a side-by-side test on real Tovil lead conversations.
- What are the current WhatsApp Cloud API per-message/template prices for Israel, and what is a compliant design for the 24/7 student-community assistant, given the 8-participant Groups API cap (for example, 1:1 assistant threads with a human-run community group) and the ban risk of unofficial libraries?
- Which orchestration stack fits one small VM with a weekly human-approval loop and an always-on WhatsApp webhook: self-hosted n8n CE, the Claude Agent SDK, or cron + Python + Postgres? And what does the VM itself cost (Hetzner post-2025 prices vs Fly/Railway/Render)?
- Does a third-party scheduler (Ayrshare, Publer, Metricool) with already-approved Meta/TikTok/YouTube apps avoid the Business Verification, App Review and TikTok audit timeline at a monthly price lower than the engineering cost? And does a test upload confirm that unverified YouTube API projects really publish publicly now?

## Refuted claims

- Kling video on fal.ai is billed per second of output: Kling v2.5 Turbo Pro at $0.07/s, and Kling v3 Pro/Standard and Kling O3 at $0.14/s (about $0.70 for a 5-second clip). The fetch summary gave $0.84 for a 5-second Kling v3 Pro clip, which does not match 5 × $0.14. (vote 0-3; https://fal.ai/pricing)
- Gemini TTS models are billed per token and have no free tier. Gemini 2.5 Flash TTS costs $0.50 per 1M text tokens in and $10 per 1M audio tokens out. Audio is counted at 25 tokens per second, so 30 seconds of audio is about $0.0075. (vote 0-3; https://cloud.google.com/text-to-speech/pricing)

## Unverified claims


## Sources

- [primary] https://platform.claude.com/docs/en/about-claude/pricing (LLM + media API pricing, 5 claims)
- [primary] https://developers.openai.com/api/docs/pricing (LLM + media API pricing, 5 claims)
- [primary] https://ai.google.dev/gemini-api/docs/pricing (LLM + media API pricing, 5 claims)
- [primary] https://fal.ai/pricing (LLM + media API pricing, 5 claims)
- [blog] https://blog.laozhang.ai/en/posts/sora-2-pricing.md (LLM + media API pricing, 5 claims)
- [secondary] https://costbench.com/software/ai-media-apis/runway-api/alternatives/ (LLM + media API pricing, 5 claims)
- [primary] https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/audio-messages (Hebrew voice + WhatsApp Cloud API, 5 claims)
- [blog] https://github.com/danielrosehill/Hebrew-TTS-Providers (Hebrew voice + WhatsApp Cloud API, 5 claims)
- [blog] https://developer.puter.com/tutorials/elevenlabs-api-pricing/ (Hebrew voice + WhatsApp Cloud API, 5 claims)
- [primary] https://cloud.google.com/text-to-speech/pricing (Hebrew voice + WhatsApp Cloud API, 5 claims)
- [unreliable] https://elevenlabs.io/blog/google-tts-alternatives-2026 (Hebrew voice + WhatsApp Cloud API, 0 claims)
- [primary] https://docs.360dialog.com/docs/messaging/media/voice-message-beta-program (Hebrew voice + WhatsApp Cloud API, 5 claims)
- [primary] https://developers.facebook.com/docs/permissions (Platform API access and review, 5 claims)
- [primary] https://developers.tiktok.com/doc/content-posting-api-reference-direct-post (Platform API access and review, 5 claims)
- [primary] https://developers.google.cn/youtube/v3/docs/videos/insert (Platform API access and review, 4 claims)
- [primary] https://developers.google.com/google-ads/api/docs/access-levels?hl=en (Platform API access and review, 5 claims)
- [primary] https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait (Orchestration on one VM + hosting prices, 5 claims)
- [blog] https://www.activepieces.com/blog/n8n-community-edition-limits-and-features-compared.md (Orchestration on one VM + hosting prices, 5 claims)
- [primary] https://docs.langchain.com/oss/python/human-in-the-loop (Orchestration on one VM + hosting prices, 5 claims)
- [blog] https://findstack.com/resources/hetzner-price-increase-2026 (Orchestration on one VM + hosting prices, 5 claims)
- [primary] https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/ (Contrarian: ToS and ban risks, scheduler shortcuts, 5 claims)
- [unreliable] https://help.chatdaddy.tech/article/2026-whatsapp-ban-risk-report (Contrarian: ToS and ban risks, scheduler shortcuts, 0 claims)
- [blog] https://zylos.ai/research/2026-01-26-whatsapp-api-automation (Contrarian: ToS and ban risks, scheduler shortcuts, 5 claims)
- [blog] https://www.ayrshare.com/compare/buffer-api-alternative/ (Contrarian: ToS and ban risks, scheduler shortcuts, 5 claims)
