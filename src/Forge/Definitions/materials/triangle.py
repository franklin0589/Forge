import moderngl
import numpy as np


vert_str = """
        #version 330

        in vec2 in_vert;
        in vec3 in_color;

        out vec3 v_color;

        void main() {
            v_color = in_color;
            gl_Position = vec4(in_vert, 0.0, 1.0);
        }
    """
frag_str = """
        #version 330

        in vec3 v_color;

        out vec3 f_color;

        void main() {
            f_color = v_color;
        }
    """


ctx3d = Context3D()
ctx3d.build_program(vert_str, frag_str)

attributes = ["in_vert", "in_color"]
vertices = np.asarray([
    -0.75, -0.75,  1, 0, 0,
    0.75, -0.75,  0, 1, 0,
    0.0, 0.649,  0, 0, 1
], dtype='f4')
input_buffer = ctx3d.create_input_buffer(vertices, attributes)

ctx3d.render(512, 512, input_buffer, clear=True).show()