# Research Plugins

Three portable plugins by Kishore Shimikeri, derived from existing open-source projects.

- **Comfy Story Planner:** validate film continuity and timing, compile candidate shot prompts, export SRT.
- **WorldZero Lab:** run matched baseline experiments with deterministic replay evidence.
- **Heimdall Policy Lab:** draft policies and check schema, guard parameter names and composition structure.

[Public catalog](https://skishore23.github.io/research-plugins/) · [Project research](docs-research.md) · [Support](https://github.com/skishore23/research-plugins/issues)

These are skills with executable Python tools, not hosted MCP servers. Execution requires a compatible host with file and shell access. Directory publication is pending. Free distribution; all available countries are intended. Verification and current legal attestations must be completed by the publisher in the submission portal.

## Develop and verify

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest tests -q
.venv/bin/python scripts/build_site.py
python3 -m http.server 8769 --directory docs
```

`scripts/package.py` validates portable manifests, listing lengths, icons, public-upload restrictions, compatibility metadata, ZIP contents and file hashes. It writes deterministic single-plugin ZIPs to `dist/`. `scripts/build_site.py` builds the GitHub Pages site in `docs/`, including the same ZIPs and release checksums. Dependencies are downloaded during installation; the supported tool commands do not upload task inputs.

Vendored sources are pinned in each plugin's `PROVENANCE.json`. Tests cover the exposed wrappers and their integrations; the complete upstream test suites are not claimed to have run. The WorldZero website example is a recorded 20-decision run, not live browser execution.

Each package includes its own license and notices. Comfy Story Planner is AGPL-3.0-only, WorldZero Lab is Apache-2.0, and Heimdall Policy Lab is MIT. New collection website/build/test files are MIT (see LICENSE). The per-package licenses govern the corresponding plugin code and source.
