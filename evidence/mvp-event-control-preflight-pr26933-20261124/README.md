# PR #26933 clean-control input preflight

On 2026-11-24, the disposable consumer checkout at
`33a27a4d75b8381c92823b71c1856e1e746f358a` (clean) prepared a separate
source-first control oracle for OpenWrt PR #26933. The source checkout was
clean at `bce40f6a15c273778061e8fceced7b9e0f58d99b`; the disposable
control checkout was clean at the captured API base
`727d8d2f8e5b19a2121e2cf05824e9e5cac35310`. The captured pull response
was retained from an earlier same-day API read and was not refreshed for this
preflight. Python was 3.15.2. `summary.json` records the exact input and
output SHA-256 values; the raw JSON and Git objects remain under ignored
`work/gate8-control-preflight-20261124/` and
`work/incoming-live-pr26933-20261124/` and are not portable artifacts.

The input event JSON named the full source, base and control SHAs. The actual
`tools/incoming_event.py` resolver accepted that event against the captured
pull response and both canonical checkouts (exit 0), producing `receipt.json`.
After the consumer control code was committed and the checkout confirmed
clean, this exact command from the consumer checkout returned 0:

```sh
python3 -B -c 'from pathlib import Path; from tools.event_control_scan import prepare_with_report; prepare_with_report(Path("../../work/gate8-control-preflight-20261124/receipt.json"), Path("../../work/gate8-control-preflight-20261124/control"), Path("../../work/gate8-control-preflight-20261124/oracle-clean"))'
```

The independently enumerated control inventory was `inventory_ready` with
`fail_closed: false`. The resulting control manifest selected 128 exact
identities, excluded 13, and expected 93 plain plus 35 markup routes. Its
SHA-256 was `86276158f4aba6486d4554f60e9830a5fa627052b7a2f9d56d293d72391e71e2`.
The separate binding records control tree
`8396fc6de47e8e208dd52b725d327742ab1e0838`, captured receipt digest
and manifest digest. This is input-oracle evidence only. No CodeQL database,
released scan, SARIF, or clean-result assertion ran; the release lock remains
null. It does not establish Gate 8 or actual installed bytes.

After PR #160 added explicit control-role validation, the clean consumer
checkout at `2096f1d` regenerated this oracle under ignored
`work/gate8-control-preflight-20261124/oracle-role-clean/`. The actual
`validate_event_manifest(..., source_role="clean_control")` check returned
0 with 128 selected, 13 excluded and `event.source_role: clean_control`;
the revised manifest SHA-256 is
`59a9e6f808657e58c3ab247dd58bf86ba04fb34a6f4310c19a9dc046006e1d45`.
The original `summary.json` remains a receipt for the earlier clean commit
and digest, rather than being silently rewritten.
