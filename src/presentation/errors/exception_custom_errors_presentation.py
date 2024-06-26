from typing_extensions import Any


class ExceptionCustomPresentation(Exception):
    def __init__(self, message: str, type: str, status_code: int, error: Any = None):
        self.body = (
            {"message": message, "type": type, "error": error}
            if error
            else {"message": message, "type": type}
        )
        self.status_code = status_code
