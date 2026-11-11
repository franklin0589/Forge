import Forge.Definitions as gadget

class Rectangle:
    @classmethod
    def from_points(cls, top_left:gadget.Point, bottom_right:gadget.Point):
        width = bottom_right.x - top_left.x
        height = bottom_right.y - top_left.y
        return cls(top_left, width, height)

    def __init__(self, origin:gadget.Point, width:int, height:int):
        self.origin = origin
        self.width = width
        self.height = height

    def inbounds(self, point:gadget.Point) -> bool:
        return (self.origin.x <= point.x <= self.origin.x + self.width) and \
               (self.origin.y <= point.y <= self.origin.y + self.height)

    def area(self) -> int:
        return self.width * self.height


