# Dynamic Ucode discovery for incoming OpenWrt and LuCI revisions

Status: bounded implementation design, 2026-11-24. This extends the identity
preflight and drift report in PR #156; it is not evidence that full-tree
discovery, extraction, or scanning currently runs. Counts below come from the
existing pinned source inventories and v0.4 records; this note did not
independently recompute their full manifests.

## Inputs and observed denominator

Use isolated read-only source checkouts for each event SHA, not active working
trees. The inspected stage6 pins are LuCI
`b2e0be4b46ec0fd43394c081fa7c50657af14011`, OpenWrt
`4e9642517b48bae612ff10fb72fb9199e559500e`, and packages feed
`07e0d16305d2b5903b37ad7913e33e18795f81a4`. Record full SHA, tree SHA, dirty
state, event/PR identity and manifest digest for every run.

The current v0.4 baseline is 111 source identities (76 plain, 35
markup-inconclusive in its local run), with 13 exclusions. It includes 17
wifi-scripts files only under `CONFIG_WIFI_SCRIPTS_UCODE=y`. Existing broader
source-only inventory notes report 46 OpenWrt core candidates (11 already in
v0.1, 35 additional) and 37 packages-feed candidates (12 in v0.4, 25
remaining: 22 product candidates and three test mocks). The LuCI source census
reports 69 paths and 24 remaining install-shaped candidates. These are
candidate counts, not installed-file or complete-source denominators.

## Selector contract

At each event SHA, enumerate tracked files from the full trees and construct a
candidate union from these source signals:

1. `.uc`, `.ucode`, and `.ut` suffixes, independent of directory.
2. A first-line Ucode shebang, independent of suffix.
3. Extensionless files beneath known installed Ucode roots:
   `usr/share/ucode/`, `usr/share/rpcd/ucode/`, and `usr/lib/ucode/`.
4. Additional files explicitly named by package recipes, build conditionals,
   or the versioned reviewed policy, including unconventional source paths
   whose installed destination is a Ucode location.

The first three rules reproduce the existing broad source-candidate policy;
the fourth closes known recipe-driven cases and must be maintained as
reviewable policy. For each candidate, collect matching recipe evidence:
package/subpackage owner, source-to-installed path mapping, copy or rewrite
operation, config and dependency conditions, and whether the recipe is
conditional. Do not assume that a source candidate is selected for every
build configuration. Preserve each mapping as a multiset so two source
identities mapping to the same installed path remain distinguishable.

Emit an event manifest with one row per source identity and explicit status:

- `selected`: reviewed source with an applicable install mapping and frozen
  package/config policy for this run;
- `excluded`: reviewed source with a specific reason (test mock, non-product
  data, or unselected optional subpackage);
- `unreviewed`: candidate or recipe signal without an approved disposition;
- `policy-drift`: a previously selected/excluded identity changed owner,
  condition, mapping, or source-class membership.

Only reviewed selected rows proceed to extraction. Any unreviewed candidate,
policy drift, new/removed/renamed identity, missing source, or ambiguous
mapping stops the scan before CodeQL and produces a review artifact. Ordinary
content edits to a selected identity are expected incoming changes: update its
event SHA and hash, retain its stable source identity, and scan it. Content
changes to an excluded identity trigger review but do not become selected by
default.

## Install evidence and exclusions

The existing package mapping gives concrete recipe signals beyond path
heuristics: node-exporter base recipe copies 12 files, while eight `files/extra`
collectors belong to optional packages; adblock-fast rewrites `adblock-fast.uc`
version data; librespeed rewrites its extensionless shebang executable;
uvol, snort3, mwan3 and uneighbord have explicit copies. The package inventory
identifies three adblock-fast test mocks with no product install mapping.
Source hashes therefore identify source inputs, not necessarily installed
bytes. Keep rewrite operations and config-dependent package selection in the
manifest, and do not claim installed-byte identity until package outputs are
compared.

The selector should retain a reviewed exclusion registry rather than infer
exclusion from the absence of an install rule. Examples already documented:
the three test mocks; eight optional exporter collectors unless their
subpackages are in the declared matrix; and non-source files such as
`ucode.nanorc`. Unknown signals stay unreviewed.

## Event flow and checks

1. Resolve an incoming PR to an immutable repository/head SHA and verify it
   against the upstream API and fetched PR ref (the existing #156 resolver
   covers identity preflight). Resolve exact base SHA/tree too.
2. Enumerate tracked candidates at base and head independently. Compare
   identity sets and policy projections; do not rely on diff-only paths.
3. Generate the head manifest and stop on unresolved candidates or policy
   drift. Record candidate additions, deletions, renames and source-class
   transitions with reasons.
4. For a reviewed manifest, stage exactly selected source identities at their
   installed-path projections, then compare hashes, routes, extraction
   diagnostics and successful file identities with multiplicity. The current
   111-path v0.4 manifest remains a compatibility baseline, not the dynamic
   selector.
5. Only after those checks, run the pinned released scanner and same-job
   consumer. Keep selector failure, extraction failure, scan failure, new
   alert, disappeared baseline alert and clean result as distinct statuses.
6. Retain base/head manifests, source hashes/Git blobs, recipe evidence,
   conditions, tool versions, route/extraction receipts, SARIF identity and
   elapsed time. Keep generated databases and raw outputs under run-owned
   ignored `work/` paths.

## Minimum selector validation

Before enabling a poller, test a frozen source oracle against pinned base/head
pairs containing: a changed known selected file; a newly added `.uc` file;
an extensionless file under each known root; a new shebang file with an
ordinary suffix; a rename; a deleted candidate; a recipe-only install mapping
change; a config/subpackage condition change; a rewritten installed-byte
recipe; a test mock; and an unrelated non-Ucode edit. Assert exact identity
multisets and status/reason for every row. Add a deliberate unclassified
candidate and assert fail-closed behavior. The oracle must be prepared before
observing selector output. Then run a real producer-to-consumer event drill
with a known alert and clean control; a local selector test alone is not Gate
8 evidence.

## Gaps

Counts and source classes here rely on existing inventories rather than a
fresh independent recount. The candidate union is intentionally conservative
but cannot establish completeness for arbitrary generated files, build-time
code generation, or source layouts outside the known roots and recipe scan.
Package configuration matrices are not yet frozen for all candidates;
actual installed bytes are unverified for rewritten sources. Full dynamic
selection, fresh extraction on an incoming event, hosted Linux cost, periodic
polling/backlog policy, and Gate 8 remain open. This design makes no claim
about analyzer completeness or security outcomes.
