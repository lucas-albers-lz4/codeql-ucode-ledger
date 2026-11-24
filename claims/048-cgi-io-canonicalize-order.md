# Claim 048: cgi-io canonicalize_path vs ACL ordering

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category D
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-jw5r-xhf5-2xcq / CVE-2026-62947 (cgi-download ACL bypass / arbitrary root file read)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned cgi-io source, what is the exact order of path canonicalization, ACL check and file operation per endpoint, and does the consumer cgi-download oracle already decide the advisory shape?

## Method

Source oracle on cgi-io 31cb3c8 (C): transcribe canonicalize_path + session.access + open order; compare to existing policy/cgi_download.py oracle; CodeQL C only if P1 supports it and a distinct decision remains.

## Required evidence

- Order transcription with source lines
- Delta statement vs existing oracle
- If run: C extraction receipt and query identity

## Controls

- Positive: `../` collapsing before file ACL (documented behavior)
- Near miss: path that canonicalizes differently than the ACL-checked string
- Negative: absolute in-scope path

## Out of scope

- No live cgi-io execution
- No HTTP framing model (decoded inputs are preconditions per existing oracle)

## Notes

If the existing oracle already decides the exact shape, record the stop and narrow to the residual distinct decision (e.g. symlink component).

## Result

Not yet evaluated.
