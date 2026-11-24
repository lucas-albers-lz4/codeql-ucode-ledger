# Second current LuCI rpcd slice

Status: local source-staged measurement, 2026-11-24. This is a bounded
current-source inventory and draft-suite probe, not an installed-image scan
or security negative result. It follows
[claim 077](../claims/077-current-luci-openwrt-extraction.md) and the
[direct-handler rule design](next-shell-family-20261124.md).

The source-first manifest under ignored
`work/luci-rpcd-second-slice-20261124/source-first.json` has SHA-256
`ef4abca47ed268c3ef59a64c5c4c33d289d147e6b0bd94695f728c9c77b50be1`.
It selects all 17 tracked files under LuCI's `root/usr/share/rpcd/ucode`
trees at clean commit `b2e0be4b46ec0fd43394c081fa7c50657af14011`.
They span multiple LuCI package owners and have exact Git blobs, source
SHA-256 values and proposed installed paths. Verbatim source bytes were
staged; no package build or post-install byte comparison was done.

The manifest records 24 non-comment textual `popen(` sites in ten files and
132 textual handler-shape sites. These are source search counts, not AST
entities or modeled sink/handler counts. A `gpt-6-sol` security review of
`luci-app-wol` found an allowlist-shaped executable guard and argument
quoting construction around a `popen` call. Its `map`/`join` and binary
concatenation path is outside the direct-handler template rule; it remains
an unknown candidate for a future guarded-command/collection/helper analysis,
not a near miss or safety finding for that rule.

A further `gpt-6-sol` read-only source review classified all 24 textual
`popen(` sites for **this rule's shape**: two eligible quoted near misses in
`modules/luci-base/root/usr/share/rpcd/ucode/luci` at lines 343 and 400
(`getSwconfigFeatures` and `getSwconfigPortState`), where
`request.args.switch` is wrapped in `shellquote` within a `popen` template;
22 sites are outside the direct returned-handler raw-template shape. The
two eligible sites remain negatives for the scoped syntax query, not proof
that `shellquote` is safe. The outside sites include helper/interprocedural
commands (`luci.advanced-reboot`, `ddns.uc`, `luci.lldpd`,
`rustdesk-server.uc`), collection or concatenation (`tailscale.uc`,
`luci.wol`), and fixed-literal commands. No site was labeled a vulnerability
or a general security negative. The helper call in `luci.lldpd` at line 6
with fixed-string callers at lines 13–16 is a useful next-family near miss;
`ddns.uc` line 46 is a provenance challenge for helper callers. Both require
fresh AST/call-flow oracles before query implementation.

A fresh macOS CodeQL 2.27.4 run under ignored `run-a/` verified all 17 stage
hashes, selected all 17 files, reported all successful-file identities once
and zero extraction errors. A separate direct extractor route probe recorded
17 `plain` / `rpcd_raw_mode_full_path` / `plain_route_selected` decisions.
The local draft producer suite (metadata-only promotion branch `78590f2`)
resolved to `DirectRpcShellWord.ql` and two extraction diagnostics. Fresh
database analysis emitted SARIF with the direct-handler rule descriptor and
zero results in 3.568 seconds, peak RSS 468,008,960 bytes. That zero is
bounded to this selected source and rule shape; it does not prove the current
plugins safe, the rule precise, or that incoming issues will be found.

An exploratory remeasurement at draft producer
`977331713b4b8b5574813bee0884245bf6db2752` selected `ddns.uc` and
current `tailscale.uc` from this same 17-file inventory. The initial
source-first description incorrectly called them disjoint; the overlap was
corrected after cross-checking the 17-file oracle. Fresh run-g used original
LuCI source layout, observed two `rpcd_raw_mode_full_path` routes and exact
successful extraction identities once each with zero errors, then completed
the default suite and explicit testing Tailscale query with zero rows. All
11 phase commands exited zero. Its ignored local receipt is
`work/stage6-next-install-shaped/run-g/run-receipt.json` (SHA-256
`140b2b9f58bdbc1333a9fb4c7a285241a67091c9e53791ea7d9b0d4b2b5e340a`).
This is duplicate-source exploratory evidence, not an added coverage claim;
the run's attempted source-first oracle and correction remain alongside it
under ignored `work/`. Earlier failed attempts are recorded in the receipt.

Next gates are a Linux job on an immutable producer artifact, source-to-
installed byte mapping for selected package outputs, broader eligible
current/incoming source sampling with manual triage, and a fresh consumer
SARIF acceptance. The existing local consumer parser only checks supplied
bytes and cannot authenticate these steps.
