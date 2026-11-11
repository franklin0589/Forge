from Forge.Geometry.definitions.mesh.base_mesh import Mesh
import numpy as np
from Forge.shared.protocols import *
from Forge.geometry.color import Color


class LineMesh(Mesh):
    def __init__(self, start: iBuffer, end: iBuffer, color: iColor) -> None:
        super().__init__()
        self.start : iBuffer = start
        self.end : iBuffer= end
        self.color: iColor = color

    def form(self) -> None:
        self.add_vertex(self.start)
        self.add_vertex(self.end)
        self.attach_color(color=self.color)