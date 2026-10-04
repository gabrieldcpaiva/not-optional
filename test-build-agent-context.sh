#!/bin/bash

# Stop on any error
set -e

# Setup a temporary workspace
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

echo "Created temp directory: $TEMP_DIR"

# Copy the script to be tested
cp build-agent-context.sh "$TEMP_DIR/"

# Navigate to the temp directory
pushd "$TEMP_DIR" > /dev/null

# Create dummy input directories and files
mkdir -p principles
mkdir -p skills/dummy-skill-1
mkdir -p skills/dummy-skill-2

echo "Dummy Principle 1" > principles/principle1.md
echo "Dummy Principle 2" > principles/principle2.md

echo '{"token": "screen"}' > principles/tokens.screen.json
echo '{"token": "print"}' > principles/tokens.print-monochrome.json

echo "Dummy Skill 1 Content" > skills/dummy-skill-1/SKILL.md
echo "Dummy Skill 2 Content" > skills/dummy-skill-2/SKILL.md

# Run the script
./build-agent-context.sh > /dev/null

# Verify the output
OUTPUT_FILE="agent-instructions.md"
TEST_FAILED=0

if [ ! -f "$OUTPUT_FILE" ]; then
    echo "❌ Error: $OUTPUT_FILE was not created."
    TEST_FAILED=1
fi

# Function to assert that a string is present in the output file
assert_contains() {
    local expected="$1"
    if [ "$TEST_FAILED" -eq 0 ] && ! grep -qF "$expected" "$OUTPUT_FILE"; then
        echo "❌ Error: Expected string '$expected' not found in $OUTPUT_FILE."
        TEST_FAILED=1
    fi
}

assert_contains "# not-optional: Agent Accessibility Instructions"
assert_contains "Dummy Principle 1"
assert_contains "Dummy Principle 2"
assert_contains "### Skill: dummy-skill-1"
assert_contains "Dummy Skill 1 Content"
assert_contains "### Skill: dummy-skill-2"
assert_contains "Dummy Skill 2 Content"
assert_contains '{"token": "screen"}'
assert_contains '{"token": "print"}'

popd > /dev/null

if [ "$TEST_FAILED" -eq 1 ]; then
    echo "❌ Tests failed!"
    # Use a subshell to return the correct exit code without exiting the parent shell
    (exit 1)
else
    echo "✅ All tests passed successfully!"
    (exit 0)
fi
