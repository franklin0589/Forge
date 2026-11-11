from Forge.Definitions.path.segment import Segment2D
from Forge.Definitions.path.line import Line2D
import Forge.Definitions.gmath as math
import numpy as np

class Curve2D(Segment2D):
    @classmethod
    def from_control_line(cls, start: math.Point, control_line: Line2D, end: math.Point):
        return cls(start, control_line.start, control_line.end, end)

    def __init__(self, start: math.Point, control_point_a: math.Point, control_point_b: math.Point, end: math.Point):
        super().__init__(start, end)
        if start.dimension != control_point_a.dimension or start.dimension != control_point_b.dimension or start.dimension != end.dimension:
            raise ValueError("All points must have the same dimension.")
        self.dimension = start.dimension

        self.control_point_a = control_point_a
        self.control_point_b = control_point_b

    def at(self, t: float):
        """Return the point at parameter t along the cubic Bezier curve, where t is between 0 and 1."""
        time_matrix =math.Matrix(np.array([[ (1 - t)**3, 3 * (1 - t)**2 * t, 3 * (1 - t) * t**2, t**3]]))
        control_matrix_x = math.Matrix(np.array([[self.start.x, self.control_point_a.x, self.control_point_b.x, self.end.x]]).T)
        control_matrix_y = math.Matrix(np.array([[self.start.y, self.control_point_a.y, self.control_point_b.y, self.end.y]]).T)
        x = (time_matrix * control_matrix_x)[0, 0]
        y = (time_matrix * control_matrix_y)[0, 0]
        return math.Point(x, y)