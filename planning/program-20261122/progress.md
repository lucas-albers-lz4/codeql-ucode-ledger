# Evidence program progress

This log records work against the [24-package program](../next-program-20261122.md).
A completed decision gate is not an executed claim. Re-fetch and check current
ownership before each new run; the pins below are observations for this batch.

## Package 1: refresh and impact map

On 2026-11-22, fresh disposable clones under ignored `work/` were clean at
producer `6010ff2c0f101f7629c6fe117a421f671c311a2b` and consumer
`48c6a65b7578234644c6b06780fc82ccf6d61a8b`. Compared to the prior decision
baseline `0a6612fe0e66351a0ccda43ad5b51f5ef5a2724e` / `5f8bd2658483c0c06c0ebfced98fd09b1f57aeff`,
the producer added ten commits covering bounded markup CFG, a separate
creation graph, and a source-level direct-copy receiver experiment; the
consumer added two commits for the opt-in read-only v2 pilot and its public
boundary tests. No prior claim becomes evidence for new CFG semantics merely
because its AST still exists. The consumer's corpus lock was unchanged, with
SHA-256 `b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`;
it pins LuCI `b2e0be4b46ec0fd43394c081fa7c50657af14011` and grammar
`4a243af329fae2f4ff01e0fc80133cbab8314600`. The local CodeQL executable is
2.27.4; resources at preflight were 137 GiB free and 16 GiB memory. These are
not forecasts for future runs.

Producer #57 remains open with its broader CFG/dataflow work deferred; the
new modules provide specifically documented bounded graph APIs, not general
markup flow. Producer #48 remains open and blocks production member-callee
work; #58 remains deferred. Consumer #138 remains open for the read-only v2
pilot. At the selected consumer pin, v2 uses archived neutral input and a
source model; its real Linux libc gate is unknown on Darwin. Issue state,
source contracts and the concrete query delta must be checked again when
launching dependent work. The fresh clone review did not run tests.

## Packages 2–4: ordinary markup graph

The new ordinary graph supports a documented closed subset; upstream tests
already compare full node and edge sets for several normal inputs and
unsupported shapes. A distinct question is whether a valid simple identifier
tag with a whitespace-trimming open delimiter receives the same graph as the
ordinary delimiter. The pinned grammar accepts both, while the implementation
requires the ordinary opener class. A pre-query source oracle was independently
checked before the run; a reviewed copy will be retained with any claim.
Whether the distinction is intended policy is unresolved. [Claim 027](../../claims/027-markup-trim-open-cfg.md)
records the actual routing, diagnostics, AST, full projected graph and
per-identity count results, along with the failed setup attempts and the
inherited HOME limitation.

## Packages 5–6: creation graph sibling scopes

The creation module has its own graph contract. A separately reviewed oracle
compared a root with two supported callable bodies against the same sibling
shape with one unsupported call body. [Claim 028](../../claims/028-creation-sibling-scopes.md)
records exact roots, callable scopes, selected AST identities, node counts,
and edge pairs. The supported sibling remained covered in the mixed case;
the unsupported sibling retained its scope but had no callable graph nodes.
This is a bounded fixture observation, not runtime callable behavior or
general control-flow support. Failed query and setup attempts are retained.

## Package 7 preparation: real-source eligibility

An independently reviewed [source inventory](markup-cfg-inventory.md) identifies
one unsupported construct in each of the 12 selected pinned LuCI markup
files. It therefore provides no whole-root positive for the ordinary graph in
that exact profile slice. This is a source-based eligibility decision, not a
query result, a conclusion about unselected sources or a routing observation.
Package 8 should stop unless a separate in-scope positive and a distinct
real-source analysis decision emerge. The source review was preparatory work,
not a graph execution; the preceding graph results are recorded above.

## Packages 9–12: receiver-copy relevance

The new direct-copy experiment is a bounded may-reach source relation, not a
production member-callee model. A [source triage](receiver-copy-triage.md)
examines the selected 21 LuCI sources and named queries: it found direct
handle uses and a reassignment, but no copied-handle case that changes one of
those queries. That is not proof such a case does not exist elsewhere. The
package 10 decision gate is therefore not met for this selected scope; the
dependent control design and CodeQL run in packages 11–12 remain deferred.
Producer #48's production hold remains in force.

Later, producer `11a53fd8e911573860950ee8e549b337a8742438` retained a
[repository-wide LuCI lexical census](https://github.com/lucas-albers-lz4/codeql-ucode/blob/11a53fd8e911573860950ee8e549b337a8742438/docs/evidence/receiver-luci-census/README.md)
and a separate bounded receiver experiment. The census found no direct
`popen`-initializer-to-copy candidate among its enumerated text patterns;
it is not a parser, a complete syntax search or an installed-profile scan.
The experiment's five incremental direct-copy rows were synthetic, while
the selected real-file rows did not change. This broader but still limited
evidence reinforces the existing stop; #48 remains open. Revisit with an
actual affected real case and a named analysis decision.

## Packages 13–15: synthetic v2 provider scope

The current consumer's documented pilot and test contract distinguish
synthetic status inputs from the archived setBlockDetect observation. A
source-derived four-case oracle selected a provider feed change with matching
new permission and resource inputs and an independently scoped old policy.
[Claim 026](../../claims/026-v2-feed-policy-scope.md) records the actual API
and CLI results and independent comparison. A valid B provider with stale A
policy was unassessed without an assertion and rejected an asserted A
reference. The error occurs before gate computation; the otherwise identical
unasserted case shows the selected gate can pass. This is synthetic evidence,
not a fresh producer-to-consumer handoff or real policy determination.
Adapter subprocesses in the retained run used a write-denying sandbox; the
setup inherited `HOME`, a documented limitation rather than run-owned HOME.

## Packages 16–19: remaining v2 and handoff gates

The pinned consumer's `test_v2_resolver.py` already specifies duplicate IDs
before applicability, selected-authority conflicts and reference precedence;
`test_v2_adapter.py` also specifies a multi-target operation control. No
distinct additional failure-family decision was selected here, so these
source observations are not labeled a fresh test result.

The real setBlock input chain is an archived neutral observation plus pinned
source, routing, diagnostic, profile and policy inputs. The pilot explicitly
does not accept a real assessed reference until scope and authority receive
separate review. Its Linux libc modeled gate remains unknown on Darwin. No
distinct real-input decision sufficient for a new run was selected; this does
not establish a fresh producer execution, installed package or live access.

There is a relevant v1 strict-consumer implementation delta: at consumer
`48c6a65b7578234644c6b06780fc82ccf6d61a8b`, `validate_typed` delegates its
record checks to `validate_typed_records`, including an explicitly supplied
corpus revision. This merits a narrowly scoped regression handoff if the
actual producer and consumer can be run with isolated paths and the controls
required by package 20. It is a v1 compatibility question, not a new v2 live
handoff. [Claim 029](../../claims/029-typed-refactor-handoff.md) records the
fresh producer-to-v1-consumer execution and independently reviewed controls.
The output is not a v2 handoff or proof of runtime authorization.

## Packages 21–23: JavaScript UCI planning and hold

Two source parsers inspected all 88 manifest files. Their initial candidate
sets differed at three nonoptional `uci.get` accesses inside expressions
with a later optional operation. The [parser differential](../js-uci/parser-differential.md)
records that discrepancy; a [corrected pass](../js-uci/corrected-acorn-pass.md)
matched 576 candidate tuples across the two parsers under the per-access
interpretation and exercised synthetic optional and computed-index controls.
The [source candidate multiset](../js-uci/source-candidate-multiset.json)
retains all 576 tuples and the 88 path/hash identities for review.
The proposal now states that interpretation. Parser agreement is useful
source-planning evidence, but CodeQL entity classes, spans and multiplicity
are not verified and the complete independent query oracle remains open.
The existing execution hold has not been lifted; package 23 was not run.

## Package 24: reconciliation

This program produced four bounded claims: [026](../../claims/026-v2-feed-policy-scope.md)
for a synthetic v2 boundary, [027](../../claims/027-markup-trim-open-cfg.md)
for two ordinary CFG fixtures, [028](../../claims/028-creation-sibling-scopes.md)
for callable-scope isolation, and [029](../../claims/029-typed-refactor-handoff.md)
for an actual fresh typed v1 handoff. The scope and limits of each are in its
own claim and evidence; none is a coverage percentage. Packages 7–8 and 9–12
stopped at their named source/decision gates, and 16–18 have the explicitly
recorded existing-test and real-authority limits. The JS execution hold keeps
package 23 unrun. Source parser agreement does not establish a CodeQL oracle.

At the last refresh during this program, producer main was
`d3981986ac685d6fcbb78a3b369aa4ed526c1e4b` and consumer main was
`ad241b90638d269b36aa06dd1ed48032a9a03fb7`. The former adds an issue #53
helper observation and controls since `6010ff2`; the latter changes the v2
adapter, tests and documentation since `48c6a65`. These observations identify
possible future decisions, not results for those newer revisions. Before
another batch, inspect exact current deltas and existing owner evidence; do not
automatically repeat the new upstream tests. The already established gates
remain: claim 005 needs an actual supported fresh query-to-record and retention
path; the direct-exec grant join needs a supported interface and independent
policy oracle; real v2 assessment needs reviewed scope and authority; and
template arguments or direct cursor-write modeling need their own distinct
analysis decision and evidence.
