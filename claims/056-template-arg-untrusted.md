# Claim 056: Template/include argument propagation

- Status: Blocked
- Program: [Security-40](../planning/security-40-20261124.md), category E
- Producer: `lucas-albers-lz4/codeql-ucode` (historical pin: no .ut routing; see current reconciliation below)
- Producer commit: codeql-ucode 734555a9f56893e89e678cdee63028fc17ea5bc8; luci b2e0be4b46ec0fd43394c081fa7c50657af14011
- Consumer: `lucas-albers-lz4/codeql-openwrt` (file-routing / pack-contract receipts)
- Consumer commit: codeql-openwrt cc5f863021a099437beb8da66f53207712974a47
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-q335-4c83-c88h (adblock-fast status errors from delegated blocklist names)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Within the bounded markup subset, which template/include call sites pass untrusted-derived arguments, and does the supported graph observe the argument→substitution edge?

## Method

New bounded decision justified by the XSS class (the old template-argument deferral required a distinct analysis need — this is it); stay inside documented subset; no production model.

## Required evidence

- Call-site multiset
- Argument-edge observation receipts
- Subset eligibility per site

## Controls

- Positive: include with request-derived argument in subset
- Near miss: literal argument
- Negative: site outside subset

## Out of scope

- No lift of the general template-argument deferral
- No interprocedural rendering claim

## Notes

None.

## Historical result at 734555a9

Blocked — same markup extractor gate as claim 052; the argument→substitution
edge is unobservable. Security-40 lifts no gate and does not lift the old
template-argument deferral.

- codeql-openwrt `docs/file-routing.md` l.20: markup is `markup_not_modeled`;
  `docs/pack-contract.md` l.27/29: do not extract markup in M0–M3; the
  seven-case extractor gate remains codeql-ucode work, not claimed.
- Producer codeql-ucode @734555a9 (clean): no `.ut` routing in `extractor.rs`;
  `ucode_markup` grammar hidden at init; no markup query pack (m3 taint / m4
  request-args). The "new bounded decision justified by the XSS class" still
  requires a supported bounded markup subset, which is documented as
  `markup_not_modeled` — so no call-site multiset or argument-edge observation
  receipt can be produced.
- 33 `.ut` templates in pinned luci b2e0be4b are manifestable but not
  extracted. Detection gap: GHSA-q335-4c83-c88h (adblock-fast status errors)
  anchor shape present in source, invisible to the analyzer.
- Unblock: codeql-ucode markup extractor seven-case gate pass + `.ut` routing
  + markup query pack defining the bounded subset and argument edges; then
  re-run this bounded decision.
- Evidence: codeql-openwrt/docs/{file-routing.md,pack-contract.md}; producer
  extractor/src/extractor.rs, README.md, ql/src/{m3,m4};
  `/root/workspace/work/security-40/probe-ucode/`.


## Current reconciliation (2026-11-24)

The historical finding above is scoped to divergent producer pin `734555a9` and must not be read as current-main behavior. At `9166af76cf6944e1b3ea5856a9176366a1f7a6ee`, markup AST and bounded CFG libraries exist and `.ut` routing is present. In the independently audited local fresh-pack 33-file run, all 33 pinned LuCI templates had one successful-file row and zero returned `ExtractionErrors` rows; every route remained `inconclusive` / `markup_not_modeled`. See the [portable identities and receipt](../evidence/issue160-20261124-markup-33-reconciliation/README.md) for exact paths, hashes, build-source edit, diagnostics and limitations. Extraction does not establish complete ASTs or modeled flow.

**Status remains blocked.** No supported executable markup-taint or template argument-to-substitution edge probe has been established in the inspected current source. A valid source-first positive and discriminating eligible near miss, a supported model/query, and exact extraction and result evidence are still needed to answer this claim; no gate or deferred track has been lifted. This observation makes no runtime, vulnerability, rendering or security-coverage claim. The historical verification prefix `629a708` and 641/641 result remain unknown; the bounded search does not prove a history rewrite.
