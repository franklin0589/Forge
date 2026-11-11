from __future__ import annotations
import numpy as np

class Vector:
    @classmethod
    def from_tuple(cls, tpl: tuple) -> "Vector":
        return cls(list[tpl])
    
    @classmethod
    def from_numpy(cls, arr: np.ndarray) -> "Vector":
        return cls([a for a in arr])
    
    def __init__(self, components:list[int|float]):
        self.components = np.array(components, dtype=np.float32)
        self.dimension = len(components)

    def normalize(self):
        v = np.array(self.components, dtype=np.float32)
        norm = np.linalg.norm(v)
        if norm == 0.0:
            return v
        return 

    def __repr__(self) -> str:
        return f"Vector{self.dimension}({', '.join(map(str, self.components))})"
    
    def as_numpy(self) -> np.ndarray:
        raise NotImplementedError("Subclasses must implement as_numpy()")


    def __add__(self, other: Vector):
        if not isinstance(other, Vector):
            raise TypeError("Operand must be of type Vector")
        elif self.dimension != other.dimension:
            raise ValueError("Vectors must have the same dimension")
        return self.__class__([a + b for a, b in zip(self.components, other.components)])

    def __sub__(self, other: Vector):
        if not isinstance(other, Vector):
            raise TypeError("Operand must be of type Vector")
        elif self.dimension != other.dimension:
            raise ValueError("Vectors must have the same dimension")
        return self.__class__([a - b for a, b in zip(self.components, other.components)])

    def __mul__(self, scalar: float) -> "Vector":
        return self.__class__([a * scalar for a in self.components])
    
    def __truediv__(self, scalar: float) -> "Vector":
        return self.__class__([a / scalar for a in self.components])
    
    def __neg__(self) -> "Vector":
        return self.__class__([-a for a in self.components])

    def cross(self, other: Vector) -> "Vector":
        a = self.components
        b = other.components
        match self.dimension:
            case 3:
                return self.__class__([
                    a[1]*b[2] - a[2]*b[1],
                    a[2]*b[0] - a[0]*b[2],
                    a[0]*b[1] - a[1]*b[0]
                ])
            case _:
                raise ValueError("Cross product is only defined for 3-dimensional vectors")

    def __iter__(self):
        return iter(self.components)
    
class Vector2(Vector):
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y
        super().__init__([x, y])

class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x: float = x
        self.y: float = y
        self.z: float = z

class Vector4:
    def __init__(self, x: float, y: float, z: float, w: float):
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.w: float = w    

Vector = Vector2 | Vector3 | Vector4
Point = Vector2 
Vertex = Vector3

X_AXIS = Vector3(1.0, 0.0, 0.0)
Y_AXIS = Vector3(0.0, 1.0, 0.0)
Z_AXIS = Vector3(0.0, 0.0, 1.0)