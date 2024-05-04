#! /bin/bash

export PYTHONPATH="$OUTPUT_DIR/scripts:$PYTHONPATH"

# Get the absolute path of the script directory
export SCRIPT_DIR="$(realpath "$(dirname "$0")")"
echo $SCRIPT_DIR

# Set REG_DIR to the absolute path of SCRIPT_DIR/registration.d
export REG_DIR="$SCRIPT_DIR/registration.d"
echo $REG_DIR

# Get the absolute directory name of REG_DIR
export OUTPUT_DIR="$(realpath "$(dirname "$REG_DIR")")"
echo $OUTPUT_DIR

#
## Function to print a bordered banner
print_banner() {
    local message="$1"
    local border_char="="
    local border_length=$(( ${#message} + 4 ))

    printf "\n%s\n" "$(printf "%-${border_length}s" "$border_char" | tr ' ' "$border_char")"
    printf "%s  %s  %s\n" "$border_char" "$message" "$border_char"
    printf "%s\n\n" "$(printf "%-${border_length}s" "$border_char" | tr ' ' "$border_char")"
}

## Function to compile alias definitions from alias.ini
# Function to compile alias definitions from alias.ini
compile_aliases() {
    python3 scripts/compile_aliases.py "$REG_DIR/alias.ini"
    "$OUTPUT_DIR/aliases.sh" --debug
}

compile_env() {
    python3 scripts/compile_env.py "$REG_DIR/env.ini"  "$OUTPUT_DIR/env.sh" --debug
}

compile_path() {
    python3 scripts/compile_path.py "$REG_DIR/path.ini"  "$OUTPUT_DIR/path.sh"
}
#
# Update the aliases.sh file
print_banner "Updating aliases.sh."
compile_aliases
print_banner "Aliases updated."

print_banner "Updating env.sh."
compile_env
print_banner "ENV updated."

print_banner "Updating path.sh."
compile_path
print_banner "PATH updated."
#
#
