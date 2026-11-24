# Claim 049: rpcd file plugin symlink re-authorization

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category D
- Producer: source oracle (pinned rpcd file.c census; no CodeQL run)
- Producer commit: rpcd d99f703e4035d03fbcfbada3cb697db346c2b984
- Consumer: none
- Consumer commit: none
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

Demonstrated — at rpcd `d99f703e…` (post-fix; symlink fix `e37ed9d` is an
ancestor, orchestrator-verified). Source-oracle census of file.c (sha256
`03aae01e…`); no CodeQL database; no runtime/authorization claim.

- 8 registered file methods. Five (read/write/list/stat/md5) re-resolve and
  re-authorize: `rpc_check_path` → `rpc_check_symlink_access` runs `realpath`
  (file.c:269); on change `rpc_file_access(resolved)` (274) with `*path`
  replacement (289) before stat/open/opendir/md5sum consume it; new-file
  targets re-authorize the rebuilt path (349/355); dangling symlinks rejected
  (300, EACCES).
- Three (lstat/remove/exec) check the textual path only (no realpath in their
  chains): lstat/remove pair the textual check with no-follow consumers
  (lstat/unlink/rmdir); exec dereferences in lookup before ACL (859/882 <
  1065) and again at execv after the textual ACL (1172).
- Residual source-order facts: list's per-entry target stat (709) follows
  entry symlinks without per-entry re-authorization; `sid==NULL` skips ACL
  (183–184); ACL fnmatch lacks FNM_PATHNAME (session.c:147). rename/copy
  absent at pin.
- Controls: positive (read) PASS, near-miss (exec) PASS, negative
  fail-no-eligible-instance (all 8 methods path-consuming; census retained).
  compare all_match true.
- Evidence: `/root/workspace/work/security-40/049/` (oracle.{md,json},
  operations.json, compare.json, controls.json, provenance.json,
  run_pipeline.sh, anchor.md, inventory.py). Orchestrator re-ran
  `run_pipeline.sh` (exit 0); pin clean; e37ed9d ancestry confirmed;
  spot-checked file.c 183/184/269/274/289/300/709.
