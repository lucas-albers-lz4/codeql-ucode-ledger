# Claim 062: Transfer-Encoding matching case sensitivity

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category F
- Producer: source oracle (pinned uhttpd C census; no CodeQL run)
- Producer commit: uhttpd 93b05e0b65d91c23c5aa8fdde378df1f174ec71d
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-mcfg-c4r7-pjpf / CVE-2026-55614 (smuggling via case-sensitive TE matching)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned uhttpd header parsing, how is Transfer-Encoding matched (strcmp/strcasecmp/other), and does the observed comparison decide the advisory shape?

## Method

P1-gated CodeQL C or source oracle on uhttpd 93b05e0: transcribe header comparison call sites with exact functions and arguments.

## Required evidence

- Comparison-site multiset with source lines
- If CodeQL: extraction receipt, query identity, predeclared oracle

## Controls

- Positive: case-sensitive comparison of TE header (advisory shape if present)
- Near miss: case-insensitive comparison
- Negative: unrelated header comparison

## Out of scope

- No smuggling demonstration
- No HTTP state-machine completeness

## Notes

Establish fixed-vs-vulnerable from pinned source, not advisory dates.

## Result

Demonstrated — source oracle at uhttpd `93b05e0b…` (clean); advisory shape
FIXED-IN-SOURCE (fail-no-eligible-instance with census); no CodeQL database;
source-shape observation only, no runtime/exploitability/vulnerability verdict.

- TE matched case-insensitively: header NAME via strcasecmp on lowercased names
  (client.c:272 `strcasecmp(blobmsg_name(cur), "Transfer-Encoding")`); the
  framing decision uses strcasecmp and rejects unknown codings with 501. No
  case-sensitive TE value comparison anywhere in the pinned tree → the
  GHSA-mcfg-c4r7-pjpf / CVE-2026-55614 shape is not present.
- 20 entries (0 eligible, 3 near_miss, 4 negative, 13 context); 2 chains (TE
  value decision; name-lowercasing precondition); census 24 comparison sites in
  client.c/proc.c header parsing.
- Controls: POS no_eligible_instance WITH census; NEAR pass (client.c:618);
  NEG pass (find_idx 180). Second pass 20/20 agree. No oracle revisions.
- Evidence: `/root/workspace/work/security-40/062/` (oracle.{md,json},
  sites.json, controls.json, provenance.json, run_pipeline.sh, build_062.py,
  evidence/). Orchestrator re-ran `run_pipeline.sh` (exit 0); uhttpd pin clean;
  spot-checked client.c:272 strcasecmp.
