# Packages-feed Ucode candidates outside bounded corpus v0.4

Status: read-only install-rule inventory at clean packages-feed
`07e0d16305d2b5903b37ad7913e33e18795f81a4`, 2026-11-24. The
[candidate manifest](mvp-openwrt-packages-candidates-v0.1.json) lists 37
packages-feed paths; 12 base exporter files are selected in
[corpus v0.4](mvp-bounded-corpus-v0.4.md). The remaining 25 paths comprise
22 product candidates and three adblock-fast test mocks. Recipe projections
below do not prove actual package selection or installed bytes.

| Package and source paths | Proposed installed mapping and condition | Recipe |
|---|---|---|
| `prometheus-node-exporter-ucode/files/extra/{dnsmasq,ltq-dsl,netstat,openwrt,snmp6,uci_dhcp_host,wifi,wireguard}.uc` (8) | Each separate collector package copies its file to `usr/share/ucode/node-exporter/lib/<name>.uc`. All depend on the base package; dnsmasq and ltq-dsl have `@` conditions, wifi and wireguard have additional module dependencies. Selecting the base package alone does not select all eight. | `utils/prometheus-node-exporter-ucode/Makefile:52-74` |
| `net/adblock-fast/files/lib/adblock-fast/{adblock-fast,cli}.uc` (2) | Both install under `lib/adblock-fast/`. `adblock-fast.uc` then has its `version:` line rewritten using package version/release; `cli.uc` has no observed rewrite. | `net/adblock-fast/Makefile:51-57` |
| `net/snort3/files/{main,nftables,snort}.uc` (3) | `main.uc` installs at `usr/share/snort/main.uc`; the other two install at `usr/share/snort/templates/`. Recipe shows copy operations, with package/build selection still conditional. | `net/snort3/Makefile:80-98` |
| `utils/librespeed-common/files/{librespeed-aggregate,librespeed.uc}` (2) | The extensionless Ucode-shebang `librespeed-aggregate` installs at `usr/libexec/librespeed-aggregate` and is rewritten by a version substitution. `librespeed.uc` copies to `usr/share/rpcd/ucode/librespeed.uc` without that substitution. | `utils/librespeed-common/Makefile:63-75` |
| `utils/uvol/files/{blockdev_common,uci,lvm,ubi}.uc` and `files/uvol` (5) | Four `.uc` modules copy to `usr/lib/uvol/` or `usr/lib/uvol/backends/`; the Ucode-shebang `uvol` installs at `usr/sbin/uvol`. These belong to the `uvol` package; separate `autopart` has no selected Ucode file. | `utils/uvol/Makefile:69-81` |
| `net/mwan3/files/usr/share/rpcd/ucode/mwan3` (1) | Extensionless rpcd file copies to `usr/share/rpcd/ucode/mwan3`. It has no Ucode shebang; the installed rpcd path is its extractor route. | `net/mwan3/Makefile:95-97` |
| `net/uneighbord/files/usr/sbin/uneighbord` (1) | Ucode-shebang executable copies to `usr/sbin/uneighbord`. | `net/uneighbord/Makefile:32-39` |

The three tracked `net/adblock-fast/tests/lib/mocklib.uc` and
`net/adblock-fast/tests/lib/mocklib/{ubus,uci}.uc` candidates are
test fixtures with no product install mapping in the inspected package
recipe. They remain excluded from a product denominator. `ucode.nanorc` is
syntax-highlighting configuration, not Ucode source selected by this
candidate policy.

For the next source-staged expansion, the eight optional exporter files have
one clear package family and direct install paths, but require a declared
set of enabled collector subpackages. A cross-package alternative is the
direct-copy uvol, snort3, mwan3 and uneighbord files. Keep rewritten
adblock-fast and librespeed executable bytes in a separate build/IPK
comparison; source hashes cannot stand in for their installed hashes.
