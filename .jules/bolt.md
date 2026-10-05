## 2024-03-24 - Bash Subshell Performance Bottleneck
**Learning:** In bash scripts that process large numbers of files (like `build-agent-context.sh`), using subshells to call external utilities like `$(basename "$file")` and `$(dirname "$file")` inside loops introduces significant overhead due to process creation for every iteration.
**Action:** Replace `$(basename)` and `$(dirname)` inside loops with bash built-in parameter expansion (e.g., `filename="${file##*/}"`, `dir="${file%/*}"`). This is drastically faster (up to ~250x faster) as it avoids spawning external processes.
