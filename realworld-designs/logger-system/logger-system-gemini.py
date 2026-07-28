from abc import ABC, abstractmethod
from enum import IntEnum
import datetime

# ========================================================
# 1. LOG LEVEL ENUM (Hierarchical order via IntEnum)
# ========================================================
class LogLevel(IntEnum):
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4


class LogMessage:
    def __init__(self, level: LogLevel, message: str):
        self.level = level
        self.message = message
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def format() -> str:
        pass

# ========================================================
# 2. ABSTRACT HANDLER (Chain Mechanics)
# ========================================================
class AbstractLogger(ABC):
    def __init__(self, level: LogLevel):
        self.level = level
        self.next_logger: 'AbstractLogger' = None

    def set_next(self, next_logger: 'AbstractLogger') -> 'AbstractLogger':
        self.next_logger = next_logger
        return next_logger  # Enables fluent chaining: l1.set_next(l2).set_next(l3)

    def log_message(self, level: LogLevel, message: str):
        # If the current handler's log level threshold is met, write the log
        if self.level <= level:
            self.write(message)
        
        # Pass the message down the rest of the chain
        if self.next_logger:
            self.next_logger.log_message(level, message)

    @abstractmethod
    def write(self, message: str):
        pass


# ========================================================
# 3. CONCRETE LOGGERS (Specific Log Sinks / Behaviors)
# ========================================================
class ConsoleLogger(AbstractLogger):
    def __init__(self, level: LogLevel):
        super().__init__(level)

    def write(self, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🟢 [CONSOLE] [{timestamp}] [LEVEL: {self.level.name}]: {message}")


class FileLogger(AbstractLogger):
    def __init__(self, level: LogLevel, file_path: str = "app.log"):
        super().__init__(level)
        self.file_path = file_path

    def write(self, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"📁 [FILE] [{timestamp}] [LEVEL: {self.level.name}]: {message}"
        # Simulating writing to a physical log file
        print(f"--> Writing to log file ({self.file_path}): {log_entry}")


class ErrorLogger(AbstractLogger):
    def __init__(self, level: LogLevel):
        super().__init__(level)

    def write(self, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🚨 [CRITICAL ALERT / SENTRY] [{timestamp}] [LEVEL: {self.level.name}]: {message}")


# ========================================================
# 4. LOGGER MANAGER (Singleton Factory for Chains)
# ========================================================
class LoggerManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:                                                                                                                                                                                                                   
            cls._instance = super().__new__(cls)
            cls._instance._chain = cls._build_chain()
        return cls._instance

    @staticmethod
    def _build_chain() -> AbstractLogger:
        # Build the chain: Console (DEBUG+) -> File (INFO+) -> Error/Alert (ERROR+)
        console_logger = ConsoleLogger(LogLevel.DEBUG)
        file_logger = FileLogger(LogLevel.INFO)
        error_logger = ErrorLogger(LogLevel.ERROR)

        console_logger.set_next(file_logger).set_next(error_logger)
        return console_logger

    def log(self, level: LogLevel, message: str):
        self._chain.log_message(level, message)


if __name__ == "__main__":
    logger = LoggerManager()

    print("--- 1. Logging DEBUG Message (Only Console handles it) ---")
    logger.log(LogLevel.DEBUG, "User clicked on button 'A1'")

    print("\n--- 2. Logging INFO Message (Console + File handle it) ---")
    logger.log(LogLevel.INFO, "Payment processing initiated for Booking BKG-1002")

    print("\n--- 3. Logging ERROR Message (Console + File + Error Alert handle it) ---")
    logger.log(LogLevel.ERROR, "Database Connection Lost! Unable to write ticket transaction.")