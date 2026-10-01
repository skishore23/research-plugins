# WorldZero Lab

Run paired built-in agent baselines in WorldZero simulated worlds, inspect measured outcomes and verify deterministic replay. Includes the original research kernel and bounded offline commands. These demonstrations do not run LLM inference or certify causal discovery. Requires Python 3.11+, NumPy and a host with file and shell access.

Publisher: Kishore Shimikeri. Version 0.1.0.

## Try it

- Compare forager and experimenter on seed 17 with a 100-decision budget.
- Run the four built-in baselines on two matching seeds and explain censoring.
- Save the traces for a small reproducible WorldZero comparison.

Install the ZIP in a compatible skills host. Open the included skill for the exact workflow. The executable steps require a Python environment with shell/file tools; if the host cannot execute code, it can help draft inputs but must not claim that checks ran.

Dependencies: create a virtual environment and install `requirements.txt` before running the script. Installation downloads dependencies from your configured package index.

Upstream: https://github.com/skishore23/worldzero. See PROVENANCE.json for exact source revision and file hashes. See LICENSE and THIRD_PARTY.md for reuse terms.

The ZIP is a skills plugin, not a hosted MCP application. Marketplace status: preparation in progress; not submitted or published.
