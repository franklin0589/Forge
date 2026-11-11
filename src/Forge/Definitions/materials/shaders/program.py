
import moderngl

class Program:
    @classmethod
    def from_files(cls, ctx: moderngl.Context, vertex_path:str, frag_path:str):
        with open(vertex_path, 'r') as f:
            vertex_str = f.read()
        with open(frag_path, 'r') as f:
            frag_str = f.read()
        return cls(ctx,vertex_str, frag_str)

    def __init__(self, ctx: moderngl.Context, vertex_str:str, frag_str:str):
        self.ctx = ctx
        self.vetrex_shader = vertex_str
        self.frag_shader = frag_str
        self.program: moderngl.Program | None = None

    def get(self):
        if self.program is None:
            self.program = self.ctx.program(
                vertex_shader=self.vetrex_shader,
                fragment_shader=self.frag_shader
            )
        return self.program
