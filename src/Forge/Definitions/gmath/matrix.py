from __future__ import annotations
import numpy as np

class Matrix:
    def __init__(self, data: np.ndarray):
        self.data = data
        self.height = data.shape[0]
        self.width = data.shape[1]

    def __matmul__(self, other: Matrix) -> Matrix:
        return Matrix(matrix=self.matrix @ other.matrix)

    def inverse(self) -> Matrix:
        return Matrix(matrix=np.linalg.inv(self.matrix))

    def as_type(self, dtype: np.dtype) -> np.ndarray:
        return self.matrix.astype(dtype)


# TODO: Mat 22 rotation methods (rotate, scale, etc.)
class Matrix22(Matrix):
    @classmethod
    def identity(cls) -> 'Matrix':
        _identity = np.eye(2, dtype = np.float32)
        return cls(_identity)

    def __init__(self, matrix: np.ndarray):
        super().__init__(matrix)
        if self.height != 2 or self.width != 2:
            raise ValueError("Matrix22 must be 2x2")


# TODO: Mat 22 rotation methods (rotate, scale, etc.)
class Matrix33(Matrix):
    @classmethod
    def identity(cls) -> 'Matrix':
        _identity = np.eye(3, dtype = np.float32)
        return cls(_identity)

    def __init__(self, matrix: np.ndarray):
        super().__init__(matrix)
        if self.height != 3 or self.width != 3:
            raise ValueError("Matrix33 must be 3x3")


class Matrix44(Matrix):
    @classmethod
    def zero(cls) -> 'Matrix':
        _zero = np.zeros((4, 4), dtype=np.float32)
        return cls(_zero)

    @classmethod
    def translation(cls, tx: float, ty: float, tz: float) -> Matrix44:
        m = np.eye(4, dtype=np.float32)
        m[0, 3] = tx
        m[1, 3] = ty
        m[2, 3] = tz
        return Matrix44(m)

    @classmethod
    def rotation_x(cls, angle_deg: float) -> Matrix44:
        a = np.radians(angle_deg)
        c = np.cos(a)
        s = np.sin(a)
        m = np.eye(4, dtype=np.float32)
        m[1, 1] = c
        m[1, 2] = -s
        m[2, 1] = s
        m[2, 2] = c
        return Matrix44(m)

    @classmethod
    def rotation_y(cls, angle_deg: float) -> Matrix44:
        a = np.radians(angle_deg)
        c = np.cos(a)
        s = np.sin(a)
        m = np.eye(4, dtype=np.float32)
        m[0, 0] = c
        m[0, 2] = s
        m[2, 0] = -s
        m[2, 2] = c
        return Matrix44(m)

    @classmethod
    def rotation_z(angle_deg: float) -> Matrix44:
        a = np.radians(angle_deg)
        c = np.cos(a)
        s = np.sin(a)
        return Matrix44(np.array(
            [
                [c, -s, 0.0, 0.0],
                [s, c, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            dtype=np.float32,
        ))

    @classmethod
    def identity(cls) -> 'Matrix':
        _identity = np.eye(4, dtype = np.float32)
        return cls(_identity)
    
    def __init__(self, matrix: np.ndarray):
        super().__init__(matrix)
        if self.height != 4 or self.width != 4:
            raise ValueError("Matrix44 must be 4x4")
        
    def translate(self, tx: float, ty: float, tz: float):
        translation = np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ])
        self.matrix = self.matrix @ translation
        return self

    def rotate_z(self, angle_deg: float):
        a = np.radians(angle_deg)
        c = np.cos(a)
        s = np.sin(a)
        rotation_z = np.array([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.matrix = self.matrix @ rotation_z
        return self

    def rotate_y(self, angle_deg: float):
        a = np.radians(angle_deg)
        c = np.cos(a)
        s = np.sin(a)
        rotation_y = np.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ])
        self.matrix = self.matrix @ rotation_y
        return self 
    
    def rotate_x(self, angle_deg: float):
        a = np.radians(angle_deg)
        c = np.cos(a)
        s = np.sin(a)
        rotation_x = np.array([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]
        ])
        self.matrix = self.matrix @ rotation_x
        return self
    
    def scale(self, sx: float, sy: float, sz: float):
        scale = np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])
        self.matrix = self.matrix @ scale 
        return self

    def as_numpy(self) -> np.ndarray:
        return self.matrix
    
Transform = Matrix44