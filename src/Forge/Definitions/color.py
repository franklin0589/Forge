import numpy as np

class Color:
    def __init__(self, r:float, g:float, b:float, a:float = 1.0, scale:float = 1.0):
        self.r = r / scale
        self.g = g / scale
        self.b = b / scale
        self.a = a / scale

    def __iter__(self):
        return iter((self.r, self.g, self.b, self.a))

    @classmethod
    def from_tuple(cls, tpl: tuple[float, float, float, float]) -> "Color":
        return cls(tpl[0], tpl[1], tpl[2], tpl[3])

    @classmethod
    def from_numpy(cls, arr: np.ndarray) -> "Color":
        return cls(arr[0], arr[1], arr[2], arr[3])

    @classmethod
    def from_hexcode(cls, hexcode: str) -> "Color":
        hexcode = hexcode.lstrip("#")
        if len(hexcode) == 6:
            r, g, b = int(hexcode[0:2], 16), int(hexcode[2:4], 16), int(hexcode[4:6], 16)
            a = 255
        elif len(hexcode) == 8:
            r, g, b, a = int(hexcode[0:2], 16), int(hexcode[2:4], 16), int(hexcode[4:6], 16), int(hexcode[6:8], 16)
        else:
            raise ValueError("Invalid hexcode format")
        return cls(r, g, b, a, scale=255)

    def as_tuple(self) -> tuple[float, float, float, float]:
        return (self.r, self.g, self.b, self.a)

    def as_numpy(self) -> np.ndarray:
        return np.array([self.r, self.g, self.b, self.a], dtype=np.float32)

    def reverse(self):
        _red = self.red
        self.red = self.blue
        self.blue = _red
        return self

    def __iter__(self):
        return iter(self.as_tuple())

BLACK = Color(0.0, 0.0, 0.0, 1.0)
RED = Color(1.0, 0.0, 0.0, 1.0)
ORANGE = Color(1.0, 0.5, 0.0, 1.0)
YELLOW = Color(1.0, 1.0, 0.0, 1.0)
GREEN = Color(0.0, 1.0, 0.0, 1.0)
BLUE = Color(0.0, 0.0, 1.0, 1.0)
PURPLE = Color(0.5, 0.0, 0.5, 1.0)
WHITE = Color(1.0, 1.0, 1.0, 1.0)