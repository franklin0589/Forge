import numpy as np
from Forge.Definitions import Vector3, Transform


def look_at(eye: Vector3, target: Vector3, up: Vector3) -> Transform:
	f = (target-eye).normalized()
	s = f.cross(up).normalized()
	u = s.cross(f)
	m = Transform.identity().as_numpy()
	m[0, 0:3] = s
	m[1, 0:3] = u
	m[2, 0:3] = -f
	m[0, 3] = -np.dot(s, eye.as_numpy())
	m[1, 3] = -np.dot(u, eye.as_numpy())
	m[2, 3] = np.dot(f, eye.as_numpy())
	return Transform(m)

def perspective(fov_y_deg: float, aspect: float, near: float, far: float) -> Transform:
	f = 1.0 / np.tan(np.radians(fov_y_deg) * 0.5)
	m = Transform.zero().as_numpy()
	m[0, 0] = f / aspect
	m[1, 1] = f
	m[2, 2] = (far + near) / (near - far)
	m[2, 3] = (2.0 * far * near) / (near - far)
	m[3, 2] = -1.0
	return Transform(m)