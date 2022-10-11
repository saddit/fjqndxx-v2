class Sender(object):
    type: str
    key: str
    mode: str = 'fail'
    enabled: bool = False
    executor: any

    def __init__(self, dt: dict = {}) -> None:
        self.__dict__.update(dt)

    def can_send(self, success: bool) -> bool:
        return self.mode == 'both' \
            or (self.mode == 'fail' and not success) \
            or (self.mode == 'success' and success)
