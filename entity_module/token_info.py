from datetime import datetime


class TokenInfo(object):
    refreshToken: str
    refreshExpire: int
    token: str
    expire: int
    # last_refresh_time: datetime
    
    def __init__(self, dt: dict = {}) -> None:
        self.__dict__.update(dt)