class UnauthorizedException(Exception):

    def __init__(self, message: str | None = "invalid access credentials") -> None:
        self.status_code = 401
        self.type = "UnauthorizedException"
        self.message = message

    def __str__(self):
        return str(self.__dict__)