from entity_module.sender import Sender
from entity_module.token_info import TokenInfo
from entity_module.user_info import UserInfo


class Config(object):
    user_info: UserInfo
    token_info: TokenInfo
    max_retry: int
    sender: Sender
    
    __persist_func: function
    
    def __init__(self, dt: dict, save: function) -> None:
        self.__persist_func = save
        self.__dict__.update(dt)
        
    def persist(self):
        self.__persist_func(self)