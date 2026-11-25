# Claim 105: ASU keys artifacts by full SHA-256 request hash and pattern-validates package/profile fields

- Status: Demonstrated
- Program: [Security-extension Wave P](../planning/security-extension-waveP-20261125.md)
- Producer: `lucas-albers-lz4/codeql-ucode` — source-oracle lane; no analyzer grant assumed
- Producer commit: `9166af76cf6944e1b3ea5856a9176366a1f7a6ee`
- Consumer: `lucas-albers-lz4/codeql-openwrt`
- Consumer commit: `cc5f863021a099437beb8da66f53207712974a47`
- Advisory: GHSA-r3gq-96h6-3v7q / CVE-2024-54143 (critical) — build artifact poisoning via truncated SHA-256 hash and command injection
- Fix commit: `920c8a13d97b4d4095f0d939cf0aaae777e0f87e` (verified ancestor of pin)
- Source pin: `openwrt/asu` `de08b1dd64e4ed9ebc8413cd67e9459892708213`
- Evidence: `105/oracle.py`, `105/controls.py`, `105/run_pipeline.sh`, `105/blob-meta.json`

## Question

At the pinned ASU source, is the artifact store keyed by a full-length SHA-256 request hash, and are package/profile fields restricted to a safe character pattern before they reach the ImageBuilder `make` invocation?

## Source shape

- `asu/util.py:125-134` — `get_str_hash` returns the full `hashlib.sha256(...).hexdigest()` with no truncation.
- `asu/util.py:173-205` — `get_request_hash` builds the reproducible request hash via `get_str_hash`.
- `asu/build.py:144-146` — `bin_dir = settings.public_path / "store" / request_hash` keys the store by the full request hash.
- `asu/build_request.py:7` — `STRING_PATTERN = r"^[\w.,-]*$"`; `packages` (`:71-82`) and `profile` (`:60-69`) fields use `pattern=STRING_PATTERN`, excluding shell metacharacters and whitespace.
- `asu/util.py:320-325` — `run_cmd(container, command: list[str], ...)` calls `container.exec_run(command, demux=True, user="buildbot")`; no `shell=True`.
- `asu/build.py:296-305,322-329` — `make manifest` / `make image` are invoked as argument lists; `PACKAGES={' '.join(build_cmd_packages)}` is a single make variable, not a shell string.

## Controls

- P1: truncated 12-char hash + raw package string accepts `vim;touch /tmp/pwn` (collision-prone cache key and injection) — unsafe.
- NM1: full hash but raw package string still accepts the injection — unsafe (near-miss: hash fix alone is insufficient).
- N1: fixed pin full hash + `STRING_PATTERN` rejects the injection; benign `vim` accepted — safe.

## Out of scope

No runtime build, container execution, exploitability, or analyzer `path_found`. No gate lifted. `EXTRA_IMAGE_NAME=packages_hash[:12]` (`asu/build.py:327`) remains a 12-char image *filename* suffix only; it is not the artifact-store cache key.

## Result

Demonstrated (fixed-in-pin source shape). Orchestrator ran `run_pipeline.sh` (exit 0): oracle 9/9 checks PASS, controls 3/3. Blob sha256 and git-blob match verified for `asu/util.py`, `asu/build_request.py`, `asu/build.py`; fix `920c8a13d97b4d4095f0d939cf0aaae777e0f87e` verified ancestor of pin `de08b1dd64e4ed9ebc8413cd67e9459892708213`. Truncation census finds `[:12]` only at `EXTRA_IMAGE_NAME` (`build.py:327`) and a container-id log line (`build.py:56`); the request hash is never sliced. Source oracle only; no CodeQL extraction, runtime/exploit verdict, `path_found`, or gate lift.
