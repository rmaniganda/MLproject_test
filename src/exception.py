import sys
import os
from src.logger import logging
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error occurred in python script name [{file_name}] line number [{exc_tb.tb_lineno}] error message [{error}]"
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message

if __name__ == "__main__":
    try:
        log_file_path = os.path.join(os.getcwd(), "error.log")
        print(f"Log file path: {log_file_path}")

        # Clear any previous handlers before adding a new one
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # Try logging configuration
        logging.basicConfig(
            filename=log_file_path,
            filemode='w',  # Overwrite the log file each time
            format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
            level=logging.ERROR
        )

        # Add a console handler to see log output in the terminal as well
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter("[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)

        # Test logging functionality
        logging.error("Test log message")

        a = 1 / 0  # This will raise a ZeroDivisionError

    except Exception as e:
        print(f"Error while setting up logging: {e}")
        raise

    try:
        a = 1 / 0  # This will raise a ZeroDivisionError
    except ZeroDivisionError as e:
        logging.error("Divide by Zero")  # Log error message
        raise CustomException(str(e), sys)  # Raise the CustomException with details
