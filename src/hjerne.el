(require 'chatgpt-shell)

;; Vars

(defvar hjerne-python-executable-path "python3"
  "Path to the Python executable.")

(defvar hjerne-install-path "~/path/to/hjerne"
  "Path to the Hjerne installation directory.")

(defvar hjerne-project-id nil
  "ID of the current project. New changesets will be added to this project.")

(defvar hjerne-project-title "N/A"
  "Title of the current project.")

(defvar hjerne-changeset-id nil
  "ID of the current changeset.")

(defvar hjerne-changeset-title "N/A"
  "Title of the current changeset.")

(defvar hjerne-replacement-file nil
  "Path to the replacement file.")

;; Helpers

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
    (let ((output (shell-command-to-string (format "%s %s/manage.py changeset_add %d %s"
                                                   hjerne-python-executable-path
                                                   hjerne-install-path
                                                   hjerne-project-id
                                                   (shell-quote-argument title)))))
      (if (string-match "ID \\([0-9]+\\)" output)
          (let ((changeset-id (string-to-number (match-string 1 output))))
            (setq hjerne-changeset-id changeset-id)
            (setq hjerne-changeset-title title))
        (error "Failed to add changeset")))))

(defun hjerne-context-add-dwim ()
  "Add context to a changeset using the current line in the active buffer or a selected region."
  (interactive)
  (let ((filename (buffer-file-name))
        (start-line (if (use-region-p) (line-number-at-pos (region-beginning)) (line-number-at-pos (point))))
        (end-line (if (use-region-p) (line-number-at-pos (region-end)) (line-number-at-pos (point)))))
    (shell-command (format "%s %s/manage.py context_add_range %d %s %d %d"
                           hjerne-python-executable-path
                           hjerne-install-path
                           hjerne-changeset-id
                           (shell-quote-argument filename)
                           start-line
                           end-line))))

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
    (shell-command (format "%s %s/manage.py context_code_markdown %d"
                           hjerne-python-executable-path
                           hjerne-install-path
                           hjerne-changeset-id)
                   (current-buffer))
    (write-region (point-min) (point-max) hjerne-replacement-file))
  (find-file hjerne-replacement-file))

(defun hjerne-context-update (replacement-file)
  "Update the context for a given changeset."
  (interactive)
  (unless hjerne-changeset-id
    (error "hjerne-changeset-id is not set"))
  (unless hjerne-replacement-file
    (error "hjerne-replacement-file is not set"))
  (unless hjerne-install-path
    (error "hjerne-install-path is not set"))
  (shell-command (format "%s %s/manage.py context_update --from-markdown %d %s"
                         hjerne-python-executable-path
                         hjerne-install-path
                         hjerne-changeset-id
                         replacement-file)))

(defun hjerne-context-update-markdown ()
  "Update the context for a given changeset using a markdown file."
  (interactive)
  (unless hjerne-changeset-id
    (error "hjerne-changeset-id is not set"))
  (unless hjerne-replacement-file
    (error "hjerne-replacement-file is not set"))
  (unless hjerne-install-path
    (error "hjerne-install-path is not set"))
  (with-current-buffer (find-file-noselect hjerne-replacement-file)
    (save-buffer))
  (shell-command (format "%s %s/manage.py context_update_markdown %d %s"
                         hjerne-python-executable-path
                         hjerne-install-path
                         hjerne-changeset-id
                         hjerne-replacement-file)))

(defun hjerne-context-update-markdown-todo (replacement-file)
  "Update the context for a given changeset using a markdown file."
  (interactive)
  (unless hjerne-changeset-id
    (error "hjerne-changeset-id is not set"))
  (unless hjerne-replacement-file
    (error "hjerne-replacement-file is not set"))
  (unless hjerne-install-path
    (error "hjerne-install-path is not set"))
  (shell-command (format "%s %s/manage.py context_update_markdown %d %s"
                         hjerne-python-executable-path
                         hjerne-install-path
                         hjerne-changeset-id
                         replacement-file)))

(defun hjerne-send-context-code-to-chatgpt-shell ()
  "Send context code to ChatGPT shell with a prefix message."
  (interactive)
  (unless hjerne-changeset-id
    (error "hjerne-changeset-id is not set"))
  (unless hjerne-install-path
    (error "hjerne-install-path is not set"))
  (let ((prefix "\n\nWhen working with the code below it's super important that you repeat the `## file:` lines above each markdown code block.\n\nFor now just give a short summary of it. Don't repeat the code back to me! Remember to write the `## file:` lines EXACTLY the same!\n\n")
        (code (with-temp-buffer
                (shell-command (format "%s %s/manage.py context_code_markdown %d"
                                       hjerne-python-executable-path
                                       hjerne-install-path
                                       hjerne-changeset-id)
                               (current-buffer))
                (buffer-string))))
    (let ((chatgpt-buffer (car (seq-filter (lambda (buf) (string-prefix-p "*chatgpt" (buffer-name buf))) (buffer-list)))))
      (unless chatgpt-buffer
        (chatgpt-shell)
        (setq chatgpt-buffer (car (seq-filter (lambda (buf) (string-prefix-p "*chatgpt" (buffer-name buf))) (buffer-list)))))
      (with-current-buffer chatgpt-buffer
        (comint-clear-buffer)
        (chatgpt-shell-send-to-buffer (concat prefix code))))))

(defun hjerne-receive-replacement-from-chatgpt-shell (command output)
  "Receive replacement from ChatGPT shell, update context, and regenerate context code."
  (let ((temp-replacement-file (make-temp-file "hjerne-replacement-")))
    (with-temp-file temp-replacement-file
      (insert output))
    (let ((hjerne-replacement-file temp-replacement-file))
      (hjerne-context-update-markdown-todo hjerne-replacement-file))))

(add-hook 'chatgpt-shell-after-command-functions #'hjerne-receive-replacement-from-chatgpt-shell)

(defun hjerne-changeset-clear-context ()
  "Clear all contexts in the current changeset."
  (interactive)
  (unless hjerne-changeset-id
    (error "hjerne-changeset-id is not set"))
  (unless hjerne-install-path
    (error "hjerne-install-path is not set"))
  (shell-command (format "%s %s/manage.py changeset_clear_context %d"
                         hjerne-python-executable-path
                         hjerne-install-path
                         hjerne-changeset-id)))

(defun hjerne-context-add-ag ()
  "Add contexts from the current ag-mode buffer to the current changeset."
  (interactive)
  (unless hjerne-changeset-id
    (error "hjerne-changeset-id is not set"))
  (unless hjerne-install-path
    (error "hjerne-install-path is not set"))
  (unless (derived-mode-p 'ag-mode)
    (error "This function must be run in an ag-mode buffer"))
  (let ((project-root (ag/project-root default-directory)))
    (save-excursion
      (goto-char (point-min))
      (while (re-search-forward "^\\([^: ]+\\):\\([0-9]+\\):" nil t)
        (let ((file (expand-file-name (match-string 1) project-root))
              (line (string-to-number (match-string 2))))
          (when (file-exists-p file)
            (shell-command (format "%s %s/manage.py context_add %d %s %d"
                                   hjerne-python-executable-path
                                   hjerne-install-path
                                   hjerne-changeset-id
                                   (shell-quote-argument file)
                                   line))))))))

(defun hjerne-show-buffer (filename)
  "Show the buffer for the given FILENAME. If the buffer is visible, switch to it. If a buffer exists, make it visible. If not, open it."
  (let ((buffer (find-buffer-visiting filename)))
    (if buffer
        (if (get-buffer-window buffer 'visible)
            (select-window (get-buffer-window buffer))
          (switch-to-buffer buffer))
      (find-file filename))))

(defun hjerne-fetch-projects ()
  "Fetch the list of projects."
  (let ((output (shell-command-to-string (format "%s %s/manage.py project_list"
                                                 hjerne-python-executable-path
                                                 hjerne-install-path))))
    (split-string output "\n" t)))

(defun hjerne-fetch-changesets (project-id)
  "Fetch the list of changesets for a given project."
  (let ((output (shell-command-to-string (format "%s %s/manage.py changeset_list %d"
                                                 hjerne-python-executable-path
                                                 hjerne-install-path
                                                 project-id))))
    (split-string output "\n" t)))

(defun hjerne-project-select ()
  "Select a project and set `hjerne-project-id`."
  (interactive)
  (let* ((projects (hjerne-fetch-projects))
         (selection (completing-read "Select project: " projects)))
    (let* ((project-info (split-string selection " " t))
           (project-id (string-to-number (car project-info)))
           (project-title (mapconcat 'identity (cdr project-info) " ")))
      (setq hjerne-project-id project-id)
      (setq hjerne-project-title project-title))
    (setq hjerne-changeset-id nil)))
    
(defun hjerne-changeset-select (project-id)
  "Select a changeset for the given project and set `hjerne-changeset-id`."
  (interactive (list hjerne-project-id))
  (let* ((changesets (hjerne-fetch-changesets project-id))
         (selection (completing-read "Select changeset: " changesets)))
    (let* ((changeset-info (split-string selection " " t))
           (changeset-id (string-to-number (car changeset-info)))
           (changeset-title (mapconcat 'identity (cdr changeset-info) " ")))
      (setq hjerne-changeset-id changeset-id)
      (setq hjerne-changeset-title changeset-title))))

(defun hjerne-get-current-git-branch ()
  "Get the current git branch name."
  (let ((branch (string-trim (shell-command-to-string "git rev-parse --abbrev-ref HEAD"))))
    (unless (or (string= branch "xmain") (string= branch "xmaster"))
      branch)))

(defun hjerne-project-add ()
  "Add a new project and update `hjerne-project-id`."
  (interactive)
  (unless hjerne-install-path
    (error "hjerne-install-path is not set"))
  (let ((title (read-string "Enter project title: "))
        (description (read-string "Enter project description: ")))
    (let ((output (shell-command-to-string (format "%s %s/manage.py project_add %s %s"
                                                   hjerne-python-executable-path
                                                   hjerne-install-path
                                                   (shell-quote-argument title)
                                                   (shell-quote-argument description)))))
      (if (string-match "ID \\([0-9]+\\)" output)
          (progn
            (let ((project-id (string-to-number (match-string 1 output))))
              (setq hjerne-project-id project-id)
              (setq hjerne-project-title title))
            (setq hjerne-changeset-id nil))
        (error "Failed to add project")))))

(defun hjerne-context-remove-dwim ()
  "Remove context from a changeset using the current line in the active buffer or a selected region."
  (interactive)
  (let ((filename (buffer-file-name))
        (start-line (if (use-region-p) (line-number-at-pos (region-beginning)) (line-number-at-pos (point))))
        (end-line (if (use-region-p) (line-number-at-pos (region-end)) (line-number-at-pos (point)))))
    (if (use-region-p)
        (shell-command (format "%s %s/manage.py context_remove_range %d %s %d %d"
                               hjerne-python-executable-path
                               hjerne-install-path
                               hjerne-changeset-id
                               (shell-quote-argument filename)
                               start-line
                               end-line))
      (shell-command (format "%s %s/manage.py context_remove %d %s %d"
                             hjerne-python-executable-path
                             hjerne-install-path
                             hjerne-changeset-id
                             (shell-quote-argument filename)
                             start-line)))))


(require 'hydra)

(defhydra hydra-hjerne (:color blue :hint nil)
"
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
"
  ("p" hjerne-project-select)
  ("P" hjerne-project-add)
  ("A" hjerne-changeset-add)
  ("S" hjerne-changeset-select)
  ("a" hjerne-context-add-dwim)
  ("r" hjerne-context-remove-dwim)
  ("C" hjerne-changeset-clear-context)
  ("w" hjerne-context-code)
  ("u" hjerne-context-update-markdown)
  ("g" hjerne-context-add-ag)
  ("," hjerne-send-context-code-to-chatgpt-shell)
  ("." hjerne-receive-replacement-from-chatgpt-shell)
  ("q" nil :color blue))

(global-set-key (kbd "s-h") 'hydra-hjerne/body)

(provide 'hjerne)
