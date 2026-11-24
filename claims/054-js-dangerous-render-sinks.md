# Claim 054: JS dangerous-render sinks in pinned views

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category E
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-8v49-6387-7f89 (upnp port-mapping XSS)
- GHSA-vvj6-7362-pjrw / CVE-2026-32721 (WiFi scan modal)
- CVE-2019-25015 (SSID stored XSS)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned LuCI JS views contain dangerous-render sink shapes (innerHTML, insertAdjacentHTML, unescaped template interpolation into DOM), as a syntax inventory with controls?

## Method

JS syntax inventory (step1-style) over manifested view set; sink shapes fixed before inspection; no execution, no Track A staffing.

## Required evidence

- Sink-shape multiset with file/line provenance
- Shape definitions and independent transcription of expected cases

## Controls

- Positive: innerHTML assignment from non-literal
- Near miss: textContent assignment
- Negative: innerHTML with literal-only string

## Out of scope

- No runtime DOM behavior
- No taint through JS
- Track A remains unstaffed

## Notes

None.

## Result

Not yet evaluated.
