(require 'chatgpt-shell)

;; Vars

(defvar hjerne-python-executable-path "python3"
  "Path to the Python executable.")

(defvar hjerne-install-path "~/path/to/hjerne"
  "Path to the Hjerne installation directory.")

(defvar hjerne-project-id nil
  "ID of the current project. New changesets will be added to this project.")

(defvar hjerne-changeset-id nil
  "ID of the current changeset.")

(defvar hjerne-replacement-file nil
  "Path to the replacement file.")

;; Helpers

(defun hjerne-shell-maker-get-prompt-content ()
  "Get the content of the command line (and any following command output) at point."
  (let ((begin (shell-maker--prompt-begin-position)))
    (buffer-substring-no-properties
     begin
     (save-excursion
       (goto-char (shell-maker--prompt-end-position))
       (re-search-forward (shell-maker-prompt-regexp shell-maker--config) nil t)
       (if (= begin (shell-maker--prompt-begin-position))
           (point-max)
         (shell-maker--prompt-begin-position))))))

(defun hjerne-get-current-git-branch ()
  "Get the current git branch name."
  (let ((branch (string-trim (shell-command-to-string "git rev-parse --abbrev-ref HEAD"))))
    (unless (or (string= branch "main") (string= branch "master"))
      branch)))

(defun hjerne-changeset-add ()
  "Add a new changeset to the current project."
  (interactive)
  (unless hjerne-project-id
    (error "hjerne-project-id is not set"))
  (unless hjerne-install-path
    (error "hjerne-install-path is not set"))
  (let* ((default-title (hjerne-get-current-git-branch))
         (title (read-string (if default-title
                                 (format "Enter changeset title (default: %s): " default-title)
                               "Enter changeset title: ")
                             nil nil default-title)))
    (shell-command (format "%s %s/manage.py changeset_add %d %s"
                           hjerne-python-executable-path
                           hjerne-install-path
                           hjerne-project-id
                           (shell-quote-argument title)))))

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

(defun hjerne-context-code ()
  "Output code for a given changeset and write to the replacement file."
  (interactive)
  (unless hjerne-changeset-id
    (error "hjerne-changeset-id is not set"))
  (unless hjerne-replacement-file
    (error "hjerne-replacement-file is not set"))
  (unless hjerne-install-path
    (error "hjerne-install-path is not set"))
  (with-temp-buffer
    (shell-command (format "%s %s/manage.py context_code %d"
                           hjerne-python-executable-path
                           hjerne-install-path
                           hjerne-changeset-id)
                   (current-buffer))
    (write-region (point-min) (point-max) hjerne-replacement-file)))

(defun hjerne-context-update (&optional custom-replacement-file from-markdown)
  "Update the context for a given changeset. Optionally use a custom replacement file and extract code from markdown."
  (interactive)
  (unless hjerne-changeset-id
    (error "hjerne-changeset-id is not set"))
  (let ((replacement-file (or custom-replacement-file hjerne-replacement-file)))
    (unless replacement-file
      (error "Replacement file is not set"))
    (unless hjerne-install-path
      (error "hjerne-install-path is not set"))
    (shell-command (format "%s %s/manage.py context_update %d %s %s"
                           hjerne-python-executable-path
                           hjerne-install-path
                           hjerne-changeset-id
                           replacement-file
                           (if from-markdown "--from-markdown" "")))))

(defun hjerne-send-context-code-to-chatgpt-shell ()
  "Send context code to ChatGPT shell with a prefix message."
  (interactive)
  (unless hjerne-replacement-file
    (error "hjerne-replacement-file is not set"))
  (let ((prefix "Please give a short description of the following code. Don't code anything just yet :)\n\n")
        (code (with-temp-buffer
                (insert-file-contents hjerne-replacement-file)
                (buffer-string))))
    (chatgpt-shell-send-to-buffer (concat prefix code))))

(defun hjerne-receive-replacement-from-chatgpt-shell ()
  "Receive replacement from ChatGPT shell, update context, and regenerate context code."
  (interactive)
  (let ((temp-replacement-file (make-temp-file "hjerne-replacement-"))
        (content (hjerne-shell-maker-get-prompt-content)))
    (with-temp-file temp-replacement-file
      (insert content))
    (let ((hjerne-replacement-file temp-replacement-file))
      (hjerne-context-update hjerne-replacement-file t)))
  (hjerne-context-code))

(defun hjerne-context-remove-at-point ()
  "Remove context from a changeset using the current line in the active buffer."
  (interactive)
  (unless hjerne-changeset-id
    (error "hjerne-changeset-id is not set"))
  (unless hjerne-install-path
    (error "hjerne-install-path is not set"))
  (let ((filename (buffer-file-name))
        (linenumber (line-number-at-pos)))
    (shell-command (format "%s %s/manage.py context_remove %d %s"
                           hjerne-python-executable-path
                           hjerne-install-path
                           hjerne-changeset-id
                           (shell-quote-argument (thing-at-point 'symbol))))))

(defun hjerne-fetch-changesets ()
  "Fetch the list of changesets."
  (let ((output (shell-command-to-string (format "%s %s/manage.py change_sets_list"
                                                 hjerne-python-executable-path
                                                 hjerne-install-path))))
    (split-string output "\n" t)))

(defun hjerne-select-changeset ()
  "Select a changeset and set `hjerne-changeset-id`."
  (interactive)
  (let* ((changesets (hjerne-fetch-changesets))
         (selection (completing-read "Select changeset: " changesets)))
    (setq hjerne-changeset-id (string-to-number (car (split-string selection " "))))))

(defun hjerne-get-current-git-branch ()
  "Get the current git branch name."
  (let ((branch (string-trim (shell-command-to-string "git rev-parse --abbrev-ref HEAD"))))
    (unless (or (string= branch "xmain") (string= branch "xmaster"))
      branch)))

(defun hjerne-changeset-add ()
  "Add a new changeset to the current project."
  (interactive)
  (unless hjerne-project-id
    (error "hjerne-project-id is not set"))
  (unless hjerne-install-path
    (error "hjerne-install-path is not set"))
  (let* ((default-title (hjerne-get-current-git-branch))
         (title (read-string (if default-title
                                 (format "Enter changeset title (default: %s): " default-title)
                               "Enter changeset title: ")
                             nil nil default-title)))
    (shell-command (format "%s %s/manage.py changeset_add %d %s"
                           hjerne-python-executable-path
                           hjerne-install-path
                           hjerne-project-id
                           (shell-quote-argument title)))))

(require 'hydra)

(defhydra hydra-hjerne (:color blue :hint nil)
  "
^Hjerne Commands^
-----------------------------------------
[_a_] Add changeset
[_c_] Add context
[_o_] Output context code
[_u_] Update context
[_r_] Remove context
[_s_] Select changeset
[_t_] Send context code to ChatGPT shell
[_g_] Receive replacement from ChatGPT shell
[_q_] Quit
"
  ("a" hjerne-changeset-add)
  ("c" hjerne-context-add)
  ("o" hjerne-context-code)
  ("u" hjerne-context-update)
  ("r" hjerne-context-remove-at-point)
  ("s" hjerne-select-changeset)
  ("t" hjerne-send-context-code-to-chatgpt-shell)
  ("g" hjerne-receive-replacement-from-chatgpt-shell)
  ("q" nil :color blue))

(provide 'hjerne)
