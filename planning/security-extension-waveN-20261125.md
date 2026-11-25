# Security-extension Wave N — odhcpd / mdnsd resource and serialization fixes

Date: 2026-11-25

## Scope

This wave uses six advisories discovered outside the original Security-40 catalog repos (odhcpd and mdnsd project advisories). It preserves every existing gate and adds no analyzer grant. All claims are pinned-source oracle designs; C extraction is not assumed.

| Claim | Advisory | CVE | Corpus pin | Fix commit(s) |
|---|---|---|---|---|
| 096 | GHSA-7hcw-g2jh-pqv5 | CVE-2026-53922 | odhcpd `5d7be43f8b9dec0eb47e245cfab81108bb131273` | `d08dbcc527cb8f296cd132c1e5bca696e77095b8`, `d168c27fb6a55a07ac4c888e09ff2f41e263d7b7` |
| 097 | GHSA-x8x4-7gvf-gp45 | CVE-2026-55606 | odhcpd `5d7be43f8b9dec0eb47e245cfab81108bb131273` | `6907f28f9ddeef9f69f5ee10bbc9ba8adc0ef57f` |
| 098 | GHSA-7fwx-hhrg-3496 | CVE-2026-53921 | odhcpd `5d7be43f8b9dec0eb47e245cfab81108bb131273` | `d168c27fb6a55a07ac4c888e09ff2f41e263d7b7`, `6634b7a3c79c41a27687925c98c35c8aea2f2b5a`, `89d18771810bdf73f05db042d0baa4fd1af71eae` |
| 099 | GHSA-p769-5v73-pc4f | CVE-2026-53920 | odhcpd `5d7be43f8b9dec0eb47e245cfab81108bb131273` | `719fc3abc0d7e7059871f9f572fb05ada86b8ff2` |
| 100 | GHSA-44ff-jcwh-wgc2 | CVE-2026-53918 | odhcpd `5d7be43f8b9dec0eb47e245cfab81108bb131273` | `5b283832c0a77aed20f1cc384ffc40bc768b06e9` |
| 101 | GHSA-jg8f-fhfw-jg46 | CVE-2026-55492 | mdnsd `defe7ccfd20281b9ef4dfa45437813386a64f8ba` | `1b5e7bf1cec775b89f1a6068dc0b9df3593b5986`, `bd7599d021571e785bd32a75469e7148eb1772e3` |

## Preserved gates

- JS UCI hold, markup extractor gate, template-argument deferral, application-ucode routing gate (#154) remain intact.
- No `path_found`, no new grants/effects, no gate lift.
- Fixed-in-pin results require controls + census; synthetic controls are labeled synthetic.

## Method

Disposable blobless clones under `work/security-extension-20261125/shared/{odhcpd,mdnsd}`; pinned-blob reads only. Fix ancestry verified for all listed commits at reservation time. Lanes produce separate oracles/controls/summaries/run_pipeline.sh; orchestrator re-runs pipelines before status transitions.
