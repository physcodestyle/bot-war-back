import sys, random
from modules.coords import Coords
from modules.object import Object, ObjectType
from modules.map import Map
from modules.bot import Bot
from bots.bots import is_bot_registered, get_bot_class_with_name


class BotFactory:
    def __init__(self):
        self.map = None
        self.bot_modules = []


    def build(self, map_size: int, bot_list: list[str]) -> list[Bot]:
        bots = [Bot]
        self.map = Map(size=map_size)
        for bot_name in bot_list:
            if is_bot_registered(bot_name=bot_name):
                NewBot = get_bot_class_with_name(bot_name=bot_name)
                orientation = self._generate_bot_orientation()
                coords = self._generate_bot_coords(is_vertical=orientation)
                bot = NewBot(map=self.map, origin=coords, name=bot_name, is_vertical=orientation)
                bots.append(bot)
                self.map.add_object(Object(origin=bot.get_origin(), size=bot.get_size(), name=bot_name, object_type=ObjectType.bot))
    

    def _generate_bot_coords(self, is_vertical: bool = True) -> Coords:
        size, _ = self.map.get_size().get()
        top = random.random.randint(1, size)
        left = random.random.randint(1, size)
        height = 3 if is_vertical else 2
        width = 2 if is_vertical else 3
        for i in range(height + 2):
            for j in range(width + 2):
                point = Coords(top=top - 1 + i, left=left - 1 + j)
                if self.map.get_object_list_at_coords(coords=point):
                    return self._generate_bot_coords(is_vertical=is_vertical)
        return Coords(top=top, left=left)
    

    def _generate_bot_orientation(self, ) -> bool:
        return bool(random.getrandbits(1))
