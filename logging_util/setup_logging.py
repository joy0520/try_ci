import logging
import logging.handlers
from multiprocessing import Queue

LOG_FORMAT = '%(asctime)s %(processName)22s %(levelname)-8s | %(message)s'


def setup_logging(log_file_path: str, name: str = '', daily: bool = True,
                  stream_level: int = logging.INFO, file_level: int = logging.DEBUG):
    """
    I hope this setting would fit the three main programs, FEMD, SID and PLU.
    Use logging as usual whether in main process or a sub-process, since QueueListener
    and QueueHandler handle multi-processing stuff for you already.

    Usage example:

    Main.py
        ...
        setup_logging()
        ...

    Sub_process.py
        ...
        logger = logging.getLogger('path/to/log.txt')
        logger.debug()


    @param log_file_path: path to the log file
    @param name: the name attribute to get a logging.Logger instance
    @param daily: True to rotate file daily, or False to do it hourly
    @param stream_level: logging level for StreamHandler
    @param file_level: logging level for FileHandler
    """
    # root logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # default is WARNING

    # formatter
    formatter = logging.Formatter(LOG_FORMAT)
    # stream handler
    stream_handler = _stream_handler(formatter, stream_level)
    # file handler
    file_handler = _file_handler(log_file_path, formatter, file_level, daily)

    _setup_queue_handler_and_listener(logger, stream_handler, file_handler)


def _daily_file_handler(log_file_path: str, backup_count: int = 7) -> logging.FileHandler:
    h = logging.handlers.TimedRotatingFileHandler(log_file_path, when='midnight', backupCount=backup_count, utc=True)

    return h


def _file_handler(log_file_path: str, formatter: logging.Formatter, level: int, daily: bool) -> logging.FileHandler:
    if daily:
        file_handler = _daily_file_handler(log_file_path)
    else:
        file_handler = _hourly_file_handler(log_file_path)

    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    return file_handler


def _hourly_file_handler(log_file_path: str, backup_count: int = 168) -> logging.FileHandler:
    h = logging.handlers.TimedRotatingFileHandler(log_file_path, when='H', backupCount=backup_count, utc=True)

    return h


def _stream_handler(formatter: logging.Formatter, level: int) -> logging.StreamHandler:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    return stream_handler


def _setup_queue_handler_and_listener(logger: logging.Logger, *handlers: logging.Handler):
    """
    Use QueueListener and QueueHandler to handle multiprocessing use case.
    @param logger: parent logger for QueueHandler to add
    @param handlers: handlers that handle LogRecords which come out off a multiprocessing.Queue
    """
    q = Queue()
    # queue handler
    queue_handler = logging.handlers.QueueHandler(q)
    queue_handler.setLevel(logging.DEBUG)
    logger.addHandler(queue_handler)

    # queue listener
    queue_listener = logging.handlers.QueueListener(q, *handlers, respect_handler_level=True)
    queue_listener.start()
