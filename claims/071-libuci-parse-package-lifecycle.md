# Claim 071: libuci uci_parse_package object lifecycle

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category H
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- CVE-2020-28951 (UAF via malicious package names, uci_parse_package/uci_strdup)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned libuci file.c/util.c, what is the ownership/lifecycle of package-name strings through uci_parse_package, and is the historical UAF shape observable?

## Method

Source oracle / P1-gated CodeQL C on libuci (resolve pin at execution): transcribe alloc/free/use chains for package names.

## Required evidence

- Lifecycle chain multiset with source lines

## Controls

- Positive: use-after-free chain (if present)
- Near miss: strdup-owned name
- Negative: literal name path

## Out of scope

- No UAF execution
- No full libuci model

## Notes

None.

## Result

Not yet evaluated.
