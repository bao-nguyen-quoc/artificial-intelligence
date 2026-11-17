# Conventions and commands

## Notebook format (`resources/notebook-chapN.md`)
Written in Vietnamese; English terms in parentheses on first use; keywords in **bold**; code identifiers and formulas in backticks. Template, taken from chapters 9 and 10:

1. `# Artificial Intelligence Notebook`, the `> Dựa trên tài liệu ...` quote, then `## Chapter N: Tên tiếng Việt (English name)`.
2. `### Mục lục` as a nested link list (anchors: lowercase, dots and punctuation removed, spaces to `-`, Vietnamese letters kept).
3. `**Vấn đề:**` (why the earlier chapters are not enough) and `**Mục tiêu:**` (what the student can do afterwards).
4. Sections `### N.1 ...` to `### N.k`, subsections `#### N.x.y ...`.
5. `*Chú ý:*` paragraphs for pitfalls, tables for comparisons, ASCII diagrams in plain code fences.
6. One hand-calculated example with small numbers; a Python implementation whose output matches it where the chapter's task needs code (chapter 10's owner removed it as redundant: do not duplicate what the hand example and the library already show).
7. A `**Thử thay đổi để hiểu thêm:**` table with columns `Thử | Quan sát cần kiểm tra` (questions, not answers), when the chapter has runnable code.
8. Last two sections: `Tổng kết` (table `Nội dung | Ý chính`) and `Từ khoá để tự tìm hiểu thêm` (table `Chủ đề | Từ khoá tìm kiếm`, ending with a "Tài liệu tham khảo" row).
9. Cross-reference earlier chapters by section number (e.g. "mục 9.2.4") and name the next chapter in the summary.

## Verify before writing
- Run every code block and paste the real output. Extract blocks from the finished `.md` with a small script, run them, and diff against the printed-output blocks (strip `\r` first; Windows redirection adds CRLF).
- Recompute every hand-calculated number with code before it goes in a table.
- Check that every TOC link matches a heading slug, and run `ruff check` on extracted code (the repo uses ruff).
- Quote randomised results with the seed and trial count, and say they may differ slightly across Python versions.

## Commands (Windows, Git Bash or PowerShell)
- Console encoding: `export PYTHONIOENCODING=utf-8` (PowerShell: `$env:PYTHONIOENCODING='utf-8'`) before running scripts that print Vietnamese.
- Scratch work goes in the session scratchpad, not the repo. For scikit-learn, make a venv there: `python -m venv venv && venv/Scripts/pip install scikit-learn numpy pillow ruff`. The system Python has no scikit-learn.
- PDF text: `pdftotext -layout resources/ai-chapN-*.pdf out.txt` (available in Git Bash). Slide exercises ("Bài tập") at the end of the PDF are worth turning into notebook sections.
- Repo tests (chapters with `src/`): `pytest` from the repo root; `pyproject.toml` sets `pythonpath = [".", "src"]`.

## Git
- Branch per chapter (`feature/chapter-N`); commit messages like `feat: done chapter 9 (#31)`. Only commit when asked.
