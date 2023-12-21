from datetime import datetime as dt
from enum import Enum
from dataclasses import dataclass
import os


class LogType(Enum):
    LOG_INFO: int = 0
    LOG_WARNING: int = 1
    LOG_ERROR: int = 2


@dataclass(frozen=True)
class LogEntry:
    log_t: LogType
    message: str


class Logger:
    def __init__(
        self,
        console_print=False,
        file_write=False,
        file_path="log.txt",
    ):
        self.logs: list = []
        self.console_print: bool = console_print
        self.file_path: str = file_path
        self.file_write: bool = file_write

    @staticmethod
    def current_date_time_to_string() -> str:
        return dt.now().strftime("%b-%d-%Y %I:%M:%S %p")

    def write_log_to_file(self, message) -> None:
        if not self.file_write:
            return
        if not os.path.exists(self.file_path):
            open(self.file_path, "w").close()
        with open(self.file_path, "a") as f:
            f.write(message + "\n")

    def print_log_to_console(self, message) -> None:
        if not self.console_print:
            return
        print(message)

    def Log(self, message) -> None:
        message = f"LOG: [{self.current_date_time_to_string()}] {message}"
        # print out the log message to the console in green
        self.print_log_to_console(f"\033[92m{message}\033[0m")
        self.write_log_to_file(message)
        self.logs.append(LogEntry(LogType.LOG_INFO, message))

    def Warn(self, message) -> None:
        message = f"WARN: [{self.current_date_time_to_string()}] {message}"
        # print out the warning message to the console in yellow
        self.print_log_to_console(f"\033[93m{message}\033[0m")
        self.write_log_to_file(message)
        self.logs.append(LogEntry(LogType.LOG_WARNING, message))

    def Err(self, message) -> None:
        message = f"ERR: [{self.current_date_time_to_string()}] {message}"
        # print out the error message to the console in red
        self.print_log_to_console(f"\033[91m{message}\033[0m")
        self.write_log_to_file(message)
        self.logs.append(LogEntry(LogType.LOG_ERROR, message))

    def get_logs(self) -> list:
        return self.logs

    def clear_logs(self) -> None:
        self.logs.clear()
