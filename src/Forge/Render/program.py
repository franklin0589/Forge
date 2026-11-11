from Forge.Render.frag_shader import FragmentShader
from Forge.Render.vertex_shader import VertexShader
from dataclasses import dataclass


@dataclass
class ShaderProgram:
    vertex_shader: str
    fragment_shader: str


# @dataclass
# class ShaderScript:
# 	# Pair of generated shader sources for one material configuration.
# 	vertex_source: str
# 	fragment_source: str


class ProgramBuilder:
	"""Build GLSL from feature-based ScriptBlocks.

	Each section is assembled from small blocks so the active features are
	easy to reason about and easy to extend.
	"""

	@staticmethod
	def build(has_normal: bool, has_uv: bool, use_texture: bool, use_lighting: bool) -> ShaderProgram:
		return ProgramBuilder.build_with_skin(
			has_normal=has_normal,
			has_uv=has_uv,
			use_texture=use_texture,
			use_lighting=use_lighting,
			has_skin=False,
		)

	@staticmethod
	def build_with_skin(
		has_normal: bool,
		has_uv: bool,
		use_texture: bool,
		use_lighting: bool,
		has_skin: bool,
	) -> ShaderProgram:
		# Vertex blocks.

		vertex_source = VertexShader(has_normal, has_uv, has_skin).build()
		fragment_source = FragmentShader(has_normal, has_uv, use_texture, use_lighting).build()
		
		return ShaderProgram(vertex_shader=vertex_source, fragment_shader=fragment_source)
