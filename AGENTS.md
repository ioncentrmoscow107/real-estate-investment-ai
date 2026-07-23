# Codex working rules

Codex must complete each implementation task end-to-end without requiring the user to manually run tests, commit, or push, unless Windows permissions or GitHub authentication require one-time user action.

## Required workflow for every task

1. Inspect repository state:

git status --short
git branch --show-current
git remote -v

2. Make only the changes required for the requested task.

3. Run backend tests:

.\.venv\Scripts\python.exe -m pytest backend/tests

4. Run frontend checks:

cd frontend
npm.cmd run lint
npm.cmd run build
cd ..

5. If checks pass, create a task branch unless already on the correct task branch:

git checkout -b task-XXX-short-name

6. Stage only relevant files:

git add <specific files>

Do not use git add . unless the full status has been inspected and all changed files are intentional.

7. Before commit, verify staged files:

git status --short
git diff --cached --stat

8. Do not stage frontend/next-env.d.ts unless the task explicitly requires it.

9. Commit:

git commit -m "TASK-XXX: short description"

10. Push:

git push -u origin task-XXX-short-name

11. Verify final state:

git status
git log -1 --oneline
git branch --show-current

12. Final report must include:

* changed files;
* test results;
* lint/build results;
* branch name;
* commit hash;
* push status;
* exact errors if anything failed.

## If Git fails with .git/index.lock

Codex must not stop after the first failure.

Codex should:

1. Check for active Git processes:

Get-Process git -ErrorAction SilentlyContinue

2. Check whether lock file exists:

Test-Path .git\index.lock

3. If no Git process is running and lock exists, remove the stale lock:

Remove-Item ".git\index.lock" -Force

4. Retry:

git status --short

5. If the same permission error persists, do not force changes inside .git.

6. Use a clean clone or Codex worktree instead.

7. If push still fails, provide:

* exact command;
* exact error;
* changed files;
* test results;
* fallback manual commands.

## Branch policy

Codex must not commit directly to main.

Every task should use a separate branch:

task-XXX-short-name

Examples:

task-010-git-workflow
task-011-stabilization
task-012-manual-listing-import

## User intervention policy

The user should only be asked to intervene for:

1. one-time GitHub authentication;
2. Windows permission issues outside the repository;
3. manual review/merge decision;
4. choosing between multiple risky migration options.

The user should not be asked to manually run tests, commit, or push during normal tasks.
