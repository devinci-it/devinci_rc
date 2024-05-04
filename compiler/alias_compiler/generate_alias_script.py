import os
from compiler.devinci_rc.utilities import Utilities

def generate_alias_script(preface, alias_info_list, output_file, force=False):
    """
    Generate an alias script.

    Args:
        preface (str): Content to be placed at the beginning of the script.
        alias_info_list (list): List of tuples containing alias information.
            Each tuple should contain (alias, command) or (alias, script_path).
        output_file (str): Path to the output alias script file.
        force (bool, optional): If True, override the existing file without prompting. Defaults to False.

    Returns:
        str: The generated alias script content.
    """
    script_content = ""

    def generate_alias_line(alias, command_or_script):
        if os.path.exists(command_or_script):
            script = f'$ALIAS_SCRIPT_DIR/{command_or_script}'
            return f'source {script}\nalias {alias}="{alias}"\n'
        else:
            return f'alias {alias}="{command_or_script}"\n'

    # Write the preface content
    script_content += preface.strip() + '\n\n'

    # Iterate through the list of alias information
    for alias, command_or_script in alias_info_list:
        script_content += generate_alias_line(alias, command_or_script)

        # Add a clear separation between alias definitions
        # Separate sections for better readability
        script_content += Utilities.create_centered_banner('Alias Definitions')

    try:
        # Write the generated script content to the output file
        with open(output_file, 'x') as f:
            f.write(script_content)
        print(f"Alias script generated: {output_file}")

    except FileExistsError:
        if force:
            # Override existing file without prompting
            with open(output_file, 'w') as f:
                f.write(script_content)
            print(f"Alias script generated: {output_file}")
        else:
            user_input = input(f"The file '{output_file}' already exists. Do you want to override it? (y/n): ")
            if user_input.lower() == 'y':
                # Override existing file
                with open(output_file, 'w') as f:
                    f.write(script_content)
                print(f"Alias script generated: {output_file}")
            else:
                print("Generation aborted.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Generation aborted.")

    finally:
        return script_content
