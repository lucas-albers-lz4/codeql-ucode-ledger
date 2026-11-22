# Twelve-wave evidence roadmap

See the [progress log](roadmap-progress-20261121.md) for completed and deferred
gates. The [unblocking map](unblocking-20261121.md) identifies
which prerequisite work can be done in the ledger and which gates remain upstream.

This is an ordered queue of **12 waves**, not 12 promised claims or an
instruction to execute them automatically. A wave is a bounded analysis
decision, generally one to three claims when the evidence warrants it. Work
through the queue in order; when a stated gate is not met, record a short
reason and move to the next independent eligible wave. Do not create an empty
claim merely to fill a slot. Reassess the remaining queue after each two or
three waves and whenever upstream contracts or ownership change.

The first four waves are the existing [four-decision next wave](wave-next-20261121.md),
now placed in a longer sequence. Its detailed sources, controls and stop
conditions remain authoritative. This roadmap does not supersede
[AGENTS.md](../AGENTS.md), the claim template, or upstream issue ownership.

## Common launch and completion rules

Before each eligible wave, fetch and select full project and corpus SHAs,
inspect relevant deltas and current issue ownership, and check available
resources. The observed planning-time heads were producer
`0a6612fe0e66351a0ccda43ad5b51f5ef5a2724e` and consumer
`d37adeadaf836ba97049f75087a348165027f7f9`; these are observations, not future
pins. Use isolated checkouts, databases, caches and outputs; serial heavy runs
are the default. Establish independent expected identities and multiplicities
before results, with valid positive and discriminating eligible near-miss
controls. Check exact routing, extraction identities and diagnostics before
query interpretation. Time setup, extraction, query and any consumer action,
and retain reviewed portable receipts. Distinguish upstream bytes staged at an
installed path from bytes produced by the configured installation process.

After each wave, review results and limitations, update the ledger only for
actual evidence, and identify whether the next wave remains useful. Do not
count claims, corpus paths or passed controls as a coverage percentage. A
fresh handoff requires the actual producer output passed to the actual
consumer. No planned step authorizes invention of an upstream exporter or a
model merely to complete the queue.

Wave 1 is recorded in [claim 021](../claims/021-pinned-luci-template-extraction.md).
Wave 2 is recorded in [claim 022](../claims/022-pinned-mixed-template-ast.md).
The remaining waves retain their individual gates.

## Ordered waves

| Wave | Decision and candidate evidence | Gate and boundary | Default role |
|---|---|---|---|
| 1. Profile markup selection | Reconcile the selected LuCI profile's real `.ut` sources, installed-path mapping, routing and per-file extraction diagnostics with independently enumerated inputs. Use a known valid markup positive and a plain/shebang control. | Re-pin and verify sources, symlinks, collisions and `SubstituteVersion`; raw staged source is not necessarily installed bytes. Preserve `markup_not_modeled` and report parse errors per identity. OpenWrt [#68](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/68). | Luna collects and runs a specified inventory; Terra verifies setup and exact receipts. |
| 2. Mixed-template AST | On a clean source from wave 1, e.g. `view.ut`, distinguish selected expression tags and statement calls from literal text with exact spans, parents and a valid lookalike control. | Defer if no relevant clean source or independent AST identity oracle exists. AST observations do not prove rendering, escaping, CFG or flow. OpenWrt #68; ucode [#57](https://github.com/lucas-albers-lz4/codeql-ucode/issues/57). | Sol designs the controls when identity is ambiguous; Luna runs the bounded collection; Terra checks it. |
| 3. Plain template arguments | For a named downstream inventory decision, test `getTemplateArgument(index)` on distinct real `runtime.uc` calls and compare exact arguments/substitutions with non-template and argument-position controls. | Defer if the current upstream gate already answers the decision or no consumer needs it. No template value-flow or runtime claim. Ucode [#127](https://github.com/lucas-albers-lz4/codeql-ucode/issues/127) shipped its foundation. | Luna inventories candidate sites; Terra validates API and output; Sol only for a difficult semantic boundary. |
| 4. Indirect UCI syntax | Determine whether a source inventory can distinguish the `uci.uc` indirect `commit` candidate from `changes`, session `set`, an unrelated same-named helper and property-read controls. | The upstream audit explicitly requests exact syntax and controls for a separately scoped indirect-ubus inventory; this is a producer-side feasibility decision, not a consumer join. Proceed only if the new controls add evidence beyond that audit. Preserve AST-entity multiplicity where tuples coincide; ambiguity yields partial/deferred evidence. This is not a direct cursor-write or effect model. Ucode [#53](https://github.com/lucas-albers-lz4/codeql-ucode/issues/53). | Sol sets entity/binding controls; Luna gathers receipts; Terra verifies. |
| 5. JavaScript inventory transfer | For a **named downstream need** not already satisfied by upstream, choose one bounded pinned LuCI JS surface from the OpenWrt #69 inventories, independently enumerate sites and controls, and compare fresh extraction and the actual inventory query. | The bounded 88-file extraction and RPC/fs/CGI inventories already shipped; the macOS fixture-test path change alone does not justify a corpus rerun. The user has authorized bounded JS UCI planning, while the earlier execution hold remains pending review. Re-derive the relevant baseline and skip without a named delta or gap; no Track A, runtime, authorization or full-profile claim. OpenWrt [#69](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/69). | Luna performs the mechanical inventory and receipt; Terra validates revision/identity; Sol only if query semantics require it. |
| 6. Receiver-alias relevance | Revisit the producer's experimental receiver-alias flow only if a pinned real case and downstream query outcome make aliasing consequential. Derive per-use positive/reassignment controls and preserve entity identity. | The current prototype's synthetic observations do not establish a production `fd.read` model or runtime resource identity. Skip without a discriminating affected case and current owner scope. Ucode [#48](https://github.com/lucas-albers-lz4/codeql-ucode/issues/48). | Sol designs flow controls; Terra verifies; Luna inventories inputs. |
| 7. Changed handoff contract | When a relevant source/query/exporter/adapter/lock delta appears, select **one** affected existing handoff (getBlockDevices, setBlockDetect CSV or typed, or setLocaltime) and exercise the actual fresh producer through its actual consumer with rejection controls. | No delta or changed decision means skip. Keep typed and CSV contracts separate and use isolated consumer copies. Ucode [#55](https://github.com/lucas-albers-lz4/codeql-ucode/issues/55), OpenWrt [#65](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/65). | Luna collects the delta and runs a reviewed recipe; Terra coordinates and verifies the live chain; Sol reviews incompatible or ambiguous contracts. |
| 8. Retained direct-exec grant join | If a supported fresh producer-to-record path becomes available, trace one actual direct-exec output into the consumer's retained grant join, using an independently defined identity/policy-context oracle and a rejected near miss. | Currently no such fresh record interface was identified; retained-row tests, including OpenWrt [PR #113](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/113), are not a live handoff. Keep blocked until the actual interface exists. | Terra coordinates paired execution; Sol reviews oracle and policy boundaries; Luna collects receipts. |
| 9. Imported-callee boundary | Revisit claim 005 only when a supported fresh imported-callee query-to-record path exists; establish exact source/sink identities and multiplicity, controls, producer output and consumer retention. | Keep claim 005 partial until that path is observed; no invented exporter, inferred cross-file taint or historical record relabeling. Ucode [#50](https://github.com/lucas-albers-lz4/codeql-ucode/issues/50), [#54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54), OpenWrt #65. | Sol owns the semantic/control review; Terra verifies the real handoff; Luna can inventory candidate artifacts. |
| 10. Markup CFG after implementation | If an actual supported markup CFG implementation appears, choose a narrow real or source-derived case and compare its full documented node/edge identities against a predeclared positive and unsupported or malformed controls. | Ucode #57's current proposal is not an implementation. Skip until the owning issue and implementation permit this scope; no inference of rendering, taint or security from AST extraction. | Sol designs edge/unsupported controls; Terra reproduces; Luna collects bounded identities. |
| 11. Independent policy oracle | If a named policy decision needs it, test a small declaration/grant comparison against an independently sourced policy oracle and a discriminating near miss. | Claim 012's retained catalog is not automatically ground truth; defer without an independent oracle and explicit interpretation boundary. Do not claim live authorization or runtime behavior. | Sol evaluates oracle independence and policy semantics; Terra checks reproducibility; Luna collects source evidence. |
| 12. Deliberately broader source slice | User selected the nine non-generated plain plus twelve markup profile sources for a mixed-routing decision; independently enumerate identities and transformations, then measure selection, extraction, errors, exclusions and one supported query with controls if gates pass. | Check resources and serial run plan first. No extrapolated full-corpus runtime, completeness or safety claim from a slice; revisit current owners and all prior results before selecting it. | Luna can inventory and execute a reviewed run; Terra verifies scope, resource plan and evidence; Sol assists only for nontrivial query semantics. |

## User-selected decision defaults

A concrete upstream analysis need may justify a bounded source/query
investigation without a downstream consumer. Use documented project intent as
the starting policy authority; ask the user to decide when intended policy is
missing rather than infer it from current behavior. The user chose to prepare
and run the nine-plain/twelve-markup mixed profile slice if its evidence and
resource gates pass. The user also chose to resume bounded JS UCI **planning**;
that does not itself lift the existing execution hold.

## Routing and cost discipline

**Luna can do much of the mechanical work**: pin and path inventories, source
and issue collection, preparing receipts, running a reviewed recipe, comparing
exact output with an independently prepared oracle, and flagging mismatches.
Its output must be checked against source and command results. Terra is useful
for coordinating isolated producer/consumer runs and reviewing revisions,
identity, failures and claims; it is not mandatory for every simple command or
every wave. Use Sol selectively for control design, difficult semantics,
independent-oracle questions and ambiguous evidence boundaries. These roles
are not a fixed three-model pipeline.

At execution time resolve and smoke-test the configured exact model routes;
if one is unavailable, report it and do not silently switch. Only claim an
independent model review if it actually occurred. Delegate bounded independent
tasks, not simultaneous scans against shared writable artifacts. Compare cost
or speed only from measured usage and timing; this plan does not assert a
particular savings. Authentication and billing routes remain unchanged unless
the user requests and confirms a change.
