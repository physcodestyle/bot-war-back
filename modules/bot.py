from modules.coords import Coords
from modules.map import Map
from modules.size import Size
from modules.object import Object, ObjectType


class Bot:
    def __init__(self, map: Map, origin: Coords, name: str = 'Bot', is_vertical: bool = True):
        self.name = name
        self.map = map
        self.live = 6
        width = 2 if is_vertical else 3
        height = 3 if is_vertical else 2
        size = Size(width=width, height=height)
        bot = Object(origin=origin, size=size, object_type=ObjectType.bot)
        self.map.add_object(object=bot)
    

    def is_live(self) -> bool:
        return self.live > 0
    

    def get_origin(self) -> Coords:
        return self.map.get_object_at_index(index=0).get_origin()
    

    def get_size(self) -> Size:
        return self.map.get_object_at_index(index=0).get_size()


    def get_name(self) -> str:
        return self.name


    def shot(self) -> Coords:
        pass


    def give_report(self, shot_result: bool):
        pass
