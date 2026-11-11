from Major.main import glApp
import numpy as np
import moderngl
import math

class Triangle:
    def __init__(self, ctx):
        self.ctx  = ctx
        self.prog = self.ctx.program(
        vertex_shader="""
            #version 330
            in vec2 in_vert;
            in vec3 in_color;
            out vec3 v_color;
            void main() {
                v_color = in_color;
                gl_Position = vec4(in_vert, 0.0, 1.0);
            }
        """,
        fragment_shader="""
            #version 330
            in vec3 v_color;
            out vec3 f_color;
            void main() {
                f_color = v_color;
            }
        """,
    )  
        self.x = 0
        self.y = 0


    def update(self):
        vertices = np.asarray(
            [
                # x,     y,     r, g, b
                -0.6+self.x, -0.6+self.y, 1.0, 0.0, 0.0,  # Vertex 1: Red
                0.6+self.x, -0.6+self.y, 0.0, 1.0, 0.0,  # Vertex 2: Green
                0.0+self.x, 0.6+self.y, 0.0, 0.0, 1.0,  # Vertex 3: Blue
            ],
            dtype="f4",
        )
        vbo = self.ctx.buffer(vertices)
        self.vao = self.ctx.vertex_array(self.prog, [(vbo, "2f 3f", "in_vert", "in_color")])

    def render(self):
        self.vao.render(moderngl.TRIANGLES)

class Test(glApp):
    def setup(self):
        self.triangle =Triangle(self.ctx)

    def update(self):
        self.triangle.x = math.sin(self.clk/self.MAX_CLOCK*self.TWO_PI)
        self.triangle.update()
        self.triangle.render()