
import cairo

class Typography:
    def __init__(self, size:int = 12, face:str = "Segoe UI", slant:int = 0, bold:int = 0):
        self.face = face
        self.slant = slant
        self.bold = bold
        self.size = size

    def get_slant(self):
        slants=[cairo.FONT_SLANT_NORMAL, cairo.FONT_SLANT_ITALIC, cairo.FONT_SLANT_OBLIQUE]
        return slants[self.slant]

    def get_weight(self):
        weights=[cairo.FONT_WEIGHT_NORMAL, cairo.FONT_WEIGHT_BOLD]
        return weights[self.bold]
