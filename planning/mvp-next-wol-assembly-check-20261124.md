# Candidate after the direct RPC release: WOL command assembly

Status: read-only current-source security review, 2026-11-24. This is a
query-design candidate, not an alert or vulnerability finding. The pinned
LuCI source is clean at `b2e0be4b46ec0fd43394c081fa7c50657af14011`;
`applications/luci-app-wol/root/usr/share/rpcd/ucode/luci.wol` has Git blob
`fd9e9f0485ab6baec96ae089caf1089a6d471c99` and SHA-256
`51214ec57bcbd8d50e65016efda2a05e8eb7822dc7e510d014965834c61ef92b`.
It is selected in bounded corpus v0.4 and was extracted source-staged; no
installed-package byte comparison has been made.

At lines 37–42, the returned `exec.call(request)` handler sends
`request.args.args` through `map(..., shellquote)`, then `join(' ', parts)`
and concatenation into imported `fs.popen`. This is a concrete
request-to-sink **flow witness** outside the current direct-template rule.
The current source is an **alert near miss**: line 40 compares the requested
executable with two fixed path constants, and lines 11–13 define the
single-quoting callback used for arguments. The source observation does not
establish runtime safety, authorization or vulnerability.

The smallest next experiment is an exact AST witness query selecting the
handler, `request.args.args`, callback binding, `map` result, `join` result,
concatenation and imported `popen` call as distinct entities. Preserve the
real WOL file as a near miss. Use a synthetic sibling with the same handler
and assembly but an identity/unquoted callback as the positive, plus fixed
argument, helper-shadowing, wrong-import, nonhandler and executable-guard
controls. Check entity identities and multiplicity before treating projected
rows as unique. Then evaluate whether reviewed `map`/`join` flow and local
quote-helper semantics can support a bounded query without false passes.

The open owners are [ucode #54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54)
for the broader M4 query family and [ucode #50](https://github.com/lucas-albers-lz4/codeql-ucode/issues/50)
for flow prerequisites. Earlier Security-40 claims 042, 044 and 045 used a
different producer revision and do not decide the current model. The lldpd
named-helper alternative already has experimental claim 083; its real
callers pass fixed literals. Do not promote a WOL alert until fresh
extraction, AST/model controls, exact SARIF and source review agree.

## Current model boundary after claim 088

A read-only review of merged producer `b43592a8748557dae9f862644e1ddd3c5c60d5ce`
found no `ql/src` delta from claim 088's producer. The testing query binds
the `parts` use and `shellquote` declaration by spelling, not resolved local
identity. `m3/Models.qll` has containment and same-function named-binding
taint but explicitly lacks CFG/SSA; `m4/DirectRpcShellWord.ql` covers raw
template substitutions, while WOL's sink argument is a binary expression.
`DataFlowPrivate.qll` lacks `map`, `join` and concatenation steps, and
`FlowSummaryImpl.qll` supplies no production callback summaries. These
observations do not make the WOL assembly a supported alert.

Implement the next slice as a testing-only query first. Resolve the returned
handler and stable `request` formal, bind `parts` declaration and use through
local identity, and distinguish builtins from same-named local functions.
Model the bounded element/callback/result relation through `map`, elements
to string through `join`, both concatenation operands to result, and the
result to argument 0 of source-declared imported `fs.popen`. Review the
single-quote helper body and exact binding independently; an unproved helper
leaves the result unknown. Evaluate the fixed-executable comparison as a
separate guard rather than treating it as a flow or quote barrier.

Keep the existing identity-callback positive and fixed-array, wrong-callback
and no-join near misses. Add callback and `parts` shadow/reassignment,
wrong-import/local-`popen` shadow, nonreturned handler, altered or partially
quoting helper, mixed quoted/unquoted element, and executable-guard changes.
For every control, compare exact extraction identities, errors, AST entities,
row multiplicity and fresh SARIF before considering promotion.
