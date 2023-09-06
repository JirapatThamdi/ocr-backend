"""
This module is used to initialize the logger for the application.
This will log to the console and to a file if specified.
"""
import requests
import threading
import logging
import urllib.parse
from datetime import datetime, timedelta
import app.utils.env_config as config
from discord_webhook import DiscordWebhook

# add color to the log levels
# protected member access # pylint: disable=protected-access
logging._levelToName[logging.DEBUG] = '\033[34mDEBUG\033[0m'
logging._levelToName[logging.INFO] = '\033[32mINFO\033[0m'
logging._levelToName[logging.WARNING] = '\033[33mWARNING\033[0m'
logging._levelToName[logging.ERROR] = '\033[91mERROR\033[0m'
logging._levelToName[logging.CRITICAL] = '\033[31mCRITICAL\033[0m'

logging.basicConfig(level=config.LOG_LEVEL,
                    format='%(asctime)s [ %(levelname)s ] [%(name)s %(lineno)d] %(message)s')

def perform_get_request_with_timeout(msg, timeout=5):
    def do_get_request(msg):
        try:
            msg = config.DISCORD_PREFIX + " : " + msg
            webhook = DiscordWebhook(url=config.DISCORD_WEBHOOK_URL, 
                                     content= msg, 
                                     timeout=timeout)
            _ = webhook.execute()
        except Exception as excep:
            logging.error("Error sending discord notification: %s", excep)
            return

    thread = threading.Thread(target=do_get_request, args=(msg,))
    thread.start()
class DiscordLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.message_map = {}

    def emit(self, record):
        if record.levelno >= logging.WARNING:
            msg =self.format(record)
            self.add_message(msg)
    
    def add_message(self, msg):
        current_time = datetime.now()
        if msg in self.message_map:
            last_time = self.message_map[msg]
            if current_time - last_time < timedelta(hours=1):
                return  # Filter out the message if received within 1 hour
        self.message_map[msg] = current_time
        perform_get_request_with_timeout(msg)

def init_logger(name):
    """
    Initialize the logger with module name and return it.
    """
    logger = logging.getLogger(name)
    logger.setLevel(config.LOG_LEVEL)
    formatter = logging.Formatter(
        "%(asctime)s [ %(levelname)s ] [%(name)s %(lineno)d] %(message)s")
    if config.LOG_FILE:
        file_handler = logging.FileHandler(config.LOG_FILE)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    
    # add custom log handler
    # logger.addHandler(custom_log)

    # best practices for library logging:
    # https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
    # imported library uses root logger, so we need to remove the root logger's handler
    # TODO: find a better way to do this # pylint: disable=fixme

    root_logger = logging.getLogger()
    if len(root_logger.handlers) > 0:
        root_logger.removeHandler(root_logger.handlers[0])

    logger.addHandler(stream_handler)

    return logger
