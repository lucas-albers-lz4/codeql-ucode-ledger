# 091 — luci-app-lxc ACL consistency and container-name path validation

- Status: Proposed
- Question: At the pinned LuCI corpus, do all LXC backend function routes require the `luci-app-lxc` ACL, and do configuration get/set reject container names that escape the configured `lxcpath`, closing the advisory shape in GHSA-jf59-v86x-fwf2 / CVE-2026-55278?
- Corpus pin: `luci b2e0be4b46ec0fd43394c081fa7c50657af14011`.
- Producer commit: `codeql-ucode 9166af76cf6944e1b3ea5856a9176366a1f7a6ee`; application-ucode routing remains gated by codeql-ucode#154, so this claim uses a pinned-source oracle.
- Source anchor: `applications/luci-app-lxc/root/usr/share/luci/menu.d/luci-app-lxc.json:27-121`; `applications/luci-app-lxc/ucode/controller/lxc.uc:20-24,127-172`; fix commit `8291c9f52485fc336c590137a86ae44f3195d5e7`.
- Expected observable: a source census reports every `admin/services/lxc/*` function route has `depends.acl = ["luci-app-lxc"]`, and the name validator rejects periods, slashes, and leading dashes before `fs.readfile`/`fs.writefile`; no eligible vulnerable route/name path remains in the pin.
- Oracle: pinned-source JSON/ucode census plus a deterministic name-validator emulator; advisory anchors motivation/source-shape only; no runtime or exploit verdict.
- Controls: positive vulnerable fixture (backend route missing ACL; `../`-bearing name accepted), near-miss valid name with dash/underscore, negative fixed pin; fail-no-eligible-instance with full route/name-consumer census if fixed.
- Result: pending lane evidence.
