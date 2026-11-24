# Claim 055: uhttpd CGI error/URI reflection

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category E
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- CVE-2018-19630 (cgi_handle_request reflected XSS via URI)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned uhttpd source, where do error/response paths echo request URI or header data into HTML output, and is any encoding observed in-source?

## Method

Source oracle on uhttpd 93b05e0 cgi.c/uh_error paths; CodeQL C if P1 supports; record exact echo sites and any escaping calls.

## Required evidence

- Echo-site multiset with source lines
- Encoding observation per site

## Controls

- Positive: URI echoed into error body without observed encoding
- Near miss: echoed through an observed escape helper
- Negative: fixed literal error body

## Out of scope

- No reflected-XSS execution
- No HTTP parsing completeness

## Notes

None.

## Result

Not yet evaluated.
