
from Forge.Definitions import Color
from Forge.Definitions.gradient import Gradient

class Pen:
    def __init__(self, brd_color: Color|str, fill_color: Color|str, width: float, gradient: Gradient = None):
        if isinstance(brd_color, str):
            brd_color = Color.from_hexcode(brd_color)
        self.brd_color : Color = brd_color
       
        if isinstance(fill_color, str):
            fill_color = Color.from_hexcode(fill_color)
        self.fill_color = fill_color
        
        self.width = width
        self.gradient = gradient