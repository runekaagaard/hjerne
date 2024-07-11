# HJERNE MANAGEMENT COMMANDS

Usage: python manage.py <command> [options] [arguments]

## project_add

```bash
Usage: python manage.py project_add <title> <description>

Add a new project to the system.

Arguments:
  title         The title of the project
  description   The description of the project

Options:
  -h, --help    Show this help message and exit
```

## project_list

```bash
Usage: python manage.py project_list

List all projects with their IDs and titles.

Options:
  -h, --help    Show this help message and exit
```

## changeset_add

```bash
Usage: python manage.py changeset_add <project_id> <title>

Add a new changeset to a project.

Arguments:
  project_id    The ID of the project
  title         The title of the changeset

Options:
  -h, --help    Show this help message and exit
```

## changeset_list

```bash
Usage: python manage.py changeset_list <project_id>

List all changesets for a given project.

Arguments:
  project_id    The ID of the project

Options:
  -h, --help    Show this help message and exit
```

## changeset_clear_context

```bash
Usage: python manage.py changeset_clear_context <changeset_id>

Clear all contexts in a changeset.

Arguments:
  changeset_id  The ID of the changeset

Options:
  -h, --help    Show this help message and exit
```

## context_add

```bash
Usage: python manage.py context_add <changeset_id> <filename> <linenumber>

Add a context to a changeset.

Arguments:
  changeset_id  The ID of the changeset
  filename      The name of the file
  linenumber    The line number in the file

Options:
  -h, --help    Show this help message and exit
```

## context_add_range

```bash
Usage: python manage.py context_add_range <changeset_id> <file_path> <from_line> <to_line>

Add contexts to a changeset for a given range of lines in a file.

Arguments:
  changeset_id  The ID of the changeset
  file_path     The path to the file
  from_line     The starting line number
  to_line       The ending line number

Options:
  -h, --help    Show this help message and exit
```

## context_remove

```bash
Usage: python manage.py context_remove <changeset_id> <filename> <linenumber>

Remove a context from a changeset.

Arguments:
  changeset_id  The ID of the changeset
  filename      The name of the file
  linenumber    The line number in the file

Options:
  -h, --help    Show this help message and exit
```

## context_remove_range

```bash
Usage: python manage.py context_remove_range <changeset_id> <file_path> <from_line> <to_line>

Remove contexts from a changeset for a given range of lines in a file.

Arguments:
  changeset_id  The ID of the changeset
  file_path     The path to the file
  from_line     The starting line number
  to_line       The ending line number

Options:
  -h, --help    Show this help message and exit
```

## context_update

```bash
Usage: python manage.py context_update <changeset_id> <replacement_file> [--from-markdown]

Update the context for a given changeset.

Arguments:
  changeset_id      The ID of the changeset
  replacement_file  The path to the replacement file

Options:
  --from-markdown   Extract code from markdown blocks
  -h, --help        Show this help message and exit
```

## context_update_markdown

```bash
Usage: python manage.py context_update_markdown <changeset_id> <markdown_file>

Update the context for a given changeset using a markdown file.

Arguments:
  changeset_id    The ID of the changeset
  markdown_file   The path to the markdown file

Options:
  -h, --help      Show this help message and exit
```

## context_code

```bash
Usage: python manage.py context_code <changeset_id>

Output code for a given changeset.

Arguments:
  changeset_id  The ID of the changeset

Options:
  -h, --help    Show this help message and exit
```

## context_code_markdown

```bash
Usage: python manage.py context_code_markdown <changeset_id>

Output code for a given changeset in markdown format, grouped by language.

Arguments:
  changeset_id  The ID of the changeset

Options:
  -h, --help    Show this help message and exit
```

For more information on a specific command, run:
  python manage.py <command> --help
