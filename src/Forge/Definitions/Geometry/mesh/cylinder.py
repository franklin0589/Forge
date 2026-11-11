from Forge.geometry.color import Color
from Forge.Geometry.definitions.mesh.base_mesh import Mesh
import numpy as np

class CylinderMesh(Mesh):
    def __init__(self, radius: float = 1.0, height: float = 2.0, segments: int = 32, color: Color | None = None):
        super().__init__()
        self.radius = radius
        self.height = height
        self.segments = segments
        self.color = color

    def structure(self):
        # Create the top and bottom circle vertices
        for i in range(self.segments):
            angle = 2 * np.pi * i / self.segments
            x = self.radius * np.cos(angle)
            z = self.radius * np.sin(angle)
            bottom_vertex = np.array([x, 0.0, z], dtype=np.float32)
            top_vertex = np.array([x, self.height, z], dtype=np.float32)
            self.mesh_context.add_vertex(bottom_vertex)
            self.mesh_context.add_vertex(top_vertex)

        # Create the side faces (quads)
        for i in range(self.segments):
            next_index = (i + 1) % self.segments
            self.mesh_context.add_quad(
                i * 2, next_index * 2, next_index * 2 + 1, i * 2 + 1
            )

        # Create the top and bottom faces (triangles)
        top_center_index = self.segments * 2
        bottom_center_index = self.segments * 2 + 1
        self.mesh_context.add_vertex(np.array([0.0, self.height, 0.0], dtype=np.float32))  # Top center
        self.mesh_context.add_vertex(np.array([0.0, 0.0, 0.0], dtype=np.float32))  # Bottom center

        for i in range(self.segments):
            next_index = (i + 1) % self.segments
            self.mesh_context.add_triangle(bottom_center_index, next_index * 2, i * 2)  # Bottom face
            self.mesh_context.add_triangle(top_center_index, i * 2 + 1, next_index * 2 + 1)  # Top face

        if self.color:
            self.mesh_context.attach_color(color=self.color.as_tuple())

class TexturedCylinderMesh(CylinderMesh):
    def __init__(self, radius: float = 1.0, height: float = 2.0, segments: int = 32, color: Color | None = None):
        super().__init__()
        self.radius = radius
        self.height = height
        self.segments = segments
        self.color = color
    
    def structure(self):
        super().structure()
        # Attach UV coordinates for the side faces
        uv_side = [(i / self.segments, 0.0) for i in range(self.segments)] + [(i / self.segments, 1.0) for i in range(self.segments)]
        for i in range(self.segments):
            self.mesh_context.attach_data_to_vertex(i * 2, np.array(uv_side[i], dtype=np.float32))  # Bottom vertex
            self.mesh_context.attach_data_to_vertex(i * 2 + 1, np.array(uv_side[i + self.segments], dtype=np.float32))  # Top vertex
