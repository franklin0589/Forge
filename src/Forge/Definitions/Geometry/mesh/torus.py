from Forge.Geometry.definitions.mesh.base_mesh import Mesh
import numpy as np
from Forge.geometry.color import Color


class TorusMesh(Mesh):
    def __init__(self, major_radius: float = 1.0, minor_radius: float = 0.3, major_segments: int = 32, minor_segments: int = 16, color: Color | None = None):
        super().__init__()
        self.major_radius = major_radius
        self.minor_radius = minor_radius
        self.major_segments = major_segments
        self.minor_segments = minor_segments
        self.color = color
    

    def structure(self):
        color = list(self.color.as_tuple()) if self.color else [0.95, 0.55, 0.25]
        for i in range(self.major_segments):
            theta = 2 * np.pi * i / self.major_segments
            cos_theta = np.cos(theta)
            sin_theta = np.sin(theta)

            for j in range(self.minor_segments):
                phi = 2 * np.pi * j / self.minor_segments
                cos_phi = np.cos(phi)
                sin_phi = np.sin(phi)

                x = (self.major_radius + self.minor_radius * cos_phi) * cos_theta
                y = (self.major_radius + self.minor_radius * cos_phi) * sin_theta
                z = self.minor_radius * sin_phi

                normal_x = cos_phi * cos_theta
                normal_y = cos_phi * sin_theta
                normal_z = sin_phi

                vertex = np.array([x, y, z] + color + [normal_x, normal_y, normal_z], dtype=np.float32)
                self.mesh_context.add_vertex(vertex)

        for i in range(self.major_segments):
            for j in range(self.minor_segments):
                next_i = (i + 1) % self.major_segments
                next_j = (j + 1) % self.minor_segments

                self.mesh_context.add_quad(
                    i * self.minor_segments + j,
                    next_i * self.minor_segments + j,
                    next_i * self.minor_segments + next_j,
                    i * self.minor_segments + next_j
                )
