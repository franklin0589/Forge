import av
from typing import Generator
from Forge.controller.canvas_controller import CanvasController

class AnimateController:
    def __init__(self, name:str, width: int, height: int):
        self.width = width
        self.height = height
        self.container = av.open(f"output/{name}.mp4", mode="w")
        self.outtype = "mp4"  # Set output type to mp4


        self.canvas_controller = CanvasController(self.width, self.height)
        self.render_frame = None

    def set_render_function(self, render_function):
        self.render_frame = render_function

    # def render_frame(self, frame_index: int):
    #     self.dc.reset_image()
    #     self.dc.fill_background((1, 1, 1, 1))  # Fill the background with white color
    #     self.dc.set_pen((0, 0, 0, 1), 2)
    #     line = self.dc.get_line(frame_index*20, 100, 700, 500)
    #     self.dc.draw_line(line)
    #     return self.dc.capture_image()

    def render_loop(self, duration: float, fps: int) -> Generator:
        total_frames = int(duration * fps)
        for i in range(total_frames):
            frame = self.render_frame(self.canvas_controller, i)
            yield frame
        
        
    def record(self, duration: float, fps:int):
        stream = self.container.add_stream("libx264", rate=24)
        stream.width = self.width
        stream.height =self.height
        stream.pix_fmt = "yuv420p"

        for frame_idx, frame_i in enumerate(self.render_loop(duration, fps)):
            frame_i = frame_i[:, :, :3]  # Ensure the frame has 3 channels (RGB)
            frame = av.VideoFrame.from_ndarray(frame_i, format="rgb24")
            frame.pts = frame_idx
            for packet in stream.encode(frame):
                self.container.mux(packet)
        # Flush stream
        for packet in stream.encode():
            self.container.mux(packet)

        # Close the file
        self.container.close()


# def animate(name:str, width:int, height:int, duration: float, fps: int):
#     def ext_wrapper(func) :
#         def int_wrapper():
#             ac = AnimateController(name, width, height)
#             ac.set_render_function(func)
#             print("Animating:", name)
#             ac.record(duration=duration, fps=fps)  # Example duration and fps
#             print("Finished animating:", name)
#         int_wrapper()
#         return int_wrapper
#     return ext_wrapper