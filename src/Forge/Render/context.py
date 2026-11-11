
import moderngl


class ShaderContext:
    def __init__(self, ctx: moderngl.Context, program, model, vertex_format: str, attributes: list[str]):
        self.ctx = ctx
        self.program = program
        self.model = model
        self.vertex_format = vertex_format
        self.attributes = attributes
        self.vbo = None
        self.ibo = None

    def set_buffer(self, input_key, input_buffer: str):
        data = input_buffer.matrix.astype("f4")
        if data.ndim == 2 and data.shape == (4, 4):
            data = data.T
        self.program[input_key].write(data.tobytes())

    def set_vec3(self, input_key: str, value) -> None:
        if input_key in self.program:
            self.program[input_key].value = tuple(float(v) for v in value)

    def set_float(self, input_key: str, value: float) -> None:
        if input_key in self.program:
            self.program[input_key].value = float(value)