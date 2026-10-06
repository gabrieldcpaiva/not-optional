## 2024-03-24 - Bash Subshell Performance Bottleneck
**Learning:** In bash scripts that process large numbers of files (like `build-agent-context.sh`), using subshells to call external utilities like `$(basename "$file")` and `$(dirname "$file")` inside loops introduces significant overhead due to process creation for every iteration.
**Action:** Replace `$(basename)` and `$(dirname)` inside loops with bash built-in parameter expansion (e.g., `filename="${file##*/}"`, `dir="${file%/*}"`). This is drastically faster (up to ~250x faster) as it avoids spawning external processes.
## 2023-10-05 - Bash string manipulation vs subshells
**Learning:** Using `$(basename "$file" .md)` in bash loops spawns a subshell process for every file, which is significantly slower than using built-in string manipulation like `${file##*/}` and `${filename%.md}`. In tight loops (like iterating over many files), subshells create a measurable performance penalty.
**Action:** Use native bash string parameter expansion `##*/` (to strip directory path) and `%.ext` (to strip extension) instead of `basename` and `dirname` within loops where performance matters.
