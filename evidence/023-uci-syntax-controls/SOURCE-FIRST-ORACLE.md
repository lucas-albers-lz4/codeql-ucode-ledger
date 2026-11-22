# Wave 4 source-first plan and oracle

Status: source-derived expectations prepared before any query/output inspection. No CodeQL, extractor, database, or query was run for this preparation. This is a syntactic inventory oracle only; it makes no claim about lexical resolution, dynamic dispatch, call binding, forwarding flow, UCI write semantics, persistence, authorization, or runtime effects.

## Pins and provenance

- Producer repository: `codeql-ucode`, detached checkout `work/wave4-prep/codeql-ucode`, commit `0a6612fe0e66351a0ccda43ad5b51f5ef5a2724e`, clean at preparation (`git status --porcelain=v1` empty). The issue-53 audit was read from `docs/issue-53-uci-inventory.md` at this pin.
- Real upstream source: OpenWrt LuCI, detached checkout `work/wave4-prep/luci-pinned`, commit `b2e0be4b46ec0fd43394c081fa7c50657af14011`, clean at preparation. File `modules/luci-base/ucode/controller/admin/uci.uc`; Git blob `c38a42b10bfefbaa31741feae9395abd8a1f8e40`; SHA-256 `ac75cfef7d74f87ed7f957778004a7bf486c76df699398c215795b4947e0c93e`.
- Consumer inventory says this source is installed as `/usr/share/ucode/luci/controller/admin/uci.uc`. That is a recorded mapping, not a reproduction of an OpenWrt build or installation transformation.
- Synthetic controls are authored under `work/wave4-prep/source-controls/`, each as a separate source identity. Their expected rows are defined below before any extractor/query execution. Hashes are listed in [pins-and-digests.json](pins-and-digests.json).

## Real-source expected identities

Coordinates are 1-based lines and columns, inclusive, measured on the pinned UTF-8 source. The expected selector is a call expression with its callee kind/name and ordered semantic arguments; punctuation is excluded from argument nodes. A checker should retain either AST entity identity or a distinct-entity count per projected tuple. Equal file/location/argument tuples can arise from multiple AST entities; row count alone is not an identity assertion.

| ID | Source identity | Enclosing declaration | Expected syntactic shape | Exact expected argument literals/spans | Boundary |
|---|---|---|---|---|---|
| R1 | `uci.uc`, line 79; callee `ubus_call` at 9–17 | `uci_apply`, declared line 47 | `CallExpression`, function child cast to `Identifier`; ordered arguments 0, 1, 2 | arg0 `'uci'` 19–23; arg1 `'commit'` 26–33; arg2 object literal 36–80 | Candidate indirect call. Do not conclude that this identifier resolves to R2 or that any arguments flow to R2. |
| R2 | `uci.uc`, line 28; callee `ubus.call` at 12–20 | `ubus_call`, declared line 25 | `CallExpression`, function child is a `MemberExpression`; receiver text `ubus`, property text `call`; ordered arguments are identifiers | arg0 `object` 22–27; arg1 `method` 30–35; arg2 `args` 38–41 | Helper-body forwarding-shaped syntax only. No binding/forwarding-flow conclusion. |
| R3 | `uci.uc`, line 76; callee `ubus_call` at 17–25 | `uci_apply`, declared line 47 | Identifier call; arg0 / arg1 / arg2 in order | arg0 `'uci'` 27–31; arg1 `'changes'` 34–42; arg2 begins at col 45 with an object literal | Discriminating UCI `changes` call, not `commit`. |
| R4 | `uci.uc`, line 59; callee `ubus.call` at 4–12 | `uci_apply`, declared line 47 | Member call; receiver `ubus`, property `call`; ordered args | arg0 `'session'` 14–22; arg1 `'set'` 25–29; arg2 object begins col 32 | Session `set`, not UCI `set`; separate from helper identifier calls. |
| R5 | `uci.uc`, line 144; callee `ubus_call` at 22–30 | `action_revert`, object property function declared line 143 | Identifier call with ordered args | arg0 `'uci'` 32–36; arg1 `'changes'` 39–47; arg2 object begins col 50 | Second `changes` occurrence; preserve it as a separate source identity. |
| R6 | `uci.uc`, line 145; callee `ubus_call` at 9–17 | `action_revert`, declared line 143 | Identifier call with ordered args | arg0 `'uci'` 19–23; arg1 `'revert'` 26–33; arg2 object begins col 36 | Nearby different UCI method. |

The source inventory contains one `ubus_call('uci', 'commit', ...)` candidate (R1), one local helper declaration named `ubus_call` (line 25), and one `ubus.call(object, method, args)` member call in that helper body (R2). The source layout alone does not prove those are a caller/callee edge. Do not relabel R1 as a direct `cursor().commit()` or direct cursor write.

## Synthetic valid syntax controls and expected discriminations

All controls are independent files, so filenames are intended source identities. Their forms use ordinary function declarations/calls and member access matching constructs present in the pinned source; no parser or extractor has been run, so parser acceptance remains to be verified in a later authorized extraction stage. Expected spans below are literal source positions and form the oracle before result inspection.

| ID | File | Expected syntax | Expected distinction |
|---|---|---|---|
| C1 | `source-controls/changes.uc` | `probe` contains identifier call `ubus_call('uci','changes',{})` at line 2; args 0=`'uci'` cols 19–23; 1=`'changes'` cols 26–34; 2=`{}` col 37–38 | Same object, different method from R1. |
| C2 | `source-controls/session-set.uc` | `probe` contains member call `ubus.call('session','set',{})` at line 2; args 0 cols 19–27, 1 cols 30–34, 2 cols 37–38 | Direct member callee and session object distinguish from identifier-shaped R1. |
| C3 | `source-controls/unrelated-same-name-helper.uc` | declaration `ubus_call` lines 1–3 returns `logger(...)`; `probe` line 6 calls `ubus_call('uci','commit',{})` with args 0 cols 19–23, 1 cols 26–33, 2 cols 36–37 | Candidate-like identifier call and same helper spelling, but the declared helper body has no `ubus.call` syntax. This is a counterexample to name-only forwarding assumptions, not a binding-resolution test. The draft query selects the line-6 candidate, not line-2 `logger`. |
| C4 | `source-controls/property-read.uc` | line 2 contains `api.ubus_call` as a member/property read, not a `CallExpression`; `saved` is returned at line 3 | Must not count a property read as a call. |
| C5 | `source-controls/unknown-direct-call.uc` | member call `ubus.call('vendor_unknown','method_unknown',{})` at line 2; args 0 cols 19–34, 1 cols 37–52, 2 cols 55–56 | Recognize direct member-call syntax while retaining unknown object/method strings; no semantic target claim. |
| C6 | `source-controls/swapped-argument-order.uc` | identifier call `ubus_call('commit','uci',{})` at line 2; arg0 cols 19–26, arg1 cols 29–33, arg2 cols 36–37 | Same literals as R1 in the wrong positions must fail the R1 ordered-argument oracle. |

For C3, the expected source facts are: a function declaration whose identifier text is `ubus_call`; its body contains a call to `logger`, not a member call to `ubus.call`; and a separate identifier call in `probe` whose source spelling matches R1. Do not infer that a query can bind the `probe` call to that declaration unless the binding model is separately established.

## Multiplicity and evidence boundary

- Report source-site multiplicity: R1–R6 are six distinct source call expressions, with R3 and R5 both `uci/changes` but different file locations/parents.
- For query output, include AST entity identity when available. If the projected tuple omits node identity and duplicates, provide a per-tuple distinct entity count; do not deduplicate or accept a row count as proof of one entity.
- Argument positions must be taken from `Arguments.getChild(0/1/2)` (semantic typed children with punctuation filtered) as Sol advised; `getParentIndex()` is not the same convention because it counts raw non-extra children. Add the swapped-order control C6.
- The presence of a `ubus_call` identifier call, a same-spelled function declaration, and a `ubus.call` member call in a helper body are three source observations. No caller binding or argument forwarding relation is asserted.
- This scope does not test or model `cursor().set/commit/delete`; the candidate is an indirect ubus method invocation only.

## Planned query shape (not executed here)

The unexecuted draft `query/Wave4UciCallSyntax.ql` selects only the predeclared source file/line identities above, requires exactly three semantic argument children, and distinguishes `UCODE::Identifier` from `UCODE::MemberExpression`. It emits raw call/callee/enclosing-function/parent/argument entities, source spans, callee spelling, typed member receiver/property, argument spelling when identifier or simple string, and argument count. The separate `query/Wave4PropertyReadControl.ql` selects the positive member-property node in C4 and explicitly excludes member nodes that are a call function. R5/R6 have enclosing `FunctionExpression` shapes, so the query reports nearest enclosing function kind and structural parent rather than assuming every enclosing function is a `FunctionDeclaration`. Raw AST argument nodes are selected with `Arguments.getChild(0/1/2)`; punctuation-filtered semantic indexes are distinct from raw `getParentIndex`. Literal values are matched to the source oracle, not treated as bindings or method semantics. Preserve all entity columns and do not collapse rows by location/text.

## Next gates

1. Verify selected source paths and expected identities against pinned bytes; preserve the manifest and SHA above.
2. If an extraction stage is authorized, independently confirm exact successful source identities and zero diagnostics for each intended positive/control file, and explicitly record parser errors if any.
3. Run the syntax-only query, compare exact nodes/arguments/spans to this predeclared oracle, and reconcile multiplicity by entity identity.
4. Keep any failures, ambiguous matches, and unsupported cases explicit. No consumer handoff or production model is implied.
