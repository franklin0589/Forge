import moderngl
from Forge.Definitions.Camera import Camera
from Forge.Render.renderer import ShaderWrapper
from PIL import Image

from Forge.Render.object.model import Model
from Forge.geometry.color import Color

class RenderFrameBuffer:
    def __init__(self, ctx: moderngl.Context, width: int, height: int) -> None:
        self.fbo = ctx.simple_framebuffer((width, height), components=4)
        
    def select(self):
        self.fbo.use()

    def clear(self, color: Color = Color(0.10, 0.12, 0.16, 1.0), depth: float = 1.0):
        """Clear the framebuffer with the specified color and depth."""
        self.fbo.clear(color.r, color.g, color.b, color.a, depth=depth)

    def read_pixels(self):
        """Read the pixels from the framebuffer."""
        raw = self.fbo.read(components=4, alignment=1)
        return raw





class RenderContext:
    def __init__(self, width: int, height: int, camera: Camera ) -> None:
        self.width = width
        self.height = height
        self.ctx = moderngl.create_standalone_context(require=330)
        self.fbo = RenderFrameBuffer(self.ctx, width, height)
        self.fbo.select()
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.fbo.clear()
        self.camera = camera

    def render_model(
        self,
        model: Model,
        vertex_shader_path: str | None,
        fragment_shader_path: str | None,
        lights=None,
        vertex_shader_source: str | None = None,
        fragment_shader_source: str | None = None,
    ) -> None:
        strategy = model.resolve_render_strategy()
        shader_script = strategy.shader_script(model)
        if shader_script is not None:
            vertex_shader_source = shader_script.vertex_source
            fragment_shader_source = shader_script.fragment_source
            if model.vertex_shader_path is None:
                vertex_shader_path = None
            if model.fragment_shader_path is None:
                fragment_shader_path = None

        prog = ShaderWrapper(
            self.ctx,
            vertex_path=vertex_shader_path,
            fragment_path=fragment_shader_path,
            vertex_source=vertex_shader_source,
            fragment_source=fragment_shader_source,
        )
        mvp = self.camera.get_mvp(model.point, self.width, self.height)

        if "u_mvp" in prog.program:
            prog.run("u_mvp", mvp)
        if "u_model" in prog.program:
            prog.run("u_model", model.point)

        strategy.upload(prog.program, model, lights=lights, view_pos=self.camera.position)

        if strategy.depth_test and getattr(model, "depth_test", True):
            self.ctx.enable(moderngl.DEPTH_TEST)
        else:
            self.ctx.disable(moderngl.DEPTH_TEST)

        prog.render(model, vertex_format=model.vertex_format, attributes=model.attributes)

        # Restore depth test for subsequent objects.
        self.ctx.enable(moderngl.DEPTH_TEST)

    def render(
        self,
        model: Model,
        vertex_shader_path: str | None,
        fragment_shader_path: str | None,
        lights=None,
        vertex_shader_source: str | None = None,
        fragment_shader_source: str | None = None,
    ) -> None:
        self.render_model(
            model,
            vertex_shader_path=vertex_shader_path,
            fragment_shader_path=fragment_shader_path,
            lights=lights,
            vertex_shader_source=vertex_shader_source,
            fragment_shader_source=fragment_shader_source,
        )

    def save_image(self, output_path: str = "output.png") -> None:
        raw = self.fbo.read_pixels()
        image = Image.frombytes("RGBA", (self.width, self.height), raw).transpose(Image.FLIP_TOP_BOTTOM)
        image.save(output_path)
        print(f"Saved: {output_path}")

    def get_buffer_image(self):
        raw = self.fbo.read_pixels()
        image = Image.frombytes("RGBA", (self.width, self.height), raw).transpose(Image.FLIP_TOP_BOTTOM)
        return image


Context = RenderContext


