#!/usr/bin/env python3
"""Validate and compile portable film plans with Comfy Story's original contracts."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'vendor'))
from comfy_story.film_io import film_plan_from_json
from comfy_story.film_plan import compile_candidate_prompt, subtitle_srt


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON field: ' + key)
        result[key] = value
    return result


def load(path):
    raw = Path(path).read_bytes()
    if len(raw) > 1024 * 1024:
        raise ValueError('plan exceeds 1 MiB')
    data = json.loads(raw, object_pairs_hook=unique, parse_constant=lambda x: (_ for _ in ()).throw(ValueError('non-finite JSON')))
    plan = film_plan_from_json(json.dumps(data, allow_nan=False))
    if len(plan.shots) > 256:
        raise ValueError('planner supports at most 256 shots')
    return plan


def report(plan):
    offset = 0
    rows = []
    for i, shot in enumerate(plan.shots):
        rows.append({'shot_id': shot.shot_id, 'start_ms': offset, 'end_ms': offset + shot.duration_ms,
                     'sha256': shot.digest, 'candidate_prompt': compile_candidate_prompt(plan, i)})
        offset += shot.duration_ms
    return {'valid': True, 'title': plan.title, 'duration_ms': offset, 'shots': rows,
            'render_preflight': {'fps': 24, 'all_shots_frame_aligned': all(s.duration_ms * 24 % 1000 == 0 for s in plan.shots),
                                 'all_shots_within_15_seconds': all(s.duration_ms <= 15000 for s in plan.shots)},
            'scope': 'Authored plan only. No video generated or visually verified; no takes accepted.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'storyboard', 'subtitles'])
    parser.add_argument('plan', type=Path)
    args = parser.parse_args()
    try:
        plan = load(args.plan)
        if args.command == 'subtitles':
            print(subtitle_srt(plan))
        else:
            result = report(plan)
            if args.command == 'validate':
                for row in result['shots']:
                    row.pop('candidate_prompt')
            print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    except (ValueError, TypeError, OSError, RecursionError) as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        return 2
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
