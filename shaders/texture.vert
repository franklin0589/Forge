#version 330
in vec3 in_pos;
in vec3 in_color;
in vec2 in_uv;
out vec3 v_color;
out vec2 v_uv;
uniform mat4 u_mvp;

void main() {
    v_color = in_color;
    v_uv = in_uv;
    gl_Position = u_mvp * vec4(in_pos, 1.0);
}
