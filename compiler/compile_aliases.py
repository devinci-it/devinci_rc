import os
import argparse
import configparser

def compile_aliases_from_ini(input_file, output_file, debug=False):
    """
    Compile alias definitions from an .ini file and generate a single aliases.sh file.

    Args:
        input_file (str): Path to the input alias.ini file.
        output_file (str): Path to the output aliases.sh file.
        debug (bool): Whether to enable debug mode (default: False).

    Returns:
        None
    """
    try:
        pre_path = os.path.join(os.getcwd(), 'docs', 'docstring',
                                 'alias.txt')
        preface = open(pre_path, 'r').read() if os.path.exists(
            pre_path) else ""

        if debug:
            print("Reading alias definitions from the .ini file.")
        # Read alias definitions from the .ini file
        config = configparser.ConfigParser()
        config.read(input_file)

        if debug:
            print("Generating alias commands.")
        # Generate alias commands and write them to the output file
        with open(output_file, 'w') as output_file:
            output_file.write(f'{preface}\n')
            for alias_name in config.sections():
                alias= config[alias_name].get('alias','')
                command = config[alias_name].get('command', '')
                script = config[alias_name].get('script', '')

                # Format the alias command
                if command:
                    alias_command = f"alias {alias}='{command}'\n"
                    output_file.write(alias_command)
                elif script:
                    alias_command = f"alias {alias}='sh \"{script}\"'\n"
                    output_file.write(alias_command)

        if debug:
            print("Aliases compilation completed successfully.")
    except Exception as e:
        print(f"An exception occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compile alias definitions from an .ini file.')
    parser.add_argument('input_file', type=str, help='Path to the input alias.ini file.')
    parser.add_argument('output_file', type=str, help='Path to the output aliases.sh file.')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode.')
    args = parser.parse_args()

    # Run the main function with debug mode enabled if specified
    compile_aliases_from_ini(args.input_file, args.output_file, debug=args.debug)
