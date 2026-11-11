import Forge.Definitions.gmath as math
from Forge.Definitions.path.segment import Segment2D


class Line2D(Segment2D):
    def __init__(self, start: math.Point, end: math.Point):
        super().__init__(start, end)

    def length(self) -> float:
        """Return the length of the line segment."""
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        return (dx**2 + dy**2)**0.5

    def direction(self) -> math.Vector2:
        """Return the direction vector of the line as a tuple (dx, dy)."""
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        return math.Vector2(dx, dy).normalize()
        
    def at(self, t: float):
        """Return the point at parameter t along the line, where t is between 0 and 1."""
        x = self.start.x + t * (self.end.x - self.start.x)
        y = self.start.y + t * (self.end.y - self.start.y)
        return math.Point(x, y)