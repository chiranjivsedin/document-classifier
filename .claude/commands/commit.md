---
description: Stage and commit current changes using Conventional Commits.
argument-hint: [optional commit message hint]
---

Create a focused commit that follows Conventional Commits.

1. Run `git status` (no `-uall`) and `git diff` (staged + unstaged) to understand the changes. Also run `git log -5 --oneline` to match this repo's commit style.
2. Optional user hint to factor in: **$ARGUMENTS**
3. Stage relevant files **by name** — avoid `git add -A` / `git add .` so secrets and large artifacts don't slip in. Refuse to stage anything that looks like a secret (`.env*`, credentials, API keys, model weights).
4. Compose the message — **subject line only by default**:
   - **Type**: `feat` | `fix` | `chore` | `docs` | `refactor` | `test` | `perf` | `style` | `build` | `ci`
   - **Scope** (optional, lowercase, narrow): e.g. `api`, `pipeline`, `config`, `deps`, `ocr`, `classifier`
   - **Subject**: imperative mood ("add", not "added"), ≤72 chars, no trailing period
   - **Body**: omit unless the user asks for one, or the *why* is genuinely non-obvious from the diff. Keep it terse when included.
   - **Footers** (only when relevant): `BREAKING CHANGE: …`, `Refs: …`
5. Run the commit via a HEREDOC so multi-line bodies format correctly.
6. Run `git status` afterward to confirm a clean tree.

Rules:
- One logical change per commit. If the diff spans unrelated changes, ask whether to split.
- Never use `--no-verify`. Never amend or push unless the user explicitly asks.
- If a pre-commit hook fails, fix the underlying issue and create a new commit (do not amend).
- **Do not add `Co-Authored-By: Claude ...` or any AI co-author trailer.** End the message at the body.
