from __future__ import annotations
from Forge.Rigging.bone import Bone
from Forge.geometry.transform import Transform
from typing import Optional, Any

from dataclasses import dataclass, field
import numpy as np

def default(var:Any, default_value:Any) -> Any:
    if var is None:
        return default_value
    else:
        return var

@dataclass
class Pose:
    skeleton: "Skeleton" = field(default=None)
    bind_matrices: list[Transform] = []
    pose_matrices: list[Transform] = []
    inverse_bind_matrices: list[Transform] = [] 
    skinning_matrices: list[Transform] =[]

    def calculate_skinning_matrices(self) -> list[Transform]:
        """Compute skinning matrices as pose * inverse(bind)."""
        return [
            pose @ inv_bind
            for pose, inv_bind in zip(self.pose_matrices, self.inverse_bind_matrices)
        ]

    def calculate_inverse_bind_matrices(self) -> list[Transform]:
        """Compute the inverse of each bind matrix."""
        return [m.inverse() for m in self.bind_matrices]

    def compute_world_matrices(self, use_pose: bool) -> list[Transform]:
        world: list[Transform] = [Transform() for _ in self.skeleton.bones]
        for i, bone in enumerate(self.skeleton.bones):
            local = bone.local_pose if use_pose else bone.local_bind
            if bone.parent < 0:
                world[i] = local
            else:
                world[i] = world[bone.parent] @ local
        return world

    def generate_skinning_buffer(self) -> np.ndarray:
        """Flatten skinning matrices for UBO/SSBO style upload."""
        if not self.skinning_matrices:
            return np.array([], dtype=np.float32)
        return np.stack([m.matrix for m in self.skinning_matrices]).astype(np.float32)


class Skeleton:

    def __init__(self, bones: list[Bone] | None = None) -> None:
        self.bones: list[Bone] = bones if bones is not None else []
        self.pose = Pose(skeleton=self)

    def _validate_hierarchy(self) -> None:
        for i, bone in enumerate(self.bones):
            if bone.parent >= i:
                raise ValueError(
                    "Skeleton expects parent bones to appear before children. "
                    f"Bone '{bone.name}' has parent index {bone.parent} at position {i}."
                )

    def _validate_index(self, bone_index: int) -> None:
        if bone_index < 0 or bone_index >= len(self.bones):
            raise IndexError(f"Bone index out of range: {bone_index}")

    def _validate_parent(self, bone: Bone) -> None:
        if bone.parent >= len(self.bones):
            raise ValueError(f"Invalid parent index {bone.parent} for bone '{bone.name}'")


    def create_bone(self, name: str, parent: int, local_bind:Optional[Transform], local_pose:Optional[Transform]) -> int:
        """Append a bone and return its index."""
        _bind = default(local_bind, Transform())
        _pose = default(local_pose, _bind.copy())
        _bone = Bone(name=name, parent=parent, local_bind=_bind, local_pose=_pose)
        self._validate_parent(_bone)
        self.bones.append(_bone)
        self.rebuild()
        return len(self.bones) - 1 # Return the index of the newly added bone

    def add_bone(self, bone: Bone) -> int:
        """Append a prebuilt bone and return its index."""
        self._validate_parent(bone)
        self.bones.append(bone)
        self.rebuild()
        return len(self.bones) - 1

    def find_bone(self, name: str) -> int:
        for i, bone in enumerate(self.bones):
            if bone.name == name:
                return i
        return -1
    
    def build_bone_mesh(self, color: tuple[float, float, float] = (1.0, 0.25, 0.15)):
        from Forge.Render.definitions.form import BoneMesh

        self.update_pose()
        mesh = BoneMesh(self)
        mesh.color = color
        mesh.rebuild()
        return mesh

    def set_local_pose(self, bone_index: int, local_pose: Transform ) -> None:
        self._validate_index(bone_index)
        self.bones[bone_index].local_pose = local_pose.copy()

    def set_local_bind(self, bone_index: int, local_bind: Transform) -> None:
        self._validate_index(bone_index)
        self.bones[bone_index].local_bind = local_bind.copy()

    def reset_pose_to_bind(self) -> None:
        for bone in self.bones:
            bone.local_pose = bone.local_bind.copy()

    def rebuild(self) -> None:
        """Recompute bind + pose caches and skinning matrices."""
        self._validate_hierarchy()
        self.pose.bind_matrices = self.pose.compute_world_matrices(use_pose=False)
        self.pose.pose_matrices = self.pose.compute_world_matrices(use_pose=True)
        self.pose.inverse_bind_matrices = self.pose.calculate_inverse_bind_matrices()
        self.pose.skinning_matrices = self.pose.calculate_skinning_matrices()
    
    
    def update_pose(self) -> None:
        """Refresh pose-dependent matrices after editing local poses."""
        if not self.bones:
            return
        self.pose.pose_matrices = self.pose.compute_world_matrices(use_pose=True)
        if not self.pose.inverse_bind_matrices:
            self.pose.inverse_bind_matrices = [m.inverse() for m in self.pose.bind_matrices]
        self.pose.skinning_matrices = [
            pose @ inv_bind
            for pose, inv_bind in zip(self.pose.pose_matrices, self.pose.inverse_bind_matrices)
        ]