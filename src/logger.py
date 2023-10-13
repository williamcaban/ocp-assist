import logging, sys, os

class Logger:
    def __init__(self, log_level=logging.INFO, show_message=False):
        msg=f"""
        #######################################################################################################
            For controlling verbosity of messages set LOG_LEVEL environment variable (e.g., INFO, DEBUG)
        #######################################################################################################
        """
        if show_message: print(msg)
        self.log_level=os.getenv("LOG_LEVEL", log_level)
        self.set_logger()
        
    def set_logger(self):
        """
        A simple logger function that logs messages at a specified level.

        :param level:   The logging level (e.g. 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        :param message: The message to log
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.log_level)

        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

        # console logging handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        # console_handler.setLevel(logging.INFO)
        console_handler.setStream(sys.stdout)
        console_handler.setFormatter(formatter)

        # file logging handler
        file_handler = logging.FileHandler('log.txt')
        file_handler.setLevel(logging.DEBUG)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

# logger.debug('Debug message')
# logger.info('Info message')
# logger.warning('Warning message')
# logger.error('Error message')
# logger.critical('Critical message')

# self.logger.debug(f"[{inspect.stack()[0][3]}] Message here.")
# self.logger = logger if logger else Logger(show_message=False).logger

