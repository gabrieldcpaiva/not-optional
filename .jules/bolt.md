## 2024-03-24 - Bash Subshell Performance Bottleneck
**Learning:** In bash scripts that process large numbers of files (like `build-agent-context.sh`), using subshells to call external utilities like `$(basename "$file")` and `$(dirname "$file")` inside loops introduces significant overhead due to process creation for every iteration.
**Action:** Replace `$(basename)` and `$(dirname)` inside loops with bash built-in parameter expansion (e.g., `filename="${file##*/}"`, `dir="${file%/*}"`). This is drastically faster (up to ~250x faster) as it avoids spawning external processes.
## 2023-10-05 - Bash string manipulation vs subshells
**Learning:** Using `$(basename "$file" .md)` in bash loops spawns a subshell process for every file, which is significantly slower than using built-in string manipulation like `${file##*/}` and `${filename%.md}`. In tight loops (like iterating over many files), subshells create a measurable performance penalty.
**Action:** Use native bash string parameter expansion `##*/` (to strip directory path) and `%.ext` (to strip extension) instead of `basename` and `dirname` within loops where performance matters.
## 2025-02-12 - Duplicate Block Overwriting Optimization & Bug Fix
**Learning:** A bash script was designed to output headers and principles, but a later duplicated code block in the script erroneously re-generated those headers/principles and used the destructive output redirection `> "$OUTPUT_FILE"` instead of appending `>> "$OUTPUT_FILE"`. This wiped out the previous output and performed redundant disk I/O and process spawns.
**Action:** When finding logic duplicated across blocks writing to the same file, examine the file redirection operators. Remove the redundant loop and change `> "$OUTPUT_FILE"` to `>> "$OUTPUT_FILE"` to fix the bug and improve performance.
## 2026-10-08 - CI npx Dynamic Resolution Overhead
**Learning:** In repositories without a `package.json`, using `npx -y <package>` sequentially in CI workflows causes significant performance overhead because npm has to dynamically resolve, download, and install the package for every command.
**Action:** Always batch install all required CLI tools (like `pa11y-ci` and `ajv-cli`) in a single `npm install --no-save` step, and remove the `-y` flag from subsequent `npx` commands. This allows npx to use the locally installed binaries instantly.
