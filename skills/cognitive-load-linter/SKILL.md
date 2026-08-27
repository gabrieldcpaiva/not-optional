---
name: cognitive-load-linter
description: Fail body blocks over 4 lines or 45 words or 65 characters per line. Printable canvas must keep ≥40% empty space.
---

# cognitive-load-linter

## Load with

`principles/micro-chunking.md`

## Law (once)

| Check | Fail if |
| --- | --- |
| Visual lines in one body block | > 4 |
| Words in one body block | > 45 |
| Characters per line | > 65 (hard max 75) |
| Empty space on a printable page | < 40% |

On fail: split into a shorter paragraph or a list. Do not publish the long block.
