import re
import argparse
import re

def parse_positional_args(command):
    """
    Parses positional arguments in a command string.

    This function searches for positional arguments in a given command string
    and returns a tuple containing a list of matched patterns and their count.

    Args:
        command (str): The command string to parse.

    Returns:
        tuple: A tuple containing a list of positional argument patterns found in the command
               and the count of positional arguments.
    """
    command_parts = command.split(' ')
    pattern_matches = [part for part in command_parts if any(
        re.search(pattern, part) for pattern in [r'\$\d', r'<[a-zA-Z]+>'])]
    return pattern_matches, len(pattern_matches)

def test_parse_positional_arguments():
    """
    Test function for parse_positional_arguments.

    This function tests the parse_positional_arguments function
    with different command strings to ensure correct parsing.
    """
    # Test cases
    commands = [
        "ls $1",
        "echo <arg>",
        "grep -A $2",
        "python script.py <file>",
        "cp $1 $2",
    ]
    for command in commands:
        matches, count = parse_positional_args(command)
        print(f"Command: {command}, Matches: {matches}, Count: {count}")



# Run the test function if this module is executed directly
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse positional arguments from a command line.")
    parser.add_argument("command", metavar="COMMAND", nargs="?",
                        help="The command line to parse for positional arguments. If not provided, a default command will be used.",
                        default="grep -A $2 <id> $1")
    parser.add_argument("--list",
                        help="Treat positional arguments as a list (comma-separated).",
                        action="store_true")
    args = parser.parse_args()

    matches = parse_positional_args(args.command)

    if args.list:
        matches = [match.strip("$<>") for match in matches]

    print(f"Command: {args.command}, Matches: {matches}")