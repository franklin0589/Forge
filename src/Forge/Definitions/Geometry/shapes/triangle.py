import Forge.Definitions as gadget

class Triangle:
    def __init__(self, pointA: gadget.Point, pointB: gadget.Point, pointC: gadget.Point):
        self.pointA = pointA
        self.pointB = pointB
        self.pointC = pointC

    def edges(self) -> list[gadget.Line]:
        return [
            gadget.Line(self.pointA, self.pointB),
            gadget.Line(self.pointB, self.pointC),
            gadget.Line(self.pointC, self.pointA)
        ]

    def midpoint(self) -> gadget.Point:
        x = (self.pointA.x + self.pointB.x + self.pointC.x) / 3
        y = (self.pointA.y + self.pointB.y + self.pointC.y) / 3
        return gadget.Point(x, y)

    

    def form(self):
        # Define the triangle mesh structure here
        pass