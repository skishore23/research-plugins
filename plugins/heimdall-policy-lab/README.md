# Heimdall Policy Lab

Draft and statically check Heimdall policies using its original JSON schema and a source-derived guard catalog. Find unknown fields, missing parameter names, invalid compositions and fail-open settings. No gateway, credentials or model calls needed. Does not enforce policies, validate runtime parameter semantics or certify compliance. Requires Python 3.11+, jsonschema, PyYAML and file/shell access.

Publisher: Kishore Shimikeri. Version 0.1.0.

## Try it

- Draft a Heimdall policy allowing only read_story and plan_shots tools.
- Check this Heimdall policy for structural mistakes and fail-open settings.
- Show the parameters for the tools.allowlist guard.

Install the ZIP in a compatible skills host. Open the included skill for the exact workflow. The executable steps require a Python environment with shell/file tools; if the host cannot execute code, it can help draft inputs but must not claim that checks ran.

Dependencies: create a virtual environment and install `requirements.txt` before running the script. Installation downloads dependencies from your configured package index.

Upstream: https://github.com/skishore23/heimdall. See PROVENANCE.json for exact source revision and file hashes. See LICENSE and THIRD_PARTY.md for reuse terms.

The ZIP is a skills plugin, not a hosted MCP application. Marketplace status: preparation in progress; not submitted or published.
