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

# Tag the script
VERSION="v1.0"
LOCK_FILE="./config-script.lock"
SCRIPT_HASH=$(sha256sum "$0" | cut -d ' ' -f 1)

if [ -f "$LOCK_FILE" ]; then
    # Read the hash from the lock file
    OLD_HASH=$(head -n 1 "$LOCK_FILE")
    if [ "$SCRIPT_HASH" != "$OLD_HASH" ]; then
        echo "Script has been modified since the last execution. Please review changes."
        exit 1
    fi
fi

# Write the new hash to the lock file
echo "$SCRIPT_HASH" > "$LOCK_FILE"

# Tag the script
git tag -a "config-script-$VERSION" -m "Version $VERSION of the configuration script"
git push origin "config-script-$VERSION"

# End of script
