from abc import ABC, abstractmethod
import configparser
import os

class Compiler(ABC):
    def __init__(self, input_file, output_file, debug=False, logcls=None):
        self.input_file = input_file
        self.output_file = output_file
        self.debug = debug
        self.logger = logcls if logcls else setup_logger()

    @abstractmethod
    def read_from_ini(self):
        """
        Read data from an .ini file.

        Returns:
            dict: A dictionary containing the data read from the .ini file.
        """
        pass

    @abstractmethod
    def generate_script(self, data, docstring_preface=""):
        """
        Generate a script based on the data read from the .ini file.

        Args:
            data (dict): Dictionary containing the data read from the .ini file.
            docstring_preface (str): Contents of the docstring preface.

        Returns:
            None
        """
        pass

    def compile_from_ini(self):
        """
        Compile data from an .ini file and generate a script.

        Returns:
            None
        """
        try:
            data = self.read_from_ini()
            preface_path = os.path.join(os.getcwd(), 'docs', 'docstring', 'alias.txt')
            with open(preface_path, 'r') as f:
                docstring_preface = f.read()
            self.generate_script(data, docstring_preface)
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")