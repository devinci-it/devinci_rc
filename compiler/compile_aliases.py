import os
import re


from .devinci_rc.rc_logger import setup_logger
import configparser
from .devinci_rc.rc_helper import FileParser, FileWriter

class AliasGenerator:
    def __init__(self, debug=False):
        self.debug = debug
        self.logger = setup_logger(debug)
        self.bash_function=None
        self.command=None

    def _find_pattern_in_command(self,command):
        self.logger.info(f"Finding pattern in command: {command}")
        self.logger.debug(f"Executing _find_pattern_in_command with command: {command}")

        command_parts = command.split(' ')
        pattern_matches = [part for part in command_parts if any(
            re.search(pattern, part) for pattern in [r'\$\d', r'<[a-zA-Z]+>'])]
        self.logger.info(f'{len(pattern_matches)} found in command: {command}')
        self.logger.debug(f'{command}\n{pattern_matches},\n{type(pattern_matches)}')
        return pattern_matches
    def compile_aliases(self, input_file, output_file):
        """
        Compile alias definitions from an .ini file and generate a single aliases.sh file.

        Args:
            input_file (str): Path to the input alias.ini file.
            output_file (str): Path to the output aliases.sh file.

        Returns:
            None
        """
        try:
            pre_path = os.path.join(os.getcwd(), 'docs', 'docstring', 'alias.txt')
            preface = open(pre_path, 'r').read() if os.path.exists(pre_path) else ""

            if self.debug:
                print("Reading alias definitions from the .ini file.")
            # Read alias definitions from the .ini file
            parser = FileParser()
            config = parser.parse_input_file(input_file)

            if self.debug:
                print("Generating alias commands.")
            # Generate alias commands and write them to the output file
            alias_commands = self.generate_alias_commands(config)

            writer = FileWriter()
            writer.write_to_file(output_file, f"{preface}\n{alias_commands}")

            if self.debug:
                print("Aliases compilation completed successfully.")

        except Exception as e:
            print(f"An exception occurred: {e}")

    def generate_alias_commands(self, config):
        alias_commands = []
        for alias_name in config.sections():
            alias = self.normalize_alias(alias_name)
            command = config[alias_name].get('command', '')
            script = config[alias_name].get('script', '')

            # Check if the command contains positional arguments
            if any(re.search(pattern, command) for pattern in [r'\$\d', r'<[a-zA-Z]+>']):
                argument_list=self._find_pattern_in_command(command)
                self.bash_function = self.generate_bash_function(alias, command)
            else:
                bash_function = None
                self.command=command.strip('')

            alias_commands.append((alias, command, script, bash_function))
        return alias_commands

    def generate_bash_function(self, alias, command):
        # Extract argument list from the command
        argument_list = self._find_pattern_in_command(command)

        # Generate bash function script
        bash_function_script = f'''
         function {alias}() {{
             {command} {' '.join(argument_list)}
         }}
         '''
        return bash_function_script


    def normalize_alias(self, alias):
        # Replace spaces and hyphens with underscores
        normalized_alias = re.sub(r'[\s-]', '_', alias)
        # Convert camelCase/PascalCase to snake_case
        normalized_alias = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', normalized_alias)
        normalized_alias = re.sub(r'([a-z])([A-Z0-9])', r'\1_\2', normalized_alias)
        # Convert to lowercase
        normalized_alias = normalized_alias.lower()
        return normalized_alias
