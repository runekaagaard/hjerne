(defvar hjerne-python-executable-path "python3"
  "Path to the Python executable.")

(defvar hjerne-install-path "~/path/to/hjerne"
  "Path to the Hjerne installation directory.")

(defvar hjerne-changeset-id nil
  "ID of the current changeset.")

(defvar hjerne-replacement-file nil
  "Path to the replacement file.")

(defun hjerne-context-add ()
  "Add context to a changeset using the current line in the active buffer."
  (interactive)
  (unless hjerne-changeset-id
    (error "hjerne-changeset-id is not set"))
  (unless hjerne-install-path
    (error "hjerne-install-path is not set"))
  (let ((filename (buffer-file-name))
        (linenumber (line-number-at-pos)))
    (shell-command (format "%s %s/manage.py context_add %d %s %d"
                           hjerne-python-executable-path
                           hjerne-install-path
                           hjerne-changeset-id
                           filename
                           linenumber))))

(defun hjerne-context-code (replacement-file)
  "Output code for a given changeset and write to the replacement file."
  (interactive "FReplacement file: ")
  (unless hjerne-changeset-id
    (error "hjerne-changeset-id is not set"))
  (unless hjerne-install-path
    (error "hjerne-install-path is not set"))
  (with-temp-buffer
    (shell-command (format "%s %s/manage.py context_code %d"
                           hjerne-python-executable-path
                           hjerne-install-path
                           hjerne-changeset-id)
                   (current-buffer))
    (write-region (point-min) (point-max) replacement-file)))

(defun hjerne-context-update ()
  "Update the context for a given changeset."
  (interactive)
  (unless hjerne-changeset-id
    (error "hjerne-changeset-id is not set"))
  (unless hjerne-replacement-file
    (error "hjerne-replacement-file is not set"))
  (unless hjerne-install-path
    (error "hjerne-install-path is not set"))
  (shell-command (format "%s %s/manage.py context_update %d %s"
                         hjerne-python-executable-path
                         hjerne-install-path
                         hjerne-changeset-id
                         hjerne-replacement-file)))

(provide 'hjerne)
