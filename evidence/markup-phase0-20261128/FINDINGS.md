# Phase 0 item 1 receipt — ucode markup escaping facts (codeql-ucode#182)

Pins (both read-only; this is the first time the interpreter *and* the escape
helper's home are pinned):
- Interpreter: `ucode-lang/ucode` @ `49dacb2cc2d86b4d6a1c8a3b281b1986a846bd31`
  (2026-11-27; cloned blobless to work/.../shared/ucode-interp)
- Escape helper + templates + scope: `luci` @ `b2e0be4b46ec0fd43394c081fa7c50657af14011`
No CodeQL execution; no other track's state touched.

## Facts (all path:line at the pins)

1. **Template mode is an interpreter compiler flag, not a library.**
   `include/ucode/compiler.h:35` `bool raw_mode;`; `lexer.c:627`
   `bool tpl = !(lex->config && lex->config->raw_mode);`. luci drives it with
   `loadfile(path, { raw_mode: false })` (`runtime.uc:75` render_ucode).

2. **Template grammar**: `{{`/`}}` expression (`lexer.c:658`/`:639`), `{%`/`%}`
   statement (`:661`/`:853`), `{#` comment, and `-}}`/`-%}` trim modifiers set
   `lex->modifier = MINUS` (`lexer.c:769-788`). The tree-sitter `ucode_markup`
   grammar mirrors this (`expression_tag`, `statement_tag*`, `comment_tag*`,
   `*_trim_open/close`).

3. **The output path does NOT escape.** `compiler.c:4154-4167`
   `uc_compiler_compile_tplexp` = compile expression → `I_PRINT`; `vm.c:3690` →
   `uc_vm_insn_print` (`vm.c:3061-3086`): UC_STRING is `fwrite`'d **verbatim**;
   objects/arrays via `ucv_to_jsonstring`/`ucv_to_string` (JSON quoting —
   `"`,`\`,`<` `>` `&` are not HTML-escaped). **There is no HTML-escape function
   in the interpreter at all** (`grep html_escape|escape_html|htmlspecialchars|uc_html`
   over the tree: empty).

4. **Escaping is an application opt-in from luci's own contrib module.**
   `entityencode` / `striptags` are NOT in ucode — they ship in
   `luci@b2e0be4b contrib/package/ucode-mod-html/src/html.c`:
   `uc_html_entityencode` (`:2730`) encodes `"`→`&#34;`, `&`→`&#38;`,
   `'`→`&#39;`, `<`→`&#60;`, `>`→`&#62;` (`:2755-2760`); `striptags` at `:2693`.
   `dispatcher.uc:5` imports them and injects them into every render scope
   (`dispatcher.uc:910-911`).

5. **Real-corpus ratio (luci .ut @ pin)**: 274 `{{ }}` substitutions across 32
   template files, but only **28 `entityencode` references across 14 files** —
   i.e. the large majority of substitutions are unescaped, and escaping is by
   author convention.

## Consequences for Phase 0 items 2-3 (design note; NOT yet decided)

- **Claim 052's premise needs re-wording.** At the engine level there is a single
  output form (raw); the escaped-vs-raw distinction is *not* a template syntax
  property — it is whether an `entityencode`/`striptags` helper (from #4) wraps
  the printed value. "Does the graph distinguish escaped vs raw output forms?"
  becomes "can the model see an `entityencode`/`striptags` call between the tainted
  value and `I_PRINT`?"
- **Sink model is simplified**: every substitution node is a default sink (raw);
  `entityencode` (and `striptags`) become sanitizer/barrier predicates keyed on the
  ucode-mod-html function identities. That is #155-style sink/sanitizer modeling,
  not CFG expressiveness — an important scope reduction.
- **The JSON-stringify substitution** (printing an object/array) is itself an HTML
  sink (no `<`/`>` escaping) and must be an explicit census observation, not
  silently treated as safe.
- **Bridge direction**: values flow `.uc render call scope` → `.ut substitution`;
  the ucode-mod-html helpers are the only sanitizers in scope, so the sanitizer set
  is small and enumerable from `dispatcher.uc`.

## Status

- #182 Phase 0 item 1: **complete** (pins + cited facts, incl. the escape helper's
  true home in luci contrib).
- Item 2 (granularity decision + rejected alternatives): input ready — the
  whole-`values`-table vs per-field propagation question stands; the sanitizer
  predicate is now concretely `entityencode`/`striptags` identities.
- Item 3 (design pass): pending reviewer.
- Claims 052/056: remain Blocked; this receipt refines the framing, does not
  discharge them.
