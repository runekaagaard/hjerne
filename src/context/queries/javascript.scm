; Scopes
;-------
(statement_block) @local.scope

(function_expression) @local.scope

(arrow_function) @local.scope

(function_declaration) @local.scope

(method_definition) @local.scope

(for_statement) @local.scope

(for_in_statement) @local.scope

(catch_clause) @local.scope

; Definitions
;------------
(variable_declarator
  name: (identifier) @local.definition.var)

(import_specifier
  (identifier) @local.definition.import)

(namespace_import
  (identifier) @local.definition.import)

(function_declaration
  (identifier) @local.definition.function
  (#set! definition.var.scope parent))

(method_definition
  (property_identifier) @local.definition.function
  (#set! definition.var.scope parent))

; References
;------------
(identifier) @local.reference

(shorthand_property_identifier) @local.reference

; Match top-level function declarations
(function_declaration
  name: (identifier) @symbol.name)

; Match top-level class declarations
(class_declaration
  name: (identifier) @symbol.name)

; Match top-level variable declarations
(lexical_declaration
  (variable_declarator
    name: (identifier) @symbol.name))

; Match top-level function expressions assigned to variables
(variable_declaration
  (variable_declarator
    name: (identifier) @symbol.name
    value: (function)))

; Match top-level arrow function expressions assigned to variables
(variable_declaration
  (variable_declarator
    name: (identifier) @symbol.name
    value: (arrow_function)))

; Match top-level function expressions assigned to variables with export
(export_statement
  (variable_declaration
    (variable_declarator
      name: (identifier) @symbol.name
      value: (function))))

; Match top-level arrow function expressions assigned to variables with export
(export_statement
  (variable_declaration
    (variable_declarator
      name: (identifier) @symbol.name
      value: (arrow_function))))

; Match top-level JSX elements
(program
  (expression_statement
    (jsx_element
      (jsx_opening_element
        name: (identifier) @symbol.name))))
