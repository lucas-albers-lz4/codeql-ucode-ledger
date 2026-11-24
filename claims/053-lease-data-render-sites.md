# Claim 053: Lease/UCI-derived strings in status render paths

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category E
- Producer: source/syntax oracle (pinned luci + odhcpd; no CodeQL run)
- Producer commit: luci b2e0be4b46ec0fd43394c081fa7c50657af14011; odhcpd 5d7be43f8b9dec0eb47e245cfab81108bb131273; openwrt 4e9642517b48bae612ff10fb72fb9199e559500e (git show)
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-hhmc-92hw-535f / CVE-2026-62948 (odhcpd FQDN → lease file → LuCI, critical)
- GHSA-686p-p8p9-x6fh (DHCPv6 hostname)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned LuCI status views render lease-file or UCI-derived string fields, and can the data chain (odhcpd lease write → LuCI read → render) be transcribed from pinned sources?

## Method

Source inventory: odhcpd lease-file writer fields (pinned packages), LuCI lease readers, render sites consuming those fields; syntax/source level only.

## Required evidence

- Chain transcription with source lines at each hop
- Render-site multiset

## Controls

- Positive: hostname field rendered without observed encoding
- Near miss: field passed through an observed encoding helper
- Negative: numeric-only lease field

## Out of scope

- No XSS execution
- No odhcpd runtime behavior
- JS execution hold unchanged

## Notes

None.

## Result

Demonstrated — source/syntax inventory at luci `b2e0be4b…` + odhcpd
`5d7be43f…` (+ openwrt `4e964251…` via git show); no CodeQL database; JS UCI
hold and Track A state unchanged; no runtime/taint/exploitability verdict.

- 40 render sites across the 4 getDHCPLeases views + host-hint/UCI status
  includes; exact multiset byte-verified; completeness scan clean (56 declared
  chain-hop lines, 0 uncovered). Census: escaped_html 8, raw_html 17, numeric
  4, text_node 5, mixed_html 2, attribute 3, api_consumed 1.
- Chain transcribes end-to-end (chain.md): odhcpd option-12/FQDN intake →
  hostname_valid → statefiles.c write (this pin escapes non-LDH hostname bytes
  `\xNN`, prefixes invalid names "broken\x20", statefiles.c:503–581) →
  /tmp/odhcpd.leases → rpcd-mod-luci lease_next/getDHCPLeases (hostname
  verbatim :1987–1988) → 4 JS views → cbi_update_table → ui.Table.update →
  luci.js:1394 scalar innerHTML. Hostname cells %h-escaped; the one
  hostname-shaped unencoded scalar render is 60_wifi.js:307 (host-hint name).
  dnsmasq-format leasefile writer is outside the odhcpd escape — chain
  boundary, not adjudicated. Absent at pin: .uc/.ut lease renders, direct
  odhcpd-ubus→JS reads; connections.js getHostHints is a dead declaration.
- Controls 3/3 pass. Oracle rev2/rev3 fixed transcription errors caught by
  pinned-byte re-read; rev4 descriptive metadata only.
- Gaps: S3 boundary bounded (zonename/zone-title/SSID); adjacent 29_ports/
  10_system UCI renders logged as negative context; dnsmasq lease writer
  byte-shape outside the odhcpd pin.
- Evidence: `/root/workspace/work/security-40/053/` (oracle.{md,json},
  render_sites.json, chain.md, controls.json, provenance.json,
  run_pipeline.sh, odhcpd/). Orchestrator re-ran `run_pipeline.sh` (exit 0,
  40 sites, 3/3 controls); luci + odhcpd pins clean; spot-checked
  statefiles.c 503/581, luci.js 1394, 60_wifi.js 307.
