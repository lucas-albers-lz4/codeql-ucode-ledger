# Claim 052: Unescaped substitution in bounded markup subset

- Status: Blocked
- Program: [Security-40](../planning/security-40-20261124.md), category E
- Producer: `lucas-albers-lz4/codeql-ucode` (markup not modeled; no .ut routing)
- Producer commit: codeql-ucode 734555a9f56893e89e678cdee63028fc17ea5bc8; luci b2e0be4b46ec0fd43394c081fa7c50657af14011
- Consumer: `lucas-albers-lz4/codeql-openwrt` (file-routing / pack-contract receipts)
- Consumer commit: codeql-openwrt cc5f863021a099437beb8da66f53207712974a47
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-p5pg-wcpc-qg27 (unbound notice)
- GHSA-c6vf-395q-4jv6 (https-dns-proxy resolver_url)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Within the producer’s documented bounded markup CFG subset, which pinned .ut templates contain substitution nodes whose value source is untrusted, and does the graph distinguish escaped vs raw output forms?

## Method

Use only the supported bounded markup graph (clean roots per producer docs); inventory substitution node kinds in a manifested template set; no extractor-gate claim, no rendering semantics.

## Required evidence

- Bounded-subset eligibility receipt
- Node-kind multiset with template provenance
- Producer doc/pack digest defining the subset

## Controls

- Positive: raw-output substitution node in subset
- Near miss: escaped-output form
- Negative: template outside subset (recorded excluded, not analyzed)

## Out of scope

- No markup extractor gate pass
- No rendering/XSS execution claim
- No full markup CFG

## Notes

Producer bounded CFG limits are restated from its docs at execution pin.

## Result

Blocked — markup extractor gate; no supported bounded markup graph at the
pins. Security-40 lifts no gate.

- codeql-openwrt `docs/file-routing.md` (clean @cc5f8630): l.14 `.ut` →
  markup classification; l.20 "**Markup** is `markup_not_modeled`;
  classification does not claim a markup extractor."
- `docs/pack-contract.md` l.27 "Do not extract markup in M0–M3"; l.29
  "Markup stays `markup_not_modeled`. The extractor seven-case gate remains
  `codeql-ucode` work and is not claimed."
- Producer codeql-ucode @734555a9 (clean): `extractor.rs` has no `.ut`/markup
  routing; the `ucode_markup` tree-sitter grammar is present but its
  node-types are hidden at init (README l.13); query packs m3 (taint) / m4
  (request-args) contain no markup query. `TemplateSubstitution.qll` /
  `TemplateString.qll` are AST libs for template strings, not a routed `.ut`
  markup graph.
- 33 `.ut` templates exist in pinned luci b2e0be4b (manifestable) but are not
  extracted → substitution-node kinds and escaped-vs-raw forms unobservable.
  Detection gap: GHSA-p5pg-wcpc-qg27 / GHSA-c6vf-395q-4jv6 anchor shapes
  present in source, invisible to the analyzer.
- No node-kind multiset produced (method requires a supported bounded graph +
  producer doc/pack digest defining the subset; neither exists).
- Unblock: codeql-ucode markup extractor seven-case gate pass + `.ut` routing
  + a markup query pack defining the bounded subset; then re-run.
- Evidence: codeql-openwrt/docs/{file-routing.md,pack-contract.md}; producer
  extractor/src/extractor.rs, README.md, ql/src/{m3,m4};
  `/root/workspace/work/security-40/probe-ucode/`.
