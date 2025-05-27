import logging
from deploy_chatbot_python.logging.logger import Logger


def get_logger(name: str):
    if name in logging.Logger.manager.loggerDict.keys():
        return logging.getLogger(name)
    logger = Logger(name=name).get_logger
    return logger

logger_ = get_logger(name='logger_name')
