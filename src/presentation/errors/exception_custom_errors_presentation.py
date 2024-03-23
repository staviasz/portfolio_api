class ExceptionCustomPresentation(Exception):
    def __init__(self, message: str, type: str, status_code: int):
        self.body = {"message": message, "type": type}
        self.status_code = status_code
