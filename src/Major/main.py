from __future__ import annotations
import tkinter as tk
import time
import math
from typing import Protocol
import math
from abc import ABC, abstractmethod
import moderngl
from PIL import Image, ImageTk
class glApp:
    def __init__(self):
        self.root = tk.Tk()
        self.width = 800
        self.height = 600
        self.root.geometry(f"{self.width}x{self.height}")

        self.label = tk.Label(self.root, text="ModernGL Framebuffer Image:")
        self.label.pack()

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, background="blue")
        self.canvas.pack(expand=True, fill="both")
        # 2. Setup standalone offscreen ModernGL context
        self.ctx = moderngl.create_context(standalone=True)
        # Create a Framebuffer to render into
        self.fbo = self.ctx.simple_framebuffer((self.width, self.height))
        self.MAX_CLOCK = 255
        self.TWO_PI = math.pi*2
        self.clk = 0
        self.img_id = self.canvas.create_image(0, 0, anchor=tk.NW)
        self.target_dt = 1 / 60
        self.min_dt = 1 / 120
        self.max_dt = 1 / 30
        self.avg_frame_time = self.target_dt
        self.period = self.MAX_CLOCK / 60  # seconds per full animation loop
        self.t0 = time.perf_counter()
        self._next_frame = None
        self.fbo.use()

    def pre_process(self):
        self.background_color = (0.15, 0.15, 3)
        self.ctx.clear(*self.background_color)

    def post_process(self):
        pixel_data = self.fbo.read(components=3)

        self.img = Image.frombytes('RGB', (self.width, self.height), pixel_data, "raw", "RGB", 0, -1)

        self.tk_image = ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.img_id, image=self.tk_image)
        self.clk = (self.clk+ 1)%self.MAX_CLOCK

    def setup(self):
        ...

    def update(self):
        ...


    def tick(self):
        return ((time.perf_counter() - self.t0) / self.period) % 1.0

    def adapt_interval(self, frame_time):
        self.avg_frame_time = 0.9 * self.avg_frame_time + 0.1 * frame_time
        self.target_dt = max(self.min_dt, min(self.max_dt, self.avg_frame_time * 1.1))

    def update_loop(self):
        start = time.perf_counter()
        if self._next_frame is None:
            self._next_frame = start

        self.pre_process()
        self.update()
        self.post_process()

        # now = time.perf_counter()
        # self.adapt_interval(now - start)
        # self._next_frame += self.target_dt
        # delay_ms = (self._next_frame - now) * 1000
        # if delay_ms < 1:
        #     delay_ms = 1
        #     self._next_frame = now
        self.root.after(10, self.update_loop)

    def run(self):
        self.setup()
        self.update_loop()
        self.root.mainloop()

    def __init_subclass__(cls):
            cls().run()

class SampleApp(ABC):
    def __init__(self):
        self.root = tk.Tk()
        self.update_interval = 1/30
        self.start_delay = 500
        self.WIDTH = 800
        self.HEIGHT = 600

    def __enter__(self):
        self.root.title("My Tkinter App")

        self.root.geometry("800x600")
        self.canvas = tk.Canvas(self.root)
        self.context = CanvasContext(self.canvas)

        
        self.MAX_CLOCK = 256
        self.TWO_PI = math.pi * 2
    
        self.clk = 0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context.pack(expand=True, fill='both')
       
        self.root.mainloop()

    def clear(self):
        self.context.clear()

    def preprocess(self):
        self.WIDTH = self.canvas.winfo_width()
        self.HEIGHT = self.canvas.winfo_height()
        self.context.update_center()
    
        pass

    def postprocess(self):
        self.clk = (self.clk + 1) % self.MAX_CLOCK

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def update(self):
        pass

    def schedule_update(self): 
        self.preprocess()
        self.update()
        self.postprocess()
        self.root.after(int(self.update_interval * 1000), self.schedule_update)

    def tick(self):
        return (self.clk/self.MAX_CLOCK)

    def sine(self, angle: float, beta: float=0.0) -> float:
        return math.sin(angle*math.pi*2 + beta)
    def cosine(self, angle: float, beta: float=0.0) -> float:
        return math.cos(angle*math.pi*2 + beta)

    def tan(self, angle: float, beta: float=0.0) -> float:
        return math.tan(angle*math.pi*2 + beta)
    

    def run(self):
        with self:
            self.setup()
            time.sleep(self.start_delay/1000)
            self.root.after(1, self.schedule_update)
            pass

    def __init_subclass__(cls):
        cls().run()


class CanvasContext:
    def __init__(self:CanvasContextInterface, canvas: tk.Canvas):
        self.canvas = canvas
        self.base_rotation = 0.0
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.center = (self.canvas.winfo_width()//2, self.canvas.winfo_height()//2)
        self.snapshots: list[tuple] = []

    def save_context(self):
        self.snapshots.append((self.base_rotation, self.scale_x, self.scale_y, self.center))

    def restore_context(self):
        if self.snapshots:
            self.base_rotation, self.scale_x, self.scale_y, self.center = self.snapshots.pop()

    def update_center(self):
        self.center = (self.canvas.winfo_width()//2, self.canvas.winfo_height()//2)
    def clear(self):
        self.canvas.delete("all")

    def draw_text(self, origin, text, color="black", font=("Arial", 12)):
        x, y = origin[0]+self.center[0], origin[1]+self.center[1]
        font = (font[0], int(font[1]*self.scale_y))
        self.canvas.create_text(int(x), int(y), text=text, fill=color, font=font)

    def draw_circle(self, origin, radius, color="red"):
        x, y = origin[0]+self.center[0], origin[1]+self.center[1]
        r_size = int(radius//2 * math.sqrt(2))
        top_left  = (self.scale_x*int(x - r_size), self.scale_y*int(y - r_size))
        bottom_right = (self.scale_x*int(x + r_size), self.scale_y*int(y + r_size))
        self.canvas.create_oval(*(top_left + bottom_right), outline=color, fill=color)

    def pack(self, expand=True, fill='both'):
        self.canvas.pack(expand=expand, fill=fill)

class CanvasContextInterface(Protocol):
    canvas:tk.Canvas
    center: tuple[float, float]
    base_rotation: float
    scale_x: float
    scale_y: float
    snapshots: list

    def pack(self, expand=True, fill='both'):
        ...
    def draw_circle(self, origin, radius, color="red"):
        ...
    def draw_text(self, origin, text, color="black", font=("Arial", 12)):
        ...

class App(Protocol):
    root:tk.Tk
    canvas: tk.Canvas
    context: CanvasContext
    update_interval: int
    clk: int
    MAX_CLOCK: int
    WIDTH: int
    HEIGHT: int
    TWO_PI: float
    def clear(self):
        ...
    def cosine(self, angle: float, beta: float) -> float:
        ...
    def sine(self, angle: float, beta: float) -> float:
        ...
    def tan(self, angle: float, beta: float=0.0) -> float:
        ...

    def setup(self):
        ...

    def update(self):
        ...