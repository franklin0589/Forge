
from Forge.Geometry.definitions.mesh.base_mesh import Mesh
import numpy as np
from Forge.geometry.color import Color


class TriangularPrismMesh(Mesh):
    def __init__(self, base_length: float = 1.0, height: float = 1.0, depth: float = 1.0, color: Color | None = None):
        super().__init__()
        self.base_length = base_length
        self.height = height
        self.depth = depth
        self.color = color
    
    def structure(self):
        half_base = self.base_length / 2.0
        half_depth = self.depth / 2.0

        # Define vertices for the triangular prism
        vertices = [
            np.array([-half_base, 0.0, -half_depth], dtype=np.float32),  # Base vertex 1
            np.array([half_base, 0.0, -half_depth], dtype=np.float32),   # Base vertex 2
            np.array([0.0, self.height, -half_depth], dtype=np.float32), # Apex vertex
            np.array([-half_base, 0.0, half_depth], dtype=np.float32),   # Base vertex 3
            np.array([half_base, 0.0, half_depth], dtype=np.float32),    # Base vertex 4
            np.array([0.0, self.height, half_depth], dtype=np.float32)   # Apex vertex
        ]

        for vertex in vertices:
            self.mesh_context.add_vertex(vertex)

        # Define faces (triangles and quads) of the prism
        self.mesh_context.add_triangle(0, 1, 2)  # Front face
        self.mesh_context.add_triangle(3, 4, 5)  # Back face
        self.mesh_context.add_quad(0, 1, 4, 3)   # Bottom face
        self.mesh_context.add_quad(1, 2, 5, 4)   # Right face
        self.mesh_context.add_quad(2, 0, 3, 5)   # Left face

        if self.color:
            self.mesh_context.attach_color(color=self.color.as_tuple())

class RectangularPrismMesh(Mesh):
    def __init__(self, width: float = 1.0, height: float = 1.0, depth: float = 1.0, color: Color | None = None):
        super().__init__()
        self.width = width
        self.height = height
        self.depth = depth
        self.color = color
    
    def structure(self):
        half_width = self.width / 2.0
        half_height = self.height / 2.0
        half_depth = self.depth / 2.0

        # Define vertices for the rectangular prism
        vertices = [
            np.array([-half_width, -half_height, -half_depth], dtype=np.float32),  # Vertex 0
            np.array([half_width, -half_height, -half_depth], dtype=np.float32),   # Vertex 1
            np.array([half_width, half_height, -half_depth], dtype=np.float32),    # Vertex 2
            np.array([-half_width, half_height, -half_depth], dtype=np.float32),   # Vertex 3
            np.array([-half_width, -half_height, half_depth], dtype=np.float32),   # Vertex 4
            np.array([half_width, -half_height, half_depth], dtype=np.float32),    # Vertex 5
            np.array([half_width, half_height, half_depth], dtype=np.float32),     # Vertex 6
            np.array([-half_width, half_height, half_depth], dtype=np.float32)     # Vertex 7
        ]

        for vertex in vertices:
            self.mesh_context.add_vertex(vertex)

        # Define faces (quads) of the prism
        self.mesh_context.add_quad(0, 1, 2, 3)  # Back face
        self.mesh_context.add_quad(4, 5, 6, 7)  # Front face
        self.mesh_context.add_quad(0, 1, 5, 4)  # Bottom face
        self.mesh_context.add_quad(2, 3, 7, 6)  # Top face
        self.mesh_context.add_quad(1, 2, 6, 5)  # Right face
        self.mesh_context.add_quad(0, 3, 7, 4)  # Left face

        if self.color:
            self.mesh_context.attach_color(color=self.color.as_tuple())