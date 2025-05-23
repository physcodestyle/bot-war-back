from modules.coords import Coords
from modules.map import Map


class Bot:
    def __init__(self, coords: Coords, map: Map):
        self.origin = coords
        self.map = map


    def shot(self) -> Coords:
        pass


    def result(self, result: bool) -> bool:
        pass
