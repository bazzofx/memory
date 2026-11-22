# Environments — OS, tools, configurations and dependencies

Load when: running commands, installing things, or debugging "works elsewhere" problems.
Format: `- [YYYY-MM-DD] <fact>.` Update in place when a version changes. Newest first.

- [2026-11-22] Main machine: Windows 10 Pro; Claude Code's Bash tool is Git Bash (POSIX paths like `/c/...`; `cygpath` available). Commands given to the user run in PowerShell.
- [2026-11-22] Node v22 is installed and on PATH (used for project hooks).
- [2026-11-22] Git converts LF→CRLF on commit (`core.autocrlf`); the "LF will be replaced by CRLF" warning is expected and harmless.
