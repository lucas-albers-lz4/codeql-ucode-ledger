# Claim 073: banip log-monitor first-IP extraction

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category G
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: source-oracle pin packages `07e0d16305d2b5903b37ad7913e33e18795f81a4` (banip; no CodeQL run)
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-r6hx-4f83-vp8m (attacker-controlled log fields → wrong-target blocking)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned banip log-monitor source, how is the blocked IP extracted from log lines, and can attacker-controlled fields precede the extracted value in-source?

## Method

Source oracle over pinned banip shell/ucode parse logic: transcribe regex/awk/sed extraction and field ordering assumptions.

## Required evidence

- Extraction-chain transcription with source lines
- Field-order assumption statement

## Controls

- Positive: first-match extraction with attacker-controllable prefix (advisory shape)
- Near miss: anchored field extraction
- Negative: non-log input path

## Out of scope

- No blocking execution
- No firewall runtime claim

## Notes

None.

## Result

Demonstrated (source oracle; static source observation only — no runtime/exploit/vulnerability
verdict; no gate lifted). Evaluated 2026-11-24 (UTC) at packages feed pin
07e0d16305d2b5903b37ad7913e33e18795f81a4 (2026-11-11, "domoticz: update to 2026.4"),
banip 1.9.1-r5 (net/banip/Makefile:9-10). shared/packages working tree DIRTY (~5356 deletions)
and NEVER read; all citations from git show <pin>:<path> blobs, sha256-recorded and
re-extracted/re-verified at evaluation time (run_pipeline.sh R5).

Verdict: FIXED-IN-PIN for the unconditional first-IP advisory shape — fail-no-eligible-instance,
WITH census. The pinned log monitor (f_monitor, banip-functions.sh:2923) contains NO
unconditional positional-first IP selection. Default extraction is the LAST valid IP-shaped
token in the normalized log line; positional-first exists only as explicit per-logterm config
opt-in (`first:` prefix, banip-functions.sh:350-353), classified CONFIG_OPT_IN (chain C02).
The advisory's leftmost-match shape is reproduced only in the declared historical control
(banip 1.8.9-2, pre-fix commit 830e5276a3e3b0e08e167a25c8b31ef020cdd301, functions blob sha256
8300cc19d5588ed586d206cf14f25ffc92f91e5447db06a9246e4fbdfc94daf3).

Evidence (all under work/security-40/073/):
- Extraction chain transcribed from pinned bytes: logread -fe "${ban_logterm}" (3016) → awk
  valid_ip (3020-3025: v4 contains-dot only, NO octet range check; v6 hex/:::/double-::/colon-count
  gates reject HH:MM:SS timestamps) → pick_ip (3026-3044: leftmost ERE token scan
  `([0-9]{1,3}\.){3}[0-9]{1,3}|([A-Fa-f0-9]{0,4}:){2,7}[A-Fa-f0-9]{0,4}`, preceding-char
  word-boundary reject 3031/3039, colon trims 3034/3038; first-mode break 3041 vs last-mode
  overwrite 3040) → anchor_for/ban_logterm_map (3045-3052/3062, default last, all-last fast path
  3058) → normalization (3063-3065: ::ffff: v4 unwrap, first ]:port strip, <>[] removal) →
  excludes (3070 ^127./^0.; 3075 v6 loopback/unspecified) → cnt[ip]==threshold (3093, ban_logcount
  default 1 @59) → BLOCK/RESET emit (3094) → shell read loop (3099) → RDAP range guard (3103-3111)
  → allow/block/cache skip (3126/3134) → nft get element allowlist CIDR skip (3145) → nft add
  element blocklist (3159) → RDAP fetch (3213) → blocklist append (3276). Config: banip.conf:5-6
  default logterms both bare → list_cb ban_logterm arm (348-376) → eval join (365) → awk map (3019).
- Field-order statement: NO field-key guard (no SRC=/DST=/from parsing anywhere in awk 3019-3099);
  selection purely positional in both modes. For the shipped LuCI failed-login format
  `luci: failed login on <urlpath> for <user> from <ip>` (indirect source: luci dispatcher.uc:517-518,
  clean pin b2e0be4b46ec0fd43394c081fa7c50657af14011), an attacker IP-shaped urlpath token PRECEDES
  the trailing source IP: pre-fix leftmost extraction takes the attacker token (POS control →
  1.2.3.4); pinned last-mode takes the real trailing source (NEAR control → 10.0.0.5). Residual
  source shape: opt-in `first:` restores positional-first (INFO-FIRST → 1.2.3.4); last-mode is
  spoofable when the attacker token is the LAST valid token (glued real source rejected by the
  boundary guard, INFO-GLUED → 1.2.3.4). Source-shape observations only, not exploitability claims.
- chains.json: 11 chains (2 log-intake extraction-to-block, monitor gate, 2 RDAP sinks, blocklist
  append, log-emit, config eval, historical control) + dispositions; 108 citations machine-verified
  against pinned bytes (oracle R0). Census 97 sites / 5 files, coverage 97/97 (oracle R2).
  Eligible unconditional positional-first instances at pin: 0.
- Present-vs-fixed by ancestry: f514c565a3cade68a302de43da045fff4a952ed3 ("banip: release 1.8.10-1",
  2026-06-28; message names GHSA-r6hx-4f83-vp8m and the last-default/first-opt-in design) is an
  ancestor of the pin (merge-base verified in run_pipeline.sh).
- Controls 3/3 gate (controls.json, Python transcription of awk semantics; NO shell execution;
  gawk-ERE vs Python-re alternation-order agreement asserted per line, 0 divergences):
  POS = pre-fix 1.8.9-2 model on synthetic SPOOF line → 1.2.3.4 (advisory shape reproduced,
  historical only); NEAR = pinned-last on same line → 10.0.0.5; NEG = pinned-last no-IP line → None.
  Informational 5/5: INFO-FIRST, INFO-GLUED, INFO-V6 (2001:db8::1), INFO-MAPPED (::ffff:192.0.2.9 →
  192.0.2.9), INFO-PREFIX-NOIP. All control lines SYNTHETIC; format motivation from declared
  indirect source only.
- Predeclared oracle: oracle.md (rules R0-R5 declared before evaluation), oracle.json (results),
  provenance.json (8 pinned blobs + historical control + indirect luci pin, all sha256),
  work/revisions.md (R1-R4, incl. delegation fallback).

Gaps: pass B is an independent PROCEDURE executed in-session (scripts/expected.py, structural
re-derivation, 30/30 field agreements with pass A), not an independent model — delegated
second-pass subagent failed provider auth (HTTP 401 invalidated oauth token; logged R4).
No shell execution, no CodeQL database (shell not extracted by codeql-ucode/codeql-openwrt).
Indirect source shared/luci used ONLY for log-line format motivation and logterm UI help, not
banip source. valid_ip v4 accepts any dotted token (e.g. 999.999.999.999) — source-shape
observation only. No device pass; source observation only.
