from __future__ import annotations
from Forge.context import RenderContext


from abc import ABC, abstractmethod

from typing import Protocol


from Forge.Render.object.object_manager import ObjectManager
from Forge.Definitions.Camera import Camera
from Forge.Lights.skybox import Skybox


class PScene(Protocol):
	context: RenderContext
	object_manager: ObjectManager

	def setup(self) -> None:
		...

	def update(self) -> None:
		...


class Scene(ABC):
	def __init__(
		self:PScene,
		width: int,
		height: int,
		cam: Camera,
		vertex_shader_path: str,
		fragment_shader_path: str,
	) -> None:
		self.context = RenderContext(width=width, height=height, camera=cam)
		self.vertex_shader_path = vertex_shader_path
		self.fragment_shader_path = fragment_shader_path
    
		self.object_manager = ObjectManager()
		self.skybox: Skybox | None = None
 
		self._lights: list = []
		self.model_vertex_shaders:dict[int, str] = {}
		self.model_frag_shaders:dict[int, str] = {}
		self.scene_time = 0
		self.setup()




	def update_scene_time(self) -> None:
		self.scene_time += 1

	@abstractmethod
	def setup(self) -> None:
		"""Override this method to build the scene."""
		pass

	@abstractmethod
	def update(self) -> None:
		...

	def set_skybox(self, skybox: Skybox) -> None:
		self.skybox = skybox
		
	def render(self) -> None:
		self.context.fbo.clear()
		active_lights = self.object_manager.get_lights()
		if not active_lights:
			active_lights = self._lights

		if self.skybox is not None:
			self.skybox.sync_to_camera(aspect=self.context.width / self.context.height)
			self.context.render(
				self.skybox.model,
				vertex_shader_path=self.skybox.model.vertex_shader_path,
				fragment_shader_path=self.skybox.model.fragment_shader_path,
				vertex_shader_source=self.skybox.model.vertex_shader_source,
				fragment_shader_source=self.skybox.model.fragment_shader_source,
			)

		for object, vertex_shader_path, fragment_shader_path in self.object_manager.get_objects():
			self.context.render(
				object.model,
				vertex_shader_path=vertex_shader_path,
				fragment_shader_path=fragment_shader_path,
				lights=active_lights,
				vertex_shader_source=object.model.vertex_shader_source,
				fragment_shader_source=object.model.fragment_shader_source,
			)

	def render_image(self, output_path: str = "output.png") -> None:
		self.render()
		self.context.save_image(output_path=output_path)

	def render_gif(self, output_path: str = "output.gif", duration: int = 100, loop: int = 0) -> None:
		buffers = []
		for i in range(duration):
			
			self.update_scene_time()
			self.update()
			self.render()

			buffer_image = self.context.get_buffer_image()
			buffers.append(buffer_image)
		buffers[0].save(
			output_path,
			save_all=True,
			append_images=buffers[1:],
			duration=duration,
			loop=loop,
		)
		