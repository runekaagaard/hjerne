(defvar hjerne-changeset-id nil
  "The ID of the changeset to which the context will be added.")

(defun hjerne-context-add ()
  "Add a context to the changeset using the current line in the active buffer."
  (interactive)
  (let ((filename (buffer-file-name))
        (linenumber (line-number-at-pos)))
    (unless hjerne-changeset-id
      (error "hjerne-changeset-id is not set"))
    (unless filename
      (error "Buffer is not visiting a file"))
    (shell-command (format "python manage.py context_add %d %s %d"
                           hjerne-changeset-id
                           filename
                           linenumber))))

(provide 'hjerne)
