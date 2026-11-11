
import cairo
import numpy as np
import PIL.Image as Image

class Surface:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

    def save(self, filename):
        self.surface.write_to_png(filename)

    def capture(self):
        self.surface.flush()
        buf = self.surface.get_data()
        array = np.ndarray(shape=(self.height, self.width, 4), dtype=np.uint8, buffer=buf)
        return array

    
    def to_pil(self) -> Image:
        format = self.surface.get_format()
        size = (self.surface.get_width(), self.surface.get_height())
        stride = self.surface.get_stride()

        with self.surface.get_data() as memory:
            if format == cairo.Format.RGB24:
                return Image.frombuffer(
                    "RGB", size, memory.tobytes(),
                    'raw', "BGRX", stride)
            elif format == cairo.Format.ARGB32:
                return Image.frombuffer(
                    "RGBA", size, memory.tobytes(),
                    'raw', "BGRa", stride)
            else:
                raise NotImplementedError(repr(format))
