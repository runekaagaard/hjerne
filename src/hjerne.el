(defvar hjerne-changeset-id nil
  "The ID of the changeset to which the context will be added.")

(defvar hjerne-python-executable-path "python"
  "The path to the Python executable.")

(defvar hjerne-install-path nil
  "The path to the Hjerne installation directory.")

(defun hjerne-context-add ()
  "Add a context to the changeset using the current line in the active buffer."
  (interactive)
  (let ((filename (buffer-file-name))
        (linenumber (line-number-at-pos)))
    (unless hjerne-changeset-id
      (error "hjerne-changeset-id is not set"))
    (unless filename
      (error "Buffer is not visiting a file"))
    (unless hjerne-install-path
      (error "hjerne-install-path is not set"))
    (shell-command (format "%s %s/manage.py context_add %d %s %d"
                           hjerne-python-executable-path
                           hjerne-install-path
                           hjerne-changeset-id
                           filename
                           linenumber))))

(provide 'hjerne)
