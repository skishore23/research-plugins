import copy
import importlib.util
import json
from pathlib import Path
import sys
import os
import pytest
ROOT = Path(os.environ.get("PLUGIN_TEST_ROOT", Path(__file__).resolve().parents[1]))


def module(plugin, name):
    path = ROOT / 'plugins' / plugin / 'scripts' / (name + '.py')
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

planner = module('comfy-story-planner', 'planner')
policy = module('heimdall-policy-lab', 'policy_lab')
lab = module('worldzero-lab', 'lab')
PLAN = json.loads((ROOT/'plugins/comfy-story-planner/examples/film-plan.json').read_text())
POLICY = json.loads((ROOT/'plugins/heimdall-policy-lab/examples/tool-policy.json').read_text())


def load_plan(tmp_path, data):
    p = tmp_path/'plan.json'; p.write_text(json.dumps(data))
    return planner.load(p)


def test_storyboard_offsets_and_subtitles(tmp_path):
    p = load_plan(tmp_path, PLAN)
    report = planner.report(p)
    assert [(s['start_ms'],s['end_ms']) for s in report['shots']] == [(0,4000),(4000,8000),(8000,12000)]
    assert '00:00:08,000 --> 00:00:09,500' in planner.subtitle_srt(p)
    assert all(s['candidate_prompt'] for s in report['shots'])


@pytest.mark.parametrize('change', ['continuity','duration','future_dependency','cast','cue'])
def test_film_invalid_contracts(tmp_path, change):
    p = copy.deepcopy(PLAN)
    if change=='continuity': p['shots'][1]['effects']=[]
    elif change=='duration': p['target_duration_ms']=13000
    elif change=='future_dependency': p['shots'][0]['depends_on']=['departure']
    elif change=='cast': p['shots'][0]['absent']=['Mira']
    else: p['shots'][0]['dialogue'][0]['end_ms']=5000
    with pytest.raises(ValueError): load_plan(tmp_path,p)


def test_plan_duplicate_json_rejected(tmp_path):
    p=tmp_path/'bad.json';p.write_text('{"shots":[],"shots":[]}')
    with pytest.raises(ValueError,match='duplicate'):planner.load(p)


def test_valid_policy_and_warnings():
    assert policy.lint(POLICY)['valid']
    p=copy.deepcopy(POLICY);p['performance']['fail_mode']='open'
    assert any('Fail-open' in x for x in policy.lint(p)['warnings'])


@pytest.mark.parametrize('expr', ['__import__("os").system("echo hacked")','tools_allowlist.__class__','[x for x in tools_allowlist]','kOf(2, tools_allowlist)','unless(tools_allowlist)','input','True'])
def test_unsafe_or_invalid_compositions(expr):
    p=copy.deepcopy(POLICY);p['compose']['root']=expr
    assert not policy.lint(p)['valid']


def test_valid_nested_composition():
    p=copy.deepcopy(POLICY);p['compose']['root']='allOf(kOf(1, tools_allowlist), seq(tools_allowlist), parallel=True)'
    assert policy.lint(p)['valid']


def test_unknown_and_missing_parameters():
    p=copy.deepcopy(POLICY);p['guards'][0]['with']={'allowed_toolz':['read_story']}
    result=policy.lint(p)
    assert not result['valid']
    assert len(result['errors'])==2


@pytest.mark.parametrize('raw',['guards: []\nguards: []','guards: &a [*a]','!!python/object/apply:os.system [echo bad]'])
def test_yaml_input_restrictions(tmp_path,raw):
    path=tmp_path/'bad.yaml';path.write_text(raw)
    with pytest.raises((ValueError,policy.yaml.YAMLError)):policy.load(path)


def test_unknown_schema_field():
    p=copy.deepcopy(POLICY);p['secret_runtime_override']=True
    assert not policy.lint(p)['valid']


def test_worldzero_reproducible_replay_and_tampering():
    first=lab.compare([17],['forager'],3)
    second=lab.compare([17],['forager'],3)
    assert first==second
    assert first['runs'][0]['replay']['verified']
    assert first['llm_inference_executed'] is False
    _,_,trace=lab.simulate(17,'forager',lab.Config(max_decisions=3),capture=True)
    original=lab.digest(trace)
    trace['final']['time'] += 1
    with pytest.raises((ValueError,AssertionError)):
        lab.verify_replay(trace,expected_trace_sha256=original)


def test_worldzero_bounds_and_preserve_existing(tmp_path):
    for seeds,policies,decisions in [([1]*2,['random'],3),([-1],['random'],3),([1],['llm'],3),([1],['random'],501)]:
        with pytest.raises(ValueError):lab.compare(seeds,policies,decisions)
    with pytest.raises(FileExistsError):lab.compare([17],['forager'],3,tmp_path)
