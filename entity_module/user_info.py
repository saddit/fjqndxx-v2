from exception.exceptions import KnownException


class UserInfo(object):
    id: int
    name: str
    id_number: str
    platform: int = 3
    openid: str
    mp_openid: str
    unionid: str

    def __init__(self, dt: dict = {}) -> None:
        self.id = dt.get('id', 0)
        self.name = str(dt.get('name', ''))
        self.id_number = dt.get('id_number', '')
        self.platform = dt.get('platform', 3)
        self.openid = dt.get('openid', '')
        try:
            self.mp_openid = dt['mp_openid']
            self.unionid = dt['unionid']
        except Exception as e:
            raise KnownException("初始化TokenInfo失败")
