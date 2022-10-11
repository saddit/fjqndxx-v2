from datetime import datetime, timedelta


class TokenInfo(object):
    refresh_token: str
    refresh_expire: int
    token: str
    expire: int
    expire_at: float

    def __init__(self, dt: dict = {}) -> None:
        self.refresh_expire = dt.get('refreshExpire', dt.get('refresh_expire', 0))
        self.refresh_token = dt.get('refreshToken', dt.get('refresh_token', ''))
        self.token = dt.get('token', '')
        self.expire = dt.get('expire', 0)
        ts = (datetime.now() + timedelta(seconds=self.expire)).timestamp()
        self.expire_at = dt.get('expire_at', ts)

    def get_expired_at(self) -> datetime:
        return datetime.fromtimestamp(self.expire_at)
