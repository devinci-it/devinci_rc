import argparse
import configparser
import os
from rc_logger import setup_logger

class PathCompiler:
    def __init__(self, input_file, output_file, debug=False, logcls=None):
        self.input_file = input_file
        self.output_file = output_file
        self.debug = debug
        self.logger = logcls if logcls else setup_logger()

    def read_docstring_preface(self, file_path):
        """
        Read and return the contents of the docstring preface file.

        Args:
            file_path (str): Path to the docstring preface file.

        Returns:
            str: Contents of the docstring preface file.
        """
        preface = ""
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                preface = f.read()
        return preface

    def read_paths_from_ini(self):
        """
        Read paths from a path.ini file.

        Returns:
            dict: A dictionary containing paths and their priorities.
        """
        config = configparser.ConfigParser()
        config.read(self.input_file)

        paths = {}
        for section in config.sections():
            path = config[section].get('absolute_path', '')
            priority = int(config[section].get('priority', 0))
            if path:
                paths[section] = {'path': path, 'priority': priority}

        return paths

    def sort_paths_by_priority(self, paths):
        """
        Sort paths based on priority and return only the paths.

        Args:
            paths (dict): Dictionary containing paths and their priorities.

        Returns:
            list: A sorted list of paths based on priority.
        """
        sorted_paths = sorted(paths.items(), key=lambda x: x[1]['priority'], reverse=True)
        return [path_info['path'] for _, path_info in sorted_paths]

    def generate_script(self, paths, docstring_preface=""):
        """
        Generate a shell script to append paths to the PATH variable.

        Args:
            paths (list): List of paths.
            docstring_preface (str): Contents of the docstring preface.

        Returns:
            None
        """
        with open(self.output_file, 'w') as output_file:
            self.logger.info("Starting compilation of paths from path.ini")

            output_file.write(docstring_preface)
            output_file.write("# Append paths to the PATH variable\n")
            existing_paths = set()
            for path in paths:
                if self.debug:
                    output_file.write(f"# export PATH=\"{path}:$PATH\"\n")
                else:
                    if path not in existing_paths:
                        if os.path.exists(path):
                            output_file.write(
                                f"export PATH=\"{path}:$PATH\"\n")
                            existing_paths.add(path)
                        else:
                            self.logger.error(
                                f"Path does not exist: {path}")
                    else:
                        self.logger.error(
                            f"Path already exists in PATH: {path}")

    def compile_paths_from_ini(self):
        """
        Compile paths from a path.ini file and generate a shell script to append them to the PATH variable.

        Returns:
            None
        """
        try:
            paths = self.read_paths_from_ini()
            if self.debug:
                print("Reading paths from the path.ini file.")
                print(f"PATHS:{paths}\nTYPE{type(paths)}")

            sorted_paths = self.sort_paths_by_priority(paths)
            if self.debug:
                print("Sorting paths by priority.")
                print(sorted_paths)

            preface_path = os.path.join(os.getcwd(), 'docs', 'docstring', 'alias.txt')
            docstring_preface = self.read_docstring_preface(preface_path)
            self.generate_script(sorted_paths, docstring_preface)

            if self.debug:
                print("Script generation completed successfully.")

        except Exception as e:
            self.logger.error("Error parsing path.ini")

            print(f"An exception occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compile paths from a path.ini file and generate a shell script.')
    parser.add_argument('input_file', type=str, help='Path to the input path.ini file.')
    parser.add_argument('output_file', type=str, help='Path to the output script file.')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode.')
    args = parser.parse_args()
    logger=setup_logger()
    # Instantiate PathCompiler and run compile_paths_from_ini
    try:
        compiler = PathCompiler(args.input_file, args.output_file,
                                debug=args.debug,logcls=logger)
        compiler.compile_paths_from_ini()
    except Exception as e:
        logger.error(f"An error occurred: {e}")