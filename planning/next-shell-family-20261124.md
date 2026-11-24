# Next shell-rule family for incoming-source value

Status: reviewed design direction, not an implemented or validated check.
The experimental OpenVPN and Tailscale rules discriminate their respective
historical source/fix pairs, but constrain file/RPC/field or complete command
shape too narrowly to establish detection of new incoming OpenWrt/LuCI shell
issues. Retain them as regression gates while measuring a separate family.

The smallest proposed generalization is **direct RPC argument interpolation
into imported `fs.popen`**. Bind the actual `methods.<name>.call` formal
regardless of its spelling or selected `args` field. Accept a direct template
substitution in the `popen` argument or one uniquely bound local assignment
that reaches a direct `popen` call in the same callable. Require a separate
source-derived determination that the substitution lands in a raw shell word;
do not infer safety or danger from a helper's name alone. Resolve the `fs`
import/local binding, the request formal, local writes and nested callables.
An unresolved binding or quote context must remain unknown, not silently
treated as a safe negative.

Source-backed positive: historical OpenVPN `req.args?.cl_meta` at line 71 to
`popen(cmd)` at line 77. Eligible real-source near misses: its fixed commit
keeps the sink and wraps the field in `shellquote`; the pinned LuCI `luci`
rpcd module's getSwconfigFeatures and getSwconfigPortState paths pass
`request.args.switch` through `shellquote` before `popen` (claims 018–019).
The latter cases still need fresh extraction and exact AST witnesses at the
selected current producer before becoming current-rule controls. Derived
constant-sink, reassigned-formal, shadowed-local and nested-callable controls
remain useful discriminators, while remaining synthetic.

Do not promote the broad testing `ShellInjection.ql` as a security check based
on same-file candidate rows. Tailscale's collection flow and outer double
quoted `sh -c` context need a separate family after array propagation and
two-stage quote modeling are supported. In the selected current slice, review
every candidate and measure performance. A fresh changed-revision CI scan and
default-suite SARIF handoff remain required before claiming that incoming
issues are detected as they happen.

## First local candidate and review

A testing-tagged implementation on isolated producer branch
`security/direct-rpc-shell-word` at `9da947a7cc6a35e7a6e44eaf82b6817f29bb3c31`
uses lexical formal/local identity and imported `fs.popen`, with an explicit
literal shell-word boundary. Its final query SHA-256 is
`7995398bfb8c9bb7002a9ccde4fe5b0015b6d464aefe64b699b5cfa5460b1b80`.
The fresh local matrix at ignored `work/direct-rpc-shell-run-20261124-e/`
extracted OpenVPN parent, fix, pinned LuCI `swconfig`, and 11 controls exactly
once each with zero errors. It emitted one parent result at 71:115–132, zero
on the fix and `swconfig`, and three intended synthetic positives. All 44
matrix and four SARIF commands exited zero. This is explicit-query evidence,
not default-suite or downstream CI execution. Its preflight recorded the
uncommitted query/fixture bytes on base `18afe77` before the exact tested
bytes were committed; independent review matched the final query/oracle
hashes to commit `9da947a7`.

Independent security review identified three missing discriminators before
default-suite consideration: an unregistered RPC-shaped object (the current
model recognizes a methods/call shape without registration proof), mutually
exclusive assignment and sink branches (line order is not control flow), and
an earlier dynamic substitution that changes shell quote context. The alert
wording must match what the model proves. Same-line local initialization is
currently excluded. The worker is adding those controls and rerunning; this
snapshot is superseded if query bytes change.

The first exploratory query against a copied 21-file current-slice database
was interrupted after 183.36 seconds, exit 130, peak RSS 1,467,498,496
bytes. The copied database's diagnostics matched the exact 21-file selection
and zero errors, but the rule produced no completed result. Its evaluator
spent time expanding generic variable-binding relations across roughly
54,000 AST nodes before the rule-specific joins. This is a performance gate,
not an empty current-corpus alert result. A revised binding strategy must
retain the historical matrix and new security controls, then finish a fresh
bounded current-slice probe before any default-suite consideration.

A narrowed provisional revision at `6d7d7705023e6a9cbb85db678f0cdc169771a881`
completed that copied 21-file query in 11.093 seconds with 471,793,664 bytes
peak RSS and zero rows; an explicit SARIF analyze took 10.06 seconds. Its
fresh historical matrix still had parent/fix 1/0 and current pinned LuCI
`swconfig` zero, with 14 control files extracted once each and zero errors.
The unregistered-object and mutually exclusive-branch controls returned zero.
The multi-substitution control produced two candidates because the earlier
dynamic value can change the runtime quote context; their precise alert
interpretation is under security review. The query also emitted an unused
parameter warning. The worker is removing that warning and will rerun exact
final bytes, so these provisional receipts do not establish a promotion-ready
revision.

The next revision will keep the OpenVPN positive while reducing duplicate
alerts from multiple direct handler-field substitutions in one template. This
is alert deduplication, not quote-state proof: earlier non-field dynamic
values can still change runtime quoting, and suppressing a later field can
hide a more consequential source. A two-field control with a restricted first
field and raw second field, plus a complete field witness, is required before
adopting that choice. The alert should describe a literal-whitespace
substitution requiring full quote-context review.

The final local experimental revision is producer commit
`29d8a6e9b352e0904065ec5572db4d845ff15919`, query SHA-256
`046c57aa2003c5b0a5c1a8eec9afc7ca00fdb727928839bff51a4236f5e93f48`,
with source-first oracle SHA-256
`fcab0ad97ee83389e62ecaafb6491675f6605e4a7987c3d666f8ee8669e712ea`.
Fresh run-i used separate parent/fix/swconfig/control databases and recorded
44 extraction/query commands plus four SARIF commands, all exit zero. It
extracted 24 staged files once each with zero errors. The parent/fix/current
`swconfig` result counts were 1/0/0; 21 controls produced five exact
predeclared results. The first raw field in the multi-substitution control
alerts once and the later field is suppressed; a raw second field after a
quoted first field remains visible. Both source identities remain in AST
witnesses. The OpenVPN SARIF result is at 71:115–132. Query times were
3.101–4.996 seconds, with peak RSS at most 446 MB.

The final query on a copied, previously source-verified 21-file current-slice
database finished in 5.846 seconds, peak RSS 481,148,928 bytes; explicit
SARIF analyze took 4.074 seconds. Both output formats had zero rows. These
are exploratory query measurements, not a fresh extraction or proof that
the selected current code is safe. The branch remains testing-tagged and
outside the default suite. Final independent security review is in progress.
Independent read-only security review then matched the final commit, oracle,
all 48 command exits, exact source and control SARIF locations, and the six
named shadow-control negatives. It found no matrix regression or obvious new
false-positive path in the final guards. Its recommendation is to prepare a
draft default-suite promotion change as a **scoped review candidate**, while
keeping the rule testing-tagged until a fresh Linux suite run, installed-byte
mapping, consumer acceptance and manual triage on a larger eligible slice
are complete. Returned-table shape is not runtime registration; the binding
guards approximate lexical identity; literal whitespace does not establish
full shell quote state. The current-slice zero rows are not precision proof.

## Helper-flow candidate after the direct rule

The pinned LuCI `luci.lldpd` source at
`b2e0be4b46ec0fd43394c081fa7c50657af14011` has a raw template
`fs.popen` in `lldpcli_json(section)` at line 6. Its four visible callers at
lines 13–16 pass fixed literals. A source-first oracle and contrasting
request-derived versus fixed-literal synthetic fixtures are held under ignored
`work/luci-lldpd-helper-oracle/`; the oracle SHA-256 is
`f269580b4cc3e17c37b5e9fe07836041173c3270c15a9982fd6a211f490556f9`.
The pinned source SHA-256 is
`a9d6e6477307408a130ce20ad9f92813dfeca611e5c8a5a7a86f2ca746081eac`.
The two synthetic controls now use the same returned `methods`/`getStatus.call`
shape, with a request-derived argument versus a fixed literal. This is a
future caller-to-formal flow control, not an observed alert or a security
conclusion. It requires imported sink binding, unique helper call resolution,
caller identity, formal-read identity, and fixed-literal discrimination. The
current direct rule cannot cover a sink inside this named helper; a separate
query is needed. The syntax does not prove loader acceptance, RPC registration,
runtime invocation, or full shell quote context. At oracle preparation, no
CodeQL run had been made against these fixtures.

A subsequent testing-tagged implementation is local producer commit
`3111982595ab5cc873d95db09bb0ae71057d63e8`, query SHA-256
`43143b692f848bcb490a9bf3333adeb0073285fd057152c893deaac9f822593e`.
Its fresh 21-file run-d extracted each staged source once with zero errors and
reported only two distinct synthetic dynamic controls at 12:23–43. The real
`luci.lldpd` file and 18 synthetic near misses were empty. Adversarial review
led to loop/catch/write and nested-block scope controls; the final matrix
addresses those specific gaps. See [claim 083](../claims/083-named-helper-shell-word-experiment.md).
The rule remains outside the default suite; unbraced scope shapes, actual
registration and complete quote context are unproven.
