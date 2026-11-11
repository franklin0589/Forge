from __future__ import annotations
import moderngl 
from pathlib import Path

from Forge.Definitions import Image

from Forge.shared.logs import RenderLogs

class Texture:
	@staticmethod
	def get_texture_load(ctx, resource_path:str, flip_y: bool = True, repeat: bool = True) -> Texture:
		img = Image.from_file(str(resource_path), flip_y=flip_y)
		tex = Texture(ctx.texture(img.data.size, 4, img.data.tobytes()))
		if repeat:
			tex.set_repeat(repeat_x=True, repeat_y=True)
			tex.build_mipmaps()
		return tex

	def __init__(self, texture: moderngl.Texture) -> None:
		self.data: moderngl.Texture = texture
		RenderLogs().logger().info(f"Texture created with size: {texture.size}")

	def set_filter(self, min_filter: int, mag_filter: int) -> None:
		RenderLogs().logger().info(f"Setting texture filter: min_filter={min_filter}, mag_filter={mag_filter}")
		self.data.filter = (min_filter, mag_filter)

	def set_repeat(self, repeat_x: bool, repeat_y: bool) -> None:
		RenderLogs().logger().info(f"Setting texture repeat: repeat_x={repeat_x}, repeat_y={repeat_y}")
		self.data.repeat_x = repeat_x
		self.data.repeat_y = repeat_y

	def build_mipmaps(self) -> None:
		RenderLogs().logger().info("Building mipmaps for texture")
		self.data.build_mipmaps()

	def use(self, unit: int = 0) -> None:
		RenderLogs().logger().info(f"Using texture on unit {unit}")
		self.data.use(location=unit)
