# Submission handoff — three independent plugins

Each package is a separate install and needs a separate plugin identity/listing in the OpenAI portal. This repository and its catalog are shared source hosting only; there is no all-in-one plugin ZIP.

| Display name | Portable identity | Upload file |
|---|---|---|
| Comfy Story Planner | comfy-story-planner | dist/comfy-story-planner-0.1.0.zip |
| WorldZero Lab | worldzero-lab | dist/worldzero-lab-0.1.0.zip |
| Heimdall Policy Lab | heimdall-policy-lab | dist/heimdall-policy-lab-0.1.0.zip |

## Completed

- Actual executable workflows, examples and source provenance, with original licenses.
- Publisher-provided identity: Kishore Shimikeri (individual); portal verification remains unverified.
- Publisher-selected countries: all available; free; no publisher telemetry/uploads; GitHub Issues support.
- Separate square PNG icons and listing metadata for each plugin.
- Public website, support, privacy and terms pages: all 12 fetched and content verified.
- All three published ZIP checksums matched the locally validated packages.
- Portable manifest and Codex compatibility validation passed.
- 23 regression tests passed against the extracted ZIPs; GitHub CI passed.
- Local browser layout, continuity interaction and example panels checked.
- GitHub source, Pages catalog and v0.1.0 release published.

## Not completed

- No public-directory draft was uploaded, review submitted or directory release published.
- In-app browser access to https://platform.openai.com/plugins remained on Cloudflare verification. The publisher was asked to complete sign-in/verification in a browser.
- Developer identity and intended organization/project could not be inspected in the portal.
- Host-level installation and conversational behavior in ChatGPT/Codex are unverified; executable tests do not prove the host exposes Python/file/shell capabilities.
- Current legal/policy attestations must be completed by the authorized developer.

## Continue

Open https://platform.openai.com/plugins in the intended verified individual publisher organization/project. Upload each ZIP independently; inspect the imported display name, icon, countries, skills and listing links for each saved version. Complete required scans and publisher attestations. These skills-only packages have no MCP server, so do not invent connection URLs, MCP cases or demo recordings. Follow the portal's actual review/publication state and verify each resulting public listing.

Private account creation via Plugin Creator is a separate operation and was not substituted for public-directory submission. Do not create duplicate private identities to represent an uploaded directory draft.

References: https://developers.openai.com/plugins/deploy/submission and the Plugin Creator prepare-plugin-submission skill used in this task.
