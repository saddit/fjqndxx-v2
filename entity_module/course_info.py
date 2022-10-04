from mimetypes import init


class CourseInfo(object):
    id: int
    season_episode: str
    
    def __init__(self, dt: dict = {}) -> None:
        self.__dict__.update(dt)