
;; Added by Package.el.  This must come before configurations of
;; installed packages.  Don't delete this line.  If you don't want it,
;; just comment it out by adding a semicolon to the start of the line.
;; You may delete these explanatory comments.
;;(package-initialize)

(when (>= emacs-major-version 24)
  (require 'package)
  (package-initialize)
  (add-to-list 'package-archives '("melpa" . "http://melpa.org/packages/") t)
  )
(require 'cl)

;;add whatever packages you want here

(defvar jie/packages '(
		       company
		       monokai-theme
		       hungry-delete
		       ;;smex
		       swiper
		       counsel
		       smartparens
		       js2-mode
		       exec-path-from-shell
		       ) "Default packages")

;;(setq package-selected-packages jie/packages)

(defun jie/packages-installed-p ()
  (loop for pkg in jie/packages
	when (not (package-installed-p pkg)) do (return nil)
	finally (return t)))
(unless (jie/packages-installed-p)
  (message "%s" "Refreshing package database...")
  (package-refresh-contents)
  (dolist (pkg jie/packages)
    (when (not (package-installed-p pkg))
      (package-install pkg))))

;;let emacs could find the execuable
(when (memq window-system '(mac ns))
  (exec-path-from-shell-initialize))

(tool-bar-mode -1)  ;关掉工具栏
(scroll-bar-mode -1) ;关掉滚动条
;;(electric-indent-mode -1)
(global-linum-mode t) ;显示行号
(setq inhibit-splash-screen t) ;关闭启动画面


(defun open-my-init-file()
  (interactive)
  (find-file "~/.emacs.d/init.el"))

(global-set-key (kbd "<f2>") 'open-my-init-file)

;;(recentf-mode t) ;最近打开的文件
(global-company-mode t)
(setq-default cursor-type 'bar)

;;(setq make-backup-files nil)  ;

;;(require 'org)
;;(setq org-src-fontify-natively t)  ;支持org语法高亮
(load-theme 'monokai t)
(require 'hungry-delete)
(global-hungry-delete-mode)


;;支持最近打开文件
(require 'recentf)
(recentf-mode 1)
(setq recentf-max-menu-items 25)
(global-set-key "\C-x\ \C-r" 'recentf-open-files)


(delete-selection-mode t)

;;(setq initial-frame-alist (quote ((fullscreen . maximized)))) ;启动最大化
(add-hook 'emacs-lisp-mode 'show-paren-mode)

(global-hl-line-mode)  ;;显示当前行位置
;;smex  meta-x的使用效率
;;(require 'smex) ; Not needed if you use package.el
;;(smex-initialize) ; Can be omitted. This might cause a (minimal) delay
;; when Smex is auto-initialized on its first run.
;;(global-set-key (kbd "M-x") 'smex)

;;swiper
(ivy-mode 1)
(setq ivy-use-virtual-buffers t)
(setq enable-recursive-minibuffers t)
(global-set-key "\C-s" 'swiper)
(global-set-key (kbd "C-c C-r") 'ivy-resume)
;;(global-set-key (kbd "<f6>") 'ivy-resume)
(global-set-key (kbd "M-x") 'counsel-M-x)
(global-set-key (kbd "C-x C-f") 'counsel-find-file)
(global-set-key (kbd "<f1> f") 'counsel-describe-function)
(global-set-key (kbd "<f1> v") 'counsel-describe-variable)

;;smartparens
(require 'smartparens-config)
(add-hook 'emacs-lisp-mode-hook 'smartparens-mode)

;;config js2-mode
(setq auto-mode-alist
      (append
       '(("\\.js\\'" . js2-mode))
       auto-mode-alist))

;;org mode日程安排
;;(setq org-agenda-files '(org-agenda))
;;(global-set-key (kbd "C-c a" 'org-agenda))

(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(custom-safe-themes
   (quote
    ("8ed752276957903a270c797c4ab52931199806ccd9f0c3bb77f6f4b9e71b9272" default)))
 '(package-selected-packages
   (quote
    (exec-path-from-shell js2-mode counsel swiper smex company))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
