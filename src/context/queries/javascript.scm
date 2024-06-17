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

; Match top-level JSX elements
(program
  (expression_statement
    (jsx_element
      (jsx_opening_element
        name: (identifier) @symbol.name))))
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

; Match top-level JSX elements
(program
  (expression_statement
    (jsx_element
      (jsx_opening_element
        name: (identifier) @symbol.name))))
