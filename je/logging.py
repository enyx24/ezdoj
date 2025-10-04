import logging
from colorama import Fore, Style, init

init(autoreset=True)

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{log_color}{message}{Style.RESET_ALL}"

def logging_config():
    handler = logging.StreamHandler()
    formatter = ColorFormatter("[%(levelname)s] %(asctime)s - %(name)s - %(message)s", "%H:%M:%S")
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers = [handler]

