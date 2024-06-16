# Hjerne

Hjerne is an app for managing projects, changesets, and contexts. It uses Tree-sitter to understand the code and supports sending changesets into a changeset file or the Emacs ChatGPT-shell buffer and merging the updated code directly back into your project.

## Features

- 📁 **Project Management**: Add, list, and manage projects. Each project has an ID, title, and description.
- 🌳 **Changeset Management**: Add, list, and manage changesets within a project. Changesets represent a collection of changes or contexts.
- 📝 **Context Management**: Add, remove, and update contexts within a changeset. Contexts represent specific code elements (like functions, classes, or variables).
- 🌐 **Integration with Tree-sitter**: Utilize Tree-sitter for parsing and analyzing source code to identify top-level symbols and nodes.
- 🧠 **Integration with ChatGPT**: Send and receive context code to and from a ChatGPT shell for code analysis or generation.
- 🛠️ **Elisp Integration**: Integrate with Emacs, providing functions to interact with Django management commands and manage projects, changesets, and contexts.
- 🗃️ **Django Admin**: Manage projects, changesets, and contexts through the Django admin interface.
- 🗂️ **Hydra Menu**: Uses Hydra in Emacs for easy access to various management functions.

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

### `context_add_range`
Adds contexts to a changeset for a given range of lines in a file.

Usage:
```sh
python manage.py context_add_range <changeset_id> <file_path> <from_line> <to_line>
```

### `context_remove`

Removes a context from a changeset.

Usage:
```sh
python manage.py context_remove <changeset_id> <filename> <linenumber>
```

### `context_update`

Updates the context for a given changeset.

### `treesitter_top_level_symbols_in_range`
Outputs top-level symbols in a given range for a given file using Tree-sitter.

Usage:
```sh
python manage.py treesitter_top_level_symbols_in_range <file_path> <row_from> <row_to>
```

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

## Emacs Integration

Hjerne provides a set of Emacs Lisp functions to interact with the Django management commands and manage projects, changesets, and contexts directly from Emacs. The functions are accessible through a Hydra menu for easy access.

### Installation

To use Hjerne with Emacs, add the following to your `init.el` file:

```emacs-lisp
(add-to-list 'load-path "/install/path/to/hjerne/src")
(require 'hjerne)
(setq hjerne-install-path "/install/path/to/hjerne/src")
(setq hjerne-replacement-file "/path/to/my/changeset.py")
(setq hjerne-python-executable-path "/path/to/python")
(setq chatgpt-shell-prompt-query-response-style 'shell)
```

### Key Functions

- `hjerne-project-add`: Add a new project and update `hjerne-project-id`.
- `hjerne-project-select`: Select a project and set `hjerne-project-id`.
- `hjerne-changeset-add`: Add a new changeset to the current project.
- `hjerne-changeset-select`: Select a changeset for the given project and set `hjerne-changeset-id`.
- `hjerne-context-add-dwim`: Add context to a changeset using the current line in the active buffer or a selected region.
- `hjerne-context-remove`: Remove context from a changeset using the current line in the active buffer.
- `hjerne-context-code`: Output code for a given changeset and write to the replacement file.
- `hjerne-context-update`: Update the context for a given changeset.
- `hjerne-send-context-code-to-chatgpt-shell`: Send context code to ChatGPT shell with a prefix message.
- `hjerne-receive-replacement-from-chatgpt-shell`: Receive replacement from ChatGPT shell, update context, and regenerate context code.
- `hjerne-changeset-clear-context`: Clear all contexts in the current changeset.
- `hjerne-context-add-ag`: Add contexts from the current ag-mode buffer to the current changeset.

### Hydra Menu

```emacs-lisp
^Hjerne^
^Project^          ^Changeset^       ^Context^         ^Other^
------------------------------------------------------------------------------
[_p_] Select       [_A_] Add         [_a_] Add         [_,_] chatgpt-shell send
[_P_] Add          [_S_] Select      [_r_] Remove      [_._] chatgpt-shell receive
^ ^                [_C_] Clear       [_w_] Write       [_q_] Quit
^ ^                ^ ^               [_u_] Update
^ ^                ^ ^               [_g_] Add from ag

Project: %`hjerne-project-id %s`hjerne-project-title
Changeset: %`hjerne-changeset-id %s`hjerne-changeset-title
```
```

## Getting Started

To get started with Hjerne, follow these steps to set up your environment and begin managing your projects efficiently:

1. Clone the repository.
2. Install the required dependencies listed in `requirements.txt`.
3. Set up your Django environment and run the necessary migrations.
4. Start using the management commands to add projects, changesets, and contexts.
5. Integrate with Emacs for an enhanced coding experience.
