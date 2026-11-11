from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from Forge.Definitions.gmath.matrix import Transform

@dataclass
class Bone:
    # local_bind/local_pose are parent-relative transforms.
    name: str
    local_bind: Transform
    local_pose: Transform
    parent: int = -1


