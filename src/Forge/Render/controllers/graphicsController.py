class GraphicContext:
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.background_color = "#FFFFFF"

    def set_background(self, color:str):
        self.background_color = color

class GraphicContext2D(GraphicContext):
    def __init__(self, width:int, height:int):
        self.context_type = "2D"
        super().__init__(width, height)




import moderngl
from Forge.Definitions.materials.inputBuffers import InputBuffer
from Forge.Definitions.materials.targets.frameBuffer import OutputBuffer
from Forge.Definitions.materials.shaders.program import Program

class GraphicsContext3D:
    def __init__(self):
        self.ctx = moderngl.create_context(standalone=True)
        self.program = None


    def set_program(self, program: Program):
        self.program = program

    def build_program(self, vertex_str: str, frag_str: str) -> Program:
        program = Program(self.ctx, vertex_str, frag_str)
        self.program = program
        return program
        
    def load_program(self, vertex_path:str, frag_path:str) -> Program:
        program = Program.from_files(self.ctx, vertex_path, frag_path)
        self.program = program
        return program

    def create_input_buffer(self, vertices, attributes) -> InputBuffer:
        if self.program is None:
            raise ValueError("Program not set")
        ib = InputBuffer(self.ctx)
        ib.vertices = vertices
        ib.attributes = attributes
        ib.set_program(self.program)
        return ib

    def render(self, width, height, input_buffer: InputBuffer, clear: bool = False):
        return OutputBuffer(self.ctx, width, height).render_image(input_buffer, clear=clear)



