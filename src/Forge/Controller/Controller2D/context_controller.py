import math
import cairo
from Forge.Definitions import Point
from Forge.Definitions.pen import Pen
from Forge.Definitions.text import Typography


class ContextController:
    def __init__(self, surfaceController):
        self.surfaceController = surfaceController
        self.context:cairo.Context = cairo.Context(surfaceController.surface)
        self.pen: Pen = Pen("#000000", "#000000", 1)
        self.context.set_antialias(cairo.ANTIALIAS_NONE)

    def __enter__(self):
        self.context.save()
        return self.context

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context.restore()

    def get_pen(self):
        return self.pen

    def set_pen(self, pen: Pen):
        self.pen = pen

    def rotate_context(self, center: Point, angle: float):
        self.context.translate(center.x, center.y)
        self.context.rotate(math.radians(angle))
        self.context.translate(-center.x, -center.y)


    def trace(self, points:list[Point]):
        if not points:
            return
        self.context.move_to(*points[0])
        for point in points[1:]:
            self.context.line_to(*point)
        self.context.close_path()


    def paint(self, preserve: bool = False):
        if self.pen.gradient is not None:
            self.context.set_source(self.pen.gradient.get_gradient())
        else:
            self.context.set_source_rgba(*self.pen.fill_color.as_tuple())
        if preserve:
            self.context.fill_preserve()
        else:
            self.context.fill()

    def ink(self):
        # with self:
        self.context.set_source_rgba(*self.pen.brd_color.as_tuple())
        self.context.set_line_width(self.pen.width)
        self.context.stroke()

    def draw(self):
        self.paint(preserve=True)
        self.ink()

    def set_Typography(self, text: Typography):
        self.context.set_font_size(text.size)
        self.context.select_font_face(text.face, text.get_slant(), text.get_weight())
