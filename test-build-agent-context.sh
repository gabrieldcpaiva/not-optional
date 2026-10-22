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

# ⚡ Bolt Optimization: Read file into memory once to avoid spawning a process on each assert
if [ -f "$OUTPUT_FILE" ]; then
    OUTPUT_CONTENT=$(<"$OUTPUT_FILE")
fi

# Function to assert that a string is present in the output file
assert_contains() {
    local expected="$1"
    # ⚡ Bolt Optimization: Use bash built-in string matching instead of grep -qF
    if [ "$TEST_FAILED" -eq 0 ] && [[ "$OUTPUT_CONTENT" != *"$expected"* ]]; then
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


# Test with a custom output file name
CUSTOM_OUTPUT="custom-instructions.md"
./build-agent-context.sh "$CUSTOM_OUTPUT" > /dev/null

if [ ! -f "$CUSTOM_OUTPUT" ]; then
    echo "❌ Error: $CUSTOM_OUTPUT was not created."
    TEST_FAILED=1
fi

if [ "$TEST_FAILED" -eq 0 ]; then
    OUTPUT_CONTENT=$(<"$CUSTOM_OUTPUT")
    OUTPUT_FILE="$CUSTOM_OUTPUT"
    assert_contains "Dummy Principle 1"
fi

popd > /dev/null

if [ "$TEST_FAILED" -eq 1 ]; then
    echo "❌ Tests failed!"
    # Use a subshell to return the correct exit code without exiting the parent shell
    (exit 1)
else
    echo "✅ All tests passed successfully!"
    (exit 0)
fi
