# Experiment contract
The wrapper uses the upstream legacy catalysis world through simulate(seed, policy, Config(max_decisions=...), capture=True), then verify_replay with the recorded trace digest. NumPy is pinned for this release. All other Config values are returned with results. Same-seed baseline runs share the world design/random streams, but differing actions cause different trajectories.

The wrapper intentionally exposes only random, forager, experimenter and informed. The last has hidden evaluator knowledge. It does not run LLMs, load community law families, execute arbitrary policy factories or expose a network server. Vendored upstream code contains broader research features, but these are outside this plugin's supported entry point.

A censored run reached a budget boundary; do not count it as a completed survival. Replay consistency validates repeatability of the captured trajectory, not the truth of a research hypothesis. Positive results on one seed are exploratory. Retain original traces, config, upstream commit and comparison output together.
