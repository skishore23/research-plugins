#!/usr/bin/env python3
"""Run bounded, paired WorldZero baseline experiments and verify captured replay."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'vendor'))
from worldzero.kernel import Config
from worldzero.experiment import simulate, verify_replay
from worldzero.util import digest

POLICIES = ('random', 'forager', 'experimenter', 'informed')


def compare(seeds, policies, decisions=100, trace_dir=None):
    if not seeds or len(seeds) > 8 or len(set(seeds)) != len(seeds) or any(type(s) is not int or not 0 <= s <= 2147483647 for s in seeds):
        raise ValueError('provide 1–8 unique integer seeds between 0 and 2147483647')
    if not policies or len(set(policies)) != len(policies) or any(p not in POLICIES for p in policies):
        raise ValueError('choose unique built-in baseline policies')
    if type(decisions) is not int or not 1 <= decisions <= 500:
        raise ValueError('decisions must be an integer between 1 and 500')
    if trace_dir is not None:
        trace_dir = Path(trace_dir)
        trace_dir.mkdir(parents=True, exist_ok=False)
    config = Config(max_decisions=decisions)
    rows = []
    for seed in seeds:
        for policy in policies:
            _, result, trace = simulate(seed, policy, config, capture=True)
            trace_hash = digest(trace)
            replay = verify_replay(trace, expected_trace_sha256=trace_hash)
            if not replay['verified']:
                raise ValueError('replay verification failed')
            row = {'seed': seed, 'policy': policy, 'result': result, 'replay': replay, 'trace_sha256': trace_hash}
            if trace_dir is not None:
                path = trace_dir / f'{seed}-{policy}.json'
                path.write_text(json.dumps(trace, allow_nan=False) + '\n')
                row['trace_file'] = str(path)
            rows.append(row)
    return {'schema': 'worldzero-lab-comparison-v1', 'config': asdict(config), 'runs': rows,
            'llm_inference_executed': False, 'scope': 'Paired built-in baseline demonstration, not a held-out benchmark or proof of causal discovery. Informed has evaluator-only knowledge. Censored runs must be reported separately.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seeds', nargs='+', type=int, default=[17])
    parser.add_argument('--policies', nargs='+', choices=POLICIES, default=['forager', 'experimenter'])
    parser.add_argument('--decisions', type=int, default=100)
    parser.add_argument('--trace-dir', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(compare(args.seeds, args.policies, args.decisions, args.trace_dir), indent=2, allow_nan=False))
    except (ValueError, OSError, AssertionError) as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        return 2
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
