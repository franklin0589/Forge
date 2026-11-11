import numpy as np
# from Forge.Gadgets.geometry.persp1ective import look_at, perspective
from Forge.Definitions.gmath.quaternion import AQuaternion, Quaternion
from Forge.Definitions.gmath.matrix import Transform
from Forge.Definitions import Vector3

from Forge.Camera.utils import look_at, perspective

class Camera:
    def __init__(
        self,
        position: Vector3,
        target: Vector3,
        up: Vector3,
        fov_y_deg: float = 60.0,
        near: float = 0.1,
        far: float = 100.0,
    ) -> None:
        self._position = position
        self._target = target
        self._up = up
        self.fov_y_deg = fov_y_deg
        self.near = near
        self.far = far

    @property
    def up(self) -> Vector3:
        return self._up
    @up.setter
    def up(self, up: Vector3) -> None:
        self._up = up

    @property
    def position(self) -> Vector3:
        return self._position

    @position.setter
    def position(self, position: Vector3) -> None:
        self._position = position

    @property
    def target(self) -> Vector3:
        return self._target
    @target.setter
    def target(self, target: Vector3) -> None:
        self._target = target


    def get_mvp(self, width: int, height: int) -> Transform:
        look_matrix =look_at(self.position, self.target, self.up)
        aspect = width / height
        project_matrix = perspective(self.fov_y_deg, aspect, self.near, self.far)
        return project_matrix(width, height) @ look_matrix

    