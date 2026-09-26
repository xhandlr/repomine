# repomine — project conventions

## Issues (GitHub)
- Before starting any non-trivial task, run `gh issue list` and check if it matches an open issue.
- If a task corresponds to an existing issue, reference it in the proposal and in the commit (e.g. `Refs #2`, or `Closes #2` if it fully resolves it).
- When a new feature/metric idea comes up in conversation and it's already been approved as something to build, register it as a GitHub issue automatically — no need to ask each time.
- Do NOT auto-create an issue when:
  - the idea hasn't been approved yet — it's still exploratory/undecided
  - it would contain personal information
  - it touches sensitive or internal details (e.g. specifics of a teammate's repo/work, credentials, private data)

  In those cases, ask first instead of creating it, or keep it in conversation only.

## Commits
- Always in English.
- Subject line: imperative mood, under 72 characters (e.g. "add", not "added" or "adding").
- Blank line, then a body explaining what changed and why, when it's not obvious from the subject alone.
- Never run `git commit` without being explicitly asked to, in that same message.
- Reference the related issue number when one exists.

## Language
- Commits, README, and all new docs: English.
- `core/git/classifier.py` keyword support: keep both English and Spanish — this is about the analyzed repos' commit language, not repomine's own.
