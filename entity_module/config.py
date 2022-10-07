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
        self.__dict__.update(dt)
        self.__persist_func = save
        self.token_info = TokenInfo(dt['token_info'])
        self.user_info = UserInfo(dt['user_info'])
        self.sender = Sender(dt['sender'])
        
    def persist(self):
        self.__persist_func(self)