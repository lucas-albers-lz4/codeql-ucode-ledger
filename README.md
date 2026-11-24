# codeql-ucode-ledger

A small, independent workspace for examining **specific coverage claims** across [codeql-ucode](https://github.com/lucas-albers-lz4/codeql-ucode) and [codeql-openwrt](https://github.com/lucas-albers-lz4/codeql-openwrt).

The ledger connects a claim to the source it concerns, the analyzer behavior it relies on, the tests or observations that support it, and what remains unknown. It is not an overall coverage percentage or a list of security guarantees.

## Start here

For the next batch, read [PLAN.md](PLAN.md); agent workflow guidance is in [AGENTS.md](AGENTS.md).

The initial claims and their current status are:

1. [Explicit staged-root extraction](claims/001-staged-root-extraction.md): demonstrated for one pinned fixture and root; see the run record.
2. [getBlockDevices query observation](claims/002-getblock-query.md): demonstrated for a pinned fixture and controls.
3. [getBlockDevices producer–consumer handoff](claims/003-getblock-handoff.md): demonstrated for a freshly generated table and pinned consumer.

Together these move from source selection through extraction, query, and consumer, but each claim stands on its own evidence. Claims **001–003** have bounded run records; reassess them when the selected revisions change. The [coverage portfolio](planning/coverage-portfolio.md) maps representative paths; the [candidate lead list](planning/claim-opportunities.md) records prioritization, ownership and stop conditions without inflating leads into claims. See [the claim template](claims/TEMPLATE.md) before adding a result.

## Claim index

| Claim | Current ledger status | Scope |
|---|---|---|
| [001](claims/001-staged-root-extraction.md) | Demonstrated | Explicit staging root and extraction |
| [002](claims/002-getblock-query.md) | Demonstrated | `getBlockDevices` source-table query |
| [003](claims/003-getblock-handoff.md) | Demonstrated | `getBlockDevices` CSV handoff |
| [004](claims/004-system-shadowing.md) | Demonstrated | Bounded `system` shadowing controls |
| [005](claims/005-imported-callee-boundary.md) | Partial | Imported-callee observation; no fresh retained-record path identified |
| [006](claims/006-setlocaltime-construction.md) | Demonstrated | `setLocaltime` source construction and consumer |
| [007](claims/007-setblock-csv-handoff.md) | Demonstrated | `setBlockDetect` CSV handoff |
| [008](claims/008-setblock-typed-handoff.md) | Demonstrated | `setBlockDetect` typed handoff, refreshed at the 2026-11-21 pair |
| [009](claims/009-luci-sys-status.md) | Demonstrated | Two LuCI status helper source shapes |
| [010](claims/010-ubus-call-inventory.md) | Demonstrated | Direct `ubus.call` syntax |
| [011](claims/011-same-file-jump-local.md) | Demonstrated | Experimental same-file argument-to-parameter flow |
| [012](claims/012-backend-declaration-comparison.md) | Demonstrated | Pinned source declarations versus catalog, with oracle qualification |
| [013](claims/013-getfeatures-direct-calls.md) | Demonstrated | `getFeatures` direct call inventory |
| [014](claims/014-fs-binding-guard.md) | Demonstrated | Conservative `fs` binding controls |
| [015](claims/015-pinned-luci-source-extraction.md) | Demonstrated | Three pinned upstream LuCI sources extracted |
| [016](claims/016-pinned-luci-status-query.md) | Demonstrated | Status source-shape query on the upstream slice |
| [017](claims/017-rpcd-login-negation-whitespace.md) | Demonstrated | Consumer login-ACL whitespace parity with pinned rpcd reference |
| [018](claims/018-pinned-luci-shellquote-candidates.md) | Demonstrated | Seven conservative candidate rows on one pinned LuCI source file |
| [019](claims/019-pinned-luci-shellquote-slice.md) | Demonstrated | Shell-injection query on eight selected pinned LuCI source files |
| [020](claims/020-pinned-markup-call-syntax.md) | Demonstrated | Markup AST call syntax on one pinned LuCI file and controls |
| [021](claims/021-pinned-luci-template-extraction.md) | Demonstrated | Extraction of 11 staged pinned LuCI templates and controls |
| [022](claims/022-pinned-mixed-template-ast.md) | Demonstrated | Selected mixed-template AST syntax and literal lookalike |
| [023](claims/023-uci-syntax-controls.md) | Demonstrated | Selected UCI controller call and argument syntax with controls |
| [024](claims/024-markup-declaration-ast.md) | Demonstrated | Markup declaration and initializer AST prerequisite |
| [025](claims/025-mixed-profile.md) | Demonstrated | Plain and markup AST roots for a selected mixed LuCI stage |
| [026](claims/026-v2-feed-policy-scope.md) | Demonstrated | Synthetic v2 provider-feed and policy-scope boundary |
| [027](claims/027-markup-trim-open-cfg.md) | Demonstrated | Ordinary markup CFG and trim-open exclusion on two fixtures |
| [028](claims/028-creation-sibling-scopes.md) | Demonstrated | Creation graph isolation for supported and unsupported sibling callables |
| [029](claims/029-typed-refactor-handoff.md) | Demonstrated | Fresh typed v1 handoff after consumer validation refactor |
| [030](claims/030-v2-archive-receipt-boundary.md) | Demonstrated | V2 archive identity boundary for fresh v1 handoff receipts |
| [031](claims/031-uci-helper-lexical-identity.md) | Demonstrated | UCI helper formal identity under reassignment and local alias controls |
| [032](claims/032-markup-trim-matrix-implementation.md) | Demonstrated | Current markup CFG behavior across a six-fixture trim matrix |
| [033](claims/033-bounded-markup-callable-call-order.md) | Demonstrated | Updated bounded callable ordering with a computed-callee control |
| [034](claims/034-markup-trim-delimiters.md) | Demonstrated | Local trim-delimiter ordering patch with exact controls |
| [035](claims/035-acl-file-read-glob-breadth.md) | Demonstrated | Security-40: ACL file-read globs spanning path separators |
| [036](claims/036-acl-exec-in-read-scope.md) | Demonstrated | Security-40: Exec rules misplaced into read ACL scope |
| [037](claims/037-acl-shell-interpreter-exec.md) | Demonstrated | Security-40: Shell-interpreter exec grants |
| [038](claims/038-acl-init-action-argv.md) | Demonstrated | Security-40: Init-script exec grants and action argv control |
| [039](claims/039-acl-persistence-write.md) | Demonstrated | Security-40: Write grants to persistence paths |
| [040](claims/040-acl-read-scope-mutating-ubus.md) | Demonstrated | Security-40: Mutating ubus methods under read-only ACL |
| [041](claims/041-ucode-app-request-system.md) | Blocked | Security-40: request.args to system() in application ucode backends |
| [042](claims/042-ucode-app-request-popen.md) | Blocked | Security-40: request.args to popen() in application ucode backends |
| [043](claims/043-ucode-app-fs-exec-argv.md) | Blocked | Security-40: request.args to fs.exec / fs.exec_direct argv |
| [044](claims/044-app-shellquote-placement.md) | Blocked | Security-40: shellquote placement in application command templates |
| [045](claims/045-app-sprintf-command-assembly.md) | Blocked | Security-40: sprintf/concatenation command assembly before sinks |
| [046](claims/046-luci-base-getfeatures-templates.md) | Demonstrated | Security-40: Fixed-command template substitution in getFeatures |
| [047](claims/047-ucode-request-path-read.md) | Blocked | Security-40: Request-controlled paths into ucode fs read/stat |
| [048](claims/048-cgi-io-canonicalize-order.md) | Demonstrated | Security-40: cgi-io canonicalize_path vs ACL ordering |
| [049](claims/049-rpcd-file-symlink-reauth.md) | Demonstrated | Security-40: rpcd file plugin symlink re-authorization |
| [050](claims/050-rpcd-session-tmpdir.md) | Demonstrated | Security-40: Session-token-derived temporary UCI paths |
| [051](claims/051-ucode-request-path-write.md) | Blocked | Security-40: Request-controlled destinations into fs.write/rename |
| [052](claims/052-markup-unescaped-substitution.md) | Blocked | Security-40: Unescaped substitution in bounded markup subset |
| [053](claims/053-lease-data-render-sites.md) | Demonstrated | Security-40: Lease/UCI-derived strings in status render paths |
| [054](claims/054-js-dangerous-render-sinks.md) | Demonstrated | Security-40: JS dangerous-render sinks in pinned views |
| [055](claims/055-uhttpd-cgi-uri-reflection.md) | Demonstrated | Security-40: uhttpd CGI error/URI reflection |
| [056](claims/056-template-arg-untrusted.md) | Blocked | Security-40: Template/include argument propagation |
| [057](claims/057-ucode-request-uci-set.md) | Blocked | Security-40: Request values into uci.set in ucode backends |
| [058](claims/058-js-rpc-uci-set-sites.md) | Demonstrated | Security-40: JS rpc.declare UCI set call sites (enumeration only) |
| [059](claims/059-shell-eval-config-values.md) | Proposed | Security-40: Package shell eval/sh -c of config values |
| [060](claims/060-uci-newline-line-formats.md) | Proposed | Security-40: Newline-bearing UCI values into line-based formats |
| [061](claims/061-ucode-commit-restart-adjacency.md) | Blocked | Security-40: uci.commit to service-restart adjacency |
| [062](claims/062-uhttpd-te-case-match.md) | Proposed | Security-40: Transfer-Encoding matching case sensitivity |
| [063](claims/063-uhttpd-cl-chunk-signedness.md) | Proposed | Security-40: Content-Length signedness and chunk-size state |
| [064](claims/064-uhttpd-ubus-params-type.md) | Proposed | Security-40: POST /ubus/call params type validation |
| [065](claims/065-uhttpd-keepalive-drain.md) | Proposed | Security-40: Keep-alive body drain and parse-error desync |
| [066](claims/066-uhttpd-realm-handler-enforce.md) | Proposed | Security-40: Basic Auth realm enforcement on handler dispatch |
| [067](claims/067-ubusd-blobmsg-peer-bounds.md) | Proposed | Security-40: ubusd peer blobmsg parsing bounds |
| [068](claims/068-px5g-signing-bounds.md) | Proposed | Security-40: px5g certificate-signing buffer bounds |
| [069](claims/069-mdnsd-ptr-stack-bounds.md) | Proposed | Security-40: mdnsd PTR/reverse-lookup stack buffers |
| [070](claims/070-libubox-blobmsg-json-bounds.md) | Proposed | Security-40: libubox blobmsg JSON serialization bounds |
| [071](claims/071-libuci-parse-package-lifecycle.md) | Proposed | Security-40: libuci uci_parse_package object lifecycle |
| [072](claims/072-procd-path-env-filter.md) | Proposed | Security-40: procd PATH/environment filter in service exec |
| [073](claims/073-banip-log-first-ip.md) | Proposed | Security-40: banip log-monitor first-IP extraction |
| [074](claims/074-travelmate-fcheck-injection.md) | Proposed | Security-40: travelmate f_check script/script_args injection |

Every demonstrated status is limited to the run, inputs, controls and revisions
in that claim. These rows are not a coverage percentage.

## Scope and status

- **Proposed:** a question or expected contract; no current run is claimed.
- **Demonstrated:** supported by an identified run, exact revisions, commands, expected identities, observed outputs and relevant controls; scoped to those inputs.
- **Partial:** some, but not all, required evidence exists. State exactly what is missing.
- **Unknown:** insufficient evidence; this is not a negative result.
- **Deferred:** intentionally out of scope or owned elsewhere, with a reference and revisit condition.

A clean extraction does not prove semantic accuracy; a query result does not prove runtime reachability; an empty result does not establish safety; a matching fixture does not prove a fresh producer execution. Separate language support, analyzed source coverage and policy interpretation. Do not infer device behavior, authorization, taint, or vulnerability from a source observation alone.

## Working on another server

Clone this repository and create **separate disposable checkouts** of the two projects. Do not use active development checkouts or share writable CodeQL databases between runs. Each run needs its own workspace, database, outputs, and enough disk, memory and CPU. Local run artifacts belong under `work/`, which is ignored by Git; selectively retain small, reviewed evidence separately when useful. Do not commit credentials, raw private data, generated databases or unexplained host paths.

For lightweight receipt and local-link checks, see [the verification scripts](scripts/README.md). They do not authenticate runs or validate claim semantics.

This repository is a documentation and investigation starting point. **It does not yet contain an automated end-to-end runner or CI.** Follow the linked project instructions for the exact selected revisions; inspect scripts before running them. Build and test commands can modify their working directory, invoke network operations and consume substantial resources. Never run an adapter that rewrites reports against an active checkout: use a disposable consumer copy.

### Reference pair

The initial source links refer to a **historical reference pair**, not a recommendation to use stale code for every run:

| Repository | Reference commit |
|---|---|
| `codeql-ucode` | `7a1ded90962cc85a3e3a94949584c64214426aed` |
| `codeql-openwrt` | `a8bdef3c22c8d5ba9999baa978052b59bd22907e` |

When you start a new run, choose and record both commits explicitly. Fetch the branches first, then create detached checkouts at the chosen full SHAs in a private workspace. For example, after cloning each project into `work/codeql-ucode` and `work/codeql-openwrt`:

```sh
git -C work/codeql-ucode fetch origin
git -C work/codeql-openwrt fetch origin
git -C work/codeql-ucode checkout --detach <ucode-commit>
git -C work/codeql-openwrt checkout --detach <openwrt-commit>
git -C work/codeql-ucode rev-parse HEAD
git -C work/codeql-openwrt rev-parse HEAD
```

Replace the placeholders; do not paste the example unchanged. Record dirty state, tools/versions, fixture or corpus pins, commands and actual outcomes. Recheck the relevant source contracts and existing issues at those commits: the reference pair may differ from current `main`. Comparing different pairs requires an explicit delta review; an earlier pass does not automatically transfer.

## Optional model roles

For model-assisted work, keep the split simple:

- **Luna:** bounded mechanical collection, inventories, mapping paths to existing tests, and organizing run receipts. Check its output against the actual sources or commands.
- **Terra:** coordinate the paired pins and isolated runs, verify claims and reproduce candidate results, reconcile overlap with existing issues, and maintain the ledger.
- **Sol:** assess difficult semantic questions, choose discriminating controls, judge evidence boundaries, and synthesize the strongest unresolved coverage questions.

These are task roles, not separate mandatory stages or a requirement to run three models for every claim. Start with the simplest useful workflow. Resolve and smoke-test the desired model route at execution time; do not silently substitute another model. A second pass by the same model is fresh review, not independent-model corroboration.

## Relationship to the projects

This is an incubation workspace, not a submodule or a new authoritative implementation. Reuse existing project tests and issues. As the work matures, move producer-only regressions to `codeql-ucode` and consumer-only regressions to `codeql-openwrt`; decide separately where genuinely paired integration tests belong. Do not duplicate a finding already owned by an open issue.
