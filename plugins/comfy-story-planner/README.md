# Comfy Story Planner

Turn a film idea into a continuity-aware shot plan, validate exact timing, compile candidate prompts and export authored dialogue as SRT. Uses original Comfy Story contracts. No GPU needed for planning; does not render video or verify visual continuity. Requires Python 3.11+ and a host with file and shell access.

Publisher: Kishore Shimikeri. Version 0.1.0.

## Try it

- Plan a 12-second film about lending a key, with three shots and consistent ownership.
- Check my film plan for timing and continuity errors.
- Export the dialogue in my film plan as timed SRT subtitles.

Install the ZIP in a compatible skills host. Open the included skill for the exact workflow. The executable steps require a Python environment with shell/file tools; if the host cannot execute code, it can help draft inputs but must not claim that checks ran.

Uses only the Python standard library.

Upstream: https://github.com/skishore23/comfy-story. See PROVENANCE.json for exact source revision and file hashes. See LICENSE and THIRD_PARTY.md for reuse terms.

The ZIP is a skills plugin, not a hosted MCP application. Marketplace status: preparation in progress; not submitted or published.
