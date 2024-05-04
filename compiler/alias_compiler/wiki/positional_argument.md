
# Positional Argument Parser

This script provides functions to parse positional arguments in a command string and to test their parsing functionality.

## `parse_positional_args`

### Description

The `parse_positional_args` function searches for positional arguments in a given command string and returns a tuple containing a list of matched patterns and their count.

#### Parameters

- `command` (str): The command string to parse.

#### Returns

- tuple: A tuple containing a list of positional argument patterns found in the command and the count of positional arguments.

### Example

```python
from positional_argument_parser import parse_positional_args

command = "ls $1"
matches, count = parse_positional_args(command)
print(f"Command: {command}, Matches: {matches}, Count: {count}")
```

### Output

```
Command: ls $1, Matches: ['$1'], Count: 1
```

## `test_parse_positional_arguments`

### Description

The `test_parse_positional_arguments` function tests the `parse_positional_args` function with different command strings to ensure correct parsing.

### Usage

To run the test function, execute the script directly.

```bash
python positional_argument_parser.py [--command COMMAND] [--list]
```

- `--command COMMAND` (optional): The command line to parse for positional arguments. If not provided, a default command will be used.
- `--list` (optional): Treat positional arguments as a list (comma-separated).

#### Example

```bash
python positional_argument_parser.py --command "grep -A $2 <id> $1" --list
```

### Output

The script will print the command string and the parsed positional argument matches.

```
Command: grep -A $2 <id> $1, Matches: ['$2', '<id>', '$1'], Count: 3
```

## Dependencies

- `argparse`: For parsing command-line arguments.
- `re`: For regular expression operations.
