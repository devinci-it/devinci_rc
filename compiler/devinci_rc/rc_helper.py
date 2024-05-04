import os
import configparser
from .rc_logger import setup_logger

class FileParser:
    def parse_input_file(self, input_file):
        """
        Parse an input file using the configparser module.

        Args:
            input_file (str): The path to the input file to be parsed.

        Returns:
            configparser.ConfigParser: A ConfigParser object with the data read from the input file.
            None: If an exception occurs during the parsing process, the method will handle the exception and return None.

        Raises:
            Exception: If there's an error while parsing the input file, it raises an exception which is then handled by the ErrorHandler.
        """
        try:
            config = configparser.ConfigParser()
            config.read(input_file)
            return config
        except Exception as e:
            ErrorHandler.handle_exception(f"An error occurred while parsing the input file: {e}")
            return None

class FileWriter:
    @staticmethod
    def _write_to_file(output_file, content):
        try:
            with open(output_file, 'w') as file:
                file.write(content)
            LoggerManager.display_info("File written successfully.")
        except Exception as e:
            ErrorHandler.handle_exception(f"An error occurred while writing to the file: {e}")

    @staticmethod
    def write_to_file(output_file, content, force=False):
        try:
            # Check if the file or directory exists
            if not force and os.path.exists(output_file):
                raise FileExistsError(f"The file '{output_file}' already exists.")

            # Create directories if they don't exist
            output_dir = os.path.dirname(output_file)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Write to the file
            FileWriter._write_to_file(output_file, content)
        except Exception as e:
            ErrorHandler.handle_exception(f"An error occurred while writing to the file: {e}")
class LoggerManager:
    def __init__(self, debug=False):
        self.debug = debug
        self.logger=setup_logger(debug=debug)

    def display_info(self, message):
        print(message)
        self.logger.info(message)


class ErrorHandler:
    @staticmethod
    def handle_exception(logger,message):
        print(message)
        logger.error(message)
