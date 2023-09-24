from enum import Enum

__app_name__ = "todo"
__version__ = "0.1.0"


class ReturnCode(Enum):
    SUCCESS = 0
    DIR_ERROR = 1
    FILE_ERROR = 2
    DB_READ_ERROR = 3
    DB_WRITE_ERROR = 4
    JSON_ERROR = 5
    ID_ERROR = 6
