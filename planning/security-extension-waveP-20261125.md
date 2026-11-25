# Security-extension Wave P — ASU artifact integrity (2026-11-25)

## Scope

One high-value unclaimed advisory surfaced by the openwrt-org sweep (`sweep-advisories.json`):

- 105 — GHSA-r3gq-96h6-3v7q / CVE-2024-54143 (critical), `openwrt/asu`: build artifact poisoning via truncated SHA-256 request hash + package-name command injection.

## Method

Pinned-source oracle only (Python service; no ucode/CodeQL extraction assumed). Pin `de08b1dd64e4ed9ebc8413cd67e9459892708213`; fix `920c8a13d97b4d4095f0d939cf0aaae777e0f87e` verified ancestor. Blob sha256 + git-blob match recorded in `105/blob-meta.json`. Controls P1/NM1/N1 emulate hash length and package-pattern acceptance.

## Gates

No gate lifted; no `path_found`; no runtime/container/exploit verdict. JS UCI hold, markup extractor gate, template-argument deferral, and application-ucode routing gate (codeql-ucode#154) are unaffected (ASU is Python, outside ucode routing).

## Status

105 Demonstrated (orchestrator pipeline exit 0, oracle 9/9, controls 3/3).
