; Match top-level rules
(rule_set
  (prelude (selector_list (selector) @symbol.name)))

; Match top-level at-rules
(at_rule
  (prelude (identifier) @symbol.name))
