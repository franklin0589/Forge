#version 330

struct PointLight {
    vec3 position;
    vec3 color;
    float ambient_strength;
    float diffuse_strength;
    float specular_strength;
    float shininess;
};

in vec3 v_color;
in vec3 v_normal;
in vec3 v_frag_pos;
in vec2 v_uv;

out vec4 fragColor;

uniform sampler2D u_tex;
uniform PointLight u_light;
uniform vec3 u_view_pos;

void main() {
    vec3 normal = normalize(v_normal);
    vec3 light_dir = normalize(u_light.position - v_frag_pos);
    vec3 view_dir = normalize(u_view_pos - v_frag_pos);
    vec3 half_dir = normalize(light_dir + view_dir);

    float diff = max(dot(normal, light_dir), 0.0);
    float spec = pow(max(dot(normal, half_dir), 0.0), u_light.shininess);

    vec3 ambient = u_light.ambient_strength * u_light.color;
    vec3 diffuse = u_light.diffuse_strength * diff * u_light.color;
    vec3 specular = u_light.specular_strength * spec * u_light.color;

    vec3 lit = ambient + diffuse + specular;
    vec4 texel = texture(u_tex, v_uv);
    vec3 albedo = texel.rgb * v_color;

    fragColor = vec4(albedo * lit, texel.a);
}
