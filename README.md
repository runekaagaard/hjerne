# Hjerne

Hjerne is a Django-based application for managing projects, changesets, and contexts. It uses Tree-sitter to understand code and supports sending changesets into a changeset file or the Emacs ChatGPT-shell buffer, and merging the updated code directly back into your project.

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

### Project Management

- `project_add`: Add a new project.
- `project_list`: List all projects with their IDs and titles.

### Changeset Management

- `changeset_add`: Add a new changeset to a project.
- `changeset_list`: List all changesets for a given project.
- `changeset_clear_context`: Clear all contexts in a changeset.

### Context Management

- `context_add`: Add a context to a changeset.
- `context_add_range`: Add contexts to a changeset for a given range of lines in a file.
- `context_remove`: Remove a context from a changeset.
- `context_remove_range`: Remove contexts from a changeset for a given range of lines in a file.
- `context_update`: Update the context for a given changeset.
- `context_update_markdown`: Update the context for a given changeset using a markdown file.
- `context_code`: Output code for a given changeset.
- `context_code_markdown`: Output code for a given changeset in markdown format, grouped by language.

### Tree-sitter Integration

- `treesitter_top_level_symbols`: Output top-level symbols for a given file using Tree-sitter.
- `treesitter_top_level_symbols_in_range`: Output top-level symbols in a given range for a given file using Tree-sitter.

## Emacs Integration

Hjerne provides a set of Emacs Lisp functions to interact with the Django management commands and manage projects, changesets, and contexts directly from Emacs. The functions are accessible through a Hydra menu for easy access.

### Installation

To use Hjerne with Emacs, add the following to your `init.el` file:

```emacs-lisp
(add-to-list 'load-path "/path/to/hjerne/src")
(require 'hjerne)
(setq hjerne-install-path "/path/to/hjerne/src")
(setq hjerne-replacement-file "/path/to/changeset.py")
(setq hjerne-python-executable-path "/path/to/python")
(setq chatgpt-shell-prompt-query-response-style 'shell)
```

### Key Functions

- `hjerne-project-add`: Add a new project and update `hjerne-project-id`.
- `hjerne-project-select`: Select a project and set `hjerne-project-id`.
- `hjerne-changeset-add`: Add a new changeset to the current project.
- `hjerne-changeset-select`: Select a changeset for the given project and set `hjerne-changeset-id`.
- `hjerne-context-add-dwim`: Add context to a changeset using the current line in the active buffer or a selected region.
- `hjerne-context-remove-dwim`: Remove context from a changeset using the current line in the active buffer or a selected region.
- `hjerne-context-code`: Output code for a given changeset and write to the replacement file.
- `hjerne-context-update-markdown`: Update the context for a given changeset using a markdown file.
- `hjerne-send-context-code-to-chatgpt-shell`: Send context code to ChatGPT shell with a prefix message.
- `hjerne-receive-replacement-from-chatgpt-shell`: Receive replacement from ChatGPT shell, update context, and regenerate context code.
- `hjerne-changeset-clear-context`: Clear all contexts in the current changeset.
- `hjerne-context-add-ag`: Add contexts from the current ag-mode buffer to the current changeset.

### Hydra Menu

Hjerne provides a Hydra menu for easy access to its functions:

```
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

## Getting Started

To get started with Hjerne:

1. Clone the repository.
2. Install the required dependencies listed in `requirements.txt`.
3. Set up your Django environment and run the necessary migrations.
4. Start using the management commands to add projects, changesets, and contexts.
5. Integrate with Emacs for an enhanced coding experience.

For detailed usage instructions, refer to the individual command descriptions and Emacs function documentation.
