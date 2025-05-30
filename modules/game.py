from modules.object import Object, ObjectType
from modules.map import Map
from modules.bot import Bot
from modules.size import Size


class Game:
    def __init__(self, map_size: int, bots: list[Bot]):
        objects = []
        for bot in bots:
            objects.append(Object(origin=bot.get_origin(), size=bot.get_size(), name=bot.get_name(), object_type=ObjectType.bot))
        self.map = Map(size=map_size, objects=objects)
        self.bots = bots
    

    def play_round(self) -> list[str]:
        for bot in self.bots:
            coords = bot.shot()
            self.map.add_object(Object(origin=coords, size=Size(), name=bot.get_name()))
            bot.give_report(shot_result=len(self.map.get_object_list_at_coords(coords=coords)) == 1)
            if not bot.is_live():
                self.map.remove_object_with_name(bot.get_name())
                bot_index = self._get_bot_index_with_name(bot.get_name())
                if not bot_index == -1:
                    self.bots.pop(bot_index)
        return self.get_report()


    def get_report(self) -> list[str]:
        bot_list = []
        for bot in self.bots:
            bot_list.append(bot.get_name())
        return bot_list


    def _get_bot_index_with_name(self, name: str) -> int:
        index = 0
        for bot in self.bots:
            if name == bot.get_name():
                return index
        return -1
