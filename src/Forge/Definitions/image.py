from Forge.shared.protocols import *
from PIL import Image as PILImage
from pathlib import Path
import numpy as np
import cairo

class Image:
    def __init__(self, data:PILImage.Image) -> None:
        self.data: PILImage.Image = data
        self.width: int = self.data.width
        self.height: int = self.data.height


    @classmethod
    def from_file(cls, resource_path: str, flip_y: bool = False) -> "Image":
        _path = Path(resource_path)
        if not _path.is_file():
            raise FileNotFoundError(f"File not found: {resource_path}")
        img = PILImage.open(_path).convert("RGBA")
        if flip_y:
            img = img.transpose(PILImage.FLIP_TOP_BOTTOM)
        return Image(img)

    def to_cairo_surface(self):
        rgba_image = self.data.convert("RGBA")
        arr = np.array(rgba_image)
        bgra_arr = arr[..., [2, 1, 0, 3]].copy()
        width, height = rgba_image.size
        stride = width * 4
        surface = cairo.ImageSurface.create_for_data(
            bgra_arr, cairo.FORMAT_ARGB32, width, height, stride
        )
        # surface._numpy_buffer = bgra_arr
        return surface

    def resize(self, width: int, height: int) -> None:
        self.data = self.data.resize((width, height))
        self.width = width
        self.height = height

    def flip_y(self) -> None:
        self.data = self.data.transpose(PILImage.FLIP_TOP_BOTTOM)
        self.height, self.width = self.width, self.height

    def save(self, resource_path: str) -> None:
        _path = Path(resource_path)
        self.data.save(_path)
