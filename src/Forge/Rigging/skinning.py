"""
the bridge between your mesh vertex data and your skeleton animation shader path.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from Forge.Render.object.model import Model
from Forge.Rigging.skeleton import Skeleton


@dataclass
class SkinWeights:
    bone_ids: np.ndarray
    bone_weights: np.ndarray

    def validate(self, vertex_count: int) -> None:
        if self.bone_ids.shape != (vertex_count, 4):
            raise ValueError(
                f"bone_ids shape must be ({vertex_count}, 4), got {self.bone_ids.shape}"
            )
        if self.bone_weights.shape != (vertex_count, 4):
            raise ValueError(
                f"bone_weights shape must be ({vertex_count}, 4), got {self.bone_weights.shape}"
            )


class Skinning:
    """Attach skeleton + vertex skin weights to a Model for GPU skinning."""

    def __init__(self, model: Model, skeleton: Skeleton, max_bones: int = 64):
        self.model = model
        self.skeleton = skeleton
        self.max_bones = max_bones

    @staticmethod
    def _parse_vertex_stride(vertex_format: str) -> int:
        stride = 0
        for token in vertex_format.split():
            token = token.strip()
            if not token.endswith("f"):
                continue
            stride += int(token[:-1])
        if stride <= 0:
            raise ValueError(f"Unsupported vertex format: {vertex_format}")
        return stride

    def attach(self, skin_weights: SkinWeights) -> Model:
        # 1) Decode current vertex stride/layout.
        base_stride = self._parse_vertex_stride(self.model.vertex_format)
        vertices = self.model.vertices.reshape(-1, base_stride)
        vertex_count = vertices.shape[0]

        skin_weights.validate(vertex_count)

        bone_ids_i32 = skin_weights.bone_ids.astype(np.int32)
        bone_w = skin_weights.bone_weights.astype(np.float32)

        # 2) Remove invalid influences for the active skeleton.
        bone_count = len(self.skeleton.bones)
        valid_mask = (bone_ids_i32 >= 0) & (bone_ids_i32 < bone_count)
        bone_w = bone_w * valid_mask.astype(np.float32)
        bone_ids_i32 = np.where(valid_mask, bone_ids_i32, 0)

        # 3) Renormalize so each vertex keeps total weight = 1.
        sums = np.sum(bone_w, axis=1, keepdims=True)
        empty = sums[:, 0] == 0.0
        if np.any(empty):
            # Ensure each vertex has at least one valid influence.
            bone_ids_i32[empty, 0] = 0
            bone_w[empty, 0] = 1.0
            sums = np.sum(bone_w, axis=1, keepdims=True)
        bone_w = bone_w / sums

        bone_ids = bone_ids_i32.astype(np.float32)

        # 4) Append ids+weights to the vertex stream for shader skinning.
        skinned_vertices = np.hstack((vertices, bone_ids, bone_w)).astype(np.float32)
        self.model.vertices = skinned_vertices.reshape(-1)
        self.model.vertex_format = f"{self.model.vertex_format} 4f 4f"
        self.model.attributes = [*self.model.attributes, "in_bone_ids", "in_bone_weights"]
        self.model.skeleton = self.skeleton
        self.model.max_bones = self.max_bones
        return self.model

    @staticmethod
    def rigid_weights(vertex_count: int, bone_index: int = 0) -> SkinWeights:
        bone_ids = np.zeros((vertex_count, 4), dtype=np.int32)
        bone_ids[:, 0] = bone_index
        bone_weights = np.zeros((vertex_count, 4), dtype=np.float32)
        bone_weights[:, 0] = 1.0
        return SkinWeights(bone_ids=bone_ids, bone_weights=bone_weights)

    @staticmethod
    def axis_gradient_weights(
        model: Model,
        low_bone: int = 0,
        high_bone: int = 1,
        axis: int = 1,
    ) -> SkinWeights:
        """Create rough 2-bone weights from vertex position along one axis."""
        stride = Skinning._parse_vertex_stride(model.vertex_format)
        verts = model.vertices.reshape(-1, stride)
        values = verts[:, axis].astype(np.float32)

        vmin = float(np.min(values))
        vmax = float(np.max(values))
        denom = vmax - vmin
        if denom <= 1e-8:
            t = np.zeros_like(values, dtype=np.float32)
        else:
            t = (values - vmin) / denom

        bone_ids = np.zeros((verts.shape[0], 4), dtype=np.int32)
        bone_ids[:, 0] = low_bone
        bone_ids[:, 1] = high_bone

        bone_weights = np.zeros((verts.shape[0], 4), dtype=np.float32)
        bone_weights[:, 0] = 1.0 - t
        bone_weights[:, 1] = t
        return SkinWeights(bone_ids=bone_ids, bone_weights=bone_weights)