# Candidate claim leads (triage, not claim records)

Inventory date: 2026-11-18 UTC. This is a prioritized lead list, not a coverage
denominator, issue list, or set of results. The current project heads checked
for triage were producer `8376a6d72a2879de24e68a28c6ef1e02b319df83` and
consumer `1d025213c102dfa68a0f1a5cb46de65f5b0c4e33`; fetch again before a new
run. These 17 leads are intentionally not expanded into 100 claim files:
several are refreshes of existing evidence, several lack an actual producer or
source path, and some are explicitly deferred by their owning issues.

## Ranked leads

| Rank | Evidence question | Current disposition / owner |
|---|---|---|
| 1 | Does the current login permission oracle match pinned rpcd's C-locale whitespace behavior, including ASCII controls and UTF-8 NBSP/EM SPACE, through the consumer's session gate? | Completed as [claim 017](../claims/017-rpcd-login-negation-whitespace.md), against rpcd `d99f703e` and consumer `1d025213`. Bounded source-copy differential; not a live auth test. OpenWrt #116 owns the implementation. |
| 2 | Does the current shell-injection candidate query retain exact real-source rows and discriminate the supported quote/context controls on the pinned LuCI source? | Completed as [claim 018](../claims/018-pinned-luci-shellquote-candidates.md). It also records the historical consumer-report boundary; no fresh producer-to-consumer handoff is claimed. Ucode #75 still owns broader control and reconciliation criteria. |
| 3 | Is there a real fresh producer output path into the consumer's retained direct-exec `join_policy_grants` check? | Blocked: current consumer tests use retained rows; no fresh query-to-record interface was identified. Keep separate from claim 017 and issue #113. |
| 4 | Do `getBlockDevices` query output and consumer adapter still agree at a deliberately refreshed pair? | Refresh of claims 002–003 only if relevant query, source, or adapter contracts changed; a new pair is required, not assumed. |
| 5 | Do `setBlockDetect` CSV and typed handoffs still pass current pins with actual producer output? | Refresh of claims 007–008 only if producer/exporter/consumer contracts or evidence need changed. Keep CSV and typed paths distinct. |
| 6 | Does the current `setLocaltime` query output pass the current consumer-owned source oracle and invalid-row control? | Refresh of claim 006 if consumer acceptance or relevant contracts changed. The recent consumer delta was unrelated; inspect current issue #64/#98 before spending a run. |
| 7 | What exact direct `ubus.call` sites appear in pinned installed controller modules beyond the existing plugin fixture? | Technically testable with `UbusCallInventory`, but issue #53 says the inventory is already gated; only pursue for a named downstream analysis need. No receiver binding or dispatch claim. |
| 8 | Does current `GetFeaturesDirectExec.ql` still produce the expected rows on actual upstream bytes, not just the byte-identical historical fixture? | Testable refresh of claim 013. Low priority unless a producer/query delta or current-consumer join needs makes the result decision-relevant. |
| 9 | Can additional installed `luci-base` `.uc` modules be reconstructed and extracted at their locked paths with exact identities? | Candidate only when tied to a query or analysis need; extraction alone is not semantic coverage. Dispatcher policy remains deferred. |
| 10 | Can the consumer's declaration/grant comparison be independently approved as an ACL-correctness oracle? | Not established by claim 012. Requires a separate policy oracle; do not reinterpret its frozen grant catalog as ground truth. |
| 11 | Can imported `init_action` calls be freshly produced and retained by an actual producer-to-consumer path? | Keep claim 005 partial: no current query-to-record path identified. Do not invent an exporter. Ucode #50/#54 and OpenWrt #65 own adjacent work. |
| 12 | Is there a pinned, extractable UCI write call that would justify a write-effect query? | No such call was found in the current audited LuCI fixture; issue #53 says this slice is blocked. Reopen only with a named real write site. |
| 13 | Does `realpath`/`stat` library-call habitation change an observable query result? | Issue #51's current census measured no affected result; do not promote on target counts alone. Reopen only with a discriminating affected case. |
| 14 | Does exceptional-flow modeling change an observable pinned query result? | Issue #51's audit found no qualifying affected result. A syntax or CFG count is not enough; defer until a decision-relevant case exists. |
| 15 | What are the exact dispatcher ingress/ACL route semantics for `/cgi-bin/luci` and `admin/ubus/*`? | Explicitly deferred by ucode #58 and OpenWrt #70. Do not infer SID bypass, runtime routing, or BAC from direct-call inventory. |
| 16 | Which real markup/template sources and sinks are supported, and with what text-node guarantees? | Owned/deferred by ucode #56/#57 and OpenWrt #68/#70. No coverage claim from a green renderer test or an empty query. |
| 17 | What selection, successful extraction, errors, exclusions and elapsed time result from a defined larger corpus? | Requires an explicit corpus boundary, independently enumerated expected identities, resources, and serial run plan. No full-corpus time or coverage percentage follows from the small slices already recorded. |

## Working rule

Do not repeat ranks 1–2 at the same pins. Start the next two- or three-claim
batch with a concrete decision and the smallest claim that can change it.
Rank 3 stays blocked until a fresh producer-to-record interface exists. For a
refresh lead, first inspect the selected-source/query/consumer diff; if no
relevant delta exists, stop. Otherwise choose a new source slice whose identity,
positive and eligible near miss can be established independently. Keep blocked
leads as stop conditions, not as empty or proposed query results.
