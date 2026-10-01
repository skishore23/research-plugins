#!/usr/bin/env python3
"""Offline policy structure checks; never executes expressions or enforces live requests."""
import argparse
import ast
import json
from pathlib import Path
import sys
import jsonschema
import yaml
ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / 'vendor/policy.schema.json').read_text())
CATALOG = json.loads((ROOT / 'references/guard-catalog.json').read_text())
COMBINATORS = {'seq', 'allOf', 'anyOf', 'kOf', 'unless'}


class UniqueLoader(yaml.SafeLoader):
    pass


def mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise ValueError('policy mapping keys must be unique strings')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def load(path):
    raw = Path(path).read_text()
    if len(raw.encode()) > 262144:
        raise ValueError('policy exceeds 256 KiB')
    # Alias expansion is unnecessary for the supported portable subset.
    if any(isinstance(t, (yaml.tokens.AliasToken, yaml.tokens.AnchorToken)) for t in yaml.scan(raw)):
        raise ValueError('YAML aliases and anchors are unsupported; expand values explicitly')
    return yaml.load(raw, Loader=UniqueLoader)


def expression(expr, names):
    tree = ast.parse(expr, mode='eval')
    if sum(1 for _ in ast.walk(tree)) > 256:
        raise ValueError('composition exceeds 256 syntax nodes')
    used = set()
    def check(node):
        if isinstance(node, ast.Name) and node.id in names:
            used.add(node.id)
            return
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id not in COMBINATORS:
            raise ValueError('only guard names and seq/allOf/anyOf/kOf/unless calls are supported')
        args = list(node.args)
        name = node.func.id
        if node.keywords:
            if name != 'allOf' or len(node.keywords) != 1 or node.keywords[0].arg != 'parallel' or not isinstance(node.keywords[0].value, ast.Constant) or type(node.keywords[0].value.value) is not bool:
                raise ValueError('only allOf(..., parallel=true/false) is supported (Python True/False in expressions)')
        if name == 'kOf':
            if not args or not isinstance(args[0], ast.Constant) or type(args[0].value) is not int:
                raise ValueError('kOf requires an integer threshold')
            k = args.pop(0).value
            if not 1 <= k <= len(args):
                raise ValueError('kOf threshold must be between 1 and the number of guards')
        if not args or (name == 'unless' and len(args) != 2):
            raise ValueError('combinator arity is invalid')
        for arg in args:
            check(arg)
    check(tree.body)
    return used


def lint(data):
    errors = [{'path': '/'.join(map(str,e.path)), 'message': e.message} for e in jsonschema.Draft7Validator(SCHEMA).iter_errors(data)]
    warnings = []
    if errors:
        return {'valid': False, 'errors': errors, 'warnings': warnings}
    names = {}
    for guard in data['guards']:
        gid = guard['id']; alias = gid.replace('.', '_')
        if alias in names or alias in COMBINATORS:
            errors.append({'path': 'guards', 'message': 'duplicate or ambiguous guard alias: '+alias})
        names[alias] = gid
        if gid not in CATALOG:
            errors.append({'path': 'guards', 'message': 'guard is absent from the pinned catalog: '+gid})
        else:
            params = guard.get('with', {})
            spec = CATALOG[gid]
            if not spec['variadic']:
                for k in params.keys() - set(spec['parameters']):
                    errors.append({'path': 'guards/'+gid, 'message': 'unknown parameter: '+k})
            for k in set(spec['required']) - params.keys():
                errors.append({'path': 'guards/'+gid, 'message': 'missing required parameter: '+k})
        if 'with_ref' in guard:
            errors.append({'path': 'guards/'+gid, 'message': 'external with_ref files are unsupported; inline parameters'})
        if guard.get('enabled') is False:
            warnings.append('Disabled guard: '+gid)
    used = set()
    for phase, expr in data['compose'].items():
        try:
            refs = expression(expr, set(names))
            if phase == 'root': used = refs
        except (ValueError, SyntaxError, RecursionError) as e:
            errors.append({'path':'compose/'+phase,'message':str(e)})
    for alias in names.keys() - used:
        warnings.append('Guard not referenced by root: '+names[alias])
    if data.get('performance',{}).get('fail_mode') == 'open':
        warnings.append('Fail-open configuration: runtime failures may pass requests.')
    if data.get('failure_mode') == 'warn':
        warnings.append('Warn mode does not promise blocking.')
    return {'valid':not errors, 'errors':errors, 'warnings':warnings,
            'guard_count':len(data['guards']), 'scope':'Static schema, catalog parameter names, and composition checks only. Parameter semantics, JSONPath behavior, runtime enforcement and compliance are unverified.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['lint','catalog'])
    p.add_argument('policy',nargs='?',type=Path)
    args=p.parse_args()
    try:
        if args.command == 'catalog':
            result=CATALOG
        else:
            if args.policy is None: p.error('lint requires a policy file')
            result=lint(load(args.policy))
        print(json.dumps(result,indent=2,allow_nan=False))
        return 0 if result.get('valid',True) else 1
    except (ValueError,TypeError,OSError,yaml.YAMLError,RecursionError) as e:
        print(json.dumps({'error':str(e)}),file=sys.stderr)
        return 2
if __name__ == '__main__':
    raise SystemExit(main())
