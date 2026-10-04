#!/bin/bash

# Define the output file
OUTPUT_FILE="agent-instructions.md"

echo "Building $OUTPUT_FILE..."

{
  # Write the header
  echo "# not-optional: Agent Accessibility Instructions"
  echo ""
  echo "This document aggregates the accessibility laws and constraints from the \`not-optional\` toolkit."
  echo "When building or auditing web interfaces and print documents, you must strictly follow these rules."
  echo ""
  echo "## Core Principles"

  # Append all principles
  for file in principles/*.md; do
    echo ""
    echo "### $(basename "$file" .md)"
    cat "$file"
  done

  echo ""
  echo "## Agent Skills"

  # Append all skills
  for file in skills/*/SKILL.md; do
    [ -e "$file" ] || continue
    skill_name=$(basename "$(dirname "$file")")
    printf '\n### Skill: %s\n' "$skill_name"
    cat "$file"
  done

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
} > "$OUTPUT_FILE"

echo "Successfully built $OUTPUT_FILE"
