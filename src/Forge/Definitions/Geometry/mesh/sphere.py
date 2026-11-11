
from Forge.Geometry.definitions.mesh.base_mesh import Mesh
import numpy as np
from Forge.geometry.color import Color

class SphereMesh(Mesh):
    def __init__(self, radius: float = 1.0, segments: int = 16, rings: int = 16, color:Color = None) -> None:
        super().__init__()
        self.radius = radius
        self.segments = segments
        self.rings = rings
        self.color = color

    def structure(self) -> None:
        color =list(self.color.as_tuple()) if self.color else [0.95, 0.55, 0.25]
        for ring in range(self.rings + 1):
            theta = np.pi * ring / self.rings
            sin_theta = np.sin(theta)
            cos_theta = np.cos(theta)

            for segment in range(self.segments + 1):
                phi = 2 * np.pi * segment / self.segments
                sin_phi = np.sin(phi)
                cos_phi = np.cos(phi)

                x = self.radius * sin_theta * cos_phi
                y = self.radius * cos_theta
                z = self.radius * sin_theta * sin_phi
                normal = self.calculate_normal(np.array([x, y, z], dtype=np.float32))
                self.mesh_context.add_vertex(np.array([x, y, z]+list(color)+list(normal)))
                
        for ring in range(self.rings):
            for segment in range(self.segments):
                first = (ring * (self.segments + 1)) + segment
                second = first + self.segments + 1
                self.mesh_context.add_quad(first, second, second + 1, first + 1)


    def calculate_normal(self, vertex: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(vertex)
        if norm == 0:
            return np.array([0.0, 0.0, 0.0], dtype=np.float32)
        return vertex / norm


class TexturedSphereMesh(SphereMesh):
    def __init__(self, radius: float = 1.0, segments: int = 16, rings: int = 16, color:Color = None) -> None:
        super().__init__(radius, segments, rings, color)

    def structure(self) -> None:
        super().structure()
        for ring in range(self.rings + 1):
            for segment in range(self.segments + 1):
                u = segment / self.segments
                v = ring / self.rings
                self.mesh_context.attach_data_to_vertex(ring * (self.segments + 1) + segment, np.array([u, v], dtype=np.float32))