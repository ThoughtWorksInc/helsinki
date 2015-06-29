import logging

def init_logger():
    logger = logging.getLogger('helsinki_log')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                    '%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

_logger = init_logger()

def get_logger():
    return _logger
