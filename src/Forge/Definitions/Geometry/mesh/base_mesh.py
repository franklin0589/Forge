# from abc import ABC, abstractmethod
# from Forge.shared.protocols import *
# import numpy as np
# from Forge.shared.buffer import Buffer
# from Forge.shared.logs import RenderLogs

import numpy as np

class VertexAttribute:
    def __init__(self, name: str, data: np.ndarray):
        self.name = name
        self.data = data

class ColorAttribute(VertexAttribute):
    def __init__(self, data: np.ndarray):
        super().__init__("color", data)

class PositionAttribute(VertexAttribute):
    def __init__(self, data: np.ndarray):
        super().__init__("position", data)

import numpy as np

from enum import IntEnum, auto

class triEnum(IntEnum):
    one = auto()
    two = auto()
    three = auto()

class Triangle:
    def __init__(self):
        self.data = {}

    def get_attribute_number(self, index:triEnum):
        t = 32*index
        while t in self.data:
            t += 1
        return t

    def attribute_bounds(self, i:int):
        t = 32*i
        s = 32*(i+1)
        return (t, s)

    def add_attribute(self, index:triEnum, vertex_attribute: VertexAttribute):
        attribute_index = self.get_attribute_number(index)
        self.data[attribute_index] = vertex_attribute

    def get_attributes(self, index:triEnum):
        for i in range(*self.attribute_bounds):
            if i in self.data:
                yield self.data[i]
            else:
                continue


class Mesh:
    def __init__(self) -> None:    
        self.triBuffer:list[Triangle] = []
        self.indBuffer:list[int] = []

    def form(self):
        """Override this method to define the mesh structure."""
        pass

    def add_index(self, index: int) -> None:
        self.indBuffer += [index]

    def fill_triangle(self, indexA, indexB, indexC):
        self.indBuffer += [indexA,indexB,indexC]

        
    def add_triangle(self, ver_per_attribute:list[list[VertexAttribute]], constant_attributes:list[VertexAttribute]) -> list[int]:
        triangle = Triangle()
        indices = []
    
        for i in triEnum:
            vertex_index = len(self.triBuffer) * 3 + i
            attributes = ver_per_attribute[i]+constant_attributes
            for attr in attributes:
                triangle.add_attribute(i, attr)
            indices += [vertex_index]
        self.triBuffer += [triangle]
        self.fill_triangle(*indices)
        return indices

    

    def add_quad_index(self, ver_per_attribute:list[list[VertexAttribute]], constant_attributes:list[VertexAttribute]):
        try:
            RenderLogs().logger.info(f"Mesh : Add Quad: Adding quad indices {index0}, {index1}, {index2}, {index3}")
            self.add_triangle(index0, index1, index2)
            self.add_triangle(index0, index2, index3)
            if data is not None:
                for idx in [index0, index1, index2, index3]:
                    self.attach_data_to_vertex(idx, data)
            RenderLogs().logger.info(f"Mesh : Add Quad: Successfully added quad indices {index0}, {index1}, {index2}, {index3}")
        except Exception as e:
            RenderLogs().logger.error(f"Mesh : Add Quad: Failed to add quadrilateral indices: {e}")
            return Failure(f"Failed to add quadrilateral indices: {e}")

    # def attach_data_to_vertex_index(self, vertex_index: int, data: iBuffer) -> Result[bool, str]:
    #     if self.vertices.in_buffer(vertex_index):
    #         RenderLogs().logger.error(f"Mesh : Attach Data: Vertex index {vertex_index} exceeds the number of vertices.")
    #         return Failure(f"Vertex index {vertex_index} exceeds the number of vertices.")

    #     self.vertices.attach_data_to_index(vertex_index, data)
    #     return Success(True)

    # def attach_vertex_data(self, data: iBuffer):
    #     if not self.vertices.is_same_length(data):
    #         RenderLogs().logger.error("Mesh : Attach Data: Data length must match the number of vertices.")
    #         return Failure("Data length must match the number of vertices.")
    #     self.vertices.attach_data(data)

    # def attach_data_per_vertex_section(self, data: iBuffer, start: int, end: int):
    #     if self.vertices.in_buffer(start) or self.vertices.in_buffer(end):
    #         RenderLogs().logger.error("Mesh : Attach Data: End index exceeds the number of vertices.")
    #         return Failure("End index exceeds the number of vertices.")
    #     RenderLogs().logger.info(f"Mesh : Attach Data: Attaching data to vertices from index {start} to {end}")
    #     self.vertices.attach_data_per_section(data, start, end)
        
    # def attach_color(self, color: iColor):
        RenderLogs().logger.info(f"Mesh : Attach Color: Attaching color {color} to all vertices") 
        color_array = Buffer.make_copy_repeating([color.r, color.g, color.b], self.vertices)
        self.attach_per_vertex_data(color_array)

    def attach_uv(self, uv:iVector2):
        RenderLogs().logger.info(f"Mesh : Attach UV: Attaching UV coordinates {uv} to all vertices")
        uv_coords= [[0, 0], [uv.x, 0], [uv.x, uv.y], [0, uv.y]]
        uv_buffer = Buffer.make(uv_coords)
        self.attach_per_vertex_data(uv_buffer)


