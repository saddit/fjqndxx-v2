class UserInfo(object):
    id: int
    name: str
    id_number: str
    platform: int = 3
    openid: str
    
    def __init__(self, dt: dict = {}) -> None:
        self.__dict__.update(dt)