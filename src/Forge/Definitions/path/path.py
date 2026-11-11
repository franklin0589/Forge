from Forge.Definitions.gmath.vector import Point
from Forge.Definitions.path.segment import Segment2D
from Forge.Definitions.path.line import Line2D
from Forge.Definitions.path.curve import Curve2D



class Path2D:
    def __init__(self, segements:list[Segment2D] = []):
        self.segments:list[Segment2D] = segements
        self.connected = True
        self.check_connected()
    
        self.last_point = segements[-1].end if segements else None
        self.length = len(segements)

    def get_points(self) -> list[Point]:
        points = []
        for segment in self.segments:
            if not points:
                points.append(segment.start)
            points.append(segment.end)
        return points

    @staticmethod
    def check_segement_connected(segmentA: Segment2D, segmentB: Segment2D):
        return segmentA.end == segmentB.start

    def check_connected(self):
        # Check if the path is connected by ensuring each segment's end matches the next segment's start.
        if len(self.segments) <= 1:
            # A path with 0 or 1 segment is trivially connected.
            self.connected = True
            return self.connected
        
        for i in range(len(self.segments) - 1):
            if not Path2D.check_segement_connected(self.segments[i], self.segments[i + 1]):
                self.connected = False
                return self.connected
        self.connected = True
        return self.connected

    def add_segment(self, segment: Segment2D):
        if not isinstance(segment, Segment2D):
            raise ValueError("segment must be an instance of Segment2D.")
        self.segments.append(segment)
        self.length = len(self.segments)
        self.check_connected()

    def at(self, t: float):
        if not self.segments:
            return None
        segment_index = int(t)
        if t >= self.length or segment_index >= self.length:
            return self.last_point
        if t < 0:
            return self.segments[0].start
        segment_t = t - segment_index
        return self.segments[segment_index].at(segment_t)

    def along(self, step: float):
        if not self.segments:
            return None
        t = 0.0
        while t < self.length:
            yield self.at(t)
            t += step
        if t >= self.length and self.last_point is not None:
            yield self.last_point

class LinePath2D(Path2D):
    @classmethod
    def from_points(cls, points: list[Point]):
        if not points:
            return cls([])
        lines = [Line2D(points[i], points[i + 1]) for i in range(len(points) - 1)]
        return cls(lines)

    def __init__(self, lines: list[Line2D] = []):
        for segment in lines:
            if not isinstance(segment, Line2D):
                raise ValueError("All elements must be instances of Segment2D.")
        super().__init__(lines)

    def add_line(self, new_line:Line2D):
        if not isinstance(new_line, Line2D):
            raise ValueError("new_line must be an instance of Line2D.")
        self.last_point = new_line.end
        self.add_segment(new_line)
        return new_line

    def add_point(self, new_point:Point):
        if self.last_point is None:
            raise ValueError("Cannot add a point without an initial point.")
        line = Line2D(self.last_point, new_point)
        self.last_point = new_point
        self.add_segment(line)
        return line

class CurvePath2D(Path2D):
    @classmethod
    def from_points(cls, points: list[Point], control_points: list[Point]):
        if len(points) != len(control_points):
            raise ValueError("Number of control points must match the number of curve segments.")
        
        curves = [Curve2D(points[i], control_points[i], control_points[i+1], points[i + 1]) for i in range(0, len(points) - 1, 2)]
        return cls(curves)

    def __init__(self, curves: list[Curve2D] = []):
        for segment in curves:
            if not isinstance(segment, Curve2D):
                raise ValueError("All elements must be instances of Curve2D.")
        super().__init__(curves)


    def get_points(self) -> list[Point]:
        points = []
        for segment in self.segments:
            if not points:
                points.append(segment.start)
            points.append(segment.control_point_a)
            points.append(segment.control_point_b)
            points.append(segment.end)
        return points


    def add_curve(self, new_curve:Curve2D):
        if not isinstance(new_curve, Curve2D):
            raise ValueError("new_curve must be an instance of Curve2D.")
        self.last_point = new_curve.end
        self.add_segment(new_curve)
        return new_curve

    def add_point(self, end_point:Point, control_pointA:Point, control_pointB:Point):
        if self.last_point is None:
            raise ValueError("Cannot add a point without an initial point.")
        curve = Curve2D(self.last_point, control_pointA, control_pointB, end_point)
        self.last_point = end_point
        self.add_segment(curve)
        return curve