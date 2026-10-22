# Infra deep research — Tovil Agent Fleet

_Generated 2026-10-19 by the deep-research workflow (run wf_d46a4829-5a3). Claims were adversarially verified (3 votes each)._

## Question

Where can a solo developer host, as cheaply as possible (free tier up to ~$20–100/month total), a production fleet of ~12 LLM-driven AI agents for a small Israeli online course academy ("Tovil", for tenant organizers in urban renewal), as of late 2026? Workload: (a) scheduled batch agents (daily/weekly): competitor research on 5 Instagram accounts, strategy/analytics, copywriting, AI image/video generation, a weekly human-approval batch, then auto-publishing to Instagram, Facebook, TikTok, YouTube and LinkedIn, plus managing Google/Meta/TikTok/LinkedIn ads; (b) always-on webhook agents: a WhatsApp sales bot that must reply to inbound leads within 30 seconds (including AI voice notes), a nurturing/reminder agent, Google Calendar booking, and a 24/7 teaching-assistant bot inside a WhatsApp student group. Compare: (1) hosting options and their current free-tier limits (Oracle Always Free, GCP e2-micro, AWS's 2025 credit-based free tier, Cloudflare Workers/Cron/Durable Objects, Cloud Run + Scheduler, Lambda + EventBridge, Fly.io, Railway, Render, Hetzner VPS, GitHub Actions cron, Supabase/Neon), including how cold starts affect the 30s SLA; (2) orchestration runtimes (Claude Agent SDK, CrewAI, LangGraph, self-hosted n8n, Temporal/Inngest/Trigger.dev) and what each means for hosting; (3) hard external constraints: current WhatsApp Business Cloud API per-message pricing in Israel (service vs utility vs marketing templates), whether official-API bots can now join or manage WhatsApp groups (Groups API) vs unofficial libraries and their ban risk, Meta Graph API publishing and comment auto-reply rules, Instagram Business Discovery API for monitoring competitor accounts vs Apify scraping, TikTok/LinkedIn/YouTube posting API access and app-review lead times, Google/Meta ads API access; (4) realistic monthly costs for current LLMs, image/video generation (official APIs only) and Hebrew TTS at ~1 post/day and dozens of leads/day; (5) Israeli privacy-law obligations (Amendment 13) for a bot collecting lead age, family status and occupation. Deliver a recommended reference architecture with a cost table, a cheaper and a more robust alternative, and flag anything blocked by business verification or app-review lead time.

## Summary

Hosting costs are not the main constraint for Tovil's fleet. Token spend and WhatsApp messaging fees are, so the cheapest workable design is one always-on small VM or container host. That host runs the WhatsApp webhook agents warm, so no cold start threatens the 30s SLA, and it runs the ~12 scheduled agents one after another rather than in parallel. Oracle Always Free still fits as the $0 tier (now 2 OCPU / 12 GB ARM since June 2026, with reclaim and shutdown risks), and a cheap paid VPS is the more robust choice. Cloudflare Workers suits stateless webhook fronts but not the Claude Agent SDK, which needs a real container. Two external constraints hit hardest: (1) since Oct 1, 2026 WhatsApp service messages in Israel cost $0.0053 each after 1,000 free per number per month, and marketing templates cost $0.0353, so drip nurturing can easily cost more than hosting; (2) the official WhatsApp Groups API caps groups at 8 participants and requires Official Business Account (OBA) status, so the 24/7 teaching-assistant-in-a-student-group design cannot run on the official API as specified. LinkedIn Page posting is gated behind legal-entity vetting with two review stages, and Amendment 13 plus the regulator's draft AI guidance require a full collection notice and AI disclosure in the sales bot.

## Findings (ranked)

### 1. [high] (vote 3-0, 3-0)

Cloudflare Workers Free gives only 10 ms CPU per HTTP request and 5 Cron Triggers per account. Paid allows up to 5 min CPU (default 30 s) and 250 crons. Cron Triggers, Queue consumers and Durable Object alarms are each capped at 15 min wall-clock per run. CPU time excludes time spent waiting on network I/O, and HTTP requests have no wall-clock limit. Workers therefore fit an I/O-bound WhatsApp webhook front or a light scheduler, but 5 free crons is too few for ~12 scheduled agents unless they share one dispatcher cron.

**Evidence:** Both claims verified 3-0 against Cloudflare's primary limits page (updated Oct 12, 2026). Quote: 'CPU Time (HTTP Requests): Free: 10 ms; Paid: 5 min (default 30 seconds)'; 'Cron Triggers per Account: Free: 5; Paid: 250 ... Cron Triggers: 15 min ... Durable Object Alarms: 15 min'. A free cron gets only 10 ms of CPU. A paid cron gets 30 s if it runs more often than hourly, 15 min if hourly or less often.

**Sources:** https://developers.cloudflare.com/workers/platform/limits

### 2. [high] (vote 3-0, 3-0)

The Claude Agent SDK is not a stateless API wrapper. Each session spawns a long-lived `claude` CLI subprocess with its own shell, working directory and JSONL session files on local disk. That needs a container or VM, not V8-isolate serverless such as Workers. Lambda is possible only for short ephemeral sessions, under its 15-min cap and with an external SessionStore. Anthropic's suggested floor is 1 GiB RAM, 5 GiB disk and 1 CPU per concurrent agent, and memory grows with session length. Running 12 agents at once would need ~12+ GiB, which rules out 1 GB micro instances. Running them one after another on a schedule keeps a single small host viable.

**Evidence:** Two claims verified 3-0 against Anthropic's own docs: 'Every running agent is a long-lived process tied to local state'; '1 GiB RAM, 5 GiB disk, and 1 CPU per agent is a reasonable starting point ... Memory usage grows with session length'; 'The 1 GiB starting point ... is a floor, not the ceiling'. Session state does not survive a container restart. Saying Workers or Lambda fit worse is the verifiers' inference, not something the doc states.

**Sources:** https://code.claude.com/docs/en/agent-sdk/hosting

### 3. [high] (vote 3-0)

LLM token spend usually exceeds container or hosting cost by 10x or more. A minimal always-on container is about $0.05/hr (~$36/mo), and a single long agent session can cost dollars. For a ~$20–100/mo budget, model choice, prompt caching and session length matter more than which host you pick. A free or €4–5 VM makes the token share even larger.

**Evidence:** Verified 3-0: 'Anthropic token cost typically dominates container infrastructure cost by an order of magnitude or more. A minimally provisioned container runs roughly $0.05 per hour, while a single long agent session can spend dollars in tokens.' The $36/mo figure is arithmetic ($0.05 x 730 h). The 10x figure is a rule of thumb, not a benchmark.

**Sources:** https://code.claude.com/docs/en/agent-sdk/hosting

### 4. [high] (vote 3-0, 3-0, 2-1)

Oracle Always Free Ampere A1 was halved around June 15, 2026, from 4 OCPU / 24 GB (3,000 OCPU-h / 18,000 GB-h per month) to 2 OCPU / 12 GB (1,500 / 9,000). On free-only accounts, oversized instances were reportedly shut down until the user resized them by hand. 2 OCPU / 12 GB is still enough for a warm webhook server plus agents run one at a time. Treat it as a $0 tier with real availability risk, not as a production SLA host.

**Evidence:** Oracle's primary docs now read 'first 1,500 OCPU hours and 9,000 GB hours per month ... equivalent to 2 OCPUs and 12 GB of memory' (3-0, 3-0). The shutdown-until-resize behaviour (2-1 vote, medium) comes only from InfoQ, Linuxiac and Terminalbytes, because Oracle made no announcement. Verifiers also noted two further risks: Oracle reclaims Always Free VMs that stay under 20% CPU, network and memory use for 7 days, and a resized VM may fail to restart if the region has no capacity.

**Sources:** https://infoq.com/news/2026/07/oracle-cloud-free-tier-limits/, https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm

### 5. [high] (vote 3-0)

AWS's 2025 Free Tier, for accounts created on or after July 15, 2025, gives $100 in credits at sign-up plus up to $100 more: $20 each for five onboarding tasks (EC2, RDS, Lambda, Bedrock, a Budget). That is a short-term trial budget, not a permanent free host.

**Evidence:** Verified 3-0 against the AWS What's New post (July 16, 2025) and confirmed by 2026 explainers. Verifiers note that the free account plan ends after 6 months or when credits run out, and that credits stay usable for up to 12 months. A separate claim, that it 'cannot host a production fleet long-term for free', was refuted 0-3. The likely reason is that accounts convert to paid plans rather than being blocked, so read AWS as credits, not a hard cutoff.

**Sources:** https://aws.amazon.com/about-aws/whats-new/2025/07/aws-free-tier-credits-month-free-plan/

### 6. [high] (vote 3-0 x5)

WhatsApp Business Platform pricing in Israel as of Oct 1, 2026: billed per message since July 1, 2025. Marketing templates are $0.0353, and utility, authentication and service messages are $0.0053 each. Service (free-form) replies are no longer free: each business phone number gets 1,000 delivered service messages per month free, then pays the per-message rate. Utility templates sent inside the 24h window also became paid (free_customer_service changed to regular). Only eligible government and non-profit organisations keep unlimited free service messages, until Dec 31, 2027.

**Evidence:** Five claims merged, all 3-0. Meta primary docs: 'Effective July 1, 2025 – Meta charges on a per-message basis'; 'free tier of 1,000 service messages per month ... Meta charges as of the 1,001st'. The Israel rates come from secondary BSP sources (whautomate, Mumble.co.il, Times of Israel blog) that agree with each other; verifiers could not read Meta's rate-card CSV directly, so the exact rates are medium confidence. Illustrative arithmetic (mine, not sourced): 30 leads/day x ~8 bot replies = ~7,200 service messages/mo, so ~6,200 billable x $0.0053 = ~$33/mo. A 4-template marketing drip per lead (30/day) = ~3,600 x $0.0353 = ~$127/mo. Drip design and Free Entry Point windows (72h free after click-to-WhatsApp ad or Page CTA, per verifier notes) are therefore major cost levers. Meta's own Business Agent category (added July 1, 2026, $2 per 1M tokens) is optional and separate from this.

**Sources:** https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing, https://developers.facebook.com/docs/whatsapp/pricing/updates-to-pricing/, https://whautomate.com/tools/whatsapp-business-api-pricing-calculator, https://respond.io/blog/whatsapp-pricing-change-2026

### 7. [high] (vote 3-0, 3-0)

The official WhatsApp Cloud API Groups API caps each group at 8 participants and needs Official Business Account (OBA, blue-badge) status. It is unavailable for WhatsApp Business app numbers and Multi-solution Conversations numbers, the business must create the group, and people join only through invite links. A 24/7 AI teaching assistant inside a real course-cohort WhatsApp group is therefore not achievable on the official API. OBA also involves a brand-notability review that a small academy may fail.

**Evidence:** Both claims verified 3-0 on the primary Meta page (fetched 2026-10-19): 'Max group participants: 8'; 'To qualify for groups features, your business must be an Official Business Account (OBA)'. Corroborated by Omnichat, WOZTELL, Unipile, Periskope and Kapso ('available, but mostly blocked by OBA'). Workable alternatives: 1:1 assistant chats on the Cloud API, many groups of 8 or fewer, or a human-run group with a 1:1 bot. Unofficial libraries are the only way into large groups. Their ban risk was raised but not verified in this run.

**Sources:** https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/

### 8. [high] (vote 2-1, 3-0)

Programmatic posting to a LinkedIn company Page through LinkedIn's own app requires the Community Management API. That API is open only to registered legal organisations with commercial use cases, and personal email addresses fail vetting. Development tier requires an approved use case, a verified business email, a verified organisation, a verified website and domain, and verification of the app by a super admin of the linked LinkedIn Page. Standard tier also requires a full integration, test credentials, a valid privacy policy and a screencast. This is a business-verification and lead-time blocker. Third-party schedulers with approved LinkedIn integrations (Buffer, Make, Zapier) avoid it.

**Evidence:** Primary LinkedIn docs on Microsoft Learn (current moniker li-lms-2026-10). Votes were 2-1 and 3-0; the dissent concerned the word 'needed', given that third-party schedulers can post for you. Quote: 'only available to registered legal organizations for commercial use cases only ... Personal email addresses won't pass the vetting process.' A rejection means creating a new app.

**Sources:** https://learn.microsoft.com/en-us/linkedin/marketing/community-management-app-review?view=li-lms-2023-11

### 9. [medium] (vote 2-1)

Through the Content Publishing API, an Instagram professional account can publish up to 50 posts per rolling 24h (a carousel counts as one). That is far above the ~1 post/day workload, so the publishing quota is not a constraint.

**Evidence:** Meta's primary reference gives quota_total 50 and quota_duration 86400 s, and Later's help article agrees. The vote was split 2-1. A related claim listing the exact permissions and Meta app review (instagram_business_content_publish and others) was refuted 1-2, so the exact permission set and app-review path still need checking.

**Sources:** https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/content_publishing_limit.md

### 10. [high] (vote 3-0, 3-0)

Amendment 13 to Israel's Privacy Protection Law 5741-1981 took effect on Aug 14, 2025. It aligns the law with GDPR-style concepts and gives the Privacy Protection Authority (PPA) administrative fines and powers to freeze or delete databases. When the lead bot collects age, family status and occupation for a CRM, its collection notice must state the purpose, third-party recipients, the consequences of not consenting, the database controller's identity and contact details, access and correction rights, and whether supplying the data is legally required or voluntary.

**Evidence:** Both verified 3-0. The Meitar memo is backed by Pearl Cohen, MineOS, the edlaw summary, the Chambers 2026 Israel guide, IAPP and Ius Laboris. The quote's 'controlling shareholder of the database' is a mistranslation of בעל השליטה במאגר, the database controller. Section 11 applies when data is collected for storage in a database, which a lead CRM is. The PPA's grace period on the DPO-appointment duty ran until Oct 31, 2025.

**Sources:** https://meitar.com/wp-content/uploads/2025/07/Amendment-13-to-the-Privacy-Protection-Law-Is-on-the-Horizon-–-Is-Your-Organization-Ready-for-the-New-Era-in-the-World-of-Privacy.pdf

### 11. [medium] (vote 3-0)

Draft PPA guidance on AI (April 2025) requires organisations to tell people when they are interacting with AI, and what data the interaction processes and how. Tovil's WhatsApp sales bot, which also sends AI voice notes, and its teaching assistant should both open with an AI disclosure. This is the regulator's interpretation, not binding statute.

**Evidence:** Verified 3-0, with corroboration from EBN Law and Gornitzky. Gornitzky frames the duty as conditional (disclose if it may significantly affect consent). No final version was found as of Oct 2026.

**Sources:** https://www.pearlcohen.com/israeli-privacy-regulator-issues-draft-guidelines-on-privacy-in-ai/

### 12. [low] (vote n/a (synthesis))

Recommended reference architecture (my synthesis from the verified facts above; host prices other than Oracle and AWS were not verified in this run). Primary: one always-on ARM VM, either Oracle A1 at 2 OCPU / 12 GB ($0) or a ~€4–5/mo VPS. It runs a warm WhatsApp Cloud API webhook service (sales, nurturing, calendar, 1:1 teaching assistant) with no cold start, a single scheduler dispatching the ~12 batch agents one after another (1 GiB each), and Postgres or SQLite for lead state. Cheaper alternative: Oracle free tier only, with a Cloudflare Workers webhook front that acknowledges and queues messages and fails over if the VM is reclaimed. More robust alternative: a paid VPS or container host plus a managed Postgres and a durable workflow engine for the weekly approval batch. Rough monthly costs: hosting $0–10; WhatsApp ~$30–150 depending on the drip design; LLM tokens are the largest variable (unverified); image, video and Hebrew TTS are unverified.

**Evidence:** I derived this from the verified findings. The always-on VM avoids cold starts for the 30s SLA. Running agents one at a time follows from the 1 GiB-per-agent floor. Workers suit I/O-bound fronts because network waits do not count as CPU time. The WhatsApp cost range is illustrative arithmetic on the verified Israel rates. Blockers to flag: WhatsApp OBA for groups; LinkedIn legal-entity, domain-email and screencast review; Meta app review for Instagram and Facebook publishing and comment automation (unverified detail); Google Ads API access review (the timing claim was refuted); TikTok content-posting audit (not verified).

**Sources:** https://code.claude.com/docs/en/agent-sdk/hosting, https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm, https://developers.cloudflare.com/workers/platform/limits, https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing

## Caveats

Large parts of the question have no verified claims: GCP e2-micro, Cloud Run, Lambda, EventBridge, Fly.io, Railway, Render and Hetzner pricing, GitHub Actions cron, Supabase/Neon free tiers, cold-start numbers, and every orchestration runtime except the Claude Agent SDK (CrewAI, LangGraph, n8n, Temporal, Inngest, Trigger.dev). Also unverified: TikTok and YouTube posting API access, Google, Meta, TikTok and LinkedIn Ads API access (the Google Ads review-time claim was refuted 0-3), Instagram Business Discovery versus Apify, LLM, image, video and Hebrew TTS pricing, and the ban risk of unofficial WhatsApp libraries. The cost table above is therefore only partly evidence-based. The Israel WhatsApp rates rest on secondary BSP sources that agree with each other, not on Meta's rate-card CSV, and Meta can change rates each quarter (next possible change Jan 1, 2027). The Oracle change was never announced, so its date and enforcement behaviour come from secondary sources, and Oracle may change Always Free terms again. The PPA AI-disclosure duty is draft, interpretive guidance. Everything here is time-sensitive: the WhatsApp pricing change is less than three weeks old as of 2026-10-19.

## Open questions

- What do the LLM tokens (Claude, OpenAI, Gemini), official image and video APIs, and Hebrew TTS for WhatsApp voice notes actually cost each month at ~1 post/day and dozens of leads/day, and which models give acceptable Hebrew quality?
- What are the current access paths and review lead times for the TikTok Content Posting API audit, YouTube Data API quota, Meta app review (instagram_business_content_publish, comment management, pages_manage_posts) and Google Ads API Basic/Standard access for a small Israeli business?
- Is the Instagram Business Discovery API enough to monitor the 5 competitor accounts (posts, engagement, no Stories or Reels insights), or is Apify-style scraping needed, and with what ToS risk?
- For the student-group teaching assistant, which compliant design works: 1:1 Cloud API chats, groups of 8 or fewer, or a human-moderated large group with a bot DM? And what is the realistic ban risk of unofficial libraries (Baileys, whatsapp-web.js) for a business number?

## Refuted claims

- The AWS free account plan expires 6 months after sign-up or when the credits run out, whichever comes first, so it cannot host a production fleet long-term for free. (vote 0-3; https://aws.amazon.com/about-aws/whats-new/2025/07/aws-free-tier-credits-month-free-plan/)
- Publishing via Instagram Login requires the instagram_business_basic and instagram_business_content_publish permissions; via Facebook Login it requires instagram_basic, instagram_content_publish, pages_read_engagement, plus ads_management or ads_read if the user has a Business Manager role. These permissions are subject to Meta app review. (vote 1-2; https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/content_publishing_limit.md)
- Once Google Cloud brand verification is done, a pending Google Ads API Basic Access application is reviewed within a few hours. Without it, review takes up to 5 business days. (vote 0-3; https://ppc.land/google-cuts-ads-api-review-time-to-hours-with-brand-check/)

## Sources

- [secondary] https://infoq.com/news/2026/07/oracle-cloud-free-tier-limits/ (Hosting free tiers and cold starts, 5 claims)
- [primary] https://developers.cloudflare.com/workers/platform/limits (Hosting free tiers and cold starts, 5 claims)
- [primary] https://aws.amazon.com/about-aws/whats-new/2025/07/aws-free-tier-credits-month-free-plan/ (Hosting free tiers and cold starts, 5 claims)
- [blog] https://oneuptime.com/blog/post/2026-02-17-how-to-configure-minimum-instances-on-cloud-run-to-eliminate-cold-starts-for-production-services/markdown (Hosting free tiers and cold starts, 5 claims)
- [blog] https://flaviocopes.com/hosting-free-tiers/ (Hosting free tiers and cold starts, 5 claims)
- [blog] https://livemy.app/blog/free-hosting-that-doesnt-sleep (Hosting free tiers and cold starts, 5 claims)
- [primary] https://code.claude.com/docs/en/agent-sdk/hosting (Orchestration runtimes and hosting implications, 5 claims)
- [blog] https://contabo.com/blog/self-hosted-ai-orchestration-platforms/ (Orchestration runtimes and hosting implications, 5 claims)
- [blog] https://upstash.com/blog/durable-workflow-engines-compared-every-major-option-in-2026.md (Orchestration runtimes and hosting implications, 5 claims)
- [blog] https://automationatlas.io/guides/trigger-dev-vs-inngest-2026-comparison/ (Orchestration runtimes and hosting implications, 5 claims)
- [primary] https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing (WhatsApp Cloud API pricing and Groups API, 5 claims)
- [secondary] https://whautomate.com/tools/whatsapp-business-api-pricing-calculator (WhatsApp Cloud API pricing and Groups API, 5 claims)
- [primary] https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/ (WhatsApp Cloud API pricing and Groups API, 5 claims)
- [blog] https://kapso.ai/blog/whatsapp-groups-api-state-2026 (WhatsApp Cloud API pricing and Groups API, 5 claims)
- [blog] https://bundle.social/blog/tiktok-api-approval (Social publishing and ads API access/app review, 5 claims)
- [primary] https://learn.microsoft.com/en-us/linkedin/marketing/community-management-app-review?view=li-lms-2023-11 (Social publishing and ads API access/app review, 5 claims)
- [blog] https://rapidevelopers.com/api-automations/how-to-automate-youtube-video-uploads-using-the-api (Social publishing and ads API access/app review, 4 claims)
- [primary] https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/content_publishing_limit.md (Social publishing and ads API access/app review, 4 claims)
- [blog] https://bundle.social/blog/instagram-api-rate-limits (Social publishing and ads API access/app review, 5 claims)
- [secondary] https://ppc.land/google-cuts-ads-api-review-time-to-hours-with-brand-check/ (Social publishing and ads API access/app review, 4 claims)
- [blog] https://www.clym.io/blog/amendment-13-israels-updated-privacy-protection-law-and-what-businesses-must-do-now (Israeli privacy law Amendment 13 and AI cost, 5 claims)
- [secondary] https://meitar.com/wp-content/uploads/2025/07/Amendment-13-to-the-Privacy-Protection-Law-Is-on-the-Horizon-–-Is-Your-Organization-Ready-for-the-New-Era-in-the-World-of-Privacy.pdf (Israeli privacy law Amendment 13 and AI cost, 5 claims)
- [secondary] https://www.pearlcohen.com/israeli-privacy-regulator-issues-draft-guidelines-on-privacy-in-ai/ (Israeli privacy law Amendment 13 and AI cost, 5 claims)
- [secondary] https://barlaw.co.il/client-updates/israeli-privacy-protection-authority-clarifies-scope-of-duty-to-inform-on-collection-and-use-of-personal-information (Israeli privacy law Amendment 13 and AI cost, 4 claims)

## Stats

```json
{
 "angles": 5,
 "sourcesFetched": 24,
 "claimsExtracted": 116,
 "claimsVerified": 25,
 "confirmed": 22,
 "killed": 3,
 "unverified": 0,
 "afterSynthesis": 12,
 "urlDupes": 0,
 "budgetDropped": 6,
 "agentCalls": 106
}
```
