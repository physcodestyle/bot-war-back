class Size:
    def __init__(self, width: int = 1, height: int = 1):
        self.width = width
        self.height = height

    
    def get(self) -> tuple[int, int]:
        return (self.width, self.height)
