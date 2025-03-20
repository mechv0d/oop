from datetime import datetime as dt
import hashlib
import uuid
from typing import Any

# region naming
SENDER_RUNTIME = "RUNTIME"
RECORD_BEFORE_TEXT = ">>> "
DATETIME_FORMAT = "[%Y-%m-%d %H:%M:%S] "
# endregion


def md5(date_time_str: str = dt.now().strftime("[%Y-%m-%d %H:%M:%S.%f]"), salt: str = str(uuid.uuid4())) -> str:
    combined = f"{date_time_str}{salt}"
    m = hashlib.md5()
    m.update(combined.encode('utf-8'))
    return m.hexdigest()


class Logger:
    file_name: str = ''
    __closed: bool
    print_errors: bool

    def __init__(self, file_name: str, closed_on_start: bool = False, print_errors: bool = False):
        self.file_name = file_name
        self.__closed = closed_on_start
        self.print_errors = print_errors

        if not self.__closed:  # file check
            try:
                open(self.file_name, "a").close()
            except Exception as e:
                print(f"Failed to create/open log file: {e}")
                self.__closed = True

    def log(self, msg: str) -> str:
        line = self.record(SENDER_RUNTIME, msg)
        return line

    def echo(self, sender: Any, msg: str) -> str:
        line = self.record(sender, msg)
        line = line.replace(RECORD_BEFORE_TEXT, '')
        print(line)
        return line

    def record(self, sender: Any, msg: str) -> str | None:
        now = dt.now()
        formatted_datetime = now.strftime(DATETIME_FORMAT)

        if self.__closed:
            if self.print_errors:
                print(formatted_datetime, f"Logger is closed, cannot log message: {msg}")
            return None

        try:
            before_text = RECORD_BEFORE_TEXT if sender != SENDER_RUNTIME else ''
            line = formatted_datetime + before_text + (sender + ": " if sender is not None else '') + msg + "\n"
        except TypeError:
            line = formatted_datetime + msg + "\n"

        try:
            with open(self.file_name, "a", encoding='utf-8') as f:
                f.write(line)
        except Exception as e:
            print(f"Error writing to log file: {e}")
            self.__closed = True  # close the logger if error

        return line

    def close(self) -> None:
        self.__closed = True

    def open(self) -> None:
        self.__closed = False


base_logger = Logger(f'track_{md5()}.txt')
