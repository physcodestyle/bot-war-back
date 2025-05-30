from modules.coords import Coords
from modules.bot import Bot


class SuperBot(Bot):
    def __init__(self, map, origin, name='SuperBot', is_vertical = True):
        super().__init__(map, origin, name, is_vertical)


    def shot(self) -> Coords:
        pass


    def give_report(self, shot_result: bool):
        pass