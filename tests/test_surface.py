import Forge.controller as controller
import Forge.Definitions.path as path
import unittest


class TestCanvas(unittest.TestCase):
    def test_surface_background(self):
        surface_controller = controller.SurfaceController(400, 300)
        surface_controller.set_background("#CE1313")
        surface_controller.save("tests/images/test_surface_background.png")

    def test_surface_draw_point(self):
        surface_controller = controller.SurfaceController(400, 300)
        surface_controller.set_background("#FFFFFF")
        pen = surface_controller.create_pen("#000000", "#00F2FF", 1)
        p, pcmd = surface_controller.create_point((200, 150))
        surface_controller.draw_shape(pcmd)
        surface_controller.save("tests/images/test_surface_draw_point.png")

    def test_surface_draw_rectangle(self):
        surface_controller = controller.SurfaceController(400, 300)
        surface_controller.set_background("#FFFFFF")
        pen = surface_controller.create_pen("#000000", "#00F2FF", 1)
        surface_controller.swap_pen(pen)
        p, rect_cmd = surface_controller.create_rectangle((100, 100), 50, 50)
        surface_controller.draw_shape(rect_cmd)
        surface_controller.save("tests/images/test_surface_draw_rectangle.png")

    def test_surface_draw_circle(self):
        surface_controller = controller.SurfaceController(400, 300)
        surface_controller.set_background("#FFFFFF")
        pen = surface_controller.create_pen("#000000", "#00F2FF", 1)
        surface_controller.swap_pen(pen)
        c, circle_cmd = surface_controller.create_circle((200, 150), 50)
        surface_controller.draw_shape(circle_cmd)
        surface_controller.save("tests/images/test_surface_draw_circle.png")

    def test_surface_draw_curve(self):
        surface_controller = controller.SurfaceController(400, 300)
        surface_controller.set_background("#FFFFFF")
        pen = surface_controller.create_pen("#000000", "#00F2FF", 1)
        surface_controller.swap_pen(pen)
        c, curve_cmd = surface_controller.create_curve((50, 50), (150, 100), (250, 50), (350, 100))
        surface_controller.ink_shape(curve_cmd)
        surface_controller.save("tests/images/test_surface_draw_curve.png")
    
    def test_surface_draw_line_path(self):
        surface_controller = controller.SurfaceController(400, 300)
        surface_controller.set_background("#FFFFFF")
        pen = surface_controller.create_pen("#000000", "#00F2FF", 1)
        line_path, line_path_cmd = surface_controller.create_line_path([(20, 20), (100, 100), (200, 50)])
        surface_controller.ink_shape(line_path_cmd)
        surface_controller.save("tests/images/test_surface_draw_line_path.png")

    def test_surface_draw_curve_path(self):
        surface_controller = controller.SurfaceController(400, 300)
        surface_controller.set_background("#FFFFFF")
        pen = surface_controller.create_pen("#000000", "#00F2FF", 1)
        surface_controller.swap_pen(pen)
        points = [ (50, 50), (150, 100), (250, 50) , (350, 100)]
        control_points = [ (75, 75), (175, 125), (275, 75), (375, 125) ]
        curve_path, curve_path_cmd = surface_controller.create_curve_path(points, control_points)
        surface_controller.ink_shape(curve_path_cmd)
        surface_controller.save("tests/images/test_surface_draw_curve_path.png")


    def test_surface_draw_text(self):
        surface_controller = controller.SurfaceController(400, 300)
        surface_controller.set_background("#FFFFFF")
        pen = surface_controller.create_pen("#000000", "#00F2FF", 1)
        surface_controller.swap_pen(pen)
        text_cmd = surface_controller.draw_text((100, 100), "Hello, World!")
        surface_controller.ink_shape(text_cmd)
        surface_controller.save("tests/images/test_surface_draw_text.png")

    def test_surface_draw_text_different_typography(self):
        surface_controller = controller.SurfaceController(400, 300)
        surface_controller.set_background("#FFFFFF")
        pen = surface_controller.create_pen("#000000", "#00F2FF", 1)
        surface_controller.swap_pen(pen)
        surface_controller.set_font("Arial", 27, 0, 1)

        text_cmd = surface_controller.draw_text((100, 100), "Different Typography")
        surface_controller.ink_shape(text_cmd)
        surface_controller.save("tests/images/test_surface_draw_text_different_typography.png")