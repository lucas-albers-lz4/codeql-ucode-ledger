# Claim 059: Package shell eval/sh -c of config values

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category C
- Producer: source oracle (pinned packages-feed shell census; no CodeQL run)
- Producer commit: packages 07e0d16305d2b5903b37ad7913e33e18795f81a4
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-hfpc-hw28-69pj (ddns dynamic_dns_lucihelper.sh eval)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned package shell scripts pass UCI/config-derived values to `eval`, `sh -c`, or unquoted expansion in command position, and what is the value chain in-source?

## Method

Source oracle over pinned packages tree (shell is not CodeQL-extracted by either repo — method stated honestly); transcribe config_get → command chains for a manifested script set.

## Required evidence

- Chain multiset with script/line provenance
- Independent expected-case transcription

## Controls

- Positive: config_get value into eval (advisory shape)
- Near miss: value quoted and passed as single argv word
- Negative: literal-only eval

## Out of scope

- No shell runtime execution
- No claim of full packages-tree coverage

## Notes

None.

## Result

Demonstrated — source oracle at packages `07e0d163…` (pinned blobs only;
working tree dirty, never read); shell not CodeQL-extracted; no database /
shell execution / runtime / exploitability verdict; bounded declared manifest
(not whole-feed completeness).

- 85 transcribed chains → 34 eligible (16 eligible_direct, 18 eligible_indirect),
  33 near_miss, 18 negative. Eligible source classes: uci-config_get 16,
  file-content 6, program-output 6, uci-get 1, uci-callbacks 1, shell-defaults
  2, netifd-json 2.
- Census: 4918-path pinned tree; 1618-path shell universe (5 non-UTF-8 skipped);
  179 census rows (43 sink+source, 44 source+unquoted-command, 92 sink-only);
  65-script manifest (A=27 in-file source+sink, B=4 ddns anchor/hops, C=19
  command-position, D=15 libraries/handlers).
- Anchor cross-check (GHSA-hfpc-hw28-69pj): dynamic_dns_lucihelper.sh has NO
  in-file eval at pin; it sources dynamic_dns_functions.sh; the eval machinery
  is fed by updater.sh:145 load_all_config_options — eval $__RUNPROG
  (:778/:1055), eval "$ip_script" (:893), eval "...$bind_network" (:639/:687),
  eval "$1=$(( $2 * 86400 ))" (:311-314), update_aliyun_com.sh:84 eval
  "$program".
- Controls 3/3 (POS ddns functions.sh:893; NEAR ser2net.init:21; NEG
  ModemManager-monitor:142 literal sh -c). Independent second pass 34/34;
  caught + fixed one citation error (snort-mgr ubus/ACTION evals :287/:429,
  not :253/:262 from a misnumbered read). 65/65 cited blobs sha256-verified.
- Limits: bounded manifest; indirect sources (netifd-json, shell-defaults)
  external to the feed, declared not asserted; ddns update_*.sh represented by
  update_aliyun_com.sh (remainder share the eval shape via census); test/mock
  scripts excluded.
- Evidence: `/root/workspace/work/security-40/059/` (oracle.{md,json},
  chains.json, census.json, controls.json, provenance.json, run_pipeline.sh,
  build_059.py, evidence/{tree.txt,blob_meta.json,blobs/**,ctx/**}).
  Orchestrator re-ran `run_pipeline.sh` (exit 0, VERDICT PASS); spot-checked
  dynamic_dns_functions.sh:893 eval.
