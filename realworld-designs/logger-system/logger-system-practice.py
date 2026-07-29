from enum import IntEnum
from abc import ABC, abstractmethod
from datetime import datetime

class LogLevel(IntEnum):
    DEBUG = 1
    INFO = 2
    WARN = 3
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
        with open(self.filename, "a") as file:
            file.write(formatted_message + "\n")

class LogFormatter(ABC):
    def format(self, message: str, Level: LogLevel):
        pass

class PlainTextFormatter(LogFormatter):
    def format(self, message: str, level: LogLevel):
        timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        return f"[{timestamp}] [{level.name}] [{message}]"

class LogHandler(ABC):
    def __init__(self, level: LogLevel):
        self.level = level
        self.next_handler = None 

    def set_next(self, handler):
        self.next_handler = handler

    def handle(self, level: LogLevel, message: str):
        if level >= self.level:
            self.write(message)
        if self.next_handler:
            self.next_handler.handle(level, message)
    
    @abstractmethod
    def write(self, message):
        pass

class ConsoleHandler(LogHandler):
    def __init__(self, level: LogLevel, appender: LogAppender):
        super().__init__(level)
        self.appender = appender
    
    def write(self, message):
        self.appender.append(message)

class FileHandler(LogHandler):
    def __init__(self, level: LogLevel, appender: LogAppender):
        super().__init__(level)
        self.appender = appender

    def write(self, message):
        self.appender.append(message)

class Logger:
    __instance = None

    def __new__(cls, formatter: LogFormatter):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.formatter = formatter
            cls.handler_chain = None
        return cls.__instance

    def set_handler_chain(self, handler: LogHandler):
        self.handler_chain = handler

    def log(self, level: LogLevel, message: str):
        formatted_message = self.formatter.format(message, level)
        if self.handler_chain:
            self.handler_chain.handle(level, formatted_message)

    def log_info(self, message: str):
        self.log(LogLevel.INFO, message)

    def log_warn(self, message: str):
        self.log(LogLevel.WARN, message)

    def log_error(self, message: str):
        self.log(LogLevel.ERROR, message)

    def log_debug(self, message: str):
        self.log(LogLevel.DEBUG, message)

if __name__ == "__main__":

    logger = Logger(PlainTextFormatter())

    console_handler = ConsoleHandler(LogLevel.DEBUG, ConsoleAppender())
    file_handler = FileHandler(LogLevel.INFO, FileAppender("text_logs.txt"))
    console_handler.set_next(file_handler)
    logger.set_handler_chain(console_handler)

    logger.log_info("Gokul Ajith logged in!")
    logger.log_error("Error uploading invoice")

    logger = Logger(PlainTextFormatter())