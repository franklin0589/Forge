import moderngl

from Forge.Render.context import ShaderContext
from Forge.Render.program import ShaderProgram
from Forge.Render.handlers import *

    
class RenderPipeline:
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler: ShaderHandler):
        if self.handlers:
            self.handlers[-1].next_handler = handler
        self.handlers.append(handler)

    def execute(self, shader_context: ShaderContext):
        if self.handlers:
            self.handlers[0].handle(shader_context)


class ShaderRenderer:
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx
        self.render_pipeline = RenderPipeline()

    def build_context(self, program, shader_program: ShaderProgram, model, vertex_format: str, attributes: list[str]) -> ShaderContext:
        program = self.ctx.program(vertex_shader=shader_program.vertex_shader, fragment_shader=shader_program.fragment_shader)
        return ShaderContext(self.ctx, program, model, vertex_format, attributes)

    def build_pipeline(self):
        self.render_pipeline.add_handler(BufferGeneratorHandler())  
        self.render_pipeline.add_handler(IndicesHandler())
        self.render_pipeline.add_handler(TextureHandler())
        self.render_pipeline.add_handler(CubeMapHandler())
        self.render_pipeline.add_handler(MaterialUniformHandler())
        self.render_pipeline.add_handler(UVWeightHandler())
        self.render_pipeline.add_handler(RenderHandler())

    def render(self, shader_context: ShaderContext):
        self.render_pipeline.execute(shader_context)

