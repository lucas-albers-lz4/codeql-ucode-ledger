# Claim 046: Fixed-command template substitution in getFeatures

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category B
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- M4 documented unmodeled set: hostapd/wpa_supplicant system() templates, dnsmasq/odhcpd/ipset popen

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

What command-template substitution sites exist in pinned luci-base getFeatures beyond the five M4-inventoried methods, and which carry request-derived vs config-derived values?

## Method

Source inventory of getFeatures handler command construction at pinned luci SHA; classify value provenance (request.args vs uci/config vs literal); bounded query only where the supported slice reaches.

## Required evidence

- Template-site multiset with provenance class
- Source lines and oracle

## Controls

- Positive: config-derived substitution site
- Near miss: request-derived site inside supported slice
- Negative: fully literal command

## Out of scope

- No claim of full getFeatures coverage
- No interprocedural init_action modeling

## Notes

This is the documented M4 gap turned into a named bounded decision.

## Result

Not yet evaluated.
