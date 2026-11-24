# Claim 035: ACL file-read globs spanning path separators

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category A
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-4h7q-j9hv-2536 (luci-app-uhttpd `/*` read exposes /etc/shadow)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned LuCI ACL `file` read grants contain patterns that match paths outside their apparent directory under rpcd fnmatch semantics (`FNM_NOESCAPE`, no `FNM_PATHNAME`, so `*` spans `/`)?

## Method

Source-derived inventory of every `read.file` pattern in ACL JSON at the pinned luci SHA (application slice manifested separately from the luci-ssl corpus profile), joined against an independent libc fnmatch witness per pattern with concrete cross-directory probe paths.

## Required evidence

- Full pattern multiset with package/path provenance
- fnmatch witness binary/source, compile command and probe-path expectations fixed before running
- Per-pattern match/non-match table for the probe paths

## Controls

- Positive: `/*` matches `/etc/shadow`
- Near miss: `/etc/config/*` matches `/etc/config/wireless` but not `/etc/shadow`
- Negative: literal `/etc/uhttpd.key` does not match `/etc/uhttpd.crt`

## Out of scope

- No claim that any grant is reachable by a live session
- No rpcd runtime execution
- No severity scoring

## Notes

fnmatch-witness-feasibility skill governs the witness; plan-time advisory says rpcd matches with FNM_NOESCAPE and without FNM_PATHNAME — verify against pinned rpcd source, not the advisory text.

## Result

Not yet evaluated.
