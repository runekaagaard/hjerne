HJERNE MANAGEMENT COMMANDS

Usage: python manage.py <command> [options] [arguments]

Project Management:
  project_add <title> <description>
    Add a new project
    
  project_list
    List all projects with their IDs and titles

Changeset Management:
  changeset_add <project_id> <title>
    Add a new changeset to a project
    
  changeset_list <project_id>
    List all changesets for a given project
    
  changeset_clear_context <changeset_id>
    Clear all contexts in a changeset

Context Management:
  context_add <changeset_id> <filename> <linenumber>
    Add a context to a changeset
    
  context_add_range <changeset_id> <file_path> <from_line> <to_line>
    Add contexts to a changeset for a given range of lines in a file
    
  context_remove <changeset_id> <filename> <linenumber>
    Remove a context from a changeset
    
  context_remove_range <changeset_id> <file_path> <from_line> <to_line>
    Remove contexts from a changeset for a given range of lines in a file
    
  context_update <changeset_id> <replacement_file> [--from-markdown]
    Update the context for a given changeset
    Options:
      --from-markdown  Extract code from markdown blocks
    
  context_update_markdown <changeset_id> <markdown_file>
    Update the context for a given changeset using a markdown file
    
  context_code <changeset_id>
    Output code for a given changeset
    
  context_code_markdown <changeset_id>
    Output code for a given changeset in markdown format, grouped by language

Tree-sitter Integration:
  treesitter_top_level_symbols <file_path>
    Output top-level symbols for a given file using Tree-sitter
    
  treesitter_top_level_symbols_in_range <file_path> <row_from> <row_to>
    Output top-level symbols in a given range for a given file using Tree-sitter

For more information on a specific command, run:
  python manage.py <command> --help
