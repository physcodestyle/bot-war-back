from modules.size import Size
from modules.coords import Coords
from modules.object import Object, ObjectType


class Map:
    def __init__(self, size: Size, objects: list[Object] = []):
        self.size = size
        self.objects = objects

    
    def get_size(self) -> Size:
        return self.size
    

    def get_object_list_at_coords(self, coords: Coords, type: ObjectType = ObjectType.bot) -> list[Object]:
        filtered_objects = []
        for obj in self.objects:
            if type == obj.get_type() and obj.is_own_object_coords(coords=coords):
                filtered_objects.append(obj)
        return filtered_objects
    

    def get_object_at_index(self, index: int) -> Object:
        return self.objects[index]
    

    def get_object_list(self, type: ObjectType = ObjectType.bot) -> list[Object]:
        filtered_objects = []
        for obj in self.objects:
            if type == obj.get_type():
                filtered_objects.append(obj)
        return filtered_objects


    def add_object(self, object: Object):
        self.objects.append(object)


    def remove_object_at_index(self, index: int):
        self.objects.pop(index)


    def remove_object_with_name(self, name: str, type: ObjectType = ObjectType.bot):
        index = 0
        for obj in self.objects:
            if type == obj.get_type() and name == obj.get_name():
                break
            else:
                index += 1
        self.objects.pop(index)
