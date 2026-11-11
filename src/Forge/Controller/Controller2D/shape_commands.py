import math
import cairo
import Forge.Definitions as gadget
import Forge.Definitions as defs

class DrawCommand:
    def execute(self):
        raise NotImplementedError("DrawCommand subclasses must implement the execute method.")

class DrawPoint:
    def __init__(self, point: gadget.Point):
        self.point = point

    def execute(self, context: cairo.Context):
        """ Draw a Point at the given coordinates using the current pen settings. """
        context.arc(*self.point, 2, 0, 2*math.pi)


class DrawLine:
    def __init__(self, line:gadget.Line):
        self.line = line

    def execute(self, context:cairo.Context):
        """ Draw a Line from the start point to the end point using the current pen settings. """
        start = self.line.start_point
        end = self.line.end_point
        context.move_to(*start)
        context.line_to(*end)

class DrawCircle:
    def __init__(self, circle):
        self.circle = circle

    def execute(self, context:cairo.Context):
        """ Draw a Circle with the given center and radius using the current pen settings. """
        context.arc(*self.circle.center, self.circle.radius, 0, 2*math.pi)

class DrawCurve:
    def __init__(self, curve: gadget.Curve):
        self.curve = curve
    def execute(self, context:cairo.Context):
        """ Draw a Curve from the start point to the end point using the current pen settings. """
        context.move_to(*self.curve.start)
        context.curve_to(*self.curve.control_point_a,*self.curve.control_point_b,*self.curve.end)

class DrawRectangle:
    def __init__(self, rectangle: gadget.Rectangle):
        self.rectangle = rectangle

    def execute(self, context:cairo.Context):
        """ Draw a Rectangle with the given origin, width, and height using the current pen settings. """
        context.move_to(*self.rectangle.origin)
        context.line_to(self.rectangle.origin.x + self.rectangle.width, self.rectangle.origin.y)
        context.line_to(self.rectangle.origin.x + self.rectangle.width, self.rectangle.origin.y + self.rectangle.height)
        context.line_to(self.rectangle.origin.x, self.rectangle.origin.y + self.rectangle.height)
        context.close_path()

class DrawEllipse:
    def __init__(self, ellipse: gadget.Ellipse):
        self.ellipse = ellipse

    def execute(self, context:cairo.Context):
        context.move_to(self.ellipse.get_x(0), self.ellipse.get_y(0))
        for cA, cB, end in self.ellipse.get_control_points():
            context.curve_to(
                int(cA[0]), int(cA[1]),
                int(cB[0]), int(cB[1]),
                int(end[0]), int(end[1]))

class DrawText:
    def __init__(self, origin: gadget.Point, content: str, color:gadget.Color):
        self.origin = origin
        self.content = content
        self.color = color

    def execute(self, context:cairo.Context):
        context.set_source_rgba(*self.color)
        context.move_to(*self.origin)
        context.show_text(self.content)  # Simplified example, you may need to set font size, slant, bold, etc.

class DrawImage:
    def __init__(self, image: str, dimension: defs.Rectangle):
        self.image_path = image
        self.dimension = dimension

    def execute(self, context: cairo.Context):
        """ Draw an Image at the given position using the current pen settings. """
        image = gadget.Image.from_file(self.image_path)
        image.resize(self.dimension.width, self.dimension.height)
        cairo_surface = image.to_cairo_surface()
        position = self.dimension.origin
        context.set_source_surface(cairo_surface, position.x, position.y)
        context.paint()

class DrawHorizon:
    def __init__(self, horizon: int, width: int, height: int):
        self.horizon = horizon
        self.width = width
        self.height = height

    def draw_horizon(self, context:cairo.Context):
        context.rectangle(0, self.horizon, self.width,  (self.height) )

class DrawLinePath:
    def __init__(self, line_path: gadget.LinePath):
        self.line_path = line_path

    def execute(self, context:cairo.Context):
        points = self.line_path.get_points()
        if not points:
            return
        context.move_to(*points[0])
        for point in points[1:]:
            context.line_to(*point)

class DrawCurvePath:
    def __init__(self, curve_path: gadget.CurvePath2D):
        self.curve_path = curve_path

    def execute(self, context:cairo.Context):
        points = self.curve_path.get_points()
        if not points:
            return
        context.move_to(*points[0])
        for i in range(1, len(points), 3):
            cA = points[i]
            cB = points[i+1]
            end = points[i+2]
            context.curve_to(*cA, *cB, *end)