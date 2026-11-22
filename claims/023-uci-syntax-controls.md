# Claim 023: Selected LuCI UCI controller call syntax

**Status:** Demonstrated for the pinned controller sites and six synthetic
controls.

**Scope:** Distinguish the identifier-shaped call with the ordered literals
`'uci', 'commit'` and an object argument from nearby calls and a property
read. Check the direct `ubus.call` syntax in the named helper body as a
separate AST observation.

**Out of scope:** Callee or receiver resolution, argument forwarding, direct
cursor writes, configuration effects, authorization, and runtime behavior.

## Revisions and context

- Producer `0a6612fe0e66351a0ccda43ad5b51f5ef5a2724e`, with only untracked
  ledger queries in a disposable checkout. CodeQL 2.27.4 on macOS.
- Clean LuCI source `b2e0be4b46ec0fd43394c081fa7c50657af14011`.
  `modules/luci-base/ucode/controller/admin/uci.uc` has Git blob
  `c38a42b10bfefbaa31741feae9395abd8a1f8e40` and SHA-256
  `ac75cfef7d74f87ed7f957778004a7bf486c76df699398c215795b4947e0c93e`.
  The upstream bytes were staged at `usr/share/ucode/luci/controller/admin/uci.uc`.
- The extractor pack was copied from the build at
  `8375887ed14825dd59addbfd0df43616d9e684fb`, with matching relevant inputs
  at the selected revision. The grammar pin and pack/cache manifest digests
  are in the [provenance record](../evidence/023-uci-syntax-controls/pins-and-digests.json).
  The consumer inventory informs the staged path. No consumer ran.
- [Ucode #53](https://github.com/lucas-albers-lz4/codeql-ucode/issues/53) owns
  the upstream work. Its [pinned audit](https://github.com/lucas-albers-lz4/codeql-ucode/blob/0a6612fe0e66351a0ccda43ad5b51f5ef5a2724e/docs/issue-53-uci-inventory.md)
  identified the controller candidate and observed argument nodes. This run
  adds call and argument identity checks and discriminating controls.

## Evidence

The [source-first oracle](../evidence/023-uci-syntax-controls/SOURCE-FIRST-ORACLE.md)
fixed six controller call sites and the control expectations before querying.
The seven staged inputs all routed as plain `ucode_extension` and appeared
once each in the successful-file query. The extraction-error and all-diagnostic
queries returned zero rows. The [routing and extraction outputs](../evidence/023-uci-syntax-controls/outputs/)
retain the exact identities.

The split queries returned 11 distinct call IDs, seven identifier callees
and four member callees. They returned 33 distinct argument IDs, with one
argument at each ordered position 0, 1, and 2 per call. The pinned source
slices confirmed the controller call at `79:9–81` with `'uci'`, `'commit'`,
and the object literal. The separate helper-body witness is the member call
at `28:12–42` with `object`, `method`, and `args`. The observations and
entity IDs are scoped to this database. [Identity comparison](../evidence/023-uci-syntax-controls/observations.json)

The extracted controls distinguish `uci/changes`, a direct `session/set`
call, a direct call with unrelated literal names, and the same literals in
reverse order. The unrelated helper has the same declaration spelling and
a candidate-shaped call elsewhere in its file. Its selected body-call
witness slices to `logger(...)`. The property control returned the exact
`api.ubus_call` member at `2:16–28`, with no call using that member as its
function expression. The query selectors target predeclared sites.

## Run record

The November 21, 2026 local run used a fresh isolated database. Indexing
took 0.633 seconds and finalization 1.183 seconds. The initial wide query
failed at compilation with CodeQL's internal BDD node limit, exit 100,
after 8.917 seconds and 1,443,348,480 bytes peak RSS. The five split queries
then exited 0 on the finalized database, each taking 1.863–2.069 seconds
before decode. The [command receipt](../evidence/023-uci-syntax-controls/commands.json)
records exact arguments, statuses, timings, and peak RSS. The
[failure log](../evidence/023-uci-syntax-controls/raw/failed-wide-query.stderr-time.txt)
and [decoded evidence](../evidence/023-uci-syntax-controls/README.md) preserve
the observed outputs and normalization details.

The direct cursor-write gate in ucode #53 remains open. A caller-to-helper
binding and the forwarding of its arguments remain unresolved.
