(function_declaration
  name: (identifier) @symbol.name)

(class_declaration
  name: (identifier) @symbol.name)

(variable_declarator
  name: (identifier) @symbol.name)

(assignment_expression
  left: (identifier) @symbol.name)

(arrow_function
  parameter: (identifier) @symbol.name)
