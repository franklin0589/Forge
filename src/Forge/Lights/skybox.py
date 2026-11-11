from __future__ import annotations

import numpy as np

from Forge.Definitions.Camera import Camera
from Forge.geometry.transform import Transform
from Forge.geometry.vector import Vector3
from Forge.Lights.materials import Material
from Forge.Render.object.model import Model
from Forge.Render.object.object import Object


class Skybox(Object):
	"""Screen-space background skybox driven by either a gradient or a cubemap."""

	VERTEX_SHADER_SOURCE = """
#version 330

in vec3 in_pos;

out vec2 v_ndc;

void main() {
	v_ndc = in_pos.xy;
	gl_Position = vec4(in_pos, 1.0);
}
"""

	FRAGMENT_SHADER_SOURCE = """
#version 330

	in vec2 v_ndc;

uniform vec3 u_ground_color;
uniform vec3 u_horizon_color;
uniform vec3 u_zenith_color;
uniform float u_blend_exponent;
uniform vec3 u_camera_forward;
uniform vec3 u_camera_right;
uniform vec3 u_camera_up;
uniform float u_aspect;
uniform float u_fov_y_deg;

out vec4 fragColor;

void main() {
	float tan_half_fov = tan(radians(u_fov_y_deg) * 0.5);
	vec3 ray = normalize(
		u_camera_forward
		+ (v_ndc.x * u_aspect * tan_half_fov) * u_camera_right
		+ (v_ndc.y * tan_half_fov) * u_camera_up
	);
	float sky_mix = clamp(ray.y * 0.5 + 0.5, 0.0, 1.0);
	vec3 sky_color = mix(
		u_horizon_color,
		u_zenith_color,
		pow(sky_mix, u_blend_exponent)
	);
	float horizon = smoothstep(-0.12, 0.10, ray.y);
	vec3 color = mix(u_ground_color, sky_color, horizon);
	fragColor = vec4(color, 1.0);
}
"""

	CUBEMAP_FRAGMENT_SHADER_SOURCE = """
#version 330

in vec2 v_ndc;

uniform samplerCube u_cubemap;
uniform vec3 u_camera_forward;
uniform vec3 u_camera_right;
uniform vec3 u_camera_up;
uniform float u_aspect;
uniform float u_fov_y_deg;

out vec4 fragColor;

void main() {
	float tan_half_fov = tan(radians(u_fov_y_deg) * 0.5);
	vec3 ray = normalize(
		u_camera_forward
		+ (v_ndc.x * u_aspect * tan_half_fov) * u_camera_right
		+ (v_ndc.y * tan_half_fov) * u_camera_up
	);
	fragColor = texture(u_cubemap, ray);
}
"""

	def __init__(
		self,
		camera: Camera,
		radius: float = 40.0,
		horizon_color: tuple[float, float, float] = (0.72, 0.83, 0.97),
		zenith_color: tuple[float, float, float] = (0.10, 0.22, 0.46),
		ground_color: tuple[float, float, float] = (0.06, 0.08, 0.12),
		blend_exponent: float = 1.35,
		cube_map_faces: dict[str, str] | None = None,
	) -> None:
		super().__init__(transform=Transform())
		self.camera = camera
		self.radius = radius
		self.cube_map_faces = cube_map_faces
		self._vertices = np.array(
			[
				-1.0, -1.0, 0.0,
				1.0, -1.0, 0.0,
				1.0, 1.0, 0.0,
				-1.0, 1.0, 0.0,
			],
			dtype=np.float32,
		)
		self._indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)
		self.material = Material(
			use_texture=False,
			use_lighting=False,
			uniforms={
				"u_ground_color": ground_color,
				"u_horizon_color": horizon_color,
				"u_zenith_color": zenith_color,
				"u_blend_exponent": blend_exponent,
				"u_camera_forward": (0.0, 0.0, -1.0),
				"u_camera_right": (1.0, 0.0, 0.0),
				"u_camera_up": (0.0, 1.0, 0.0),
				"u_aspect": 1.0,
				"u_fov_y_deg": self.camera.fov_y_deg,
			},
		)
		self.sync_to_camera()
		self.build()

	def sync_to_camera(self, aspect: float = 1.0) -> None:
		self.set_position(self.camera.position)
		self._update_camera_uniforms(aspect=aspect)

	def _update_camera_uniforms(self, aspect: float) -> None:
		position = self.camera.position.as_numpy()
		target = self.camera.target.as_numpy()
		up = self.camera.up.as_numpy()

		forward = target - position
		forward_norm = np.linalg.norm(forward)
		if forward_norm == 0.0:
			forward = np.array([0.0, 0.0, -1.0], dtype=np.float32)
		else:
			forward = forward / forward_norm

		right = np.cross(forward, up)
		right_norm = np.linalg.norm(right)
		if right_norm == 0.0:
			right = np.array([1.0, 0.0, 0.0], dtype=np.float32)
		else:
			right = right / right_norm

		camera_up = np.cross(right, forward)
		camera_up_norm = np.linalg.norm(camera_up)
		if camera_up_norm == 0.0:
			camera_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
		else:
			camera_up = camera_up / camera_up_norm

		self.material.uniforms.update({
			"u_camera_forward": tuple(float(v) for v in forward),
			"u_camera_right": tuple(float(v) for v in right),
			"u_camera_up": tuple(float(v) for v in camera_up),
			"u_aspect": float(aspect),
			"u_fov_y_deg": float(self.camera.fov_y_deg),
		})

	def set_position(self, position: Vector3) -> None:
		transform = Transform()
		transform.translate(position.x, position.y, position.z)
		self.transform = transform
		if hasattr(self, "model"):
			self.model.point = self.transform

	def build(self) -> Model:
		self.model = Model(
			vertices=self._vertices,
			indices=self._indices,
			texture_path=None,
			cube_map_faces=self.cube_map_faces,
			vertex_format="3f",
			attributes=["in_pos"],
			point=self.transform,
			vertex_shader_source=self.VERTEX_SHADER_SOURCE,
			fragment_shader_source=(
				self.CUBEMAP_FRAGMENT_SHADER_SOURCE
				if self.cube_map_faces is not None
				else self.FRAGMENT_SHADER_SOURCE
			),
			material=self.material,
			depth_test=False,
		)
		return self.model

