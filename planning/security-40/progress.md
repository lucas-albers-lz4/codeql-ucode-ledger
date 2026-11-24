# Security-40 progress

Resume point for the [Security-40 program](../security-40-20261124.md).
Update after every claim transition; newest entries first.

## State

- Program opened: 2026-11-24
- Claims created: 035–074 (40), all Proposed
- Active wave: 0 (probes) → 1 (category A)
- Last finished claim: none
- Next eligible: P1/P2 probes; 035–040 after shared pinned checkout exists

## Pins (plan-time observations; re-resolve at execution)

- luci openwrt-25.12: b2e0be4b46ec0fd43394c081fa7c50657af14011
- openwrt openwrt-25.12: 4e9642517b48bae612ff10fb72fb9199e559500e
- packages openwrt-25.12: 07e0d16305d2b5903b37ad7913e33e18795f81a4
- rpcd PKG_SOURCE_VERSION: d99f703e4035d03fbcfbada3cb697db346c2b984
- uhttpd PKG_SOURCE_VERSION: 93b05e0b65d91c23c5aa8fdde378df1f174ec71d
- cgi-io PKG_SOURCE_VERSION: 31cb3c89f02d918d7f17bf62a80c852fc38a1ca1
- CodeQL CLI: 2.27.4 (gh extension)

## Log

### 2026-11-24 — program opened

- Advisory catalog captured: 41 published advisories + release-note security
  sections (v25.12.6, v24.10.8, v25.12.5, v24.10.4) + historical layer
  (CVE-2018-19630, CVE-2019-12272, CVE-2019-19945, CVE-2019-25015,
  CVE-2020-7248, CVE-2020-7982, CVE-2020-28951). Raw catalog kept in
  `work/security-40/` outside the repo.
- Plan and 40 claim files written; all Proposed.
- User direction: local CodeQL only (no CI); all lanes on the active session
  model (alibaba qwen4-max-preview), thinking level per lane.