# Claim 060: Newline-bearing UCI values into line-based formats

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category C
- Producer: source oracle (pinned packages-feed shell census; no CodeQL run)
- Producer commit: packages 07e0d16305d2b5903b37ad7913e33e18795f81a4
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-w6q2-vr4f-49x3 (ser2net UCI newline → YAML gensio stdio, critical)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned package init/config scripts render UCI values into line-based or structured config files (ser2net YAML, cron, hosts, dnsmasq conf) without observed newline rejection?

## Method

Source oracle over manifested init scripts: trace uci get → file write chains; record format type and any observed sanitization; cross-check ser2net advisory shape at pinned packages SHA.

## Required evidence

- Chain multiset with format classification
- Sanitization observation per chain

## Controls

- Positive: multi-line-capable value written into line-based config
- Near miss: value passed through observed newline strip
- Negative: numeric-only option

## Out of scope

- No downstream daemon parsing claim
- No runtime injection demonstration

## Notes

None.

## Result

Demonstrated — source oracle at packages `07e0d163…` (pinned blobs only;
working tree dirty, never read); shell not CodeQL-extracted; no database /
runtime / exploitability verdict; bounded declared manifest.

- 19 transcribed chains → 17 eligible (14 direct, 3 indirect), 1 near_miss,
  1 negative. Eligible format counts: YAML 7, line-based-conf 6, dnsmasq-conf
  1, cron 1, hosts/dnsmasq 1, hosts/dnsmasq/nft 1. Source classes:
  uci-config_get 11, uci-get 1, uci-load-validate 2, program-output 1,
  file-content 2.
- Census: 107 write+source scripts over the 1618-path shell universe;
  14-writer manifest (bounded, declared).
- Anchor cross-check (GHSA-w6q2-vr4f-49x3): ser2net.init renders UCI into
  /tmp/ser2net.yaml gensio config (echo :224/:231-234). Only the options list
  (custom_options :189) is filtered by list_cb_append `tr -cd ' -~'` (:19,
  rejects newline); the value: (:54/:63/:77), accepter host (:95), led device
  (:113), gensio connector serialdev,$device (:195), led *$val (:202) paths
  render UCI values WITHOUT newline rejection — advisory source-shape present
  on the device/value paths.
- Controls 3/3 (POS ser2net.init:63; NEAR ser2net.init:19/:189; NEG
  acme.init:150 literal cron). Independent second pass 17/17. 14/14 cited
  blobs sha256-verified.
- Limits: bounded manifest; indirect sources (adblock/banip downloaded-list
  content, vpnc-script VPN-env) declared not asserted; unbound.sh/tcpproxy/
  radsecproxy classified from ctx dumps (representative directive writes).
- Evidence: `/root/workspace/work/security-40/060/` (oracle.{md,json},
  chains.json, census.json, controls.json, provenance.json, run_pipeline.sh,
  build_060.py). Orchestrator re-ran `run_pipeline.sh` (exit 0, VERDICT PASS);
  spot-checked ser2net.init:19/54/63/189.
