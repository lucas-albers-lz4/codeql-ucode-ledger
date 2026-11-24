# OpenWrt core and packages-feed Ucode source candidates

Status: pinned source-only census, 2026-11-24. The exact
[candidate manifest](mvp-openwrt-packages-candidates-v0.1.json) has SHA-256
`da2f6d28bad7cec638dfc41f0036ac153c91cc4afe57eb993d70bcd2ec74a098`.
All paths, Git blobs and SHA-256 values came from clean isolated checkouts at
OpenWrt `4e9642517b48bae612ff10fb72fb9199e559500e` and packages feed
`07e0d16305d2b5903b37ad7913e33e18795f81a4`.

The explicit candidate policy selects tracked `.uc`, `.ucode` and `.ut`
files, tracked files with a first-line Ucode shebang, and extensionless files
under installed `usr/share/ucode`, `usr/share/rpcd/ucode` or `usr/lib/ucode`
path roots. It yields 46 OpenWrt core candidates, including the 11 already
in [bounded corpus v0.1](mvp-bounded-corpus-v0.1.md), and 37 packages-feed
candidates, including three adblock-fast test mocks. The additional source
queue is 35 OpenWrt candidates and 37 packages-feed candidates. This policy
can miss other unconventional Ucode source layouts; it is not an installed
or extracted denominator.

For a first expansion, use the [17-file wifi-scripts oracle](mvp-wifi-scripts-next-slice.md)
under its explicit `CONFIG_WIFI_SCRIPTS_UCODE=y` condition. Package-feed
candidates span several owners and need per-package install-rule inspection
before adding them to a versioned scan selection. Keep the three test mocks
separate from product files. Build and installed-byte checks, exact CodeQL
routes, diagnostics, query results, Linux cost and alert triage remain open.
