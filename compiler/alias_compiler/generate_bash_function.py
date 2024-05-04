import argparse
import os
import hashlib
import stat

def generate_bash_function(alias, command, function_name, write_file=True,
                           force=True):
    """
    Generates a bash function script based on the provided alias, command, and function name.

    Args:
        alias (str): The alias for the function.
        command (str): The command associated with the alias.
        function_name (str): The name of the bash function.
        write_file (bool, optional): Whether to write the script file. Defaults to True.
        force (bool, optional): Whether to force override existing files. Defaults to False.

    Returns:
        tuple or None: If write_file is True, returns a tuple containing the path to the created script file,
                       the alias, the command, and the function name. If write_file is False, returns None.
    """
    stub_path = os.path.join('stubs.d', 'alias_function.stub')
    with open(stub_path, 'r') as stub_file:
        stub_content = stub_file.read()

    bash_function_script = stub_content.format(function_name=function_name, command=command, attr="")

    script_hash = hashlib.sha256(alias.encode()).hexdigest()[:9]
    script_name = f'{alias}_{script_hash}.sh'
    script_file_path = os.path.join('aliases.d', script_name)

    if os.path.exists(script_file_path) and not force:
        raise FileExistsError(f"File {script_file_path} already exists. Use the 'force' parameter to override.")

    if write_file:
        with open(script_file_path, 'w') as script_file:
            script_file.write(bash_function_script)

        os.chmod(script_file_path, stat.S_IRWXU | stat.S_IXGRP | stat.S_IXOTH)

        return script_file_path, alias, command, function_name
    else:
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate a bash function script for an alias.")
    parser.add_argument("alias", help="The alias for the function.")
    parser.add_argument("command", help="The command associated with the alias.")
    parser.add_argument("function_name", help="The name of the bash function.")
    parser.add_argument("--no-write", action="store_false", dest="write_file", help="Generate the script content without writing to file.")
    args = parser.parse_args()

    try:
        script_file_info = generate_bash_function(args.alias, args.command, args.function_name, write_file=args.write_file)
        if script_file_info:
            script_file_path, alias, command, function_name = script_file_info
            print(f"Generated script file: {script_file_path}")
            print(f"Alias: {alias}")
            print(f"Command: {command}")
            print(f"Function Name: {function_name}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
