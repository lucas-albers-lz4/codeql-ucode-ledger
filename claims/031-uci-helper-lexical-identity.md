# Claim 031: UCI helper lexical identity under reassignment

**Status:** Demonstrated for one pinned controller, one reassigned-formal positive, and one eligible alias near miss.

**Scope:** The producer's test-only `UciHelperObservation` associates the selected `ubus_call('uci', 'commit', ...)` site with a same-file helper and requires each `ubus.call` argument identifier to resolve lexically to the corresponding helper formal. A reassigned formal still satisfies that identity check; a local alias passed in place of the formal does not.

**Out of scope:** Preservation of caller argument values, interprocedural data flow, runtime call execution or resolution, authorization, UCI effects, persistence, reachability, or security conclusions.

## Revisions and context

- Producer `1ccf5268e6915dc8d4cbb926b28be8ff79bcb0ed`; the observer was introduced in `cc87f6d7a104bd54bcb8a1ec97e9eb23afc6ba63` and is unchanged at the selected revision.
- LuCI `b2e0be4b46ec0fd43394c081fa7c50657af14011`; controller source `modules/luci-base/ucode/controller/admin/uci.uc`, blob `c38a42b10bfefbaa31741feae9395abd8a1f8e40`, SHA-256 `ac75cfef7d74f87ed7f957778004a7bf486c76df699398c215795b4947e0c93e`.
- CodeQL CLI 2.27.4. The reused extractor pack was built at producer `8375887ed14825dd59addbfd0df43616d9e684fb`; no extractor or grammar source delta was found through the selected producer pin. The run's pack, lock, and dependency digests are recorded in [provenance](../evidence/031-uci-helper-lexical-identity/provenance.json).
- Ucode issue [#53](https://github.com/lucas-albers-lz4/codeql-ucode/issues/53) owns the upstream inventory/helper work. Its direct cursor-write gate remains unmet; this evidence does not reopen or satisfy that gate.

## Evidence

The [source-first oracle](../evidence/031-uci-helper-lexical-identity/ORACLE.md) fixed the pinned controller positive, reassigned-formal positive, and alias near miss before the corrected run. The [run record](../evidence/031-uci-helper-lexical-identity/README.md) preserves exact pins, routes, identities, query results and multiplicity, timings, dependency provenance, failures, and limitations. The actual extractor routing receipt was captured before finalization: all three `.uc` inputs routed plain with reason `ucode_extension`; excluded, uncertain, markup, and duplicate counts were zero. Successful extraction returned each exact file once; extraction errors and file-located diagnostics returned zero rows.

The observer returned exactly two rows: the real controller pair at caller line 79 / helper forward line 28, and the reassigned-formal control at caller line 5 / helper forward line 3. It omitted the alias control. The separate eligibility diagnostic returned one same-file candidate and showed that argument 1 is the local `forwardedMethod` identifier and resolves to its local declaration. Aggregate queries counted one distinct call and helper for each observer-positive site, and one candidate call, argument identifier, and variable target for the alias control. These counts apply only to the specified entities and keys.

The source-first alias identifier end column was predicted as 43 using an exclusive boundary; output reports 42. Source byte counting confirms 15 bytes occupying columns 28–42 inclusive. This mismatch is retained explicitly in the oracle and result record.

## Run record

The corrected run used a fresh detached producer checkout, a separate staged source tree and database, run-owned temp/XDG/common/compilation caches, and a copied compatible extractor pack. `HOME` was inherited. Setup, indexing, finalization, diagnostics, observer and entity-count queries completed successfully after the recorded failed attempts were resolved. Full outputs are normalized in the evidence folder; raw BQRS and timing logs remain under ignored `work/` and are linked by raw hashes.

The result demonstrates a narrow model boundary: lexical variable identity survives reassignment as an AST binding fact, while the caller-supplied value need not survive. It does not establish a runtime value transfer or UCI write effect.
