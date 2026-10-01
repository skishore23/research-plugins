---
name: compare-agent-baselines
description: Run reproducible WorldZero simulated-agent baseline comparisons, inspect censoring and outcomes, and save replay-verified traces without model API calls.
---

# Compare baseline agents

Resolve the plugin root as `../..` from this skill. Read `../../references/experiment-contract.md` before interpreting outputs. The implementation uses the pinned WorldZero kernel, not a language-model simulation.

1. Confirm Python 3.11+ and NumPy are available. Use an existing suitable environment or create an isolated virtual environment and install the bundled requirements with the host's permitted package installer. Do not claim offline installation if dependencies must be downloaded.
2. Default to seed 17, policies forager and experimenter, and 100 decisions. State these parameters. To execute, run `python /absolute/plugin/root/scripts/lab.py --seeds 17 --policies forager experimenter --decisions 100`. The script limits comparisons to eight unique seeds, four built-in policies, and at most 500 decisions per run. Start small; larger runs may take minutes.
3. For persisted evidence, add `--trace-dir /absolute/new/output-directory`. The directory must not already exist; never remove existing evidence to make a run succeed. Save JSON stdout separately to a new comparison file.
4. Report one row per seed and policy, with result status/censoring where present, age, energy, decisions, functional assembly/retention where present, and replay status. Use returned fields; do not invent metrics. Compare only matched seed/budget settings. Explain when a budget-censored episode prevents a completed-survival conclusion.
5. Include config, trace digests and evidence file paths. Each captured trace is replayed before success is reported. A digest is an integrity reference, not an external authentication or proof of scientific merit.

The informed baseline receives evaluator-only hidden knowledge and is an upper/control comparison, not a fair discovery agent. These small runs are demonstrations, not preregistered held-out evaluations. No LLM inference is run, so do not claim a ChatGPT/model benchmark or causal discovery success. No remote model, third-party law plugin, arbitrary policy code, server or GPU is exposed by this wrapper. Use the upstream research protocol for deeper evaluation rather than silently expanding this plugin's claims. If dependencies or execution are unavailable, explain the limitation and provide reproducible commands, with results marked not run.
