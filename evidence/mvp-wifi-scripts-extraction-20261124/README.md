# MVP wifi-scripts source-staged route and extraction check

Status: **passed for the bounded source-staged route and extraction contract**.
The run selected only the Ucode variant on the assumption
`CONFIG_WIFI_SCRIPTS_UCODE=y`; it did not build or install the package.

## Pins and oracle

- OpenWrt source: clean `4e9642517b48bae612ff10fb72fb9199e559500e` in
  `work/stage6-openwrt`. All 17 Git blobs and source SHA-256 values were
  rechecked against the pinned commit and staged bytes.
- Input plan: `planning/mvp-wifi-scripts-next-slice.json`, SHA-256
  `f3fb3f2c53f7f905d3f8a4a612300d9a5ab2a6ef32874b15d2d3dcd93949c41e`.
- Corrected run oracle: [source-first-oracle.json](source-first-oracle.json), SHA-256
  `383027edf0d8da28ea94a5e9f40c9159dc9194940f5ba81322f0d3af3fdadd6d`.
- Producer/tool: CodeQL CLI 2.27.4; the reused extractor was built from the
  recorded producer source and binary digest in the receipt. The producer lock
  files and all eight pinned external QL dependency packs matched the successful
  prior run and were copied into the run-owned producer/cache paths.

The original plan expected 15 `.uc` extension routes and two shebang routes.
Pinned source inspection plus extractor precedence showed three `.uc` files
start with Ucode shebangs, and `has_ucode_shebang` runs before the `.uc`
extension rule. The corrected pre-run oracle therefore expects 12 extension
routes and five shebang routes. The original expectation and all intermediate
nonpassing attempts remain under ignored `work/mvp-wifi-scripts-extraction-20261124/`;
no prior mismatch is relabeled as a pass.

## Result

The fresh `run-e` direct route probe produced 17 decisions: 12
`ucode_extension` and five `ucode_shebang`, all `plain_route_selected`; exact
route identities matched the corrected oracle. The fresh CodeQL database
reported every selected staged identity once (17/17) and zero extraction-error
rows. All eight route, database and diagnostics commands exited 0.

Per-phase monotonic wall times and normalized argv are in the [run receipt](run-receipt.json);
raw command logs and database artifacts remain in ignored
`work/mvp-wifi-scripts-extraction-20261124/run-e/`. Peak RSS was not available: on
this host `/usr/bin/time -l` failed with a denied `sysctl kern.clockrate`
request, so the final run records no peak memory.
The committed receipt is a reviewed 16 KiB reduction of the raw run's
683-file hash map: it retains the source oracle, route, diagnostics and
command hashes and a SHA-256 commitment to the full sorted raw hash map.
The full map and its host-specific trap paths remain only under ignored
`work/`; another machine cannot follow those paths.

## Boundaries

The `files-ucode/*` selection follows the `CONFIG_WIFI_SCRIPTS_UCODE=y`
condition in `package/network/config/wifi-scripts/Makefile`. The shell
alternative at `files/lib/netifd/wireless/mac80211.sh` is recorded as excluded;
it maps to the same proposed installed path as the selected Ucode shebang
variant. No configured package build, IPK or rootfs was produced, so installed
bytes remain unverified. The results establish routing and extraction only; no
query, security, runtime or safety claim was tested.
