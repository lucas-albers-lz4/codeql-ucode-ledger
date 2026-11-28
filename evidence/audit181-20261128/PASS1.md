#181 fail-open audit — pass 1 (2026-11-28)

Read-only pass against pinned producer main `9166af76…`; no CodeQL execution, no heavy
slot, safe alongside other tracks. Script + JSON: `audit181.py`, `audit181-pass1.json`.

## Methodology finding (affects #180 census interpretation)

The #180 census classified kinds by whether the **snake_case kind literal** (e.g.
`"unary_expression"`) appeared in flow sources. But the CFG/data-flow layer is
**class-based**: it references T-prefixed AST classes (`TUnaryExpression`,
`TTemplateString`, …) defined in `controlflow/CfgNodes.qll` and consumed in
`controlflow/internal/ControlFlowGraphImpl.qll`. A kind can therefore be flow-covered
with zero snake_case hits. Pass 1 re-joins the 29 census "no-flow" kinds against the
class-based surface (`\bT<Camel>\b`).

Re-runnable, deterministic; the class-regex is itself an approximation — pass 2 must
confirm each hit is a real successor/flow rule and not a comment or type-decl.

## Pass-1 result

Of the 29 census audit-set kinds, re-joined against controlflow + dataflow
(`\bT<Camel>\b` class references):

- **6 kinds DO have kind-level flow references** (census undercounted):
  `declaration, primary_expression, empty_statement, expression_statement,
  lexical_declaration, unary_expression` — pass 2 must confirm each hit is a genuine
  successor/flow rule, not a comment or type-decl mention.
- **23 kinds have NO kind-level class reference** in controlflow+dataflow. Most are
  plausibly handled generically (leaf values `true/false/null/number`, regex internals
  `regex/regex_pattern/regex_flags`, import/export plumbing, comments, `arguments`,
  `optional_chain`, `switch_body`) — but that must be *shown*, not assumed.

## Material candidates for needs-rule (pass 2 priorities)

1. **`template_string` / `template_substitution`** — zero references. Backtick
   `` `...${expr}...` `` interpolation is the exact shape of the motivating shell/popen
   anchors (e.g. `` `... -c '${cmd} &'` ``). If `${expr}` value-flow to the template
   string is unmodeled, taint through interpolated strings is a **silent false negative**
   in .uc (not just .ut). Highest priority: verify whether `TAdd`/concatenation rules
   already cover template_string generically, or whether it genuinely lacks an edge.
2. **`optional_chain`** — appears only via `TCallExpression`/`TSubscriptExpression`
   optional-call predicates; confirm the `?.` short-circuit branch is modeled as a real
   choice (else `a?.b` could hide a tainted deref path).
3. **Leaf/regex/import-export kinds** — confirm the generic leaf handling in
   `DataFlowImplCommon`/`Ssa.qll` treats them as transparent (likely fine; document the
   citation, then mark intentionally-transparent).

## Status

- #181 acceptance item 1 (per-kind verdict): pass 1 gives a candidate verdict set;
  pass 2 (heavy slot) must confirm each with a rule citation and run witnesses for any
  `needs-rule` outcome. Not yet discharged.
- No gate lifted; no `path_found`; no runtime claim. This pass corrected census #180's
  interpretation — #180's table remains valid as a *string-literal* measurement but should
  not be read as the flow-coverage truth.
