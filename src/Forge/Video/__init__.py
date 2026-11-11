
from Forge.Video.controller.frame_schedule import FrameSchedule
from Forge.Video.controller.animate_controller import AnimateController

from Forge.controller import CanvasController

class Video:
    def __init__(self, name, width, height, length, fps=24):
        self.name = name
        self.width = width
        self.height = height
        self.length = length
        self.fps = fps
        self.scene_schedule = FrameSchedule()
        self.controller = AnimateController(self.name, self.width, self.height)
        self.background_color = "#FFFFFF"

    def schedule(self, second:int, function):
        self.scene_schedule.add_callback(second, function)
    
    def int_render_func(self, canvas:CanvasController, frame_index):
        # Access the background layer
        background = canvas.get_layer(0)
        background.set_background(self.background_color)

        layer = canvas.on_layer(1, new=True)
        self.scene_schedule.update(frame_index, layer)
        return canvas.export_frame()


    def record(self):
        self.controller.set_render_function(self.int_render_func)
        self.controller.record(duration=self.length, fps=self.fps) 
        