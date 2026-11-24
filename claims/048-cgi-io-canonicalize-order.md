# Claim 048: cgi-io canonicalize_path vs ACL ordering

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category D
- Producer: source oracle (pinned cgi-io C transcription + glibc canonicalize harness; no CodeQL run)
- Producer commit: cgi-io 31cb3c89f02d918d7f17bf62a80c852fc38a1ca1
- Consumer: `lucas-albers-lz4/codeql-openwrt` (policy/cgi_download.py)
- Consumer commit: codeql-openwrt cc5f863021a099437beb8da66f53207712974a47
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

Demonstrated — at cgi-io `31cb3c89…` (disposable clone, clean) and
codeql-openwrt `cc5f8630…` (consumer, clean). Bounded source-order
observation; no CodeQL database (transcription + consumer read fully answer
the question).

- Per-endpoint order (canon = `canonicalize_path` util.c:199):
  - **download**: canon main.c:549 → file-read ACL:551 → stat:554 /
    open:568 / sendfile:589. ACL string == open target == canon; raw path
    never reused. Fix rationale in-source 542–548 (rpcd fnmatch lacks
    FNM_PATHNAME → `../` must collapse before the ACL).
  - **upload**: canon filename at parse:372 → file-write ACL:348 → filecopy
    unlink:256 / linkat:262 / open:270 / chmod:293. Upload-scope ACL:403
    position depends on multipart part order.
  - **backup**: canonicalize NEVER (no request path); backup ACL:642 → fixed
    execl `/sbin/sysupgrade`:665.
  - **exec**: canon leading token:790 → ACL#1(canon+tail):810 →
    lookup_executable PATH re-resolution:818 (stat precedes ACL#2) →
    conditional ACL#2(exe):826 → execv(exe):869.
- Consumer answer (second half): **YES** — `policy/cgi_download.py` (same
  cgi-io pin) already decides the advisory shape (GHSA-jw5r-xhf5-2xcq /
  CVE-2026-62947): order matches source, ASSUMPTION_CANON (80–83),
  dotdot-deny fixture → `path_denied` (not `glob_prefix_bypass`), gcc C
  double canonicalize-then-ACL with FNM_NOESCAPE / no FNM_PATHNAME, 6/6
  fixture cases. Claim stop condition applies — recorded, not re-decided.
- Controls: positive PASS (`../dev/mtdblock0/../../../etc/passwd` →
  `/etc/passwd` before file ACL; download/exec/upload); near-miss PASS
  (eligible instance only in cgi-exec via PATH resolution; download/upload/
  backup fail-no-eligible-instance per endpoint with census, no synthetic);
  negative PASS (`/dev/mtdblock0` identity). Battery **24/24** three-way
  agreement (pinned C / hand transcription / verbatim consumer Python).
- Residuals open (recorded, not decided; follow-up candidates): cgi-exec
  canonicalize/ACL/PATH order (cgi_exec.py models session gate only);
  cgi-upload multipart part-order dependence; symlink/cwd-relative
  resolution (canonicalize_path is textual; leading `../` without a
  preceding slash survives; UNKNOWN_FS in consumers).
- No runtime/traversal/authorization/vulnerability verdict; no gate lifted.
- Evidence: `/root/workspace/work/security-40/048/` (oracle.{md,json},
  endpoint_order.json, consumer_comparison.{md,json}, controls.json,
  harness_results.json, provenance.json, run_pipeline.sh, harness/).
  Orchestrator re-ran `run_pipeline.sh` (exit 0); spot-checked main.c
  549/551/568/790/810/818/826/869 and util.c:199.
