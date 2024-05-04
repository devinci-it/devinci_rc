#!/bin/bash

# Set the output directory where compiled scripts will be stored
OUTPUT_DIR="$HOME/config"

# Set PYTHONPATH
export PYTHONPATH="$OUTPUT_DIR/scripts:$PYTHONPATH"

# Get the absolute path of the script directory
SCRIPT_DIR="$(realpath "$(dirname "$0")")"
echo "Script directory: $SCRIPT_DIR"

# Set REG_DIR to the absolute path of SCRIPT_DIR/registration.d
REG_DIR="$SCRIPT_DIR/registration.d"
echo "Registration directory: $REG_DIR"

# Get the absolute directory name of REG_DIR
OUTPUT_DIR="$(realpath "$(dirname "$REG_DIR")")"
echo "Output directory: $OUTPUT_DIR"

# Function to print a bordered banner
print_banner() {
    local message="$1"
    local border_char="="
    local border_length=$(( ${#message} + 4 ))

    printf "\n%s\n" "$(printf "%-${border_length}s" "$border_char" | tr ' ' "$border_char")"
    printf "%s  %s  %s\n" "$border_char" "$message" "$border_char"
    printf "%s\n\n" "$(printf "%-${border_length}s" "$border_char" | tr ' ' "$border_char")"
}

# Function to compile alias definitions from alias.ini
compile_aliases() {
    python3 scripts/compile_aliases.py "$REG_DIR/alias.ini"
    "$OUTPUT_DIR/aliases.sh" --debug
}

# Function to compile environment configurations from env.ini
compile_env() {
    python3 scripts/compile_env.py "$REG_DIR/env.ini" "$OUTPUT_DIR/env.sh" --debug
}

# Function to compile path configurations from path.ini
compile_path() {
    python3 scripts/compile_path.py "$REG_DIR/path.ini" "$OUTPUT_DIR/path.sh"
}

# Update alias configurations
print_banner "Updating aliases."
compile_aliases
print_banner "Aliases updated."

# Update environment configurations
print_banner "Updating environment variables."
compile_env
print_banner "Environment variables updated."

# Update path configurations
print_banner "Updating path variables."
compile_path
print_banner "Path variables updated."

# Function to commit changes to Git
commit_changes() {
    git add "$OUTPUT_DIR"/* && git commit -m "Update environment configurations" && git push
}

# Check if changes are within the registration.d directory
if ! git diff --quiet --exit-code "$REG_DIR"; then
    read -p "Changes were detected outside the 'registration.d' directory. Do you want to proceed? (yes/no): " response
    if [ "$response" != "yes" ]; then
        echo "Changes were not committed."
        exit 1
    fi
fi

# Prompt to commit changes
read -p "Do you want to commit the changes to Git? (yes/no): " response
if [ "$response" = "yes" ]; then
    commit_changes
elif [ "$response" = "force" ]; then
    commit_changes
else
    echo "Changes were not committed."
fi
# Get the latest tagged version
# Get the latest tagged version
LATEST_TAG=$(git describe --abbrev=0 --tags 2>/dev/null)

# Check if the command was successful
if [ $? -ne 0 ]; then
    # If not, set LATEST_TAG to a default value
    LATEST_TAG="config-script-v0.0.0"
fi

echo "Latest tag: $LATEST_TAG"

# Extract only the version tag from the latest tag
VERSION_TAG=$(echo "$LATEST_TAG" | grep -oP '^config-script-v\d+\.\d+\.\d+')
if [ -z "$VERSION_TAG" ]; then
    echo "Error: Unable to extract version tag from latest tag. Expected format: 'config-script-vX.Y.Z'"
    exit 1
fi
echo "Version tag: $VERSION_TAG"

# Extract version components
IFS='-' read -ra VERSION_PARTS <<< "$VERSION_TAG"

VERSION=${VERSION_PARTS[2]}
# Increment the version
IFS='.' read -ra VERSION_NUMS <<< "$VERSION"
MAJOR="${VERSION_NUMS[0]}"
MINOR="${VERSION_NUMS[1]}"
PATCH="${VERSION_NUMS[2]}"

PATCH=$((PATCH + 1))

UPDATED_VERSION="$MAJOR.$MINOR.$PATCH"
echo "Updated version: $UPDATED_VERSION"

# Tag the script with the updated version
git tag -a "config-script-$UPDATED_VERSION" -m "Version $UPDATED_VERSION of the configuration script"
git push origin "config-script-$UPDATED_VERSION"
