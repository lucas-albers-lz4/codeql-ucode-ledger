# Claim 020: a pinned LuCI markup call in the separate AST

**Status:** Demonstrated for the named source and controls at the pinned revisions.

**Decision and scope:** Can a source-only syntax inventory identify a direct
`dispatch` call in the installed LuCI `uhttpd.uc` source using the newly
extracted markup AST, while distinguishing a member call and a plain-ucode
call? This is a test of syntax identities and source positions, not a claim that
the callee resolves to a particular function or that dispatcher analysis is
supported.

## Revisions and context

- Ucode producer: `8375887ed14825dd59addbfd0df43616d9e684fb`; its tracked tree
  was clean at selection. The [inventory query](../evidence/020-markup-call/MarkupCalls.ql)
  was authored locally for this claim and copied into its disposable QL pack.
- OpenWrt inventory/lock: `33ff29f9f311fec078be8e2df04261529cba0e65`, clean
  at selection. Its checked-in profile and inventory map the source below to
  `usr/share/ucode/luci/uhttpd.uc` and mark it `markup_not_modeled`. This is a
  source-selection reference, not a fresh consumer handoff or live install.
- LuCI: clean detached checkout at `b2e0be4b46ec0fd43394c081fa7c50657af14011`;
  upstream `modules/luci-base/ucode/uhttpd.uc` has SHA-256
  `a2b2694f52c021af16dd06ac8c988b8a0a726d9e8186d308708268ebb8849493` and is
  byte-identical to the producer's checked-in fixture. The pinned `luci.mk`
  copies `ucode/*` to `/usr/share/ucode/luci/`.
- CodeQL 2.27.4, Python 3.15.2, 16 GiB memory and 10 CPUs. The copied extractor
  pack came from the build at the same producer revision recorded in
  [claim 008](008-setblock-typed-handoff.md#refresh-2026-11-21); its grammar pin
  and local bootstrap modification are documented there. The pack and caches
  were copied into this run's own workspace, with a fresh database.
- Ucode [#56](https://github.com/lucas-albers-lz4/codeql-ucode/issues/56)
  closed for AST extraction; [#57](https://github.com/lucas-albers-lz4/codeql-ucode/issues/57)
  retains markup CFG/dataflow and [#58](https://github.com/lucas-albers-lz4/codeql-ucode/issues/58)
  dispatcher work. OpenWrt [#68](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/68)
  retains integration and classification consequences and
  [#70](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/70)
  dispatcher/authorization scope.

## Evidence and observed run

The [source-first expectations](../evidence/020-markup-call/expectations.json)
were prepared before the query. In the real file, they identify a direct
`request` call at `7:12–7:49`, direct `dispatch` at `9:2–9:14`, and member
`req.close()` at `11:2–11:12`. The synthetic, eligible markup near miss
`{{ handler.dispatch(req) }}` has a member callee at `1:4–1:24`; a separate
plain source `dispatch(req);` has a direct call at `1:1–1:13`. All source
hashes and expected row multiplicities are in the receipt.

A fresh database selected exactly these three staged identities: two markup
and one plain. The [routing receipt](../evidence/020-markup-call/routing.json)
labels both markup decisions **inconclusive**, `markup_not_modeled`, even
though the new AST extraction path is present. There were zero excluded or
uncertain classifications among these three selected inputs. The
[successful-file output](../evidence/020-markup-call/extracted.csv) contains
exactly the three paths once each and the
[diagnostics](../evidence/020-markup-call/errors.csv) contain zero errors.
No other corpus files were selected or assessed.

The real CodeQL execution of the ledger query returned exactly the five
[expected rows](../evidence/020-markup-call/calls.csv), each once. The two
markup member calls appear as `MemberExpression` rows, rather than disappearing;
the same-name plain control appears in the plain AST, not the markup AST.
Consequently, filtering this bounded output to the markup tree, an `Identifier`
callee and the name `dispatch` selects exactly the real line-9 row. The query
is an inventory of syntax, not a production security query or a resolved call
edge. In particular, this does not establish callback execution, the imported
target's runtime binding, reachability, taint, authorization, or template CFG
and flow. It does not change the consumer's inconclusive classification.

The [receipt](../evidence/020-markup-call/README.md) records setup, a stalled
interrupted package-install attempt, the copied pack's provenance, separate
fresh databases, commands, statuses, normalized paths, and timings. In the
retained final run, indexing took 0.38 seconds wall, the call query 1.31
seconds, and all diagnostic queries exited 0. Per-process CPU and maximum RSS
are in the [command receipt](../evidence/020-markup-call/commands.json).
These measurements are for the selected three files and do not estimate a
corpus run. No actual consumer or runtime service was invoked.
