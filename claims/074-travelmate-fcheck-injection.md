# Claim 074: travelmate f_check script/script_args injection

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category G
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: source-oracle pin packages `07e0d16305d2b5903b37ad7913e33e18795f81a4` (travelmate; no CodeQL run)
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- travelmate 2.4.5-r3 f_check report (OpenCVE; script set to /bin/sh with attacker-controlled args)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned travelmate functions shell, how do script/script_args flow into command execution in f_check, and what validation is observed in-source?

## Method

Source oracle over pinned travelmate package (resolve pin at execution): transcribe config → script/script_args → exec chains.

## Required evidence

- Chain multiset with source lines
- Pin receipt

## Controls

- Positive: config-derived script_args into unquoted exec (advisory shape)
- Near miss: argv-pinned invocation
- Negative: literal-only command

## Out of scope

- No shell execution
- No travelmate runtime behavior

## Notes

None.

## Result

Demonstrated (source oracle; static source observation only — no runtime/exploit/vulnerability
verdict; no gate lifted). Evaluated 2026-11-24 (UTC) at packages feed pin
07e0d16305d2b5903b37ad7913e33e18795f81a4 (2026-11-11, "domoticz: update to 2026.4"),
travelmate 2.4.9-r6 (net/travelmate/Makefile:9-10). shared/packages working tree DIRTY
(~5356 deletions) and NEVER read; all citations from git show <pin>:<path> blobs,
sha256-recorded and re-extracted/re-verified at evaluation time (run_pipeline.sh R5).

Verdict: FIXED-IN-PIN for the reported arbitrary-script execution shape —
fail-no-eligible-instance, WITH census (104 exec/eval/validation sites, all covered).
The pinned f_check login-script chain (travelmate-functions.sh) is:
f_getval "script" (1082, via f_getval→uci_get 633/637) → non-empty gate (1083) →
readlink -f canonicalization (1084) → case allowlist /etc/travelmate/*.login (1085-1091,
reject arm logs and clears the path, fail-closed) → [ -f ] && [ -x ] (1093) →
f_getval "script_args" (1094) → ( set -f; exec "${login_script}" ${login_script_args} )
(1095-1098; exec 1097, path QUOTED, args UNQUOTED by design, globbing disabled, NO eval).
An arbitrary config script value such as /bin/sh is rejected by the canonicalized allowlist
before exec; the advisory's arbitrary-path shape is ABSENT at pin (0 eligible instances).

The advisory shape is PRESENT only in the declared historical control travelmate 2.4.5-r3
(commit 7f4dbf097c743fe6613340a532bdf3f5699b45d2, 2026-05-17): [ -x ] on the RAW path (953)
and direct exec (955), no allowlist/canonicalization/noglob — POS control executes
/bin/sh -c id in transcription. Fix commit d6e457a1a70a9010195edeafdc0b8eb6e3b0f7f1
("travelmate: update 2.4.6-2", 2026-06-17) is an ancestor of the pin and names these
mechanisms (motivation link only).

Controls (Python transcription over declared synthetic filesystem; no shell execution):
gate 3/3 — POS prefix /bin/sh+"-c id" → EXEC-ARBITRARY (shell -c command "id");
NEAR-MISS pinned /bin/sh+"-c id" → REJECTED-ALLOWLIST; NEG pinned
/etc/travelmate/generic-user-pass.login+"alice s3cret" → EXEC-ALLOWLISTED argv
["alice","s3cret"]. Info 9/9 (traversal, symlink-to-/bin/sh, directory, non-exec, wrong
extension, subdir admission, literal metachar args, prefix glob expansion, prefix splitting).

Residual in-source observation (not an exploit verdict): script_args content is unvalidated;
values reach the allowlisted script as split argv words (metacharacters literal, no eval,
no globbing). Argument semantics belong to the allowlisted script.

Two-pass agreement: 21/21 checks between manual chains.json (132 citations, all
anchors-on-line) and mechanical pass B (scripts/expected.py). CAVEAT: pass B is procedural
independence only (same operator); delegated independent pass unavailable (HTTP 401).

Evidence: /root/workspace/work/security-40/074/ — oracle.md, chains.json, controls.json,
provenance.json, oracle.json, scripts/{census,expected,oracle}.py, run_pipeline.sh (exit 0),
summary.md, pinned/ (11 blobs), work/ (revisions R1-R7, hashes, census, pass B, prefix
control, indirect uci.sh/jshn.sh excerpts). Indirect sources declared: shared/openwrt
ce245c873917cfbb412244dad80e395effed3167 (uci_get), shared/libubox
a396f38a8568a1d670c240465cd8d24fdfdf6463 (json_get_var); blob-only reads.
