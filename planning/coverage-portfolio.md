# Coverage claim portfolio

Inventory date: 2026-11-18 UTC. This is a prioritized working map, not a
coverage denominator or a new test result. See [the later pinned-source batch](batch-20261118.md) for newer revisions and claims 015–016. It draws on isolated snapshots of
[ucode `d3588ca`](https://github.com/lucas-albers-lz4/codeql-ucode/tree/d3588ca6821fe983d240fcbb2e80692fabcc6aab)
and [OpenWrt `a8bdef3`](https://github.com/lucas-albers-lz4/codeql-openwrt/tree/a8bdef3c22c8d5ba9999baa978052b59bd22907e),
and the open issue titles/bodies inspected on that date. These were the remote
`main` heads when checked; assess deltas and issue changes for any later run.
The projects remain the owners of their contracts, implementation and issues.
Claim 012 additionally records a fresh declaration-query-to-consumer comparison
at producer `094a163` / consumer `faf95a4`; it is scoped to that run and does
not exercise the separate retained direct-exec grant-join path.

## Selection heuristic

Start with a named analysis or decision and trace its prerequisites. Prefer a
claim when (1) its outcome would clarify a consequential uncertainty,
(2) an exact expected identity and a valid discriminating control can be
established independently, and (3) existing evidence can be reused or a run
is proportionate. Priorities below are judgment calls, not numerical coverage
scores. Do not promote historical tests or fixture tables to fresh paired runs.
When a question is already owned, link the issue and document the boundary
instead of creating a duplicate finding. Revise the list when project changes
make an assumption or priority stale.

## Representative paths

| Path and why it matters | Evidence chain and present ledger state | Next useful question / existing ownership |
|---|---|---|
| **getBlockDevices**: first small producer–consumer trace, direct imported `popen` source shape. | [001](../claims/001-staged-root-extraction.md) demonstrates one selection/extraction run; [002](../claims/002-getblock-query.md) and [003](../claims/003-getblock-handoff.md) now have bounded fresh query and handoff runs. The table records syntactic containment and an `fs` import, not lexical binding or registration. | Refresh against a newly selected revision pair when needed. [ucode #54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54), [ucode #55](https://github.com/lucas-albers-lz4/codeql-ucode/issues/55), and [OpenWrt #65](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/65). |
| **setBlockDetect**: similar handoff but tests a different language dependency, builtin `system` versus visible shadowing. | [004](../claims/004-system-shadowing.md) demonstrates a narrowly scoped language/model check through the real table query. A separate typed exporter, adapter and offline handoff checker exist. | Fresh [CSV](../claims/007-setblock-csv-handoff.md) and [typed](../claims/008-setblock-typed-handoff.md) handoffs have bounded runs; claim 008 was refreshed at the 2026-11-21 pair with shadowing controls; the existing [handoff checker](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/a8bdef3c22c8d5ba9999baa978052b59bd22907e/docs/setblock-handoff-checks.md) checks consistency but does not prove execution or freshness. |
| **setInitAction**: important boundary for request arguments reaching an imported helper. | [005](../claims/005-imported-callee-boundary.md) demonstrates the bounded source-to-call observation and remains partial for fresh retained interpretation. The documented same-file experimental jump does not resolve this imported target. | The existing imported-callee smoke checks a message substring, not exact source/sink identities or a complete negative; design controls before treating it as sufficient. [ucode #50](https://github.com/lucas-albers-lz4/codeql-ucode/issues/50) and [#54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54) own broader work. |
| **setLocaltime**: a richer six-row source construction and consumer with an independent oracle. | [006](../claims/006-setlocaltime-construction.md) records a bounded fresh paired observation and consumer rejection control. The existing consumer documentation records a paired run with an owner-accepted deviation and independent review marked `INCOMPLETE`; it does not provide the output report. | Historical raw artifacts were not found in the inspected snapshots or workspace; the fresh run is separately recorded. Do not silently promote the historical run or imply that six rows are six calls. [ucode #54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54), [OpenWrt #64](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/64). |


Additional bounded inventory paths: [009](../claims/009-luci-sys-status.md)
checks the two named `luci.sys` status-helper and wrapper shapes; [010](../claims/010-ubus-call-inventory.md)
checks direct `ubus.call` syntax. [011](../claims/011-same-file-jump-local.md)
checks an experimental same-file flow shape; [012](../claims/012-backend-declaration-comparison.md)
compares backend declarations with a pinned grant catalog, and [013](../claims/013-getfeatures-direct-calls.md)
inventories direct `getFeatures` calls. [014](../claims/014-fs-binding-guard.md)
checks selected conservative `fs` binding controls. [017](../claims/017-rpcd-login-negation-whitespace.md)
checks the consumer login-permission oracle against the pinned rpcd C function
for a bounded whitespace matrix; it is not live authorization evidence.
[018](../claims/018-pinned-luci-shellquote-candidates.md) records seven current
shell-injection candidate rows for one pinned LuCI source file, and
[019](../claims/019-pinned-luci-shellquote-slice.md) runs the same query over
eight selected plain `luci-base` sources plus controls. Neither is a consumer
handoff or vulnerability finding. These bounded examples do not establish
runtime binding or a cross-file taint path. They are selected for named
decisions and controls, not an inventory of all candidate analyses.

[020](../claims/020-pinned-markup-call-syntax.md) observes a direct call in the
pinned `uhttpd.uc` markup AST and distinguishes member and plain-tree controls.
Its routing status remains inconclusive; it does not establish dispatcher
behavior, target resolution, CFG or data flow. [021](../claims/021-pinned-luci-template-extraction.md)
records the selection and diagnostics for 11 pinned upstream `.ut` sources
staged at expected paths plus controls; its markup routes remain inconclusive.
[022](../claims/022-pinned-mixed-template-ast.md) observes selected mixed-text
AST nodes and a literal-lookalike control on one pinned template.
[023](../claims/023-uci-syntax-controls.md) checks selected UCI controller call
and argument syntax without resolving helper binding or forwarding.
[024](../claims/024-markup-declaration-ast.md) observes declaration and
initializer AST rows and a valid no-initializer control; it does not establish
the proposed markup CFG.
[025](../claims/025-mixed-profile.md) checks routing, diagnostics and root
multiplicity for 21 pinned LuCI files and three controls in one database;
markup routing remains inconclusive.
[026](../claims/026-v2-feed-policy-scope.md) checks an independently scoped
synthetic v2 provider-feed change at the consumer API and CLI. It is not a
fresh producer handoff or a real authorization assessment.
[027](../claims/027-markup-trim-open-cfg.md) checks a bounded ordinary-tag CFG
and the observed trim-open exclusion on two fixtures. It does not determine
whether that exclusion is intended policy or establish runtime behavior.
[028](../claims/028-creation-sibling-scopes.md) checks creation graph scope
isolation for two synthetic sibling-callable fixtures. It does not establish
runtime calls or general callable-body support.
[029](../claims/029-typed-refactor-handoff.md) refreshes the actual typed v1
handoff after the consumer validation refactor, with rejection controls. It is
not a v2 handoff or evidence of real authorization.
[030](../claims/030-v2-archive-receipt-boundary.md) checks the v2 archive
adapter against the actual claim 029 receipts. It records an archive-identity
boundary on Darwin, not a fresh producer-to-v2 handoff or runtime authorization.
[031](../claims/031-uci-helper-lexical-identity.md) checks the newer UCI helper
observer against reassigned-formal and copied-alias controls. It establishes
selected lexical identities, not value preservation or runtime UCI effects.
[032](../claims/032-markup-trim-matrix-implementation.md) measures the current
bounded graph for ordinary and trim delimiters with member-expression controls.
It does not decide the intended trim-support policy.
[033](../claims/033-bounded-markup-callable-call-order.md) refreshes claim 028
after bounded direct-call ordering was added: a direct-call sibling is covered
and a computed-callee sibling remains unsupported on the selected fixtures.
[034](../claims/034-markup-trim-delimiters.md) tests the user-selected trim
policy in a disposable producer checkout. The reviewed patch is local and has
not been merged upstream; rendering and runtime semantics remain outside it.

[075](../claims/075-historical-openvpn-baseline.md) measures the current
testing-tagged shell candidate query against the upstream OpenVPN vulnerable
parent and actual fix, with exact extraction, target AST witnesses and
positive/near-miss controls. It records a bounded model gap, not detection of
the historical issue or default-suite SARIF.
[076](../claims/076-historical-tailscale-baseline.md) repeats that bounded
baseline decision on the post-merge producer for the upstream Tailscale
parent/fix, a direct model-positive control and three nested-shell controls.
The real source/sink AST sites exist but the current candidate query emits no
nested-path row; it does not recognize the fix or produce a scanning alert.
[077](../claims/077-current-luci-openwrt-extraction.md) establishes exact
source-staged extraction identities for a current LuCI `luci-base` and OpenWrt
`utils/cli` slice: 21 selected files extracted once, zero errors, 20 plain
routes and one markup-inconclusive route. It does not establish installed
package bytes, full-repository selection or semantic security coverage.
[078](../claims/078-openvpn-experimental-historical-rule.md) and
[079](../claims/079-tailscale-experimental-historical-rule.md) record fresh
explicit-query historical source/fix distinctions with exact extraction,
controls and SARIF locations on separate experimental producer branches.
Both remain testing-tagged outside the default suite. They demonstrate
bounded syntax matching, not generic shell-injection detection or a fresh
downstream consumer handoff.
[080](../claims/080-final-direct-rpc-rule.md) records a separate, less
source-specific direct returned-handler interpolation query at its final
testing-tagged producer commit. The source-first OpenVPN parent/fix and pinned
LuCI swconfig plus 21 controls had exact extraction and explicit-query/SARIF
identities. A copied 21-file current-source query finished with zero rows;
that empty result is not negative security proof or a fresh extraction.
[081](../claims/081-current-luci-rpcd-direct-shell-slice.md) widens the
source-staged LuCI rpcd inventory to 17 tracked plugin files across package
owners. All selected files extracted once with zero errors and raw-mode
routing; the local draft default suite emitted zero alerts. It does not
establish installed bytes, a current rule positive or downstream acceptance.
[082](../claims/082-local-direct-rpc-sarif-handoff.md) records a fresh local
macOS draft-suite handoff to the actual disposable consumer parser: one
OpenVPN parent SARIF warning and empty fix/swconfig cases were accepted after
exact source staging, extraction and suite checks. It is not a versioned
Linux release, installed-image mapping or incoming-change CI result.
[083](../claims/083-named-helper-shell-word-experiment.md) records a separate
testing-tagged named-helper argument-to-formal shell-word query. A fresh local
21-file matrix extracted each staged file once, had zero errors and emitted
only two planned synthetic positives; pinned LuCI `luci.lldpd` and the
fixed-literal/scope controls had no rows. This is bounded syntax evidence,
not a current-source alert, default-suite promotion or runtime finding.
[084](../claims/084-current-luci-package-ucode-slice.md) adds four pinned
LuCI files from package `ucode/` trees that are disjoint from the earlier
21-file and rpcd-17 source sets. Their proposed install paths, `.uc` extension
routes, exact successful extraction identities and zero errors were verified
in a fresh run. Both the draft default suite and a separate testing query
returned zero rows; without an eligible positive/near-miss pair, these are
only bounded observations and do not establish security coverage.
[085](../claims/085-pinned-luci-ucode-source-census.md) provides a pinned
69-path Git-source candidate census with independently checked blob and byte
identities. After exact overlap with earlier slices and claim 021 templates,
24 install-shaped source candidates remain for a next routing/extraction batch:
22 `.ut` markup templates and two Ucode-shebang scripts. The projected routes
have not been run as one census, and installed bytes remain unknown.
[086](../claims/086-current-luci-markup-shebang-route-slice.md) runs that
disjoint 24-file source batch. Exact routing selected 22 markup-inconclusive
templates and two plain shebang scripts; all 24 appeared once in successful
extraction with zero errors. The successful-file diagnostic does not override
`markup_not_modeled`, and the zero-result default suite is not a security
negative. The initial local CSV validator failed on a filename typo and its
corrected check is recorded separately.


Some earlier paths overlap in the pinned LuCI fixture; these slices are not a representative
sample of all OpenWrt software or ucode syntax. The inventory deliberately
separates source extraction, model/query behavior, consumer handling and policy
interpretation. A successful earlier step is a prerequisite, not proof of a
later step. Markup AST extraction issue [ucode #56](https://github.com/lucas-albers-lz4/codeql-ucode/issues/56) closed before the 2026-11-21 refresh; that closure does not establish template semantic coverage. Remaining markup and dispatcher questions include
[ucode #57](https://github.com/lucas-albers-lz4/codeql-ucode/issues/57) and
[#58](https://github.com/lucas-albers-lz4/codeql-ucode/issues/58)
and [OpenWrt #68](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/68)
and [#70](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/70); do
not infer coverage from their presence in this list.

## Working order and refresh

[087](../claims/087-current-luci-quoted-switch-ast.md) and
[088](../claims/088-current-luci-wol-assembly-ast.md) retain current LuCI AST
prerequisite observations without claiming command-flow or sanitizer behavior.
[089](../claims/089-newer-openwrt-wifi-parse-boundary.md) records a newer
OpenWrt source-revision boundary: the v0.6 selected set routed exactly, but
two changed wifi files failed parsing, so the aggregate run stopped before
suite SARIF. This is an extractor coverage gap, not a security-negative result.
[090](../claims/090-wifi-grammar-prototype-extraction.md) tests a disposable
grammar override on those two sources and two controls: fresh CodeQL
extraction and focused AST rows pass. A later separate local 128-path corpus
run passed under the refined pack, and producer PR #161 merged grammar
support. A released Linux corpus run, installed-byte scan and consumer
handoff remain open.


1. Claim 005 has no identified existing fresh query-to-record path at the pinned
   pair. Keep the source-to-call evidence partial and revisit an interface only
   if it serves a concrete analysis need; do not relabel the historical snapshot.
2. Keep the completed setBlockDetect CSV and typed handoffs scoped to their
   recorded runs; revisit them when their contracts or selected revisions change.
3. On refresh, record the new SHAs, inspect changes to selected queries,
   models, fixtures, adapters and issue disposition, and rerun affected claims.
   Prior evidence remains scoped to its original pins.
