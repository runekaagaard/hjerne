# Hjerne Management Commands

This document provides an overview of all management commands available in the Hjerne project.

## Project Management

### project_add
- **Description**: Add a new project.
- **Usage**: `python manage.py project_add <title> <description>`
- **Arguments**:
  - `title`: The title of the project
  - `description`: The description of the project

### project_list
- **Description**: List all projects with their IDs and titles.
- **Usage**: `python manage.py project_list`

## Changeset Management

### changeset_add
- **Description**: Add a new changeset to a project.
- **Usage**: `python manage.py changeset_add <project_id> <title>`
- **Arguments**:
  - `project_id`: The ID of the project
  - `title`: The title of the changeset

### changeset_list
- **Description**: List all changesets for a given project.
- **Usage**: `python manage.py changeset_list <project_id>`
- **Arguments**:
  - `project_id`: The ID of the project

### changeset_clear_context
- **Description**: Clear all contexts in a changeset.
- **Usage**: `python manage.py changeset_clear_context <changeset_id>`
- **Arguments**:
  - `changeset_id`: The ID of the changeset

## Context Management

### context_add
- **Description**: Add a context to a changeset.
- **Usage**: `python manage.py context_add <changeset_id> <filename> <linenumber>`
- **Arguments**:
  - `changeset_id`: The ID of the changeset
  - `filename`: The name of the file
  - `linenumber`: The line number in the file

### context_add_range
- **Description**: Add contexts to a changeset for a given range of lines in a file.
- **Usage**: `python manage.py context_add_range <changeset_id> <file_path> <from_line> <to_line>`
- **Arguments**:
  - `changeset_id`: The ID of the changeset
  - `file_path`: The path to the file
  - `from_line`: The starting line number
  - `to_line`: The ending line number

### context_remove
- **Description**: Remove a context from a changeset.
- **Usage**: `python manage.py context_remove <changeset_id> <filename> <linenumber>`
- **Arguments**:
  - `changeset_id`: The ID of the changeset
  - `filename`: The name of the file
  - `linenumber`: The line number in the file

### context_remove_range
- **Description**: Remove contexts from a changeset for a given range of lines in a file.
- **Usage**: `python manage.py context_remove_range <changeset_id> <file_path> <from_line> <to_line>`
- **Arguments**:
  - `changeset_id`: The ID of the changeset
  - `file_path`: The path to the file
  - `from_line`: The starting line number
  - `to_line`: The ending line number

### context_update
- **Description**: Update the context for a given changeset.
- **Usage**: `python manage.py context_update <changeset_id> <replacement_file> [--from-markdown]`
- **Arguments**:
  - `changeset_id`: The ID of the changeset
  - `replacement_file`: The path to the replacement file
- **Options**:
  - `--from-markdown`: Extract code from markdown blocks

### context_update_markdown
- **Description**: Update the context for a given changeset using a markdown file.
- **Usage**: `python manage.py context_update_markdown <changeset_id> <markdown_file>`
- **Arguments**:
  - `changeset_id`: The ID of the changeset
  - `markdown_file`: The path to the markdown file

### context_code
- **Description**: Output code for a given changeset.
- **Usage**: `python manage.py context_code <changeset_id>`
- **Arguments**:
  - `changeset_id`: The ID of the changeset

### context_code_markdown
- **Description**: Output code for a given changeset in markdown format, grouped by language.
- **Usage**: `python manage.py context_code_markdown <changeset_id>`
- **Arguments**:
  - `changeset_id`: The ID of the changeset

## Tree-sitter Integration

### treesitter_top_level_symbols
- **Description**: Output top-level symbols for a given file using Tree-sitter.
- **Usage**: `python manage.py treesitter_top_level_symbols <file_path>`
- **Arguments**:
  - `file_path`: The path to the file

### treesitter_top_level_symbols_in_range
- **Description**: Output top-level symbols in a given range for a given file using Tree-sitter.
- **Usage**: `python manage.py treesitter_top_level_symbols_in_range <file_path> <row_from> <row_to>`
- **Arguments**:
  - `file_path`: The path to the file
  - `row_from`: The starting row number
  - `row_to`: The ending row number
