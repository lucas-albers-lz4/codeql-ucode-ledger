# Census: grammar node kinds vs dbscheme/AST/flow layers (codeql-ucode#180

- Producer pin: `9166af76cf6944e1b3ea5856a9176366a1f7a6ee`
- Grammar pin: `{r['pin_grammar']}`
- Method: kind present in `ql/lib/ucode.dbscheme`; `ast/internal/<Camel(kind)>.qll` exists; kind literal or class name appears in CFG/controlflow/DataFlow/dataflow sources.
- 'flow: none' means no kind-specific rule found at the flow layer, not necessarily unmodeled semantics (generic parent rules may cover); the list is the audit set for the fail-open follow-up.

## ucode (83 named kinds)

| kind | dbscheme | ast | flow refs | class |
|---|---|---|---|---|
| declaration | y | y | — | extracted+ast |
| expression | y | y | CfgNodes:class-ref; file:Scope:class-ref; file:DataFlowDispatch:class-ref | extracted+ast+flow |
| primary_expression | y | y | — | extracted+ast |
| statement | y | y | CfgNodes:class-ref | extracted+ast+flow |
| arguments | y | y | — | extracted+ast |
| array | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| arrow_function | y | y | file:Scope:class-ref; file:DataFlowDispatch:class-ref | extracted+ast+flow |
| assignment_expression | y | y | file:ControlFlowGraphImpl:class-ref; file:DataFlowPrivate:class-ref; file:SsaImpl:class-ref | extracted+ast+flow |
| augmented_assignment_expression | y | y | file:ControlFlowGraphImpl:class-ref; file:DataFlowPrivate:class-ref; file:SsaImpl:class-ref | extracted+ast+flow |
| binary_expression | y | y | file:ControlFlowGraphImpl:class-ref; file:DataFlowPrivate:class-ref | extracted+ast+flow |
| break_statement | y | y | file:Completion:class-ref | extracted+ast+flow |
| call_expression | y | y | CfgNodes:class-ref; file:ControlFlowGraphImpl:class-ref; file:DataFlowDispatch:class-ref | extracted+ast+flow |
| catch_clause | y | y | file:ControlFlowGraphImpl:class-ref; file:SsaImpl:class-ref | extracted+ast+flow |
| computed_property_name | y | y | — | extracted+ast |
| continue_statement | y | y | file:Completion:class-ref | extracted+ast+flow |
| delete_expression | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| elif_clause | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| else_alt_clause | y | y | — | extracted+ast |
| else_clause | y | y | — | extracted+ast |
| empty_statement | y | y | — | extracted+ast |
| export_clause | y | y | — | extracted+ast |
| export_specifier | y | y | — | extracted+ast |
| export_statement | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| expression_statement | y | y | — | extracted+ast |
| for_alt_statement | y | y | file:Completion:class-ref; file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| for_in_alt_statement | y | y | file:Completion:class-ref; file:ControlFlowGraphImpl:class-ref; file:SsaImpl:class-ref | extracted+ast+flow |
| for_in_statement | y | y | file:Completion:class-ref; file:ControlFlowGraphImpl:class-ref; file:SsaImpl:class-ref | extracted+ast+flow |
| for_statement | y | y | file:Completion:class-ref; file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| formal_parameters | y | y | file:Completion:class-ref; file:Scope:class-ref; file:DataFlowDispatch:class-ref | extracted+ast+flow |
| function_declaration | y | y | file:Scope:class-ref; file:DataFlowDispatch:class-ref | extracted+ast+flow |
| function_expression | y | y | file:Scope:class-ref | extracted+ast+flow |
| if_alt_statement | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| if_statement | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| import_clause | y | y | — | extracted+ast |
| import_specifier | y | y | file:DataFlowDispatch:class-ref | extracted+ast+flow |
| import_statement | y | y | file:DataFlowDispatch:class-ref | extracted+ast+flow |
| lexical_declaration | y | y | — | extracted+ast |
| member_expression | y | y | file:ControlFlowGraphImpl:class-ref; file:DataFlowDispatch:class-ref; file:DataFlowPrivate:class-ref | extracted+ast+flow |
| named_imports | y | y | — | extracted+ast |
| namespace_import | y | y | — | extracted+ast |
| object | y | y | file:DataFlowPrivate:class-ref; file:DataFlowPublic:class-ref | extracted+ast+flow |
| pair | y | y | file:DataFlowPrivate:class-ref; file:DataFlowPublic:class-ref | extracted+ast+flow |
| parenthesized_expression | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| program | y | y | file:ControlFlowGraphImpl:class-ref; file:Scope:class-ref | extracted+ast+flow |
| regex | y | y | — | extracted+ast |
| rest_element | y | y | file:Scope:class-ref; file:DataFlowDispatch:class-ref; file:DataFlowPrivate:class-ref | extracted+ast+flow |
| return_statement | y | y | file:Completion:class-ref; file:ControlFlowGraphImpl:class-ref; file:DataFlowPrivate:class-ref | extracted+ast+flow |
| sequence_expression | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| spread_element | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| statement_block | y | y | file:ControlFlowGraphImpl:class-ref; file:Scope:class-ref | extracted+ast+flow |
| statement_list | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| string | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| subscript_expression | y | y | file:ControlFlowGraphImpl:class-ref; file:DataFlowPrivate:class-ref | extracted+ast+flow |
| switch_body | y | y | — | extracted+ast |
| switch_case | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| switch_default | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| switch_statement | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| template_string | y | y | — | extracted+ast |
| template_substitution | y | y | — | extracted+ast |
| ternary_expression | y | y | file:ControlFlowGraphImpl:class-ref; file:DataFlowPrivate:class-ref | extracted+ast+flow |
| try_statement | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| unary_expression | y | y | — | extracted+ast |
| update_expression | y | y | file:SsaImpl:class-ref | extracted+ast+flow |
| variable_declarator | y | y | file:ControlFlowGraphImpl:class-ref; file:DataFlowPrivate:class-ref | extracted+ast+flow |
| while_alt_statement | y | y | file:Completion:class-ref; file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| while_statement | y | y | file:Completion:class-ref; file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| comment | y | y | — | extracted+ast |
| default | y | y | — | extracted+ast |
| doc_comment | y | y | file:Completion:class-ref | extracted+ast+flow |
| escape_sequence | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| false | y | y | — | extracted+ast |
| hash_bang_line | y | y | — | extracted+ast |
| identifier | y | y | file:ControlFlowGraphImpl:class-ref; file:Scope:class-ref; file:DataFlowDispatch:class-ref | extracted+ast+flow |
| null | y | y | — | extracted+ast |
| number | y | y | — | extracted+ast |
| optional_chain | y | y | — | extracted+ast |
| property_identifier | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| regex_flags | y | y | — | extracted+ast |
| regex_pattern | y | y | — | extracted+ast |
| shorthand_property_identifier | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| string_fragment | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| this | y | y | file:Completion:class-ref; file:DataFlowDispatch:class-ref; file:DataFlowPrivate:class-ref | extracted+ast+flow |
| true | y | y | — | extracted+ast |

## ucode_markup (101 named kinds)

| kind | dbscheme | ast | flow refs | class |
|---|---|---|---|---|
| declaration | y | y | — | extracted+ast |
| expression | y | y | CfgNodes:class-ref; file:Scope:class-ref; file:DataFlowDispatch:class-ref | extracted+ast+flow |
| primary_expression | y | y | — | extracted+ast |
| statement | y | y | CfgNodes:class-ref | extracted+ast+flow |
| arguments | y | y | — | extracted+ast |
| array | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| arrow_function | y | y | file:Scope:class-ref; file:DataFlowDispatch:class-ref | extracted+ast+flow |
| assignment_expression | y | y | file:ControlFlowGraphImpl:class-ref; file:DataFlowPrivate:class-ref; file:SsaImpl:class-ref | extracted+ast+flow |
| augmented_assignment_expression | y | y | file:ControlFlowGraphImpl:class-ref; file:DataFlowPrivate:class-ref; file:SsaImpl:class-ref | extracted+ast+flow |
| binary_expression | y | y | file:ControlFlowGraphImpl:class-ref; file:DataFlowPrivate:class-ref | extracted+ast+flow |
| break_statement | y | y | file:Completion:class-ref | extracted+ast+flow |
| call_expression | y | y | CfgNodes:class-ref; file:ControlFlowGraphImpl:class-ref; file:DataFlowDispatch:class-ref | extracted+ast+flow |
| catch_clause | y | y | file:ControlFlowGraphImpl:class-ref; file:SsaImpl:class-ref | extracted+ast+flow |
| comment_tag | y | n | — | extracted-only |
| computed_property_name | y | y | — | extracted+ast |
| continue_statement | y | y | file:Completion:class-ref | extracted+ast+flow |
| delete_expression | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| elif_clause | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| else_alt_clause | y | y | — | extracted+ast |
| else_clause | y | y | — | extracted+ast |
| empty_statement | y | y | — | extracted+ast |
| export_clause | y | y | — | extracted+ast |
| export_specifier | y | y | — | extracted+ast |
| export_statement | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| expression_statement | y | y | — | extracted+ast |
| expression_tag | y | n | — | extracted-only |
| for_alt_statement | y | y | file:Completion:class-ref; file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| for_in_alt_statement | y | y | file:Completion:class-ref; file:ControlFlowGraphImpl:class-ref; file:SsaImpl:class-ref | extracted+ast+flow |
| for_in_statement | y | y | file:Completion:class-ref; file:ControlFlowGraphImpl:class-ref; file:SsaImpl:class-ref | extracted+ast+flow |
| for_statement | y | y | file:Completion:class-ref; file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| formal_parameters | y | y | file:Completion:class-ref; file:Scope:class-ref; file:DataFlowDispatch:class-ref | extracted+ast+flow |
| function_declaration | y | y | file:Scope:class-ref; file:DataFlowDispatch:class-ref | extracted+ast+flow |
| function_expression | y | y | file:Scope:class-ref | extracted+ast+flow |
| if_alt_statement | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| if_statement | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| import_clause | y | y | — | extracted+ast |
| import_specifier | y | y | file:DataFlowDispatch:class-ref | extracted+ast+flow |
| import_statement | y | y | file:DataFlowDispatch:class-ref | extracted+ast+flow |
| lexical_declaration | y | y | — | extracted+ast |
| markup | y | n | — | extracted-only |
| member_expression | y | y | file:ControlFlowGraphImpl:class-ref; file:DataFlowDispatch:class-ref; file:DataFlowPrivate:class-ref | extracted+ast+flow |
| named_imports | y | y | — | extracted+ast |
| namespace_import | y | y | — | extracted+ast |
| object | y | y | file:DataFlowPrivate:class-ref; file:DataFlowPublic:class-ref | extracted+ast+flow |
| pair | y | y | file:DataFlowPrivate:class-ref; file:DataFlowPublic:class-ref | extracted+ast+flow |
| parenthesized_expression | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| regex | y | y | — | extracted+ast |
| rest_element | y | y | file:Scope:class-ref; file:DataFlowDispatch:class-ref; file:DataFlowPrivate:class-ref | extracted+ast+flow |
| return_statement | y | y | file:Completion:class-ref; file:ControlFlowGraphImpl:class-ref; file:DataFlowPrivate:class-ref | extracted+ast+flow |
| sequence_expression | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| spread_element | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| statement_block | y | y | file:ControlFlowGraphImpl:class-ref; file:Scope:class-ref | extracted+ast+flow |
| statement_list | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| string | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| subscript_expression | y | y | file:ControlFlowGraphImpl:class-ref; file:DataFlowPrivate:class-ref | extracted+ast+flow |
| switch_body | y | y | — | extracted+ast |
| switch_case | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| switch_default | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| switch_statement | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| template_string | y | y | — | extracted+ast |
| template_substitution | y | y | — | extracted+ast |
| ternary_expression | y | y | file:ControlFlowGraphImpl:class-ref; file:DataFlowPrivate:class-ref | extracted+ast+flow |
| text_statement | y | n | — | extracted-only |
| try_statement | y | y | file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| unary_expression | y | y | — | extracted+ast |
| update_expression | y | y | file:SsaImpl:class-ref | extracted+ast+flow |
| variable_declarator | y | y | file:ControlFlowGraphImpl:class-ref; file:DataFlowPrivate:class-ref | extracted+ast+flow |
| while_alt_statement | y | y | file:Completion:class-ref; file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| while_statement | y | y | file:Completion:class-ref; file:ControlFlowGraphImpl:class-ref | extracted+ast+flow |
| comment | y | y | — | extracted+ast |
| comment_content | y | n | — | extracted-only |
| comment_tag_close | y | n | — | extracted-only |
| comment_tag_open | y | n | — | extracted-only |
| comment_tag_trim_close | y | n | — | extracted-only |
| comment_tag_trim_open | y | n | — | extracted-only |
| default | y | y | — | extracted+ast |
| doc_comment | y | y | file:Completion:class-ref | extracted+ast+flow |
| escape_sequence | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| expression_tag_close | y | n | — | extracted-only |
| expression_tag_open | y | n | — | extracted-only |
| expression_tag_trim_close | y | n | — | extracted-only |
| expression_tag_trim_open | y | n | — | extracted-only |
| false | y | y | — | extracted+ast |
| hash_bang_line | y | y | — | extracted+ast |
| identifier | y | y | file:ControlFlowGraphImpl:class-ref; file:Scope:class-ref; file:DataFlowDispatch:class-ref | extracted+ast+flow |
| null | y | y | — | extracted+ast |
| number | y | y | — | extracted+ast |
| optional_chain | y | y | — | extracted+ast |
| property_identifier | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| raw_text | y | n | — | extracted-only |
| regex_flags | y | y | — | extracted+ast |
| regex_pattern | y | y | — | extracted+ast |
| shorthand_property_identifier | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| statement_tag_close | y | n | — | extracted-only |
| statement_tag_lstrip_open | y | n | — | extracted-only |
| statement_tag_open | y | n | — | extracted-only |
| statement_tag_trim_close | y | n | — | extracted-only |
| statement_tag_trim_open | y | n | — | extracted-only |
| string_fragment | y | y | file:DataFlowPrivate:class-ref | extracted+ast+flow |
| this | y | y | file:Completion:class-ref; file:DataFlowDispatch:class-ref; file:DataFlowPrivate:class-ref | extracted+ast+flow |
| true | y | y | — | extracted+ast |
