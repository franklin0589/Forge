
import moderngl
import numpy as np
from Forge.Definitions.materials.shaders.program import Program

class InputBuffer:
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx
        self.vbo: moderngl.Buffer | None = None
        self._attributes: list[str] = []
        self.state = 0

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attributes: list[str]):
        self._attributes = attributes

    def append_attribute(self, attribute: str):
        self._attributes.append(attribute)

    @property
    def vertices(self):
        return self.vbo

    @vertices.setter
    def vertices(self, vertices: np.ndarray):
        self.vbo = self.ctx.buffer(vertices.tobytes())

    def set_program(self, program: Program):
        self.program = program

    def __get_vao(self):
        if not hasattr(self, 'program'):
            raise ValueError("Program not set")
        if self.vbo is None:
            raise ValueError("Vertex buffer not set")
        return self.ctx.vertex_array(self.program.get(), self.vbo, *self.attributes)

    def render(self):
        vao = self.__get_vao()
        vao.render()