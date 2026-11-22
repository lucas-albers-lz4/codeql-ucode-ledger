# Roadmap progress, 2026-11-21

This is a decision log, not a claim or a promise that later gates remain open.
Re-fetch and check relevant deltas and issue ownership at each new run.
At this review, remote `main` was producer
`0a6612fe0e66351a0ccda43ad5b51f5ef5a2724e` and consumer
`5f8bd2658483c0c06c0ebfced98fd09b1f57aeff`; claim 022 uses the earlier
consumer inventory pin recorded in claim 021.

- **Wave 1:** [Claim 021](../claims/021-pinned-luci-template-extraction.md)
  records the 11 selected raw LuCI templates and three controls, at producer
  `0a6612fe0e66351a0ccda43ad5b51f5ef5a2724e` and consumer inventory
  `d37adeadaf836ba97049f75087a348165027f7f9`. It does not establish installed
  bytes, semantics or full-profile coverage.
- **Wave 2:** [Claim 022](../claims/022-pinned-mixed-template-ast.md) records
  selected `view.ut` AST rows and the literal-lookalike control. Markup
  routing remains inconclusive; parent kind and span are not parent entity
  identity.
- **Wave 3: deferred at the decision gate.** On the above pinned producer,
  `docs/m4-template-string-call-arguments.md` and its named smoke already
  exercise real `luci` template arguments, non-template and argument-index
  controls. On the above pinned consumer, a repository-wide `rg -n
  'getTemplateArgument'` returned no matches, and
  `corpus/luci_ssl_files.py` describes `runtime.uc` as plain with dispatcher
  support unstaffed. The candidate LuCI `runtime.uc` at
  `b2e0be4b46ec0fd43394c081fa7c50657af14011` has SHA-256
  `b15afce07020e2a7ad50718d49a874da30d0582ede7de65e54acaceb6e9d0926`
  and template call arguments at lines 65, 158 and 166; these source sites alone
  do not establish a downstream decision. Ucode #127 is closed. Revisit if a
  named analysis needs these sites or a relevant contract changes. No CodeQL
  run or new claim is asserted for this gate.
- **Wave 4: initially deferred; producer-side prerequisite reopened.** At producer
  `0a6612fe0e66351a0ccda43ad5b51f5ef5a2724e`,
  `docs/issue-53-uci-inventory.md` records the indirect `uci.commit` source
  candidate, its forwarding helper, same-location AST multiplicity and
  uncompleted relationship/control gates. It expressly distinguishes that
  candidate from a direct cursor write. At consumer
  `d37adeadaf836ba97049f75087a348165027f7f9`, `docs/pack-contract.md`
  describes a future `uci_set`/consumer-catalog join, not a consumer for this
  indirect `uci.commit` inventory. No distinct supported downstream decision
  was identified. On further review, the upstream audit itself explicitly
  requests a distinct syntax-only control gate for a separately scoped
  indirect-ubus inventory. That named producer feasibility decision is worth
  testing without a consumer join: distinguish exact candidate syntax and
  helper-body shapes from eligible controls, preserving entity multiplicity.
  This does not unblock a direct cursor-write effect, call binding or runtime
  conclusion. Source-first control design is in progress; no new CodeQL result
  is asserted here yet.
- **Wave 5: deferred at the decision gate.** The consumer `main` observed at
  `5f8bd2658483c0c06c0ebfced98fd09b1f57aeff` adds a markup assessment since
  `d37adea`; that delta does not change the JS inventories. Its
  `docs/issue-69-inventory-bridge.md` records the shipped 88-file extraction
  and RPC/fs/CGI inventories and explicitly holds the JS UCI inventory. No
  additional named downstream decision or relevant JS gap was identified.
  Do not treat this as a fresh JS result.
- **Wave 6: deferred at the decision gate.** At producer
  `0a6612fe0e66351a0ccda43ad5b51f5ef5a2724e`,
  `docs/m4-fs-receiver-provenance.md` and
  `docs/m4-fs-receiver-alias-investigation.md` describe a bounded observer
  and prototype; they do not promote runtime resource identity or production
  flow. A real `fs.popen`/`fd.read`/`fd.close` shape exists in the pinned LuCI
  plugin, but no named downstream query whose result changes on this alias
  relationship was identified. Ucode #48 remains open and blocked for
  production work. Revisit upon a discriminating affected case or relevant
  owner-contract change; no new CodeQL run is asserted.
- **Consumer markup delta:** Consumer `main` advanced to
  `5f8bd2658483c0c06c0ebfced98fd09b1f57aeff`, adding a 12-input markup
  assessment and an assessment-specific receipt validator. Its report records
  a fresh producer-to-checker observation at the same producer/LuCI revisions
  as claim 021; it does not establish a general reporting adapter or semantic
  coverage. Claim 021's actual 14-input outputs do not satisfy the checker's
  fixed 12-input contract and cannot be filtered to manufacture a handoff.
  A fresh 12-input producer run would mostly duplicate the upstream assessment;
  retain the observed distinction and revisit only for a new decision or
  relevant delta. No live consumer handoff is claimed from claim 021.
- **Wave 7: deferred at the decision gate.** Comparing claim 008's refreshed
  pair (`8375887` / `33ff29f`) with current producer `0a6612f` and consumer
  `5f8bd26` found no changes to the selected extractor/library, query, source,
  typed exporter, strict adapter or lock inputs. The consumer's generic
  numeric validator change predates that refresh and is a distinct contract.
  The newer markup receipt validator is assessment-specific, not a change to
  one of the existing handoff paths. Revisit a selected handoff on an actual
  relevant contract/source delta or new analysis decision; no repeat run is
  asserted.
- **Wave 8: deferred; interface gate unmet.** Current producer `tools/` has
  the setBlock typed exporter but no supported fresh direct-exec query-to-record
  exporter for the consumer's retained grant join. OpenWrt PR #113 tests
  retained rows, not a fresh handoff. Ucode #55 and OpenWrt #65 remain paired
  contract maintenance owners. Revisit when an actual supported fresh path
  and independent source/policy oracle exist; no synthetic adapter was made.
- **Wave 9: deferred; interface gate unmet.** Claim 005 stays partial.
  Current `ImportedCalleeTaint.ql` and the separate source/sink pair inventory
  do not create an imported-callee query-to-record path or prove cross-file
  flow. Consumer retained reports and tests are historical records. Revisit
  when a supported fresh path and actual consumer retention are available;
  ucode #50/#54 and OpenWrt #65 remain relevant owners.
- **Wave 10: deferred; implementation gate unmet.** Current `Markup.qll`
  exposes generated AST relations and says it does not model control or data
  flow. `docs/markup-cfg-proposal.md` is a proposal, not a CFG implementation;
  ucode #57 remains open and deferred. Revisit when an actual supported
  implementation and named decision exist. No CFG or runtime claim is made.
- **Wave 11: deferred at the decision gate.** Claim 012 and the consumer's
  `docs/luci-backend-comparison.md` say the grant fixture is catalog-derived
  and the source fixture is not yet independently approved. The consumer does
  have scoped policy expectations for some specific capabilities, so this is
  not a claim that independent expectations never exist. No independently
  sourced expectation applicable to a *new named declaration/grant decision*
  was identified. OpenWrt #132 remains a discussion, not an implemented
  validator. Revisit when a policy owner supplies an applicable independent
  oracle and near miss. No new claim or runtime authorization result is asserted.
- **Wave 12: deferred at the decision gate.** Claims 015–016 and 019 cover
  bounded plain-source slices; the consumer's newer markup assessment covers
  the 12 inventory markup identities, while claims 020–022 provide further
  scoped AST/diagnostic observations. The consumer's #69 evidence already
  covers the defined JS selection and several syntax inventories. No distinct,
  larger source boundary tied to an unmet named analysis decision was
  identified. Ucode #129's source discovery did not justify expanding the
  rpcd-only retained request-args report. Revisit for a concrete decision,
  independent identity oracle and resource plan; no corpus run or timing
  estimate is asserted here.
