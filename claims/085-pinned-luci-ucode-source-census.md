# Claim 085: pinned LuCI Ucode source census

**Status:** Demonstrated

**Scope:** A Git-object-derived inventory of tracked Ucode and markup candidate paths at one clean LuCI commit, with exact source identities, Git blobs, source-byte SHA-256 values and overlap against earlier selected slices. Route and install-path fields are policy projections only.

**Out of scope:** Actual extraction of the full set, installed package bytes, runtime use, query coverage, alert quality, a coverage percentage for OpenWrt, or a security finding. This is a source candidate superset, not an installed corpus count.

## Revisions and context

- LuCI: clean detached `openwrt-25.12` commit `b2e0be4b46ec0fd43394c081fa7c50657af14011`; the consumer corpus lock in clean checkout `48c6a65b7578234644c6b06780fc82ccf6d61a8b` pins the same LuCI commit, lock SHA-256 `b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`.
- Producer source-path/routing policy inspected at clean `977331713b4b8b5574813bee0884245bf6db2752`, `extractor/src/extractor.rs`; no CodeQL run was made for this census.
- Portable [inventory](../evidence/085-20261124-luci-source-census/inventory.json), SHA-256 `ec86e2f2a7cd1e9ac97f3d54db48d90d62674e2e05abd4fa937ccdae829392e9`, records the selection predicate and all path-level receipts. Independent review rechecked all 69 `git rev-parse <commit>:<path>` blob IDs and `git show <commit>:<path>` byte hashes with zero mismatches or duplicate paths. The two symlinks are hashed as Git link-target blob bytes, without dereferencing.

## Evidence required and observed

1. The pinned tree has 5,323 tracked entries. The explicit candidate policy selected 69 unique Ucode/markup paths representing 68 unique Git blobs. Mutually exclusive source groups are 17 rpcd raw-mode package files, 47 package `ucode/` files, two other package sources, one htdocs shebang, and two tests/fixtures. A positive `.uc`/`.ut` or recognized shebang candidate is distinguished from generator inputs, generic extensionless htdocs assets, and two known symlink exclusions; this is selection evidence, not query validation.
2. The inspected routing policy projects 17 plain rpcd raw-mode, 13 plain `.uc` extension, three plain shebang, 33 `.ut` markup, one markup-tag-content, and two uncertain extensionless symlink paths. These are **expected** routes; the census did not run the extractor. Markup classification does not establish template semantic modeling.
3. Exact source-path overlap with claims 077, 081 and 084 is 10, 17 and four candidates respectively. Claims 077 and 081 share one LuCI path, so those three selections cover 30 unique candidate paths and leave 39. Claim 021 had already selected 11 of those remaining real `.ut` paths and explicitly excluded two theme symlinks. After that overlap and two non-installed test fixtures, a feasible 24-path next source-route batch remains: 22 `.ut` markup templates and two Ucode-shebang package scripts. It is a proposed batch, not a completed scan or security-negative set.

## Run record

- Date/environment: 2026-11-24 UTC, read-only Git/source inventory in ignored `work/` with clean disposable LuCI, consumer and producer checkouts. No CodeQL database, query, consumer step, or heavy scan was launched.
- Commands/outputs: Git tree/path/blob and byte-hash checks; the independently repeated 69-path blob/byte comparison found zero mismatches and zero duplicate paths. Source path, object mode, link target, byte length, expected route and overlap flags are in the inventory. The producer route policy was inspected but not executed for all paths.
- Controls and limits: the candidate predicate includes recognized Ucode/markup source shapes and records extensionless symlinks, test fixtures and generator inputs separately. Package `luci.mk` and extractor path mapping support proposed install locations, but actual package transforms and installed bytes remain unknown.
- Follow-up: freeze the 24-path batch's exact source-first oracle, reconcile markup coverage with OpenWrt #68, then run separate owned extraction/route/diagnostic checks. Query semantics need their own positive and eligible near miss before any security claim.
