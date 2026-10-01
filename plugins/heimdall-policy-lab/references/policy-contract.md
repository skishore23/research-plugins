# Policy contract
The original Draft 7 JSON Schema is extracted as JSON from Heimdall's policy_schema.py. guard-catalog.json is generated from register_factory decorators and Python function signatures in the pinned source. No imported guard code executes during catalog extraction or linting.

Lint adds a deliberately restricted AST walk. Names must be declared guards; calls must be seq, allOf, anyOf, kOf or unless. kOf requires an integer threshold within the number of guard arguments. unless needs two arguments. allOf optionally accepts parallel=True or False. Attribute access, imports, arbitrary calls, comprehensions, phase references and expression evaluation are unsupported. Unknown guards and aliased name collisions fail.

Checks cover JSON structure and parameter names, not parameter types/meaning beyond the policy schema, runtime guard availability, JSONPath evaluation, policy signatures, latency or enforcement. with_ref is rejected to avoid reading external files. YAML aliases/anchors and duplicate fields are rejected. Fail-open and unused/disabled guards are warnings, not silently fixed. Validate the selected policy in a staging Heimdall runtime before deploying it.
