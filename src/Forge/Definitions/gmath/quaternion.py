import numpy as np
from Forge.Definitions.gmath.vector import *
from Forge.Definitions.gmath.matrix import Transform

class Quaternion(Vector4):
    @classmethod
    def from_axis_angle(self, axis: Vector3, angle_deg: float) -> Quaternion:
        angle_rad = np.radians(angle_deg)
        half_angle = angle_rad / 2.0
        sin_half_angle = np.sin(half_angle)
        cos_half_angle = np.cos(half_angle)
        x = axis.x * sin_half_angle
        y = axis.y * sin_half_angle
        z = axis.z * sin_half_angle
        w = cos_half_angle
        return Quaternion(x, y, z, w)

    def rotate_vector(self, vector: Vector3) -> np.ndarray:
        # Convert quaternion to rotation matrix
        q = self.as_numpy()
        x, y, z, w = q
        rotation_matrix = np.array([
            [1 - 2 * (y**2 + z**2), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x**2 + z**2), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x**2 + y**2)]
        ], dtype=np.float32)
        
        # Apply rotation to the vector
        rotated_vector = rotation_matrix @ vector.as_numpy()
        return Vector3(*rotated_vector)

    def rotate_transform(self, transform: Transform) -> Transform:
        # Convert quaternion to rotation matrix
        q = self.as_numpy()
        x, y, z, w = q
        rotation_matrix = np.array([
            [1 - 2 * (y**2 + z**2), 2 * (x * y - z * w), 2 * (x * z + y * w), 0],
            [2 * (x * y + z * w), 1 - 2 * (x**2 + z**2), 2 * (y * z - x * w), 0],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x**2 + y**2), 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        
        # Apply rotation to the transform's matrix
        new_matrix = rotation_matrix @ transform.matrix
        return Transform(matrix=new_matrix)