# Upstream change review

This record follows the upstream changes that landed during the preceding
program. It does not alter the scope of older pinned claims. Fetch and inspect
current project and issue state before launching each run; selected revisions
below are not promises about later `main`.

## V2 archive assessment

Consumer `fe5952073eeef913fef4b3324d9541ff66426492` includes the reviewed
mounts expectation and a later documented strict-v1 handoff. The pinned
consumer's exact-head Ubuntu M2 workflow completed successfully, providing
separate upstream Linux baseline evidence; it did not execute our receipt
substitution cases. Consumer issue #138 is closed. The later UCI boundary and
handoff evidence changes since `ad241b` do not alter the v2 adapter, selected
policy, corpus or historical archive.

[Claim 030](../../claims/030-v2-archive-receipt-boundary.md) tests the actual
claim 029 receipts against the public v2 archive CLI on Darwin. The archival
bundle and byte-identical typed substitution were accepted with an unknown
modeled gate and unassessed policy; each raw extraction/routing receipt
substitution was rejected by the selected byte-identity gate. The new run is
not a fresh producer-to-v2 handoff. It does not establish our five-case Linux
outcome, real device behavior, authorization or authenticated provenance.
Existing upstream tests cover individual altered inputs and synthetic coherent
path changes; this check uses actual claim 029 receipts at the public boundary.

## UCI helper source observation

The producer's newer helper observer associates a pinned controller call with
its same-file helper and checks forwarding arguments' lexical formal identity.
It does not establish the formals' values at the call or resolve the runtime
callee. A source-first regression tests a reassigned formal and a copied local
alias. Earlier exploratory output used an old checkout with the
new query copied in and did not prove owned caches, so it is not used as the
final result. The consumer's [UCI boundary](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/fe5952073eeef913fef4b3324d9541ff66426492/docs/uci-helper-consumer-boundary.md)
keeps the config identity dynamic and does not infer a catalog join.

[Claim 031](../../claims/031-uci-helper-lexical-identity.md) records the later
fresh, isolated source/query run. The observer matched the real controller
and a reassigned-formal control, while a copied alias was excluded; a separate
diagnostic and entity counts verified the selected identities. The initial
alias span prediction was one column too long and is preserved as a mismatch.
The result does not establish that the caller's value survives reassignment.

## Trim-open policy

[Claim 027](../../claims/027-markup-trim-open-cfg.md) established that the
pinned graph excludes a valid trim-open tag. The grammar permits trim and
ordinary delimiters on the same expression-tag node, but the graph's token
checks accept ordinary delimiters only. The inspected contract, issue #57 and
related merged PRs do not state whether trim-open exclusion is intended. A
On 2026-11-23 the user chose to support the same bounded graph ordering for
ordinary, trim-open, trim-close and dual-trim identifier tags. This is a new
user-selected policy, not a claim that prior upstream intent was documented.
The [decision note](trim-policy-disposition.md) records the options and the
[matrix oracle](trim-matrix-oracle.md) fixes expected source and graph identities
for either choice. [Claim 034](../../claims/034-markup-trim-delimiters.md)
records the tested local implementation and its portable producer patch; it has
not been merged upstream.
[Claim 032](../../claims/032-markup-trim-matrix-implementation.md)
subsequently measured the current implementation against six fixtures: only
the ordinary identifier tag had graph nodes and edges. The observation does
not show rendering or runtime behavior and predates the user's choice.

## Later callable-graph delta

Producer `11a53fd8e911573860950ee8e549b337a8742438` added bounded call
ordering inside callable scopes. [Claim 033](../../claims/033-bounded-markup-callable-call-order.md)
refreshes the exact claim 028 sibling fixtures and adds a computed-callee
control: the former direct-call near miss is covered at the new pin, while the
computed call remains unsupported. The result is syntactic ordering only; it
does not decide the independent trim-delimiter policy question.
