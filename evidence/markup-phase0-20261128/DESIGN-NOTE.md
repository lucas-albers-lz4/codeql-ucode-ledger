# Phase 0 design decision note — ucode markup dataflow model (APPROVED 2026-11-28)

**Design pass outcome (item 3):** APPROVED. Reviewer mandated **D1 = named-scope-
identifier** and **D2 = arg-sensitive** (`entityencode(x)` ≠ `entityencode(x,true)`;
bare `entityencode` is not attribute-safe), matching the recommendations below. Phase 0
gate is lifted; Phase 1 may proceed on these terms. Output-context modeling (text/attr/
script) is explicitly deferred (Rejected D2-B) pending #180 markup-AST work.

For author-level design pass (#182 item 3). Decisions are numbered so the reviewer
can accept/amend each independently. Grounded entirely in the pinned receipts:
`evidence/markup-phase0-20261128/FINDINGS.md` and the `runtime.uc` / `header.ut` /
`html.c` reads at `luci@b2e0be4b`, `ucode@49dacb2c`.

---

## D1 — Flow granularity into templates

**Question:** how does taint from a `.uc` render call propagate into `.ut` substitutions?

**Recommended: named-scope-identifier granularity (per-top-level-name), NOT per-deep-field.**

- Evidence: `render_ucode` passes one object (`call(tmplfunc, null, scope)`,
  `runtime.uc:74-80`); `render_any` wraps it in a `proto` chain (`runtime.uc:121`).
  Templates reference **top-level scope names** (`boardinfo`, `ctx`, `dispatcher`,
  `fs_page`, `dispatched`) and then sub-field-access inside the expression
  (`{{ boardinfo.hostname }}`, `{{ ctx.path }}`, `{{ dispatcher.lang }}`).
- So the natural unit is: taint a scope *name*, let ordinary `.field` access flow
  within the template expression as it already would for any ucode object.
- **Rejected A — whole-table (one aggregate):** if any field is untrusted, every
  substitution in the file becomes a candidate sink. Sound but useless: header.ut
  mixes `{{ _('Menu') }}` (constant) with `{{ dispatcher.lang }}` (request-derived)
  in adjacent attributes; aggregate taint collapses them.
- **Rejected B — per-deep-field at the call site:** requires statically resolving
  every `scope.a.b.c` path to every `{{ a.b.c }}` reads-site. Defeated by (i) the
  `proto()` chain — a name may be injected by an *outer* render, not the immediate
  call (`runtime.uc:121`), and (ii) `{% include(path, { boardinfo, fs_defaults }) %}`
  re-scoping (`header.ut:75,166,208`), so a template's namespace is assembled from
  ≥2 sources. Per-deep-field precision is not statically obtainable without a whole-
  app scope dataflow that #155/#156 don't provide yet.

**Reviewer decision needed:** confirm D1 = named-scope-identifier. If instead you
prefer whole-table for v1 (ship coarse+sound, refine later), say so — it changes the
Phase 1 query shape but not the pin.

## D2 — Sanitizer / barrier model

**Recommended:** the sanitizer set is exactly the two injected helpers, and
**strength is context-dependent** — model `entityencode` as a *partial* barrier:

- `entityencode(x)` (quote falsy) encodes only `< & >` (`html.c:2749-2751`).
- `entityencode(x, true)` (quote truthy) additionally encodes `" ' \0`-class
  (`html.c:2748`).
- Non-string input returns **NULL** (`html.c:2737-2738`) — so `entityencode` is not
  a drop-in guard for object/array substitution (those take the JSON path).
- `striptags(x)` removes tags but is *not* attribute-safe; used as an inner transform
  (`header.ut:86,198` chain `entityencode(striptags(...), true)`).

**Design rule:** a substitution is "sanitized for text context" iff its value passes
through `entityencode(..., true)`; "sanitized for attribute context" *also* requires
the quote arg. A bare `entityencode(x)` without `true` must NOT be treated as fully
safe in an attribute.

- **Rejected A — treat `entityencode` as an unconditional barrier:** would silence any
  attribute-substitution that omits the quote arg (false negative).
- **Rejected B — model HTML output *context* (text vs attribute vs script) from the
  surrounding markup:** more precise but requires parsing the literal HTML around each
  substitution and inferring open tags — a markup-AST capability the current bounded
  graph does not provide (see #180: 19 markup kinds are extracted-only). Defer; do not
  block on it.

> Note on positives: candidate request-derived substitutions must be checked for
> allow-list gating before being called sinks. `class="lang_{{ dispatcher.lang }}"`
> (`header.ut:87`) looks request-derived but `dispatcher.lang` is constrained to
> configured languages via `uci.get('luci','languages',cc)` (`dispatcher.uc:93-98`),
> else `'en'` — an **eligible near-miss**, not a positive. Locating a true positive is
> a Phase 1 corpus sweep using this model, not a claim of this note.

**Reviewer decision needed:** is the "quote arg required for attribute-safety" rule in
scope for v1, or do we model only `entityencode(..., true)` vs unguarded (binary) and
leave arg-sensitivity to a follow-up?

## D3 — Sink identification

**Recommended:** every `{{ expr }}` whose printed value can carry untrusted data is a
sink (there is **no** safe default — `I_PRINT` is raw, `vm.c:3061-3086`). Include the
object/array → `ucv_to_jsonstring` path explicitly: JSON quoting does not neutralize
`< > &`, so `{{ someObject }}` is an HTML sink too, not implicitly safe.

- **Rejected:** distinguishing an "output form" — D1 receipts proved there is exactly
  one form. This is the claim-052 premise correction.

## D4 — Cross-template bridge

**Recommended:** `{% include(path, {...}) %}` is a scope-join edge: tainted scope names
at the include site flow to the same-named identifiers in the included template. Model
include as a call-to-template with argument = the inline object. This is what makes
052 end-to-end (dispatcher → header → partials).

- **Deferred (not blocked here):** dynamic / computed include paths and template names
  built by string concat — record as `inconclusive` with the same honesty used for #154.

## D5 — What this changes downstream

- Turns most of #182 Phase 1 into **#155-style identity modeling** (recognize the
  `html` module functions `entityencode`/`striptags` and the `loadfile`-template entry),
  not new CFG expressiveness. Scope reduction, flagged in the item-1 receipt.
- Claim 052 re-words (single output form + sanitizer-visibility). Claim 056 (template
  argument untrusted) keeps its framing; D1 defines its source granularity.
- Both stay **Blocked** until a Phase 1 rule + 3/3 witnesses exist.

## Out of scope for this note (unchanged)
Routing (#154), native/fs sinks (#155 as its own track), cross-language JS↔ucode join
(#156), the 19 extracted-only markup kinds' AST classes, and any runtime/exploit claim.
No gate lifted.
