# Micro-chunking

## Law (not optional)

| Check | Threshold |
| --- | --- |
| Max visual lines per body block | 4 |
| Max words per body block | 45 |
| Max characters per line | 65 (hard max 75) |
| Min empty space on a printable canvas | 40% |

If any threshold is exceeded, split into a shorter paragraph or a list before publish.

## Intent

Executive-function support. Deterministic so an agent can fail a block without guessing viewport width.
