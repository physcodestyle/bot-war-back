from modules.coords import Coords
from modules.size import Size
from enum import Enum


class ObjectType(Enum):
    shot = 1
    bot = 2


class Object:
    def __init__(self, origin: Coords, size: Size, name: str = '', object_type: ObjectType = ObjectType.shot):
        self.origin = origin
        self.size = size
        self.name = name
        self.type = object_type
    

    def get_name(self) -> str:
        return self.name
    

    def get_origin(self) -> Coords:
        return self.origin
    

    def get_size(self) -> Size:
        return self.size
    

    def get_type(self) -> ObjectType:
        return self.type

    
    def is_own_object_coords(self, coords: Coords) -> bool:
        left, top = self.origin.get()
        width, height = self.size.get()
        right, bottom = left + width, top + height
        point_left, point_top = coords.get()
        return point_left >= left and point_left <= right and point_top >= top and point_top <= bottom
