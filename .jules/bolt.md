## 2024-03-24 - Bash Subshell Performance Bottleneck
**Learning:** In bash scripts that process large numbers of files (like `build-agent-context.sh`), using subshells to call external utilities like `$(basename "$file")` and `$(dirname "$file")` inside loops introduces significant overhead due to process creation for every iteration.
**Action:** Replace `$(basename)` and `$(dirname)` inside loops with bash built-in parameter expansion (e.g., `filename="${file##*/}"`, `dir="${file%/*}"`). This is drastically faster (up to ~250x faster) as it avoids spawning external processes.
## 2023-10-05 - Bash string manipulation vs subshells
**Learning:** Using `$(basename "$file" .md)` in bash loops spawns a subshell process for every file, which is significantly slower than using built-in string manipulation like `${file##*/}` and `${filename%.md}`. In tight loops (like iterating over many files), subshells create a measurable performance penalty.
**Action:** Use native bash string parameter expansion `##*/` (to strip directory path) and `%.ext` (to strip extension) instead of `basename` and `dirname` within loops where performance matters.
## 2025-02-12 - Duplicate Block Overwriting Optimization & Bug Fix
**Learning:** A bash script was designed to output headers and principles, but a later duplicated code block in the script erroneously re-generated those headers/principles and used the destructive output redirection `> "$OUTPUT_FILE"` instead of appending `>> "$OUTPUT_FILE"`. This wiped out the previous output and performed redundant disk I/O and process spawns.
**Action:** When finding logic duplicated across blocks writing to the same file, examine the file redirection operators. Remove the redundant loop and change `> "$OUTPUT_FILE"` to `>> "$OUTPUT_FILE"` to fix the bug and improve performance.

## 2025-02-12 - Dynamic CLI Tool Resolution Overhead in CI
**Learning:** In CI environments without a standard `package.json`, running `npx -y <package>` forces the package manager to dynamically resolve the package, download it, create a temporary execution environment, and tear it down. Doing this repeatedly for multiple tools (e.g., `ajv-cli` after `pa11y-ci` has already been installed) creates measurable, cumulative delays (5-10 seconds per tool).
**Action:** Always batch the installation of all required Node CLI tools in a single `npm install --no-save <tool1> <tool2> ...` step prior to their execution in CI workflows, avoiding the `npx -y` dynamic download penalty.
