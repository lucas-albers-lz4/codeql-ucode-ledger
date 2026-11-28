#181 fail-open audit — pass 2 (2026-11-28)

Read-only against pinned producer main `9166af76…`, plus two query evaluations against the
existing `routing-remeasure/db2` (no new database built; no second heavy run; slot honored).
`q-template-flow.ql` is the corpus-wide generalization of the shipped `TemplateNoValueFlow.ql`.

## Pass-1 carried forward
Census #180 joined on snake_case kind literals; the flow layer is class-based
(`T<Camel>`). 6 of the 29 "no-flow" kinds actually have kind references. This pass gives
rule-cited verdicts per the acceptance criteria.

## Verdicts (acceptance item 1)

| kind | verdict | citation |
|---|---|---|
| `primary_expression`, `declaration`, `expression_statement` (+ wrappers `expression`, `statement`) | **intentionally-transparent** | `canonicalNode` excludes `TExpression`/`TPrimaryExpression`/`TStatement`/`TDeclaration` — children flow directly (`controlflow/internal/ControlFlowGraphImpl.qll:670-675`) |
| `optional_chain` | **covered-generic** | `?.` short-circuit modeled as a CFG choice via `optionalCall`/`optionalSubscript`/`hasOptionalChain` (`:638,640,644-666`); token is a marker, not a value node |
| `template_string`, `template_substitution` | **intentional boundary — with a security caveat** (see below) | value-node absence is documented (`dataflow/internal/DataFlowPrivate.qll:675` "…templates… have neither") and *smoke-tested* (`ql/src/extractor-smoke/TemplateNoValueFlow.ql`, `TemplateCfgContract.ql`) |
| `true`, `false`, `null`, `number`, `regex`, `regex_pattern`, `regex_flags`, `comment`, `hash_bang_line` | **intentionally-transparent** (leaf/non-value) | same `DataFlowPrivate.qll:675` note; regex internals + comments are not value-producing expressions |
| `import_clause`, `named_imports`, `namespace_import`, `export_clause`, `export_specifier`, `default`, `else_clause`, `else_alt_clause`, `switch_body`, `computed_property_name`, `empty_statement`, `arguments` | **covered-generic** (structural/child traversal) | pass-3 must attach the exact per-kind successor rule; not independently re-verified this pass |

## Material finding — template interpolation is model-only, not generic

Corpus-wide over the extracted slice: **80 template strings, 93 substitution expressions,
0 template strings with a dataflow value node, 77/93 substitution expressions with one.**

- Confirms `TemplateNoValueFlow`'s required-empty result is real (not test-file-specific).
- Taint from `` `…${x}…` `` is visible up to `x` (77/93) but **does not exit across the
  template boundary via generic `localFlowStep`** — by design, since interpolation
  transforms the value.
- Consequence: `popen(\`cmd ${x}\`)` is caught **only** by the bespoke M3 model
  (`m3/Models.qll:395-403`, which keys on `shellquote(...)` inside the substitution).
  A raw (unshellquoted) interpolation into an exec sink is **not** detected generically.
  This is the one genuinely actionable fail-open item: not a missing CFG edge to add
  blindly (that would be unsound value-flow), but a *diagnostic* — flag any
  substitution-expression carrying taint into a template whose value reaches an exec sink,
  labeled "interpolation boundary — model-dependent".
- 16/93 substitution expressions have no CFG value node at all → pass-3 investigation.

## Acceptance status

- Item 1 (per-kind verdict): substantially done; 12 structural kinds need exact-rule
  citations in pass 3 to be fully discharged.
- Items 2-4 (needs-rule fail-open + witnesses + standing diagnostic): template boundary
  yields one concrete diagnostic proposal; witnesses not yet run (needs heavy slot).
- **No gate lifted; no `path_found`; no runtime claim.** Pass 2 corrects census #180's
  flow interpretation and converts the scariest candidate (template FN) into a documented,
  test-backed boundary plus one targeted fail-open recommendation.
