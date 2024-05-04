import logging

def setup_logger(debug=False):
    """
    Set up a logger to write debug and error information to a log file.

    Returns:
        logging.Logger: A logger instance.
    """

    logger = logging.getLogger(__name__)
    level=logging.WARNING if not debug else logging.DEBUG
    logger.setLevel(logging.DEBUG)

    # Create a file handler for logging to a file
    handler = logging.FileHandler('rc.log')
    handler.setLevel(logging.DEBUG)  # Set the level for the handler to DEBUG

    # Create a formatter for the log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    # Add a console handler to log messages to the console as well
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)  # Set the level for the console handler to ERROR
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
