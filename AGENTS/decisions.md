# Decisions and rationale

## Chapter 10
- **No full from-scratch implementation section (owner's call).** The first draft had one (stdlib `kmeans.py`, experiments, scikit-learn comparison, "Thử thay đổi" table), matching the original brief. The owner judged it redundant and had it removed. Do not re-add it unless asked. Chapter 8 is the only chapter with `src/` code and tests; chapters 9 and 10 are notebook only.
- **Section layout** is now 10.1-10.8 (concept, objective, algorithm, hand example, practical issues, applications, summary, keywords). The original brief said 10.1-10.9; the removal brought it to 10.8. Chapter 10 has no "Thử thay đổi" table now; there is no code at all; the applications section (10.6) is just a table.
- **Owner prefers a short notebook.** Iris example, image snippet and extra summary rows were cut as redundant; students can investigate those themselves from the applications table and keyword table. Do not re-add them unless asked.
- **Hand example**: 6 points, K=2, initial centroids A and B (deliberately poor). It takes 3 iterations and J goes 92 -> 24 -> 11.4 -> 7.5, so students see a real reassignment (B moves). Initial centroids A and F give the same result in 2 iterations.
- **Init trap example** is 1-D (`1,2,10,11,20,21`, K=3, start `1,2,10`, J=101 vs optimum 1.5) because it can be traced in a few lines.
- **`task-notebook.md`**: the owner asked for the Chapter 10 entry to be removed; the finished notebook file is added by the owner before commit.
