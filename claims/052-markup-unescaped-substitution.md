# Claim 052: Unescaped substitution in bounded markup subset

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category E
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
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

Not yet evaluated.
