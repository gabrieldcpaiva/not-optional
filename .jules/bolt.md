## 2023-10-05 - Bash string manipulation vs subshells
**Learning:** Using `$(basename "$file" .md)` in bash loops spawns a subshell process for every file, which is significantly slower than using built-in string manipulation like `${file##*/}` and `${filename%.md}`. In tight loops (like iterating over many files), subshells create a measurable performance penalty.
**Action:** Use native bash string parameter expansion `##*/` (to strip directory path) and `%.ext` (to strip extension) instead of `basename` and `dirname` within loops where performance matters.
