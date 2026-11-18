# Pitfalls and fixes

## Slides can be wrong or unreproducible
- **Chapter 10 Iris slide**: it says "petal width" but the printed centroids (1.46275, 4.22857, 5.55686) and the 95.33% purity are those of *petal length*. Petal width gives 96.00%. Re-run before quoting a slide.
- The slide's 66.0% for K=3 on all four Iris features is a *local minimum* (versicolor and virginica merged, setosa split in two, J about 143). About 21% of single random starts land there (62/300); the best run gets 89.33% with J = 78.85. Lesson: report J and the number of restarts, not just accuracy.
- Cluster "accuracy" (purity) rises with K and reaches 100% at K = n. Never use it to choose K.

## Iris practical notebook (`notebooks/k_means_clustering.ipynb`)
- sklearn's Iris has 1 duplicate row (index 101 = 142); silhouette over k=2..10 is not monotone (min at k=6, 0.317, back to 0.352 at k=10). Check prose claims like "giảm dần" against the table.
- Unscaled data gives a *higher* ARI at k=3 (0.73) than z-scored (0.62; both `n_init=10`, `random_state=42`): scaling is not a guaranteed win, so notebook text must not say it "ít ảnh hưởng".
- Editing the .ipynb: script the JSON (`indent=2`, `ensure_ascii=False`, no trailing newline), keep Colab cell `id`s, and never touch `outputs` of cells whose code did not change. Verify by exec'ing all code cells in a scratch venv with `MPLBACKEND=Agg`.

## Environment
- `UnicodeEncodeError: 'charmap' codec...` when printing Vietnamese on Windows (cp1258 console): set `PYTHONIOENCODING=utf-8`.
- Output files from Python redirected on Windows have CRLF; `grep -x` against LF text then fails for every line. Strip `\r` first.
- `scikit-learn` is not in `requirements.txt` and not installed system-wide. `requirements.txt` is UTF-16 encoded, so plain `cat` shows spaced letters; do not rewrite it by appending with a UTF-8 tool.
- Pillow 12 warns that `Image.getdata` is deprecated; use `getpixel` loops (or `get_flattened_data`) in snippets.
- Bash tool resets cwd after each call; use absolute paths or `cd ... &&` in the same command.

## Algorithm details that bit during writing
- K-means label numbers are arbitrary. Compare two runs by the partition (sets of indices), never by raw labels.
- `random.sample` picks by position, so duplicate points can both become initial centroids and produce an empty cluster. Empty clusters keep their old centroid in our code.
- `min(..., key=...)` returns the first minimum, which is the tie-break rule (lowest centroid index) the notebook relies on.
- Pure-Python K-means on an image of `n` pixels costs `O(t*n*K*d)`; shrink the image (`thumbnail`) or use `MiniBatchKMeans`.
