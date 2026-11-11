from Forge.controller.surface_controller import SurfaceController
from PIL import Image
import numpy as np
class CanvasController:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background  = SurfaceController(width, height)
        self.layers = [self.background]

    def get_layer(self, index):
        return self.layers[index]

    def add_layer(self) -> SurfaceController:
        layer = SurfaceController(self.width, self.height)
        self.layers.append(layer)
        return layer

    def remove_layer(self, index):
        if 0 <= index < len(self.layers):
            del self.layers[index]

    def reset_layer(self, index:int):
        if 0 <= index < len(self.layers):
            self.layers[index] = SurfaceController(self.width, self.height)

    def on_layer(self, index, new=False) -> SurfaceController:
        if 0 <= index < len(self.layers):
            if new:
                self.layers[index] = SurfaceController(self.width, self.height)
            return self.layers[index]
        elif index == len(self.layers):
            self.add_layer()
            return self.layers[index]
        return None

    def export_frame(self):
        if not self.layers:
            return None
        base = self.background.surface.to_pil()
        for layer in self.layers[1:]:
            base = Image.alpha_composite(base, layer.surface.to_pil())
        return np.asarray(base)

    def save(self, filepath):
        if not self.layers:
            return
        base = self.background.surface.to_pil()
        for layer in self.layers[1:]:
            base = Image.alpha_composite(base, layer.surface.to_pil())
        base.save(filepath)