
from Forge.Definitions.gmath.vector import Point, Vertex

class Segment2D:
    def __init__(self, start: Point, end: Point):
        if start.dimension != end.dimension:
            raise ValueError("Start and end points must have the same dimension.")
        self.dimension = start.dimension
        self.start = start
        self.end = end
