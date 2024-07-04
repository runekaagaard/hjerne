(function_definition
    name: (identifier) @symbol.name)
  
  ; Match top-level class definitions
  (class_definition
    name: (identifier) @symbol.name)
  
  ; Match top-level expression statements with assignment
  (expression_statement
    (assignment
      left: (identifier) @symbol.name))

  ; Match top-level attribute assignments
  (expression_statement
    (assignment
      left: (attribute
        object: (attribute
          object: (identifier) @symbol.name))))
