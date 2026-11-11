from Forge.Render.base_shader import Shader

class CustomFragmentShader(Shader):
    def __init__(self, source_path: str):
        super().__init__()
        self.custom_block_id = self.add_custom_block(source_path)

    def build(self) -> str:
        self.compile(self.custom_block_id)
        return self.render()

class SimpleFragmentShader(Shader):
    def __init__(self):
        super().__init__()
        self.header_id = self.add_block()  # Header
        self.input_id = self.add_block()  # Inputs
        self.uniform_id = self.add_block()  # Uniforms
        self.output_id = self.add_block()  # Outputs
        self.main_id = self.add_block()  # Main function body

    def fill_common_block(self):
        self.append_to_block(self.header_id, "#version 330")
        self.extend_block(
            self.input_id,
            [
                "in vec3 v_color;",
                "in vec3 v_frag_pos;",
            ],
        )
        self.append_to_block(self.output_id, "out vec4 fragColor;")
        self.append_to_block(self.main_id, "fragColor = vec4(v_color, 1.0);")
    
    def build(self) -> str:
        self.compile(self.header_id)
        self.compile(self.input_id)
        self.compile(self.uniform_id)
        self.compile(self.output_id)
        self.add_line("void main() {")
        self.compile(self.main_id)
        self.add_line("}")
        return self.render()

class TextureFragmentShader(Shader):
    def __init__(self):
        super().__init__()
        self.header_id = self.add_block()  # Header
        self.input_id = self.add_block()  # Inputs
        self.uniform_id = self.add_block()  # Uniforms
        self.output_id = self.add_block()  # Outputs
        self.main_id = self.add_block()  # Main function body
    
    def fill_common_block(self):
        self.append_to_block(self.header_id, "#version 330")
        self.extend_block(
            self.input_id,
            [
                "in vec3 v_color;",
                "in vec3 v_frag_pos;",
                "in vec2 v_uv;",
            ],
        )
        self.append_to_block(self.uniform_id, "uniform sampler2D u_tex;")
        self.append_to_block(self.output_id, "out vec4 fragColor;")
        self.append_to_block(
            self.main_id, "fragColor = texture(u_tex, v_uv) * vec4(v_color, 1.0);"
        )
    
    def build(self) -> str:
        self.compile(self.header_id)
        self.compile(self.input_id)
        self.compile(self.uniform_id)
        self.compile(self.output_id)
        self.add_line("void main() {")
        self.compile(self.main_id)
        self.add_line("}")
        return self.render()
    

class FragmentShader(Shader):
    def __init__(self):
        super().__init__()
        self.header_id = self.add_block()  # Header
        self.input_id = self.add_block()  # Inputs
        self.uniform_id = self.add_block()  # Uniforms
        self.output_id = self.add_block()  # Outputs
        self.main_id = self.add_block()  # Main function body

    def fill_common_block(self):
        self.append_to_block(self.header_id, "#version 330")
        self.extend_block(
            self.input_id,
            [
                "in vec3 v_color;",
                "in vec3 v_frag_pos;",
            ],
        )
        self.append_to_block(self.output_id, "out vec4 fragColor;")

    def fill_normal_block(self, has_lighting: bool):
        self.append_to_block(self.input_id, "in vec3 v_normal;")
        if has_lighting:
            self.extend_block(
                self.uniform_id,
                [
                    "struct PointLight {",
                    "    vec3 position;",
                    "    vec3 color;",
                    "    float ambient_strength;",
                    "    float diffuse_strength;",
                    "    float specular_strength;",
                    "    float shininess;",
                    "};",
                    "uniform PointLight u_light;",
                    "uniform vec3 u_view_pos;",
                ],
            )
            self.extend_block(
                self.main_id,
                [
                    "vec3 normal = normalize(v_normal);",
                    "vec3 light_dir = normalize(u_light.position - v_frag_pos);",
                    "vec3 view_dir = normalize(u_view_pos - v_frag_pos);",
                    "vec3 half_dir = normalize(light_dir + view_dir);",
                    "float diff = max(dot(normal, light_dir), 0.0);",
                    "float spec = pow(max(dot(normal, half_dir), 0.0), u_light.shininess);",
                    "vec3 ambient = u_light.ambient_strength * u_light.color;",
                    "vec3 diffuse = u_light.diffuse_strength * diff * u_light.color;",
                    "vec3 specular = u_light.specular_strength * spec * u_light.color;",
                    "vec3 lit = ambient + diffuse + specular;",
                ],
            )

    def fill_uv_block(self, has_texture: bool, has_lighting: bool):
        self.append_to_block(self.input_id, "in vec2 v_uv;")
        if has_texture:
            self.append_to_block(self.uniform_id, "uniform sampler2D u_tex;")
        if not has_texture:
            self.append_to_block(self.uniform_id, "uniform float u_uv_weight;")
        if has_texture:
            self.append_to_block(
                self.main_id, "vec3 albedo = texture(u_tex, v_uv).rgb * v_color;"
            )
        else:
            self.extend_block(
                self.main_id,
                [
                    "vec3 albedo = v_color;",
                    "albedo += vec3(v_uv, 0.0) * u_uv_weight;",
                ],
            )
        if has_lighting:
            self.append_to_block(self.main_id, "fragColor = vec4(albedo * lit, 1.0);")
        else:
            self.append_to_block(self.main_id, "fragColor = vec4(albedo, 1.0);")

    def fill_blocks(
        self, has_normal: bool, has_uv: bool, has_texture: bool, has_lighting: bool
    ) -> None:
        self.fill_common_block()
        if has_normal:
            self.fill_normal_block(has_lighting)
        if has_uv:
            self.fill_uv_block(has_texture, has_lighting)

    def build(self) -> str:
        self.compile(self.header_id)
        self.compile(self.input_id)
        self.compile(self.uniform_id)
        self.compile(self.output_id)
        self.add_line("void main() {")
        self.compile(self.main_id)
        self.add_line("}")
        return self.render()
