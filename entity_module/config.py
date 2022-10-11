from entity_module.sender import Sender
from entity_module.token_info import TokenInfo
from entity_module.user_info import UserInfo


class Config(object):
    user_info: UserInfo
    token_info: TokenInfo
    max_retry: int
    sender: Sender
    
    __persist_func: callable
    
    def __init__(self, dt: dict, save: callable) -> None:
        self.__persist_func = save
        self.max_retry = dt['max_retry']
        self.token_info = TokenInfo(dt['token_info'])
        self.user_info = UserInfo(dt['user_info'])
        self.sender = Sender(dt['sender'])
        
    def persist(self):
        self.__persist_func({
            'token_info': self.token_info.__dict__,
            'user_info': self.user_info.__dict__,
            'sender': self.sender.__dict__,
            'max_retry': self.max_retry
        })