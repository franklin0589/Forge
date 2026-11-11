#version 330
in vec3 in_pos;
in vec3 in_color;
in vec3 in_normal;
in vec2 in_uv;

out vec3 v_color;
out vec3 v_normal;
out vec3 v_frag_pos;
out vec2 v_uv;

uniform mat4 u_mvp;
uniform mat4 u_model;

void main() {
    vec4 world_pos = u_model * vec4(in_pos, 1.0);
    v_frag_pos = world_pos.xyz;

    mat3 normal_matrix = mat3(transpose(inverse(u_model)));
    v_normal = normalize(normal_matrix * in_normal);

    v_color = in_color;
    v_uv = in_uv;
    gl_Position = u_mvp * vec4(in_pos, 1.0);
}
