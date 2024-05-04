import os
import argparse
import configparser

def compile_env_from_ini(input_file, output_file, debug=False):
    """
    Compile environment variable definitions from an .ini file and generate a shell script.

    Args:
        input_file (str): Path to the input env.ini file.
        output_file (str): Path to the output environment script file.
        debug (bool): Whether to enable debug mode (default: False).

    Returns:
        None
    """
    try:
        pre_path = os.path.join(os.getcwd(), 'docs', 'docstring', 'env.txt')
        preface = open(pre_path, 'r').read() if os.path.exists(pre_path) else ""

        if debug:
            print("Reading environment variable definitions from the .ini file.")

        # Read environment variable definitions from the .ini file
        config = configparser.ConfigParser()
        config.read(input_file)

        if debug:
            print("Generating environment variable assignments.")

        # Generate environment variable assignments and write them to the output file
        with open(output_file, 'w') as output_file:
            output_file.write(f'{preface}\n')
            for section in config.sections():
                name = config[section].get('name', '')
                value = config[section].get('value', '')

                # Format the environment variable assignment
                if name and value:
                    env_assignment = f"export {name}='{value}'\n"
                    output_file.write(env_assignment)

        if debug:
            print("Environment variable compilation completed successfully.")
    except Exception as e:
        print(f"An exception occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compile environment variable definitions from an .ini file.')
    parser.add_argument('input_file', type=str, help='Path to the input env.ini file.')
    parser.add_argument('output_file', type=str, help='Path to the output environment script file.')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode.')
    args = parser.parse_args()

    # Run the main function with debug mode enabled if specified
    compile_env_from_ini(args.input_file, args.output_file, debug=args.debug)
