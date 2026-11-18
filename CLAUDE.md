# Project memory

## Session start
- Read `AGENTS/README.md` (index). Read other files there only if relevant to the task.
- If `AGENTS/` is missing, create it with the layout below.

## After each task (before reporting done)
Update `AGENTS/`:
- `progress.md`: one entry (date, task, outcome, open items). Newest first.
- `decisions.md`: key technical decisions + why (and alternatives rejected).
- `conventions.md`: build/test/run commands, code conventions, project structure.
- `gotchas.md`: pitfalls, non-obvious bugs, fixes.
- `README.md`: keep the index and ≤10-line project summary current.

## Layout
AGENTS/
  README.md       index + summary
  progress.md     task log
  decisions.md    decisions + rationale
  conventions.md  commands, conventions
  gotchas.md      pitfalls + fixes

## Writing rules
- Record only what future sessions need and can't quickly infer from the code.
- Edit or delete stale entries; don't just append.
- Max 1-3 lines per entry. Reference file paths instead of pasting code.
- Never store secrets, tokens, passwords, or connection strings.
- Skip session-specific noise (temporary errors, debug logs).
- Nothing new worth recording → don't update.
- When a file exceeds ~150 lines, consolidate older entries.