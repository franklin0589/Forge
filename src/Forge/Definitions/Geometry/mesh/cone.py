from Forge.geometry.color import Color
from Forge.Geometry.definitions.mesh.base_mesh import Mesh
import numpy as np

class ConeMesh(Mesh):
    def __init__(self, radius: float = 1.0, height: float = 2.0, segments: int = 32, color: Color | None = None):
        super().__init__()
        self.radius = radius
        self.height = height
        self.segments = segments
        self.color = color
    
    def structure(self):
        # Create the base circle vertices
        for i in range(self.segments):
            angle = 2 * np.pi * i / self.segments
            x = self.radius * np.cos(angle)
            z = self.radius * np.sin(angle)
            vertex = np.array([x, 0.0, z], dtype=np.float32)
            self.mesh_context.add_vertex(vertex)

        # Add the apex vertex
        apex_vertex = np.array([0.0, self.height, 0.0], dtype=np.float32)
        self.mesh_context.add_vertex(apex_vertex)

        # Create the base indices
        for i in range(self.segments):
            next_index = (i + 1) % self.segments
            self.mesh_context.add_triangle(i, next_index, self.segments)  # Base triangle

        # Create the side triangles
        for i in range(self.segments):
            next_index = (i + 1) % self.segments
            self.mesh_context.add_triangle(i, next_index, self.segments)  # Side triangle

        if self.color:
            self.mesh_context.attach_color(color=self.color.as_tuple())

class TexturedConeMesh(ConeMesh):
    def __init__(self, radius: float = 1.0, height: float = 2.0, segments: int = 32, color: Color | None = None):
        super().__init__(radius, height, segments, color)
    
    def structure(self):
        super().structure()
        # Attach UV coordinates for the base and sides
        uv_base = [(0.5 + 0.5 * np.cos(2 * np.pi * i / self.segments), 
                    0.5 + 0.5 * np.sin(2 * np.pi * i / self.segments)) for i in range(self.segments)]
        uv_apex = (0.5, 0.5)  # UV for the apex vertex

        # Attach UVs to the base vertices
        for i in range(self.segments):
            self.mesh_context.attach_data_to_vertex(i, np.array(uv_base[i], dtype=np.float32))

        # Attach UV to the apex vertex
        self.mesh_context.attach_data_to_vertex(self.segments, np.array(uv_apex, dtype=np.float32))