import logging
from pathlib import Path

class Logger:
    def __init__(self):
        # Create log directory if it doesn't exist
        log_dir = Path("log")
        log_dir.mkdir(parents=True, exist_ok=True)

        # System-wide logger setup
        self.system_logger = logging.getLogger("system_logger")
        self.system_logger.setLevel(logging.INFO)  # INFO and above

        system_log_file = log_dir / "logs_system.log"
        system_handler = logging.FileHandler(system_log_file, mode='a', encoding='utf-8')
        system_formatter = logging.Formatter(
            fmt='%(asctime)s - %(module)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        system_handler.setFormatter(system_formatter)
        self.system_logger.addHandler(system_handler)

        # Query logger setup
        self.query_logger = logging.getLogger("query_logger")
        self.query_logger.setLevel(logging.INFO)

        query_log_file = log_dir / "logs_query.log"
        query_handler = logging.FileHandler(query_log_file, mode='a', encoding='utf-8')
        query_formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        query_handler.setFormatter(query_formatter)
        self.query_logger.addHandler(query_handler)

    def log_system(self, level, message):
        if level.lower() == 'info':
            self.system_logger.info(message)
        elif level.lower() == 'warning':
            self.system_logger.warning(message)
        elif level.lower() == 'error':
            self.system_logger.error(message)
        elif level.lower() == 'debug':
            self.system_logger.debug(message)
        else:
            self.system_logger.info(message)

    def log_query(self, message):
        # Queries can be logged at INFO level
        self.query_logger.info(message)


# Example usage
if __name__ == "__main__":
    logger = Logger()
    logger.log_system('info', "System initialized successfully.")
    logger.log_system('error', "An error occurred in module xyz.")
    logger.log_query("User asked: How do I fix package conflicts?")
