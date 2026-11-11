from pathlib import Path

from Forge.Render.definitions.mesh import Mesh
from Forge.Lights.materials import Material
from Forge.Render.object.model import Model
from Forge.Rigging.skeleton import Skeleton
from Forge.geometry.transform import Transform


# Scene-level entity base with only an id + transform.
class Object:
    def __init__(self, transform: Transform | None = None):
        self.id = id(self)
        self.transform = transform if transform is not None else Transform()

    def render(self) -> None:
        # Placeholder for rendering logic; to be implemented in subclasses.
        pass


class ModelObject(Object):
    def __init__(
        self,
        transform: Transform | None = None,
        model: Model | None = None,
    ):
        super().__init__(transform=transform)
        self.model = model



    # def build(self) -> Model:
    #     # Compose one model payload from mesh + transform + material wiring.
    #     self.model = Model(
    #     	vertices=self.mesh.get_vertices(),
	# 		indices=self.mesh.get_indices(),
	# 		texture_path=str(self.material.texture_path) if self.material is not None and self.material.texture_path is not None else None,
	# 		vertex_format="3f 3f 3f 2f",
	# 		attributes=["in_pos", "in_color", "in_normal", "in_uv"],
	# 		point=self.transform,
	# 		vertex_shader_path=self.material.vertex_shader_path if self.material is not None else None,
	# 		fragment_shader_path=self.material.fragment_shader_path if self.material is not None else None,
	# 		material=self.material,
	# 	)
    #     return self.model

class LightObject(Object):
    def __init__(self, light, transform: Transform | None = None):
        super().__init__(transform=transform)
        self.light = light

    def build(self) -> Model:
        ...

class Character(Object):
    """Renderable line overlay for a Skeleton's current pose."""

    def __init__(
        self,
        skeleton: Skeleton,
        transform: Transform | None = None,
        color: tuple[float, float, float] = (1.0, 0.95, 0.2),
    ):
        super().__init__(transform=transform)
        self.skeleton = skeleton
        self.color = color
        self.material = Material(use_texture=False, use_lighting=False)
        self.mesh = self.skeleton.build_bone_mesh(color=self.color)
        self.build()

    def build(self) -> Model:
        self.model = Model(
            vertices=self.mesh.get_vertices(),
            indices=self.mesh.get_indices(),
            texture_path=None,
            vertex_format="3f 3f",
            attributes=["in_pos", "in_color"],
            point=self.transform,
            material=self.material,
            render_mode="lines",
            depth_test=False,
        )
        return self.model

    def update_from_skeleton(self) -> None:
    
        self.mesh = self.skeleton.build_bone_mesh(color=self.color)
        self.model.vertices = self.mesh.get_vertices()
        self.model.indices = self.mesh.get_indices()
        self.model.point = self.transform.matrix