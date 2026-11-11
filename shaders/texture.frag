#version 330
in vec3 v_color;
in vec2 v_uv;
out vec4 fragColor;
uniform sampler2D u_tex;

void main() {
    vec4 texel = texture(u_tex, v_uv);
    fragColor = vec4(v_color, 1.0) * texel;
}
