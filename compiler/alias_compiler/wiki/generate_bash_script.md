
# Bash Function Script Generator

This script generates a bash function script based on the provided alias, command, and function name. It allows for easy creation of bash functions for defining aliases.

## Usage

```bash
python bash_function_generator.py alias command function_name [--no-write]
```

- `alias`: The alias for the function.
- `command`: The command associated with the alias.
- `function_name`: The name of the bash function.
- `--no-write`: Optional flag to generate the script content without writing to a file.

## Dependencies

- `argparse`: For parsing command-line arguments.
- `os`: Operating system interfaces.
- `hashlib`: For hashing data.
- `stat`: For interpreting file permission bits.

## Functionality

The script works by generating a bash function script based on the provided alias, command, and function name. It writes the script to a file by default but can also generate the script content without writing to a file if the `--no-write` flag is provided.

### `generate_bash_function`

This function generates a bash function script based on the provided parameters.

#### Parameters

- `alias` (str): The alias for the function.
- `command` (str): The command associated with the alias.
- `function_name` (str): The name of the bash function.
- `write_file` (bool, optional): Whether to write the script file. Defaults to True.
- `force` (bool, optional): Whether to force override existing files. Defaults to False.

#### Returns

- tuple or None: If `write_file` is True, returns a tuple containing the path to the created script file, the alias, the command, and the function name. If `write_file` is False, returns None.

### `main`

The `main` function handles command-line argument parsing and calls `generate_bash_function` to generate the bash function script.

## Example

```bash
python bash_function_generator.py my_alias "ls -l" my_function
```

This command generates a bash function script named `my_alias_<hash>.sh` containing the alias `my_alias` and the command `ls -l`, with the function name `my_function`.

## Notes

- If a script file with the same name already exists, the script will raise a `FileExistsError` unless the `--force` flag is provided.

```