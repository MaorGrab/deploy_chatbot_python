import logging
from deploy_chatbot_python.logging.logger import Logger
from deploy_chatbot_python.config import constants


def get_logger(name: str):
    if name in logging.Logger.manager.loggerDict:
        return logging.getLogger(name)
    logger = Logger(name=name).get_logger
    return logger

log = get_logger(name=constants.LOGGER_NAME)
