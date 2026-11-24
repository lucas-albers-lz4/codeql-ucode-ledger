# Claim 065: Keep-alive body drain and parse-error desync

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category F
- Producer: source oracle (pinned uhttpd C census; no CodeQL run)
- Producer commit: uhttpd 93b05e0b65d91c23c5aa8fdde378df1f174ec71d
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-c2wg-hcff-hqrm (CL.0)
- GHSA-wgwp-64hh-f52p / CVE-2026-55613 (parse-error desync)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Where does pinned uhttpd decide connection reuse, and what body-drain / error-state handling precedes that decision in-source?

## Method

Source oracle / P1-gated CodeQL C: transcribe reuse decision sites and preceding consume/reset calls.

## Required evidence

- Decision-site multiset with drain observation
- Source lines

## Controls

- Positive: reuse path with no observed body drain (if present)
- Near miss: reuse after observed consume
- Negative: close-on-error path

## Out of scope

- No smuggling execution
- No timing/runtime claim

## Notes

None.

## Result

Demonstrated — source oracle at uhttpd `93b05e0b…` (clean); BOTH advisory
shapes FIXED-IN-SOURCE (fail-no-eligible-instance with census); no CodeQL
database; source-shape observation only, no runtime/exploit/vuln verdict.

- Reuse decided in the single uh_request_done (client.c:125-148); the ONLY
  CLIENT_STATE_INIT assignment tree-wide is :145, reached only after the
  unread-body guard (:139-140 `transfer_chunked || content_length > 0` →
  connection_close=true) and the decision (:142-143 `!keepalive || close` →
  uh_connection_close).
- Shape A (CL.0, GHSA-c2wg-hcff-hqrm): precondition exists — client.c:684-685
  `if(!d->data_send) return` leaves a declared body unconsumed for non-consuming
  handlers — but the :139-140 guard forces close before reuse (near-miss,
  neutralized).
- Shape B (parse-error desync, GHSA-wgwp-64hh-f52p / CVE-2026-55613): ubus POST
  parse error sets connection_close=true (ubus.c:1161) BEFORE return 0 (:1163);
  the unread suffix cannot be reused.
- Funnel: all 22 request_done call sites (14 direct + 8 ops->) resolve to the
  guarded decision via plugin.c:33; connection_close census 12 (client.c x10,
  ubus.c x2). uh_chunk_eof (utils.c:109-119) is RESPONSE-side, not a drain.
- 30 entries (0 eligible, 1 near_miss, 1 negative, 28 context); 4 chains. Fix
  ancestry 15346de (2021) / d6205aa (2026-08-03) / 7b1bec4 (2026-06-13) all
  ancestors of HEAD.
- Controls: POS-A / POS-B no_eligible_instance WITH census; NEAR pass (684-685);
  NEG pass (uh_chunk_eof). Second pass 30/30; funnel 22/22; census 12/12. Builder
  bug fixed pre-run (str.decode on already-text blob), logged; no oracle change.
- Evidence: `/root/workspace/work/security-40/065/` (oracle.{md,json},
  sites.json, controls.json, provenance.json, run_pipeline.sh, build_065.py,
  evidence/). Orchestrator re-ran `run_pipeline.sh` (exit 0); uhttpd pin clean;
  spot-checked client.c:139-145 + ubus.c:1161; ancestry 15346de/d6205aa confirmed.
