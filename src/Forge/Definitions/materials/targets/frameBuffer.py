
import moderngl
from Forge.Definitions.materials.inputBuffers import InputBuffer
from PIL import Image

class OutputBuffer:
    def __init__(self, ctx: moderngl.Context, width: int, height: int):
        self.ctx = ctx
        self.width = width
        self.height = height
        self.clear_color = (0.0, 0.0, 0.0, 1.0)

    def get_fbo(self):
        fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture((512, 512), 3)]
        )
        fbo.use()
        return fbo
    
    def get_clear_fbo(self):
        fbo = self.get_fbo()
        fbo.clear(*self.clear_color)
        return fbo

    def render_image(self, input_buffer: InputBuffer, clear:bool = False):
        fbo = self.get_fbo() if not clear else self.get_clear_fbo()
        input_buffer.render()
        return Image.frombytes(
            "RGB", fbo.size, fbo.color_attachments[0].read(),
            "raw", "RGB", 0, -1
        )