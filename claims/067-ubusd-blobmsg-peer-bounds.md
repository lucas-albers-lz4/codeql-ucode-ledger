# Claim 067: ubusd peer blobmsg parsing bounds

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category F
- Producer: source oracle (pinned ubus C blob census; no CodeQL run)
- Producer commit: ubus 24864e7840b3a02a9ef76284a373f6b2f00b8a9b
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-cp32-65v4-cp73 / CVE-2025-62526 (ubusd heap buffer overflow)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned ubusd peer message intake, what length/type validation precedes blobmsg copy/allocation, and is the advisory shape observable in-source?

## Method

Source oracle / P1-gated CodeQL C on pinned ubus source (resolve ubusd package pin at execution): transcribe recv → validate → copy chains.

## Required evidence

- Chain multiset with source lines
- ubus pin resolution receipt

## Controls

- Positive: length-derived allocation without observed bound check (if present)
- Near miss: validated length
- Negative: fixed-size control message path

## Out of scope

- No heap overflow execution
- No libubox internals beyond pinned source

## Notes

ubus repo pin is not in the corpus lock; resolve and record it as a new package pin for this claim.

## Result

Demonstrated — source oracle at ubus `24864e78…` (2026-06-28; shared tree dirty,
pinned blobs only via git show); advisory shape FIXED-IN-PIN
(fail-no-eligible-instance WITH census); no CodeQL database; source-shape
observation only, no runtime/exploit/vuln verdict.

- Peer intake validation-before-copy: fixed 40-byte hdrbuf recvmsg (ubusd.h:61,
  ubusd_main.c:131/149) — no peer length reaches allocation; ubus_validate_hdr
  before body alloc (blob_raw_len < sizeof(blob_attr) reject ubusd_proto.c:149,
  hdr.len > UBUS_MAX_MSGLEN :152, type bound :529) then ubus_msg_new(NULL,len,
  false) (ubusd_main.c:157 → ubusd.c:47 calloc_a); body read bounded by
  pending_msg_len (ubusd_main.c:175/180/191); blob_parse_untrusted + typed policy
  (ubusd_proto.c:39/26-34) before every handler copy.
- Advisory site ubusd_alloc_event_pattern (ubusd_event.c:56): strlen :86 →
  zero-guard `if (!len) return UBUS_STATUS_PERMISSION_DENIED` :87-88 → wildcard
  strip :90-93 → LISTEN ACL check :96 → calloc :99 → strcpy :107. The
  empty-pattern underflow → undersized calloc → strcpy overflow shape is GUARDED
  (zero length rejected before alloc). Analogous zero-guards ubusd_proto.c:244
  (lookup), ubusd_acl.c:328.
- 50 census sites (pass A line-regex == pass B sink-first function-aware, 50/50);
  29 chains covering 34 recv/alloc/copy sinks; 16 local-only sites with documented
  dispositions (50/50 coverage); 169 citations machine-verified vs pinned bytes;
  oracle R5 re-extracted 9 cited blobs + control via git show, sha256 matched.
- Fix ancestry d31effb (event zero-guard) / 60e0404 (unconditional LISTEN ACL) /
  aa4a7ee (lookup/acl guards) / f92ffd2 (size_t) all ancestors of pin.
  UBUS_MAX_MSGLEN value out-of-pin (guard presence verified, value not).
- Controls 3/3 (identical classifier): POS real pre-fix blob d31effb^:ubusd_event.c
  (sha256 d05682b8…) → UNGUARDED + conditional ACL (historical only, never a pin
  chain); NEAR pinned event pattern → GUARDED + unconditional ACL; NEG fixed
  hdrbuf recvmsg → FIXED_SIZE. No fabricated chains.
- Gaps disclosed: pass B is an independent procedure in-session, not an
  independent model (delegation OAuth 401, R1); stale-memory citations rebuilt
  from bytes (R5: 43/111 misses fixed + 5 builder catches); libubox blobmsg
  internals out-of-pin; feed HEAD drift db20eff (2026-10-28) not evaluated.
  Summary prose had shifted event line numbers; gate-verified chains.json cites
  the correct :87/:96/:99/:107.
- Evidence: `/root/workspace/work/security-40/067/` (oracle.{md,json},
  chains.json, controls.json, provenance.json, run_pipeline.sh, scripts/,
  pinned/, work/). Orchestrator re-ran `run_pipeline.sh` (exit 0); pin reachable;
  shared/ubus dirty (83) never read; spot-checked ubusd_event.c:86/87/90/96/107 +
  ubusd_proto.c:149; ancestry d31effb/60e0404/aa4a7ee/f92ffd2 confirmed.
