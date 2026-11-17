# Progress log

Newest first. One line per finished task; put the reason in decisions.md, not here.

## Chapter 10 - K-means clustering (branch feature/chapter-10)
- Done: `resources/notebook-chap10.md` (sections 10.1-10.8: concept, objective J, algorithm, hand trace, practical issues, applications table, summary, keywords). About 400 lines.
- Revisions on the owner's request (keep the notebook short): (1) removed the stdlib implementation section; (2) removed 10.6.1 (Iris) and 10.6.2 (color-quantization snippet), keeping only the applications table; (3) removed the last two rows of the summary table (`Thực hành`, `Hướng tiếp theo`). Earlier note: the stdlib implementation section (old 10.6: code, experiments, scikit-learn comparison, "Thử thay đổi") was removed as redundant; later sections were renumbered 10.6-10.8.
- Numbers and code outputs were produced by running code (see conventions.md > "Verify before writing"). The experiment figures kept in 10.5 (23% / 0.7% stuck, elbow/silhouette table, scaling example) came from the removed code and are no longer reproducible from the notebook.
- `resources/task-notebook.md`: Chapter 10 entry removed (the owner's pattern: finished chapter leaves the file).
- Left for the owner: commit and PR (nothing was committed).

## Earlier chapters (from git history)
| Chapters | Commit | Output |
|---|---|---|
| 9 | 55a25f8 | `notebook-chap9.md` (notebook only, code embedded) |
| 8 | d3adacd | `notebook-chap8.md` + `src/genetic_algorithm/` + tests |
| 7 | e114d25 | `notebook-chap7.md` |
| 4, 5, 6 | 44fd23c | `notebook-chap4..6.md`, `src/game_tree_search/` |
| 1-3 | 3ededbf, d99ab7e | `notebook-chap1..3.md`, `src/blind_search/`, `src/informed_search/` |

## Next
- Chapter 11 - artificial neural network (see `resources/task-notebook.md`: code only needs to be small and educational). No `ai-chap11` PDF in `resources/` yet; ask for it or work from the task note.
