class KnownException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnexpectedException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)