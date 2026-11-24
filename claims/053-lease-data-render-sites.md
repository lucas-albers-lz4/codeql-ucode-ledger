# Claim 053: Lease/UCI-derived strings in status render paths

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category E
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-hhmc-92hw-535f / CVE-2026-62948 (odhcpd FQDN → lease file → LuCI, critical)
- GHSA-686p-p8p9-x6fh (DHCPv6 hostname)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned LuCI status views render lease-file or UCI-derived string fields, and can the data chain (odhcpd lease write → LuCI read → render) be transcribed from pinned sources?

## Method

Source inventory: odhcpd lease-file writer fields (pinned packages), LuCI lease readers, render sites consuming those fields; syntax/source level only.

## Required evidence

- Chain transcription with source lines at each hop
- Render-site multiset

## Controls

- Positive: hostname field rendered without observed encoding
- Near miss: field passed through an observed encoding helper
- Negative: numeric-only lease field

## Out of scope

- No XSS execution
- No odhcpd runtime behavior
- JS execution hold unchanged

## Notes

None.

## Result

Not yet evaluated.
