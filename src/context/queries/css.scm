[
  (block)
  (declaration)
] @indent.begin

(block
  "}" @indent.branch)

"}" @indent.dedent

(comment) @indent.ignore

; Match top-level rules
(rule_set
  (qualified_rule
    (selector_list) @symbol.name))

; Match top-level at-rules
(at_rule
  (at_keyword) @symbol.name)
