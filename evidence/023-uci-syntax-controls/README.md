# Wave 4 UCI syntax receipt

This receipt records a bounded source/query observation on a pinned LuCI controller and six synthetic ucode controls. It is not a sink/effect model, runtime result, consumer handoff, or direct cursor-write claim. The execution used disposable checkouts and a run-owned database.

## Pins and source identity

- Producer codeql-ucode: 0a6612fe0e66351a0ccda43ad5b51f5ef5a2724e (disposable checkout; local untracked test queries only).
- LuCI: b2e0be4b46ec0fd43394c081fa7c50657af14011.
- Controller: modules/luci-base/ucode/controller/admin/uci.uc, staged at usr/share/ucode/luci/controller/admin/uci.uc; Git blob c38a42b10bfefbaa31741feae9395abd8a1f8e40, SHA-256 ac75cfef7d74f87ed7f957778004a7bf486c76df699398c215795b4947e0c93e.
- The producer audit records the luci-ssl-25.12 corpus lock hash as b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a. Source bytes here are pinned LuCI bytes, not reproduced build-installed bytes.
- CodeQL CLI 2.27.4. Pack and copied dependency cache manifests are hashed in pins-and-digests.json. The extractor pack was built at producer `8375887ed14825dd59addbfd0df43616d9e684fb`, then copied and byte-verified against the selected producer `0a6612fe0e66351a0ccda43ad5b51f5ef5a2724e`; the relevant extractor, library, pack and lock inputs were unchanged. See [claim 021](../../claims/021-pinned-luci-template-extraction.md) and [pack provenance](../021-template-extraction/pack-and-lock-provenance.json). The CodeQL toolchain was 2.27.4. The source-first expectations are preserved in SOURCE-FIRST-ORACLE.md.

## Source-first expectations and result

The exact seven input hashes and expected routing are in source-inputs.json; synthetic sources are copied under controls/. All seven were routed plain / ucode_extension / plain_route_selected, extracted exactly once, and had zero extraction-error rows. all-diagnostics.json has zero rows. Routing and extraction comparisons are retained separately.

The predeclared 11 call sites are six in the real controller and five controls. The call-arguments query returned 33 rows: 11 distinct call entity IDs, each with semantic child indexes 0, 1, and 2. All argument classes and spans matched the source-first oracle. Separate identifier/member queries returned seven and four sites; their call-ID sets are disjoint and cover the 11 sites. The helper-body query returned two structural witnesses; the property-read query returned one member expression at property-read.uc:2:16–28 and excludes a call whose function is that member. Full entity IDs, spans, and checks are in observations.json; IDs are local to this database.

Key real source shapes:

- Candidate at uci.uc:79:9–81: identifier callee ubus_call; arguments 'uci' at 19–23, 'commit' at 26–33, object at 36–80.
- Nearby UCI changes calls: uci.uc:76:17–82 and uci.uc:144:22–87.
- Session set: uci.uc:59:4–68:5, direct ubus.call('session', 'set', ...).
- Helper-body call: uci.uc:28:12–42, member callee ubus.call with identifier arguments object, method, and args.
- Controls distinguish UCI changes, session set, an unrelated same-name ubus_call helper, a property read without a call, an unknown direct ubus.call target, and swapped 'commit'/'uci' argument order.

The synthetic same-name helper body calls logger, not ubus.call. This no-forwarding observation is source-derived and remains separate from any caller binding or forwarding-flow claim. The candidate caller and helper body were not joined semantically. Nothing here establishes UCI persistence/effects, authorization, runtime reachability, or cursor().set/commit/delete support.

## Run sequence and limits

The run used a fresh isolated directory on macOS. Database init, index, finalize, routing, exact extraction identities, ExtractionErrors, and the ledger Wave1AllDiagnostics.ql all completed before syntax queries. Query execution was serial with one thread; commands, statuses, timings, and peak RSS where measured are in commands.json. The [decoded outputs](outputs/) preserve rows and database-local entity IDs with the run prefix replaced by `<RUN>`. [Output digests](output-digests.json) record hashes before and after normalization. Raw BQRS files and other logs were retained locally outside Git. The command receipts use placeholders for host-specific paths. The [reconstruction note](commands-reconstruction-note.txt) describes how the command log was completed.

The first, wider query failed during compilation after 8.917 seconds with CodeQL's internal BDD node limit (2^^25) and exit 100. The wide query was left failed. Five narrower queries subsequently succeeded using the same finalized database. The failure log is retained in raw/failed-wide-query.stderr-time.txt.
