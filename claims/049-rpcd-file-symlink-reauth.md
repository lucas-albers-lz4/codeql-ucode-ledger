# Claim 049: rpcd file plugin symlink re-authorization

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category D
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-q5gr-86pq-vvwr (release-note cited; advisory not publicly retrievable at plan time)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Does pinned rpcd-mod-file source re-resolve and re-authorize the final path component for operations that dereference symlinks, and which operations do not?

## Method

Source oracle on rpcd d99f703 file.c: enumerate path-consuming operations, record realpath/lstat/stat usage and session.access call sites relative to dereference; CodeQL C if P1 supports.

## Required evidence

- Operation→resolution→authorization table with source lines
- Release-note text retained as anchor

## Controls

- Positive: operation re-authorizing resolved path (fixed shape)
- Near miss: operation checking textual path only
- Negative: operation with no path input

## Out of scope

- No live symlink exploit
- No claim about patched vs unpatched beyond pinned source observation

## Notes

Pin predates or postdates the fix — establish from source, not from the advisory date.

## Result

Not yet evaluated.
