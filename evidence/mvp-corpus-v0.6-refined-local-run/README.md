# v0.6 local refined-producer corpus run

The source-first [v0.6 manifest](../../planning/mvp-bounded-corpus-v0.6.json),
[oracle](../mvp-corpus-v0.6-source-first-oracle.json) and
[controls](../mvp-corpus-v0.6-controls.json) preceded this scan. The pinned
LuCI, captured OpenWrt PR #26933 head, and packages commits are recorded in
the [normalized receipt](receipt.json). The disposable producer is based on
`9166af76cf6944e1b3ea5856a9176366a1f7a6ee` plus the refined
producer-owned grammar patch. Its extractor SHA-256 is
`6ed90de2e6b352daa939ad1d0c627f847383307f212168ad11d9dd06f4faf15b`.

`python3 -B work/mvp-corpus-v0.6-refined-prep-20261124/run.py --execute`
used a fresh run-owned stage, database, cache, `HOME`, `TMPDIR` and outputs
under ignored `work/mvp-corpus-v0.6-refined-local-run-20261124-d`. The
[receipt](receipt.json) records exact source/tool/patch and generated hashes,
commands, exits, phase times and raw artifact hashes. The
[128-row table](exact-identities.csv) maps each pinned source identity to
its staged path, expected and observed route, and successful-file count.
Absolute run, producer and CodeQL paths are normalized there and in the
receipt; raw outputs remain under `work/`.

All 128 route tuples matched: 93 plain and 35 markup-inconclusive, with no
duplicates, exclusions or uncertain routes. Each selected staged path had
one successful extraction row and zero error rows. Both newer wifi files
that fail under merged producer bytes succeeded once. The competing shell
source near miss was absent from the selection. The three-query default
suite resolved as expected; its SARIF had the direct-RPC rule descriptor
and zero results on this bounded current-source corpus. Source and stage
bytes were rechecked after analysis. Nine CodeQL phases exited zero and
took 18.073 seconds, including 10.981 seconds for suite analysis. Peak RSS
was unavailable.

The first attempt stopped before database initialization while enumerating
an untracked producer directory; its failure is retained under ignored
`work/mvp-corpus-v0.6-refined-local-run-20261124-c`. This completed run
used a new database. It is local macOS source-staged modified-producer
evidence. Installed OpenWrt bytes, Linux runtime/cost, a live upstream PR
event and security completeness remain unverified.
