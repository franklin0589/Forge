

from Forge.Render.object.object import Object
from typing import Generator, Tuple

class ObjectManager:
    def __init__(self):
        self._objects: dict[int, Object] = {}
        self._lights: list = []
        self.model_vertex_shaders:dict[int, str] = {}
        self.model_frag_shaders:dict[int, str] = {}
    

    def add(self, object: Object) -> None:
        if object.model.vertex_shader_path is not None:
            self.model_vertex_shaders[len(self._objects)] = object.model.vertex_shader_path
        if object.model.fragment_shader_path is not None:
            self.model_frag_shaders[len(self._objects)] = object.model.fragment_shader_path
        self._objects[len(self._objects)] = object

    def add_light(self, light) -> None:
        self._lights.append(light)

    def get_lights(self) -> list:
        return self._lights

    def get_objects(self) -> Generator[Tuple[Object, str, str], None, None]:
        for ind, object in self._objects.items():
            vertex_shader_path = self.model_vertex_shaders.get(ind, None)
            fragment_shader_path = self.model_frag_shaders.get(ind, None)
            yield object, vertex_shader_path, fragment_shader_path
        
    def clear(self) -> None:
        self._objects.clear()
        self._lights.clear()
        self.model_vertex_shaders.clear()
        self.model_frag_shaders.clear()
