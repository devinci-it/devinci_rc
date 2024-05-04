# Alias Script Generator

The Alias Script Generator is a utility script designed to simplify the process of generating alias scripts from an input .ini file containing alias definitions. This script parses the input file, processes the alias definitions, and generates a bash script containing the defined aliases.

## Usage

To use the Alias Script Generator, follow these steps:

1. **Prepare Alias Definitions**: Create an .ini file containing the alias definitions. Each alias should be defined with its corresponding command or script path.

2. **Run the Script**: Execute the script `alias_script_generator.py` with the path to the .ini file as an argument. Optionally, you can use the `--force` flag to overwrite an existing alias script.

```bash
python alias_script_generator.py ini_file [--force]
```

Replace `ini_file` with the path to your .ini file containing alias definitions.

3. **Output**: The script will generate an alias script file containing the defined aliases. By default, the script will prompt before overwriting an existing alias script.

## Dependencies

The Alias Script Generator relies on the following dependencies:

- `argparse`: For parsing command-line arguments.
- `compiler.alias_compiler`: Module containing functions for generating bash functions and alias scripts.
- `devinci_rc`: Module for handling configuration files.
- `dotenv`: For loading environment variables from a .env file.
- `compile_path.PathCompiler`: Module for reading docstring preface.
- `os`: Operating system interfaces.

Ensure these dependencies are installed before running the script.
