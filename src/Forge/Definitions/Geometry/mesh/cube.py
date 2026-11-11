
from Forge.shared.protocols import *
from Forge.shared.buffer import Buffer

from Forge.geometry.vector import Vector3

from trimesh.triangles import normals

from Forge.geometry.triangle import Triangle

from Forge.Geometry.definitions.mesh.base_mesh import Mesh
import numpy as np
from Forge.shared.logs import RenderLogs
from Forge.geometry.color import Color
from typing import Generator


def traversal_cube(size: float) ->Generator[Vector3, None, None]:
    h = size / 2.0
    for index in range(8):
        first_bit = -1 if index // 4 == 0 else 1
        second_bit = -1 if index // 2 == 0 else 1
        third_bit = -1 if index % 2 == 0 else 1
        yield Vector3(first_bit * h, second_bit * h, third_bit * h)

class CubeMesh(Mesh):
    def __init__(self, size: float, color: Color) -> None:
        super().__init__()
        self.size:float = size
        self.color:Color = color

    def form(self):    
        RenderLogs().logger.info(f"CubeMesh : Form: Creating cube mesh with size {self.size} and color {self.color.as_tuple()}")
        for x, y, z in traversal_cube(self.size):
            self.add_vertex(Buffer([x, y, z]))

        self.add_quad_index(4, 5, 6, 7)  # +Z
        self.add_quad_index(0, 1, 2, 3)  # -Z
        self.add_quad_index(0, 4, 7, 3)  # -X
        self.add_quad_index(1, 5, 6, 2)  # +X
        self.add_quad_index(3, 2, 6, 7)  # +Y
        self.add_quad_index(0, 1, 5, 4)  # -Y
        
        self.attach_color(self.color)




class TexturedCubeMesh(Mesh):

    def __init__(self, size: float = 1.0, color: Color | None = None) -> None:
        super().__init__()
        self.size = size
        self.color: Color | None = color

    def structure(self) -> None:
        h = self.size / 2.0
        color = self.color.as_tuple() if self.color else (0.95, 0.55, 0.25)

        quad_data =[(4, 5, 6, 7),   # +Z
                    (0, 1, 2, 3),  # -Z
                    (0, 4, 7, 3),  # -X
                    (1, 5, 6, 2),   # +X
                    (3, 2, 6, 7),   # +Y
                    (0, 1, 5, 4)
        ]   # -Y
        uv_quad = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
        cube_vertices = list(traversal_cube(self.size))

        for quad in quad_data:
            base_triangle = Triangle(
                vertexA=cube_vertices[quad[0]],
                vertexB=cube_vertices[quad[1]],
                vertexC=cube_vertices[quad[2]]
            )
            normal = base_triangle.calculate_normal().as_numpy()
            for vertex_index, uv in zip(quad, uv_quad):
                vertex_pos = cube_vertices[vertex_index].as_numpy()
                vertex = np.array(vertex_pos+color+normal+uv, dtype=np.float32)
                self.add_vertex(vertex)
            self.add_quad_index(*quad)
