#!/bin/bash

# Define the output file
OUTPUT_FILE="agent-instructions.md"

echo "Building $OUTPUT_FILE..."

# Write the header
echo "# not-optional: Agent Accessibility Instructions" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "This document aggregates the accessibility laws and constraints from the \`not-optional\` toolkit." >> "$OUTPUT_FILE"
echo "When building or auditing web interfaces and print documents, you must strictly follow these rules." >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "## Core Principles" >> "$OUTPUT_FILE"

# Append all principles
for file in principles/*.md; do
  echo "" >> "$OUTPUT_FILE"
  echo "### $(basename "$file" .md)" >> "$OUTPUT_FILE"
  cat "$file" >> "$OUTPUT_FILE"
done

echo "" >> "$OUTPUT_FILE"
echo "## Agent Skills" >> "$OUTPUT_FILE"

# Append all skills
for file in skills/*/SKILL.md; do
  skill_name=$(dirname "$file" | xargs basename)
  echo "" >> "$OUTPUT_FILE"
  echo "### Skill: $skill_name" >> "$OUTPUT_FILE"
  cat "$file" >> "$OUTPUT_FILE"
done

echo "" >> "$OUTPUT_FILE"
echo "## Design Tokens" >> "$OUTPUT_FILE"
echo "Agents: Refer to the raw JSON files for exact values, but use these as a structural guide:" >> "$OUTPUT_FILE"

echo "" >> "$OUTPUT_FILE"
echo "### Screen Tokens (principles/tokens.screen.json)" >> "$OUTPUT_FILE"
echo '```json' >> "$OUTPUT_FILE"
cat principles/tokens.screen.json >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"

echo "" >> "$OUTPUT_FILE"
echo "### Print Tokens (principles/tokens.print-monochrome.json)" >> "$OUTPUT_FILE"
echo '```json' >> "$OUTPUT_FILE"
cat principles/tokens.print-monochrome.json >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"

echo "Successfully built $OUTPUT_FILE"
