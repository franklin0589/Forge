import numpy as np
from typing import Protocol


class SurfaceProtocol(Protocol):
    width: int
    height: int

    def save(self, filename: str) -> None:...
    def capture(self) -> np.ndarray:...
