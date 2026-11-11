import Forge.Definitions as defs
import Forge.Definitions as gadget
import Forge.controller.shape_commands as shape_commands
from plum import dispatch
from enum import StrEnum
from typing import Any, Sequence

class ShapeType(StrEnum):
    POINT = "point"
    LINE = "line"
    CURVE = "curve"
    RECTANGLE = "rectangle"
    TYPOGRAPHY = "typography"
    ELLIPSE = "ellipse"

class SupplyFactory:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    
    def create(self, shape_type:str|ShapeType, *args, **kwargs):
        if not isinstance(shape_type, ShapeType):
            shape_type = ShapeType(shape_type)

        create_method = getattr(self, f"create_{shape_type.value}", None)
        if not create_method:
            raise ValueError(f"Unknown shape type: {shape_type}")
        return create_method(*args, **kwargs)

    @dispatch
    def create_point(self, origin:tuple[float|int, float|int]):
        point = defs.Point(*origin)
        return point, shape_commands.DrawPoint(point)

    @dispatch
    def create_point(self, origin:defs.Point):
        return origin, shape_commands.DrawPoint(origin)


    @dispatch
    def create_line(self, start_point:tuple[float|int, float|int], end_point:tuple[float|int, float|int]):
        start_point = defs.Point(*start_point)
        end_point = defs.Point(*end_point)
        line = defs.Line2D(start_point, end_point)
        return line, shape_commands.DrawLine(line)

    @dispatch
    def create_line(self, start_point: defs.Point, end_point: defs.Point):
        line = defs.Line2D(start_point, end_point)
        return line, shape_commands.DrawLine(line)


    @dispatch
    def create_line_path(self, points: list[tuple[float|int, float|int]]):
        line_path = defs.LinePath2D.from_points([defs.Point(x, y) for x, y in points])
        return line_path, shape_commands.DrawLinePath(line_path)

    @dispatch
    def create_line_path(self, points: list[defs.Point]):
        line_path = defs.LinePath2D.from_points(points)
        return line_path, shape_commands.DrawLinePath(line_path)


    @dispatch
    def create_curve_path(self, points: list[defs.Point], control_points:list[defs.Point]):
        curve_path = defs.CurvePath2D.from_points(points, control_points)
        return curve_path, shape_commands.DrawCurvePath(curve_path)
    
    @dispatch
    def create_curve_path(self, points: list[tuple[float|int, float|int]], control_points:list[tuple[float|int,float|int]]):
        points = [defs.Point(x, y) for x, y in points]
        control_points = [defs.Point(x, y) for x, y in control_points]
        curve_path = defs.CurvePath2D.from_points(points, control_points)
        return curve_path, shape_commands.DrawCurvePath(curve_path)

    @dispatch
    def create_curve(self, p1: tuple[float|int, float|int], p2: tuple[float|int, float|int], p3: tuple[float|int, float|int], p4: tuple[float|int, float|int]):
        p1 = defs.Point(*p1)
        p2 = defs.Point(*p2)
        p3 = defs.Point(*p3)
        p4 = defs.Point(*p4)
        curve = defs.Curve2D(p1, p2, p3, p4)
        return curve, shape_commands.DrawCurve(curve)

    @dispatch
    def create_curve(self, p1: defs.Point, p2: defs.Point, p3: defs.Point, p4: defs.Point):
        curve = defs.Curve2D(p1, p2, p3, p4)
        return curve, shape_commands.DrawCurve(curve)

    @dispatch
    def create_circle(self, center: tuple[float|int, float|int], radius: float|int):
        center = defs.Point(*center)
        circle = defs.Circle(center, radius)    
        return circle, shape_commands.DrawCircle(circle)
    
    @dispatch
    def create_circle(self, center:defs.Point, radius: float|int):
        circle = defs.Circle(center, radius)    
        return circle, shape_commands.DrawCircle(circle)

    
    @dispatch
    def create_rectangle(self, origin: defs.Point, width: int, height: int):
        rectangle = defs.Rectangle(origin, width, height)
        return rectangle, shape_commands.DrawRectangle(rectangle)

    @dispatch
    def create_rectangle(self, origin: tuple[float|int, float|int], width: int, height: int):
        origin = defs.Point(*origin)
        rectangle = defs.Rectangle(origin, width, height)
        return rectangle, shape_commands.DrawRectangle(rectangle)

    @dispatch
    def draw_text(self, origin: defs.Point, content:str, color:gadget.Color|str):
        if isinstance(color, str):
            color = gadget.Color.from_hexcode(color)
        return shape_commands.DrawText(origin, content, color)

    @dispatch
    def draw_text(self, origin: tuple[float|int, float|int], content: str, color:gadget.Color|str):
        origin = defs.Point(*origin)
        if isinstance(color, str):
            color = gadget.Color.from_hexcode(color)
        return shape_commands.DrawText(origin, content, color)

    def create_typography(self, size:int, face:str, slant:int, bold:int):
        typo = defs.Typography(size, face, slant, bold)
        return typo


    @dispatch
    def draw_image(self, image: str, dimension: defs.Rectangle):
        return shape_commands.DrawImage(image, dimension)
        

    @dispatch
    def draw_image(self, image: str, origin:tuple[float|int, float|int], size:tuple[float|int, float|int]):
        origin = defs.Point(*origin)
        dimension = defs.Rectangle(origin, size[0], size[1])
        return shape_commands.DrawImage(image, dimension)
    

    def create_ellipse(self, center_a:defs.Point, center_b:defs.Point, radius:int, minor_factor:float=1.0):
        ellipse = defs.Ellipse(center_a, center_b, radius, minor_factor)
        return ellipse, shape_commands.DrawEllipse(ellipse)




