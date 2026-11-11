from __future__ import annotations

import numpy as np
from Forge.Resources.materials import Material
from dataclasses import dataclass

from Forge.geometry.transform import Transform


from __future__ import annotations

from dataclasses import dataclass

import moderngl
import numpy as np

from __future__ import annotations
from Forge.geometry.transform import Transform
from Forge.Geometry.definitions.mesh.base_mesh import Mesh
from Forge.Resources.materials import Material
from Forge.Resources.texture import Texture
from Forge.Rigging.skeleton import Skeleton
import moderngl

from Forge.Render.program import ShaderProgram

from dataclasses import dataclass

@dataclass
class VertexData:
    format: str
    attributes: list[str]

@dataclass
class Model:
    mesh: Mesh
    material: Material | None = None
    textures:dict[int, Texture] = {}
    program: ShaderProgram | None = None
    vertex_data: VertexData | None = None
    depth_test: bool = True
    render_mode: str = "triangles"

    def add_texture(self, unit:int, ctx:moderngl.Context, resource_path:str) -> None:
        self.textures[unit] = Texture(ctx= ctx, resource_path=resource_path)



@dataclass
class DynamicModel(Model):
    max_bones: int = 64
    skeleton: Skeleton | None = None
	

@dataclass
class CubeMapModel(Model):
    cube_map_faces: dict[str, str] | None = None
    cube_map_unit: int = 1
