class Coords:
    def __init__(self, top: int, left: int):
        self.top = top
        self.left = left
    

    def get(self) -> tuple[int, int]:
        return (self.top, self.left)
