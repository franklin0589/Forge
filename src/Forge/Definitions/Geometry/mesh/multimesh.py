from __future__ import annotations

from Forge.geometry.color import Color
from Forge.Geometry.definitions.mesh.base_mesh import Mesh
import numpy as np


class MultiMesh(Mesh):
    def __init__(self, meshes: list[Mesh], colors: list[Color] | None = None) -> None:
        super().__init__()
        self.meshes = meshes
        self.colors = colors if colors is not None else [Color(1.0, 1.0, 1.0)] * len(meshes)

    def add_mesh(self, mesh: Mesh, color: Color | None = None) -> None:
        self.meshes.append(mesh)
        self.colors.append(color if color is not None else Color(1.0, 1.0, 1.0))
    
    def structure(self) -> None:
        for mesh, color in zip(self.meshes, self.colors):
            mesh.structure()
            self.mesh_context.add_mesh(mesh.mesh_context)
            self.mesh_context.attach_color(color=color.as_tuple())