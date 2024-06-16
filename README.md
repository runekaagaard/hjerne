Hjerne is a django project that is a complete chatgpt coder agent, with:

- Tree-sitter context management. Include specific variables, classes and functions for the agent.
- Project management. Add projects, which contains changesets which contains contexts.

## Management Commands

### `project_add`

Adds a new project.

Usage:
```sh
python manage.py project_add <title> <description>
```

### `project_list`

Lists all projects with their IDs and titles.

Usage:
```sh
python manage.py project_list
```

### `changeset_add`

Adds a new changeset to a project.

Usage:
```sh
python manage.py changeset_add <project_id> <title>
```

### `changeset_list`

Lists all changesets for a given project.

Usage:
```sh
python manage.py changeset_list <project_id>
```

### `changeset_clear_context`

Clears all contexts in a changeset.

Usage:
```sh
python manage.py changeset_clear_context <changeset_id>
```

### `context_add`

Adds a context to a changeset.

Usage:
```sh
python manage.py context_add <changeset_id> <filename> <linenumber>
```

### `context_remove`

Removes a context from a changeset.

Usage:
```sh
python manage.py context_remove <changeset_id> <filename> <linenumber>
```

### `context_update`

Updates the context for a given changeset.

Usage:
```sh
python manage.py context_update <changeset_id> <replacement_file> [--from-markdown]
```

### `context_code`

Outputs code for a given changeset.

Usage:
```sh
python manage.py context_code <changeset_id>
```
