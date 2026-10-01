# Project-to-plugin research

Reviewed October 1, 2026. The account inventory contained 51 repositories: 19 public and 32 private. Metadata and available READMEs were reviewed across the inventory; candidate source trees and selected implementations were inspected in depth. This is a product-fit assessment, not an audit of every line of every repository. Private repository names, descriptions and code are excluded from this public report.

## First release

| Plugin | User outcome | Reused implementation | Deliberate boundary |
|---|---|---|---|
| Comfy Story Planner | A coherent, timed film plan, candidate shot prompts and SRT subtitles | Original FilmPlan validator, prompt compiler and subtitle exporter | No footage rendering, GPU service or visual acceptance |
| WorldZero Lab | Repeatable matched-seed baseline comparisons with replay evidence | Original simulation, baseline policies and replay kernel | No LLM evaluation, hosted service or scientific-certification claim |
| Heimdall Policy Lab | A policy draft with concrete structural findings | Original JSON Schema plus source-derived guard signatures | No gateway, live interception, semantic enforcement or compliance certification |

These are skills packages with actual Python tools. A compatible host with shell/file access is necessary for execution; chat-only use can draft inputs but cannot claim to have run checks. Their useful scope fits bundled execution, so a new hosted MCP service is not needed for this release. Existing source licenses, including Comfy Story's AGPL, are retained.

## Market context and differentiation

OpenAI recommends starting with user outcomes and choosing skills for workflows that can be implemented with instructions and bundled resources, with MCP for live data or controlled hosted actions. That supports small, complete workflows over a generic wrapper around a whole repository. [OpenAI use-case guide](https://developers.openai.com/plugins/plan/use-case).

Runway has an existing multi-shot generation workflow and storyboard tooling. Comfy Story Planner should complement generation with explicit state continuity and exact editorial timing. It should not imply it can generate a finished film. [Runway multi-shot API](https://docs.dev.runwayml.com/recipes/multi-shot-video/), [Runway storyboard guide](https://academy.runwayml.com/tutorial/storyboard-featured-workflow).

Guardrails AI already has a broad validator ecosystem. Heimdall Policy Lab therefore focuses on authoring and offline static feedback for the user's own policy format, with a strict separation between linting and actual enforcement. [Guardrails Hub](https://guardrailsai.com/hub).

Active Causal Discovery Bench and CausaLab illustrate an active research area around interactive experimentation. WorldZero's reusable strength is its repeatable worlds and evidence/replay contracts. This release only exposes the built-in baselines; a later hosted experiment workbench could broaden access if usage justifies its operational cost. [ACDB source](https://github.com/qpiai/Active-Causal-Discovery-Bench), [CausaLab paper](https://arxiv.org/abs/2605.26029).

Directory searches also returned Runway, Vanta, PostHog, Amplitude and Statsig. These are adjacent products, not exact equivalents. Directory search is incomplete and rankings are not evidence of demand. The recommendation is an inference from existing capabilities, differentiation, implementation effort and deployability—not proven customer demand or revenue.

## Public project triage

| Repository | Decision | Rationale |
|---|---|---|
| [comfy-story](https://github.com/skishore23/comfy-story) | Build now | Strong creator workflow; portable planning contracts can run without GPU weights |
| [worldzero](https://github.com/skishore23/worldzero) | Build now | Differentiated research workflow with reproducible outputs and an existing browser demo |
| [heimdall](https://github.com/skishore23/heimdall) | Build now | Concrete policy-authoring outcome; avoid promising gateway enforcement from chat |
| [polysignal](https://github.com/skishore23/polysignal) | Already in progress | Separate PolySignal Research package in PR #9; avoid duplicating its work |
| [wink](https://github.com/skishore23/wink) | Next candidate | Existing Claude Code plugin; its hooks require careful portability review, not a manifest-only conversion |
| [receipt](https://github.com/skishore23/receipt) | Next candidate | Evidence-chain analysis could become an offline plugin; orchestration itself needs a running service |
| [ranger](https://github.com/skishore23/ranger) | Later | Experimental workflow engine; identify a stable, user-facing diagnosis or authoring workflow first |
| [coralx](https://github.com/skishore23/coralx) | Later | Useful experiment setup/result inspection; full optimization brings model and compute dependencies |
| [roster](https://github.com/skishore23/roster) | Later | Durable coding coordination requires running workspace services and precise permissions |
| [fx](https://github.com/skishore23/fx) | Later | Good typed agent-design material; needs a narrow executable value proposition |
| [LambdaCat](https://github.com/skishore23/LambdaCat) | Later | Potential teaching and composition checking; smaller specialist audience |
| [Topological-MCTS-ARC](https://github.com/skishore23/Topological-MCTS-ARC) | Later | Research harness; should first expose small supported experiments and dataset rights/requirements |
| [receipt-cli](https://github.com/skishore23/receipt-cli) | Not standalone | Release distribution for a hosted connect flow; not an independent product workflow |
| [clauden](https://github.com/skishore23/clauden) | Defer | Local account/proxy infrastructure; portability, credential handling and provider terms need separate assessment |
| [Temporal](https://github.com/skishore23/Temporal) | Skip first batch | Deployment template rather than differentiated end-user capability |
| [n8n](https://github.com/skishore23/n8n) | Skip first batch | Deployment template; existing n8n integrations already cover the broader workflow |
| [qreates-deploy](https://github.com/skishore23/qreates-deploy) | Insufficient evidence | No available README; needs product/ownership/deployment investigation before positioning |
| [react-app](https://github.com/skishore23/react-app) | Insufficient evidence | No available README or differentiated product description |
| [Charaka](https://github.com/skishore23/Charaka) | Skip first batch | Old application with only basic launch instructions; substantial rediscovery needed |

## Publication

Publisher-approved settings: individual Kishore Shimikeri, all available countries, free distribution, no publisher telemetry/uploads, public GitHub Issues support. These are publication choices, not proof that the portal has verified the developer identity.

Public GitHub availability, private plugin creation, directory draft upload, review submission and directory publication are distinct states. Follow the actual portal result. Skills-only packages do not require initial MCP review examples or a demo recording. Identity verification and current legal attestations still belong to the authorized developer. [OpenAI submission guide](https://developers.openai.com/plugins/deploy/submission).
