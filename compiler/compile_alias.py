import os
import argparse
from compiler.alias_compiler import generate_bash_function, parse_positional_args, generate_alias_script
import devinci_rc
from dotenv import load_dotenv

from compile_path import PathCompiler
def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Generate alias script.")
    parser.add_argument("ini_file", help="Path to the .ini file containing alias definitions.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing alias script.")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.dirname(__file__))
    config_dir = os.path.join(script_dir, os.getenv('CONF_REGISTRY_DIR'))
    preface_dir = os.path.join(script_dir, 'docs', 'docstring')

    raw_config = devinci_rc.utilities.Utilities.parse_ini_file(
        os.path.join(config_dir, 'alias.ini'))

    preface = PathCompiler.read_docstring_preface(os.path.join(preface_dir,
                                                               'alias.txt'))
    alias_info_list = []

    for name, binary, alias, command in raw_config:
        function_name = name.lower()
        alias = alias.strip().lower()
        command = command.strip()

        parsed_command = parse_positional_args.parse_positional_args(command)

        if parsed_command[-1] == 0:  # No need to write a function
            alias_info_list.append((alias, command))
        else:
            script_info = generate_bash_function.generate_bash_function(alias, command, function_name)
            alias_info_list.append((alias, script_info[0]))


    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'aliases.sh')
    script_content = generate_alias_script.generate_alias_script(preface,
                                                                 alias_info_list,output_path)

    # with open(output_path, 'w') as output_file:
    #     output_file.write(preface)
    #     output_file.write(script_content)

    print(f"Alias script generated: {output_path}")

if __name__ == "__main__":
    main()
