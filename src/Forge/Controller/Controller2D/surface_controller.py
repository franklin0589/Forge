import cairo
import numpy as np

from Forge.Definitions.targets import Surface
from Forge.controller.supply_factory import SupplyFactory, ShapeType
from Forge.controller.context_controller import ContextController
from Forge.controller.shape_commands import DrawCommand
from Forge.Definitions.pen import Pen


class SurfaceController(SupplyFactory):
    def __init__(self,  width:int,  height:int):
        super().__init__(width, height)
        self.width = width
        self.height = height
        
        self.surface = Surface(width, height)
        self.context = ContextController(self.surface)

    def reset(self):
        self.surface = Surface(self.width, self.height)
        self.context = cairo.Context(self.image.surface)
    
    def save(self, file_path):
        self.surface.save(file_path)

    def capture(self) -> np.ndarray:
        return self.surface.capture()

    def draw(self, shape_type:str|ShapeType, *args, **kwargs):
        obj, command = self.create(shape_type, *args, **kwargs)
        self.draw_shape(command)

    def paint(self, shape_type:str|ShapeType, *args, **kwargs):
        obj, command = self.create(shape_type, *args, **kwargs)
        self.paint_shape(command)

    def ink(self, shape_type:str|ShapeType, *args, **kwargs):
        obj, command = self.create(shape_type, *args, **kwargs)
        self.ink_shape(command)

    def ink_shape(self, command:DrawCommand):
        with self.context as context:
            command.execute(context)
            self.context.ink()

    def draw_shape(self, command:DrawCommand):
        with self.context as context:
            command.execute(context)
            self.context.draw()

    def paint_shape(self,command:DrawCommand):
        with self.context as context:
            command.execute(context)
            self.context.paint()


    def draw_text(self, origin, content, color):
        command = super().draw_text(origin, content, color)
        self.draw_shape(command)

    def set_font(self, family:str, size:int, weight:int=0, slant:int=0):
        typography = self.create_typography(size, family, slant, weight)
        self.context.set_Typography(typography)

    def set_background(self, color):
        origin, origin_command = self.create_point((0, 0))
        screen_rect, screen_rect_command = self.create("rectangle", origin, self.width, self.height)
        prev_pen = self.context.get_pen()
        temp_pen = self.create_pen("#000000", color, 0)
        self.context.set_pen(temp_pen)
        self.paint_shape(screen_rect_command)
        self.context.set_pen(prev_pen)



    def create_pen(self, brd_color, fill_color, thickness, gradient=None):
        return Pen(brd_color, fill_color, thickness, gradient=gradient)


    def swap_pen(self, pen):
        self.context.set_pen(pen)