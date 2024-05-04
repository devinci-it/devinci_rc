# Creating and Managing Custom Aliases

This wiki page provides guidelines for creating and managing custom aliases using the `devinci_rc.d` configuration structure.

## Introduction

Aliases are shortcuts or alternative names for commands, allowing users to simplify complex or frequently used commands. In the `devinci_rc.d` configuration, aliases are managed through a structured approach to ensure consistency and ease of management.

## Alias Configuration

The alias configuration is defined within the `aliases.d` directory. Each alias is defined in a separate file, making it easier to manage and organize. Alias files can have either a `.sh` extension for simple command aliases or no extension for aliases that execute scripts.

## Alias Definition

### Command Aliases

Command aliases are defined using the `alias` command followed by the desired alias name and the associated command(s). For example:

```bash
alias myalias='ls -l'
```

### Script Aliases

Script aliases are defined by creating a symbolic link to the script file within the `aliases.d` directory. The script file must have executable permissions to be executed as an alias. For example:

```bash
ln -s /path/to/script.sh /path/to/devinci_rc.d/aliases.d/myalias
```

## Managing Aliases

### Adding New Aliases

To add a new alias, follow these steps:

1. Decide whether the alias will be a command alias or a script alias.
2. If it's a command alias, define it using the `alias` command in a new `.sh` file within the `aliases.d` directory.
3. If it's a script alias, create a symbolic link to the script file in the `aliases.d` directory.

### Editing Existing Aliases

To edit an existing alias, simply modify the corresponding alias file within the `aliases.d` directory.

### Removing Aliases

To remove an alias, delete the corresponding alias file from the `aliases.d` directory.

## Notes

- When defining script aliases, ensure that the script file has executable permissions (`chmod +x script.sh`) to allow it to be executed.
- Always provide a descriptive name and purpose for each alias to maintain clarity and understanding.
- Avoid using aliases that override or conflict with existing system commands or aliases.

---
# Alias Compiler

This script compiles alias definitions from an `.ini` file and generates a single `.sh` file containing alias commands.

## Usage

```bash
python3 alias_compiler.py input_file output_file [--debug]
```


- `input_file`: Path to the input `alias.ini` file containing alias definitions.
- `output_file`: Path to the output `aliases.sh` file to generate.
- `--debug`: (Optional) Enable debug mode to print debug messages.

## Dependencies

- `os`: Provides a portable way to interact with the operating system.
- `argparse`: Parses command-line arguments.
- `configparser`: Reads and writes configuration files in INI format.

## Functionality

The script reads alias definitions from the specified `alias.ini` file and generates corresponding alias commands. Each alias definition can contain either a command or a script path. If a command is specified, it is directly used as the alias command. If a script path is specified, the script is executed when the alias is invoked.

## Example

Suppose you have an `alias.ini` file with the following content:

```ini
[ls]
command = ls -la

[my_script]
script = /path/to/my_script.sh
```

Running the script:

```bash
python3 alias_compiler.py alias.ini aliases.sh
```

will generate `aliases.sh` with the following content:

```bash
alias ls='ls -la'
alias my_script='sh "/path/to/my_script.sh"'
```

## Debugging

To enable debug mode and print debug messages, use the `--debug` flag when running the script.

```bash
python3 alias_compiler.py alias.ini aliases.sh --debug
```

## Error Handling

If any exceptions occur during execution, the script prints an error message with details about the exception.

## Author

- [devinci-it](https://github.com/devinci-it)