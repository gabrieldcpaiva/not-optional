#!/bin/bash

# Define the output file
OUTPUT_FILE="agent-instructions.md"

echo "Building $OUTPUT_FILE..."

if [ ! -d "principles" ] || [ ! -d "skills" ]; then
  echo "Error: Required directories 'principles' or 'skills' are missing." >&2
  exit 1
fi

# Write the header
echo "# not-optional: Agent Accessibility Instructions" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "This document aggregates the accessibility laws and constraints from the \`not-optional\` toolkit." >> "$OUTPUT_FILE"
echo "When building or auditing web interfaces and print documents, you must strictly follow these rules." >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "## Core Principles" >> "$OUTPUT_FILE"

# Append all principles
{
  shopt -s nullglob
  principle_files=(principles/*.md)
  if [ ${#principle_files[@]} -gt 0 ]; then
    awk '
      FNR==1 {
        n=split(FILENAME, a, "/")
        f=a[n]
        sub(/\.md$/, "", f)
        printf "\n### %s\n", f
      }
      { print }
    ' "${principle_files[@]}"
  fi
} >> "$OUTPUT_FILE"


echo "" >> "$OUTPUT_FILE"
echo "## Agent Skills" >> "$OUTPUT_FILE"

# Append all skills in one write. The loop used to open the output file
# three times per skill.
{
  # Append all skills
  shopt -s nullglob
  skill_files=(skills/*/SKILL.md)
  if [ ${#skill_files[@]} -gt 0 ]; then
    # ⚡ Bolt Optimization: Replace loop+cat with single awk process
    # Reduces process spawning overhead from O(N) to O(1)
    awk '
      FNR==1 {
        n=split(FILENAME, a, "/")
        skill_name=a[n-1]
        printf "\n### Skill: %s\n", skill_name
      }
      { print }
    ' "${skill_files[@]}"
  fi

  echo ""
  echo "## Design Tokens"
  echo "Agents: Refer to the raw JSON files for exact values, but use these as a structural guide:"

  echo ""
  echo "### Screen Tokens (principles/tokens.screen.json)"
  echo '```json'
  cat principles/tokens.screen.json
  echo '```'

  echo ""
  echo "### Print Tokens (principles/tokens.print-monochrome.json)"
  echo '```json'
  cat principles/tokens.print-monochrome.json
  echo '```'
} >> "$OUTPUT_FILE"

echo "Successfully built $OUTPUT_FILE"
