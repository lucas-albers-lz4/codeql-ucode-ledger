# Claim 063: Content-Length signedness and chunk-size state

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category F
- Producer: source oracle (pinned uhttpd C census; no CodeQL run)
- Producer commit: uhttpd 93b05e0b65d91c23c5aa8fdde378df1f174ec71d
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- CVE-2019-19945 (negative content length → OOB)
- GHSA-p55c-rmhc-qfm5 / CVE-2026-55612 (invalid chunk-length state reset)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

What integer types and parse-state transitions govern Content-Length and chunk-size handling in pinned uhttpd, and are the historical signedness/reset shapes present or fixed in-source?

## Method

Source oracle / P1-gated CodeQL C: record strtol/strtoul usage, assignment types, and chunk parser reset paths with source lines.

## Required evidence

- Type/transition table
- Historical-shape presence statement per site

## Controls

- Positive: signed assignment of parsed length (if present)
- Near miss: unsigned parse with overflow check
- Negative: unrelated integer parse

## Out of scope

- No OOB execution
- No full parser model

## Notes

None.

## Result

Demonstrated — source oracle at uhttpd `93b05e0b…` (clean); BOTH advisory
shapes FIXED-IN-SOURCE (fail-no-eligible-instance with census); no CodeQL
database; source-shape observation only, no runtime/exploit/vuln verdict.

- Shape A (negative CL, CVE-2019-19945): content_length is signed int
  (uhttpd.h:166) but parse guards before assignment — strtol (client.c:607),
  guard `(err && *err) || errno || length < 0 || length > INT_MAX` (:608) →
  400+return BEFORE the bounded cast `(int)length` (:612). No unguarded negative
  path. CL mutation multiset {612,695,747,773,786}.
- Shape B (invalid-chunk reset without close, GHSA-p55c-rmhc-qfm5 /
  CVE-2026-55612): reset exists (:773 CL=0, :774 CHUNKED_OFF) but forces
  connection_close=true (:779); all error OFF-resets close (726→727, 748→749,
  774→779); the only close-less reset :713 is normal post-drain trailer
  completion. Chunk size = strict manual hex parse with INT_MAX overflow guards
  (parse_chunksize 422-529), -1 sentinel.
- 30 entries (0 eligible, 7 near_miss, 2 negative, 21 context); 3 chains; parse
  census tree-wide 10 (1 strtol client.c:607, 9 atoi config; no strtoul/sscanf).
  Fix ancestry 2c869c0 / 9404e6c / b78f518 / 893fed8 all ancestors of HEAD.
- Controls: POS-A / POS-B no_eligible_instance WITH census; NEAR pass (:612 cast
  bounded by :608); NEG pass (main.c:463 atoi config). Second pass 30/30 agree.
  No oracle revisions.
- Evidence: `/root/workspace/work/security-40/063/` (oracle.{md,json},
  sites.json, controls.json, provenance.json, run_pipeline.sh, build_063.py,
  evidence/). Orchestrator re-ran `run_pipeline.sh` (exit 0); uhttpd pin clean;
  spot-checked client.c:607/608/612/773/774/779; ancestry 2c869c0 confirmed.
