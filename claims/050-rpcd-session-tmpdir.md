# Claim 050: Session-token-derived temporary UCI paths

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category D
- Producer: source oracle (pinned rpcd uci.c census; no CodeQL run)
- Producer commit: rpcd d99f703e4035d03fbcfbada3cb697db346c2b984
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-r2w2-q7cw-cfp2 (release-note cited; advisory not publicly retrievable at plan time)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Where does pinned rpcd uci-plugin source construct temporary paths from session tokens, and what visibility/permissions do those paths have in-source?

## Method

Source oracle on rpcd d99f703 uci.c: trace token → directory-name construction, mkstemp/mkdir mode arguments, and cleanup; record exact identities.

## Required evidence

- Construction-chain transcription with source lines
- Mode/permission constants recorded

## Controls

- Positive: token-named directory fixture shape
- Near miss: random-suffix temp name
- Negative: fixed non-token path

## Out of scope

- No cross-session read demonstration
- No runtime permission verdict

## Notes

None.

## Result

Demonstrated — at rpcd `d99f703e…`, which IS the fix commit "session: stop
naming runtime files after the session id" (GHSA-r2w2-q7cw-cfp2; subject
orchestrator-confirmed). Source-oracle census of uci.c (sha256 `bc3ca56c…`);
no CodeQL database; no runtime claim.

- 17 temp/path sites: 5 session-derived, 9 fixed-literal, 3 composed-from-args,
  **ZERO token-named**. Session-derived sites format RPC_UCI_SAVEDIR_PREFIX
  "/var/run/rpcd/uci-%s" (uci.h:33–34) with `rpc_session_dirname`/`ses->dirname`
  (uci.c:311/1537/1627/1631/1767) — a separate random 32-hex from /dev/urandom
  (session.c:334, 149–175), independent of the session id (session.c:360);
  thaw restores the name from the frozen file name (session.c:1503/1337), not
  the token.
- Modes in-source: 3 uci.c mkdir 0700 (1538/1624/1625); /var/run/rpcd 0700
  (main.c:99); umask(0077) (main.c:101); freeze O_EXCL 0600 (session.c:1246);
  copy fopen "wb+" → 0600 under that umask. The uci-<dirname> delta dir is not
  mkdir'd by rpcd at session creation; libuci context out-of-pin, labeled
  (delta.c:486–491 mkdir 0700/confdir-mode, util.c:191 delta files 0600).
- Cleanup: per-session destroy purge (uci.c:1763–1769/1828; session.c:293–294),
  startup purge (1775–1787, main.c:125), snapshot purges
  (1613–1614/1698–1699/1559–1560), freeze unlink (session.c:1507/1257). Absent,
  recorded honestly: exit-time uci-* purge; /tmp/.uci cleanup.
- Controls: positive (token-named) fail-no-eligible-instance with census
  (0 token-named sites; pin is the fix), near-miss (random-suffix) PASS,
  negative (fixed path) PASS. compare all_match true.
- Evidence: `/root/workspace/work/security-40/050/` (oracle.{md,json},
  tmppaths.json, compare.json, controls.json, provenance.json,
  run_pipeline.sh, anchor.md, inventory.py). Orchestrator re-ran
  `run_pipeline.sh` (exit 0); pin clean; fix subject confirmed; spot-checked
  uci.c 311/1537, session.c 334/360, main.c 99/101.
