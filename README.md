# About Hjerne

Hjerne is a Django project that serves as a complete ChatGPT coder agent. It offers a range of features to streamline your coding workflow and enhance productivity. 🚀

## Features

- 🌳 **Tree-sitter Context Management**: Manage specific variables, classes, and functions for the agent.
- 📁 **Project Management**: Add projects, which contain changesets, which in turn contain contexts.
- 🆕 **Project and Changeset Management**: Easily add and list projects and changesets.
- 🧹 **Context Management**: Add, remove, clear, and update contexts within changesets.
- 📝 **Code Output**: Output code for a given changeset.
- 🧠 **Integration with ChatGPT**: Send and receive context code to and from ChatGPT shell.
- 🛠️ **Management Commands**: Utilize various management commands to streamline operations.
- 🧠 **Integration with ChatGPT**: Send and receive context code to and from ChatGPT shell.

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
