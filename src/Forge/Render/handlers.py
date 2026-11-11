from abc import ABC, abstractmethod
from Forge.Render.context import ShaderContext

from Forge.Definitions.materials.cube_map import CubeMapTexture
from Forge.Definitions.materials.texture import Texture2D
import moderngl

class ShaderHandler(ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler
    
    @abstractmethod
    def handle(self, shader_context: ShaderContext):
        pass


class IndicesHandler(ShaderHandler):
    def handle(self, shader_context: ShaderContext):
        if shader_context.model.indices is not None:
            index_data = shader_context.model.indices
            if index_data.dtype != "u4":
                index_data = index_data.astype("u4")
            shader_context.ibo = shader_context.ctx.buffer(index_data.tobytes())
        if self.next_handler:
            self.next_handler.handle(shader_context)

class BufferGeneratorHandler(ShaderHandler):
    def handle(self, shader_context: ShaderContext):
        shader_context.vbo = shader_context.ctx.buffer(shader_context.model.vertices.tobytes())
        if self.next_handler:
            self.next_handler.handle(shader_context)

class TextureHandler(ShaderHandler):
    def handle(self, shader_context: ShaderContext):
        if shader_context.model.texture_path is not None and "u_tex" in shader_context.model.program:
            shader_context.model.tex = Texture2D(shader_context.ctx, shader_context.model.texture_path)
            shader_context.model.tex.use(unit=shader_context.model.texture_unit)
            shader_context.model.program["u_tex"].value = shader_context.model.texture_unit
        if self.next_handler:
            self.next_handler.handle(shader_context)

class CubeMapHandler(ShaderHandler):
    def handle(self, shader_context: ShaderContext):
        if getattr(shader_context.model, "cube_map_faces", None) is not None and "u_cubemap" in shader_context.model.program:
            shader_context.model.cube_map = CubeMapTexture(shader_context.ctx, shader_context.model.cube_map_faces)
            shader_context.model.cube_map.use(unit=shader_context.model.cube_map_unit)
            shader_context.model.program["u_cubemap"].value = shader_context.model.cube_map_unit
        if self.next_handler:
            self.next_handler.handle(shader_context)

class MaterialUniformHandler(ShaderHandler):
    def handle(self, shader_context: ShaderContext):
        if getattr(shader_context.model, "material", None) is not None:
            for key, value in shader_context.model.material.uniforms.items():
                if key not in shader_context.model.program:
                    continue
                if isinstance(value, tuple) and len(value) == 3:
                    shader_context.model.program[key].value = tuple(float(v) for v in value)
                else:
                    shader_context.model.program[key].value = float(value)
        if self.next_handler:
            self.next_handler.handle(shader_context)

class UVWeightHandler(ShaderHandler):
    def handle(self, shader_context: ShaderContext):
        if "u_uv_weight" in shader_context.model.program and (
            getattr(shader_context.model, "material", None) is None
            or "u_uv_weight" not in shader_context.model.material.uniforms
        ):
            shader_context.model.program["u_uv_weight"].value = 0.0
        if self.next_handler:
            self.next_handler.handle(shader_context)

class RenderHandler(ShaderHandler):
    def handle(self, shader_context: ShaderContext):
        mode_name = str(getattr(shader_context.model, "render_mode", "triangles")).lower()
        mode = moderngl.LINES if mode_name == "lines" else moderngl.TRIANGLES
        shader_context.model.vao.render(mode)