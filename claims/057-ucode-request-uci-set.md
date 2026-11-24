# Claim 057: Request values into uci.set in ucode backends

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category C
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-p35r-3323-6g7g (travelmate delegated UCI write → auto-login command)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned ucode backends write request-derived values via uci cursor set/set_list within the supported slice, and is any value validation observed in-source?

## Method

Bounded same-function slice over manifested application set; record value chains and observed validation (newline/metachar checks) as source observations.

## Required evidence

- Site multiset with chain identities
- Validation observation per site

## Controls

- Positive: request.args value into cursor.set without observed checks
- Near miss: value validated against a fixed allowlist in-source
- Negative: literal set value

## Out of scope

- No downstream injection verdict
- No uci runtime behavior

## Notes

None.

## Result

Not yet evaluated.
