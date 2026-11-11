from __future__ import annotations

from pathlib import Path

import moderngl
from PIL import Image


class TextureBuffer(Texture):
	def __init__(self, ctx: moderngl.Context, width: int, height: int) -> None:
		# super().__init__(ctx, resource_path="")
		self.width = width
		self.height = height
		self.data: moderngl.Texture | None = None

class CubeMapTexture:
	FACE_ORDER = (
		"right",
		"left",
		"top",
		"bottom",
		"front",
		"back",
	)

	def __init__(
		self,
		ctx: moderngl.Context,
		face_paths: dict[str, str],
		flip_y: bool = False,
	) -> None:
		self.ctx = ctx
		self.face_paths = face_paths
		self.flip_y = flip_y
		self.texture: moderngl.TextureCube | None = None

	def load(self) -> moderngl.TextureCube:
		images: list[Image.Image] = []
		size: tuple[int, int] | None = None

		for face_name in self.FACE_ORDER:
			if face_name not in self.face_paths:
				raise ValueError(f"Missing cubemap face: {face_name}")
			image = Image.open(Path(self.face_paths[face_name])).convert("RGBA")
			if self.flip_y:
				image = image.transpose(Image.FLIP_TOP_BOTTOM)
			if size is None:
				size = image.size
			elif image.size != size:
				raise ValueError("All cubemap faces must have the same size")
			images.append(image)

		assert size is not None
		texture = self.ctx.texture_cube(size, 4)
		for face_index, image in enumerate(images):
			texture.write(face=face_index, data=image.tobytes())

		texture.filter = (moderngl.LINEAR, moderngl.LINEAR)
		texture.repeat_x = False
		texture.repeat_y = False
		self.texture = texture
		return texture

	def use(self, unit: int = 0) -> None:
		if self.texture is None:
			self.load()
		assert self.texture is not None
		self.texture.use(location=unit)
