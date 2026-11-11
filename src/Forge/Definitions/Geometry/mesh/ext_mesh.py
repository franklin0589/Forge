from __future__ import annotations

from Forge.geometry.color import Color
from Forge.Geometry.definitions.mesh.base_mesh import Mesh
import numpy as np
from Forge.Rigging.skinning import SkinWeights, Skinning
from pathlib import Path
import trimesh


class ExternalMesh(Mesh):
    def __init__(
        self,
        mesh_path: str | Path,
        color: tuple[float, float, float] = (0.4, 0.85, 0.95),
    ) -> None:
        super().__init__()
        self.mesh_path = Path(mesh_path)
        if not self.mesh_path.exists():
            raise FileNotFoundError(f"Mesh file not found: {mesh_path}")
        self.color = color
        self.skin_weights: SkinWeights | None = None

    def attach_skeleton(
        self, skeleton, model, root: int = 0, high_bone: int = 0
    ) -> None:
        imported_skin = self.skin_weights
        if imported_skin is not None:
            ids = imported_skin.bone_ids.astype(np.int32)
            w = imported_skin.bone_weights.astype(np.float32)
            bone_count = len(self.mesh_skeleton.bones)
            valid = (ids >= 0) & (ids < bone_count)
            valid_weight = np.any((w > 1e-4) & valid)
            child_weight = np.any((ids == self.child_bone_index) & (w > 0.05) & valid)
            # Imported weights often target a different rig. If they don't drive our child bone,
            # switch to a procedural gradient so deformation is visible in this rough demo.
            if (not valid_weight) or (not child_weight):
                imported_skin = None
        if imported_skin is None:
            imported_skin = Skinning.axis_gradient_weights(
                model,
                low_bone=root,
                high_bone=high_bone,
                axis=1,
            )
        Skinning(model, skeleton=skeleton).attach(imported_skin)

    def structure(self) -> None:
        # External meshes are pre-structured; no additional structure is needed.

        loaded = trimesh.load(self.mesh_path, force="mesh")

        if isinstance(loaded, trimesh.Scene):
            geometries = [
                g for g in loaded.geometry.values() if isinstance(g, trimesh.Trimesh)
            ]
            if not geometries:
                raise ValueError(f"No mesh geometry found in file: {self.mesh_path}")
            mesh = trimesh.util.concatenate(geometries)
        else:
            mesh = loaded

        if not isinstance(mesh, trimesh.Trimesh):
            raise ValueError(f"Unsupported mesh payload from file: {self.mesh_path}")

        mesh = mesh.copy()
        if mesh.faces is None or len(mesh.faces) == 0:
            raise ValueError(f"Mesh has no faces: {self.mesh_path}")

        if not mesh.is_watertight:
            # Non-watertight is acceptable for rendering, but we still normalize scale.
            pass

        mesh.apply_translation(-mesh.bounding_box.centroid)
        max_extent = float(np.max(mesh.extents))
        if max_extent > 0.0:
            mesh.apply_scale(1.6 / max_extent)

        # Convert to the engine's canonical static layout:
        # pos(3), color(3), normal(3), uv(2)
        positions = mesh.vertices.astype(np.float32)
        normals = mesh.vertex_normals.astype(np.float32)

        if normals.shape[0] != positions.shape[0]:
            normals = np.zeros_like(positions, dtype=np.float32)

        uv = np.zeros((positions.shape[0], 2), dtype=np.float32)
        visual_uv = getattr(getattr(mesh, "visual", None), "uv", None)
        if visual_uv is not None:
            visual_uv = np.asarray(visual_uv, dtype=np.float32)
            if visual_uv.ndim == 2 and visual_uv.shape[1] >= 2:
                count = min(visual_uv.shape[0], uv.shape[0])
                uv[:count] = visual_uv[:count, :2]

        color = (
            color if isinstance(color, tuple) and len(color) == 3 else (0.4, 0.85, 0.95)
        )
        for pos, n, u in zip(positions, normals, uv):
            self.mesh_context.add_vertex(
                np.array([*pos, *color, *n, *u], dtype=np.float32)
            )

        for face in mesh.faces:
            if len(face) == 3:
                self.mesh_context.add_triangle(*face.astype(np.uint32))
            elif len(face) == 4:
                self.mesh_context.add_quad(*face.astype(np.uint32))
            else:
                # For polygons with more than 4 vertices, we can triangulate them.
                # Here we use a simple fan triangulation.
                for i in range(1, len(face) - 1):
                    self.mesh_context.add_triangle(face[0], face[i], face[i + 1])
        # Face indices stay in object-local vertex space.
        self.skin_weights = _extract_skin_weights(mesh, positions.shape[0])


def _extract_skin_weights(mesh, vertex_count: int) -> SkinWeights | None:
    # Rough extractor for glTF-like JOINTS_0 / WEIGHTS_0 vertex attributes.
    attrs = getattr(mesh, "vertex_attributes", None)
    if not isinstance(attrs, dict):
        return None

    joints = attrs.get("JOINTS_0") or attrs.get("joints")
    weights = attrs.get("WEIGHTS_0") or attrs.get("weights")
    if joints is None or weights is None:
        return None

    j = np.asarray(joints)
    w = np.asarray(weights, dtype=np.float32)
    if j.ndim != 2 or w.ndim != 2:
        return None
    if j.shape[1] < 1 or w.shape[1] < 1:
        return None

    if j.shape[1] < 4:
        j_pad = np.zeros((j.shape[0], 4), dtype=np.int32)
        j_pad[:, : j.shape[1]] = j.astype(np.int32)
        j = j_pad
    else:
        j = j[:, :4].astype(np.int32)

    if w.shape[1] < 4:
        w_pad = np.zeros((w.shape[0], 4), dtype=np.float32)
        w_pad[:, : w.shape[1]] = w.astype(np.float32)
        w = w_pad
    else:
        w = w[:, :4].astype(np.float32)

    if j.shape[0] != vertex_count or w.shape[0] != vertex_count:
        count = min(vertex_count, j.shape[0], w.shape[0])
        j_fix = np.zeros((vertex_count, 4), dtype=np.int32)
        w_fix = np.zeros((vertex_count, 4), dtype=np.float32)
        j_fix[:count] = j[:count]
        w_fix[:count] = w[:count]
        j, w = j_fix, w_fix

    return SkinWeights(bone_ids=j, bone_weights=w)
