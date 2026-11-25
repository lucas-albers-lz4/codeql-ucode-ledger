# 092 — luci-app-adblock-fast raw cron writer removal and field validation

- Status: Proposed
- Question: At the pinned LuCI corpus, is the caller-supplied `setCronEntry` RPC absent from both the method table and ACL, and does `syncCron` render cron lines only from discrete validated fields, closing the newline-injection shape in GHSA-ggpf-xrph-wg5v / CVE-2026-45767?
- Corpus pin: `luci b2e0be4b46ec0fd43394c081fa7c50657af14011`.
- Producer commit: `codeql-ucode 9166af76cf6944e1b3ea5856a9176366a1f7a6ee`; application-ucode routing remains gated by codeql-ucode#154, so this claim uses a pinned-source oracle.
- Source anchor: `applications/luci-app-adblock-fast/root/usr/share/rpcd/ucode/luci.adblock-fast:160-235,346-360,470-480`; `applications/luci-app-adblock-fast/root/usr/share/rpcd/acl.d/luci-app-adblock-fast.json:27-39`; removal/update commit `9ccd99b5898457e5ef39dc21aea226d7fb6e5c7e`.
- Expected observable: no `setCronEntry`/`set_cron_entry` writer is exported or ACL-granted; `cron_write` validates/clamps discrete schedule fields before assembling a fixed `/etc/init.d/<package> dl` line; no caller-supplied physical cron line reaches `writefile`.
- Oracle: pinned-source method/ACL census plus deterministic cron-field validator emulator; advisory anchors motivation/source-shape only; no runtime or exploit verdict.
- Controls: positive vulnerable fixture (raw `entry` containing `\n` written verbatim), near-miss newline-bearing discrete field rejected/clamped, negative fixed pin; fail-no-eligible-instance with full cron-writer census if fixed.
- Result: pending lane evidence.
