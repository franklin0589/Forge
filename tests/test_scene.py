import unittest
import Forge as f
from pathlib import Path
from PIL import Image


# class DemoScene(f.Scene):
#     def __init__(self, width: int = 1280, height: int = 720):
#         base_dir = Path(__file__).resolve().parent
#         shader_dir = base_dir / "shaders"
#         position = f.Vector3(x=0.0, y=0.0, z=3.0)
#         target = f.Vector3(x=0.0, y=0.0, z=0.0)
#         up = f.Vector3(x=0.0, y=1.0, z=0.0)
#         cam = f.Camera(position=position, target=target, up=up)

#         super().__init__(
#             width=width,
#             height=height,
#             cam=cam,
#             vertex_shader_path=str(shader_dir / "lit_texture.vert"),
#             fragment_shader_path=str(shader_dir / "lit_texture.frag"),
#         )

#     def setup(self) -> None:
#         t = f.Transform()
#         t.translate(0.0, -1, -3.0)
#         self.cube_transform = t

#         cube_mesh = f.form.TexturedCubeMesh(size=1.0)

#         cube = f.RenderableObject(
#             mesh=cube_mesh,
#             transform=self.cube_transform,
#             material=f.Material(
#                 vertex_shader_path=self.vertex_shader_path,
#                 fragment_shader_path=self.fragment_shader_path,
#                 texture_path=str(Path(__file__).resolve().parent / "textures" / "box.jpg"),
#                 use_lighting=True,
#                 use_texture=True,
#             )
#         )
#         self.object_manager.add(cube)

#     # Joint markers make the animated skeleton readable in final renders.
#         light_position = f.Vector3(x=3.5, y=4.0, z=3.0)
#         color = f.Color(r=1.0, g=1.0, b=1.0)
#         self.object_manager.add_light(
#             f.PointLight(
#                 position=light_position,
#                 color=color,
#                 ambient_strength=0.20,
#                 diffuse_strength=0.95,
#                 specular_strength=0.45,
#                 shininess=32.0,
#             )
#         )


#     def update(self) -> None:
#         self.scene_time += 1

# class TestBuildingScene(unittest.TestCase):
#     def test_render_cube_photo(self) -> None:
#         scene = DemoScene(400, 300)
#         scene.render_image(output_path="output.png")
#         with Image.open("output.png") as image:
#             center_pixel = image.getpixel((image.width // 2, image.height // 2))
#         self.assertNotEqual(center_pixel[:3], (0, 0, 0))
#     ...