from abc import ABC, abstractmethod
from enum import IntEnum
from datetime import datetime
import threading


class LogLevel(IntEnum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4


class LogAppender(ABC):
    @abstractmethod
    def append(self, formatted_message: str):
        pass


class ConsoleAppender(LogAppender):
    def append(self, formatted_message: str):
        print(formatted_message)


class FileAppender(LogAppender):
    def __init__(self, filename: str):
        self.filename = filename

    def append(self, formatted_message: str):
        with open(self.filename, "a") as f:
            f.write(formatted_message + "\n")


class LogFormatter(ABC):
    @abstractmethod
    def format(self, level: LogLevel, message: str) -> str:
        pass


class SimpleFormatter(LogFormatter):
    def format(self, level: LogLevel, message: str) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] [{level.name}] {message}"


class LogHandler(ABC):
    def __init__(self, level: LogLevel):
        self.level = level
        self.next_handler = None

    def set_next(self, handler: "LogHandler"):
        self.next_handler = handler
        return handler

    def handle(self, level: LogLevel, formatted_message: str):
        if level >= self.level:
            self.write(formatted_message)
        if self.next_handler:
            self.next_handler.handle(level, formatted_message)

    @abstractmethod
    def write(self, formatted_message: str):
        pass


class ConsoleHandler(LogHandler):
    def __init__(self, level: LogLevel, appender: LogAppender):
        super().__init__(level)
        self.appender = appender

    def write(self, formatted_message: str):
        self.appender.append(formatted_message)


class FileHandler(LogHandler):
    def __init__(self, level: LogLevel, appender: LogAppender):
        super().__init__(level)
        self.appender = appender

    def write(self, formatted_message: str):
        self.appender.append(formatted_message)


class Logger:
    _instance = None
    _lock = threading.Lock()

    def __init__(self, formatter: LogFormatter):
        if Logger._instance is not None:
            raise Exception("Use get_instance()")
        self.formatter = formatter
        self.handler_chain = None

    @staticmethod
    def get_instance(formatter: LogFormatter = None):
        with Logger._lock:
            if Logger._instance is None:
                Logger._instance = Logger(formatter or SimpleFormatter())
        return Logger._instance

    def set_handler_chain(self, handler: LogHandler):
        self.handler_chain = handler

    def log(self, level: LogLevel, message: str):
        formatted = self.formatter.format(level, message)
        if self.handler_chain:
            self.handler_chain.handle(level, formatted)

    def debug(self, message):
        self.log(LogLevel.DEBUG, message)

    def info(self, message):
        self.log(LogLevel.INFO, message)

    def warning(self, message):
        self.log(LogLevel.WARNING, message)

    def error(self, message):
        self.log(LogLevel.ERROR, message)


if __name__ == "__main__":
    logger = Logger.get_instance()

    console_handler = ConsoleHandler(LogLevel.DEBUG, ConsoleAppender())
    file_handler = FileHandler(LogLevel.ERROR, FileAppender("output/app.log"))
    console_handler.set_next(file_handler)
    logger.set_handler_chain(console_handler)

    logger.debug("Debugging value x=10")
    logger.info("Service started successfully")
    logger.warning("High memory usage detected")
    logger.error("Database connection failed")