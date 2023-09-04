import os

PROJECT_NAME = os.environ.get('PROJECT_NAME', "OCR Backend")
RELEASE_VERSION = os.environ.get('RELEASE_VERSION', "DEV")

DEBUG = int(os.environ.get('DEBUG', 0))

HOST = os.environ.get('HOST', "0.0.0.0")
PORT = int(os.environ.get('PORT', 8008))

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
LOG_FILE = os.environ.get('LOG_FILE', None)

MONGO_USERNAME = os.environ.get('MONGO_USER_NAME', "plam2544")
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', "RULiHPvYiDIFL3KE")
MONGO_HOST = os.environ.get('MONGO_HOST', "cluster0.0x0qdjp.mongodb.net")
MONGO_PARAMS = os.environ.get('MONGO_EXTRA_PARAMS', "retryWrites=true&w=majority")
mongo_conn_str = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_PARAMS}"
MONGO_CONN_STR = os.environ.get('MONGO_CONN_STR', mongo_conn_str)
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', "ocr-engine")

def print_config(logger):
    """
    Print the configuration
    """
    logger.info(f"HOST: {HOST}")
    logger.info(f"PORT: {PORT}")
    logger.info(f"LOG_LEVEL: {LOG_LEVEL}")
    logger.info(f"LOG_FILE: {LOG_FILE}")
    logger.info(f"DEBUG: {DEBUG}")
    logger.info(f"MONGO_CONN_STR: {MONGO_CONN_STR}")
    logger.info(f"MONGO_DB_NAME: {MONGO_DB_NAME}")


def print_config_warning(logger):
    """
    Print the configuration warnings
    """
    logger.warning("......................................................")
    if LOG_LEVEL == "DEBUG":
        logger.warning(
            "LOG_LEVEL is set to DEBUG. This is not recommended for production.")

    if LOG_FILE is None:
        logger.warning("LOG_FILE is not set.")

    if DEBUG:
        logger.warning(
            "DEBUG is set to True. This is not recommended for production.")

