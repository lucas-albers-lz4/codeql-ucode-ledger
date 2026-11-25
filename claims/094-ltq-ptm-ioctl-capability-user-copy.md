# 094 — ltq-ptm ioctl capability gate and user-memory accessors

- Status: Proposed
- Question: At the pinned OpenWrt corpus, do ltq-ptm private ioctls require `CAP_NET_ADMIN` and use `copy_from_user`/`copy_to_user` for user-supplied buffers, closing the arbitrary kernel-memory access shape in GHSA-h427-frpr-7cqr / CVE-2025-65123?
- Corpus pin: `openwrt 4e9642517b48bae612ff10fb72fb9199e559500e`.
- Producer commit: `codeql-ucode 9166af76cf6944e1b3ea5856a9176366a1f7a6ee`; source oracle on pinned kernel C, no assumed CodeQL extraction.
- Source anchor: `package/kernel/lantiq/ltq-ptm/src/ifxmips_ptm_vdsl.c:389-481`; `package/kernel/lantiq/ltq-ptm/src/ifxmips_ptm_adsl.c` ioctl census; fix commit `2a76abc5442e3f74d95b4caa9bb57e5488fc132e` (verified ancestor of corpus pin).
- Expected observable: every private ioctl entry checks capability before processing, and user-buffer cases use bounded user-copy accessors rather than direct dereference; no eligible unprivileged direct-access path remains in the pin.
- Oracle: pinned-source ioctl/capability/user-copy census across PTM variants; advisory anchors motivation/source-shape only; no runtime, kernel exploit, or device verdict.
- Controls: positive vulnerable fixture (no capability check; direct user-pointer dereference), near-miss capability-present but wrong accessor, negative fixed pin; fail-no-eligible-instance with full ioctl census if fixed.
- Result: pending lane evidence.
