
from Forge.Geometry.definitions.mesh.base_mesh import Mesh
import numpy as np
from Forge.geometry.color import Color

class PlaneMesh(Mesh):
    def __init__(
        self,
        width: float = 2.0,
        depth: float = 2.0,
        color: Color|None = None,
    ) -> None:
        super().__init__()
        self.width = width
        self.depth = depth
        self.color = color

    def structure(self) -> None:
        hw = self.width * 0.5
        hd = self.depth * 0.5
        color = self.color.as_tuple() if self.color else (0.95, 0.55, 0.25)
        normal = (0.0, 1.0, 0.0)

        for i in range(4):
            x = -hw if i % 2 == 0 else hw
            z = -hd if i < 2 else hd
            vertex = np.array([x, 0.0, z] + color+ normal, dtype=np.float32)
            self.mesh_context.add_vertex(vertex)
        self.mesh_context.add_quad(0, 1, 2, 3)
        

class TexturedPlaneMesh(Mesh):
    def __init__(
        self,
        width: float = 2.0,
        depth: float = 2.0,
        color: tuple[float, float, float] = (1.0, 1.0, 1.0),
        uv_scale: tuple[float, float] = (1.0, 1.0),
    ) -> None:
        super().__init__()
        self.width = width
        self.depth = depth
        self.color = color
        self.uv_scale = uv_scale

    def structure(self) -> None:
        hw = self.width * 0.5
        hd = self.depth * 0.5
        su, sv = self.uv_scale
        color = self.color.as_tuple() if self.color else (0.95, 0.55, 0.25)
        normal = (0.0, 1.0, 0.0)

        uv_quad = [(0.0, 0.0), (su, 0.0), (su, sv), (0.0, sv)]
        # Plane on XZ with +Y normal.
        # Layout per vertex: pos(3), color(3), normal(3), uv(2)
        for i, uv in enumerate(uv_quad):
            x = -hw if i % 2 == 0 else hw
            z = -hd if i < 2 else hd
            vertex = np.array([x, 0.0, z] + list(color) + list(normal) + list(uv), dtype=np.float32)
            self.mesh_context.add_vertex(vertex)

        self.mesh_context.add_quad(0, 1, 2, 3)