from __future__ import annotations

from dataclasses import dataclass, field
from Forge.Render.program import ShaderScript, ShaderScriptBuilder


@dataclass
class Material:
	# Optional fixed shader paths override dynamic shader generation.
	texture_path: str | None = None
	vertex_shader_path: str | None = None
	fragment_shader_path: str | None = None
	use_texture: bool = False
	use_lighting: bool = False
	uniforms: dict[str, float | tuple[float, float, float]] = field(default_factory=dict)

	def build_shader_script(self, attributes: list[str]) -> ShaderScript | None:
		# Use file-based shaders when explicitly provided.
		if self.vertex_shader_path or self.fragment_shader_path:
			return None
		has_normal = "in_normal" in attributes
		has_uv = "in_uv" in attributes
		has_skin = "in_bone_ids" in attributes and "in_bone_weights" in attributes
		return ShaderScriptBuilder.build_with_skin(
			has_normal=has_normal,
			has_uv=has_uv,
			use_texture=self.use_texture,
			use_lighting=self.use_lighting,
			has_skin=has_skin,
		)
