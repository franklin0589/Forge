import unittest
import tempfile

import Forge as f
from pathlib import Path
from PIL import Image
    

# class TestSkybox(unittest.TestCase):
#     def test_skybox_tracks_camera_position(self) -> None:
#         camera = f.Camera(
#             position=f.Vector3(x=1.0, y=2.0, z=3.0),
#             target=f.Vector3(x=0.0, y=0.0, z=0.0),
#             up=f.Vector3(x=0.0, y=1.0, z=0.0),
#         )

#         skybox = f.Skybox(camera=camera, radius=15.0)

#         self.assertEqual(skybox.model.vertex_format, "3f")
#         self.assertFalse(skybox.model.depth_test)
#         self.assertAlmostEqual(float(skybox.transform.matrix[0, 3]), 1.0)
#         self.assertAlmostEqual(float(skybox.transform.matrix[1, 3]), 2.0)
#         self.assertAlmostEqual(float(skybox.transform.matrix[2, 3]), 3.0)

#         camera.set_position(f.Vector3(x=-4.0, y=0.5, z=8.0))
#         skybox.sync_to_camera()

#         self.assertAlmostEqual(float(skybox.model.point.matrix[0, 3]), -4.0)
#         self.assertAlmostEqual(float(skybox.model.point.matrix[1, 3]), 0.5)
#         self.assertAlmostEqual(float(skybox.model.point.matrix[2, 3]), 8.0)


# class TestSkyboxBuild(unittest.TestCase):
#     def test_skybox_build(self) -> None:
#         camera = f.Camera(
#             position=f.Vector3(x=0.0, y=0.0, z=5.0),
#             target=f.Vector3(x=0.0, y=0.0, z=0.0),
#             up=f.Vector3(x=0.0, y=1.0, z=0.0),
#         )

#         skybox = f.Skybox(camera=camera, radius=20.0)
#         model = skybox.build()

#         self.assertEqual(model.vertex_format, "3f")
#         self.assertFalse(model.depth_test)
#         self.assertEqual(model.attributes, ["in_pos"])





# class SkyboxScene(f.Scene):
#     def __init__(self, width: int = 1280, height: int = 720):
#         base_dir = Path(__file__).resolve().parent
#         shader_dir = base_dir / "shaders"
#         position = f.Vector3(x=0.0, y=0.0, z=3.0)
#         target = f.Vector3(x=0.0, y=0.0, z=0.0)
#         up = f.Vector3(x=0.0, y=1.0, z=0.0)
#         self.cam = f.Camera(position=position, target=target, up=up)

#         super().__init__(
#             width=width,
#             height=height,
#             cam=self.cam,
#             vertex_shader_path=str(shader_dir / "lit_texture.vert"),
#             fragment_shader_path=str(shader_dir / "lit_texture.frag"),
#         )

#     def setup(self) -> None:
#         self.skybox = f.Skybox(camera=self.cam, radius=40.0)
#         self.set_skybox(self.skybox)
        

#     def update(self) -> None:
#         ...

# class TestSkyboxScene(unittest.TestCase):
#     def test_skybox_output(self) -> None:
#         scene = SkyboxScene(width=800, height=600)
#         output_path = Path("skybox_scene.png")
#         scene.render_image(output_path=str(output_path))

#         with Image.open(output_path) as image:
#             center_pixel = image.getpixel((image.width // 2, image.height // 2))
#             top_pixel = image.getpixel((image.width // 2, 10))

#         self.assertNotEqual(center_pixel[:3], (26, 31, 41))
#         self.assertNotEqual(top_pixel[:3], center_pixel[:3])

#     def test_skybox_output_changes_with_camera_pitch(self) -> None:
#         scene = SkyboxScene(width=320, height=240)

#         look_level_path = Path("skybox_level.png")
#         scene.render_image(output_path=str(look_level_path))
#         with Image.open(look_level_path) as level_image:
#             level_center_pixel = level_image.getpixel((level_image.width // 2, level_image.height // 2))

#         scene.cam.set_target(f.Vector3(x=0.0, y=3.0, z=0.0))
#         look_up_path = Path("skybox_look_up.png")
#         scene.render_image(output_path=str(look_up_path))
#         with Image.open(look_up_path) as look_up_image:
#             look_up_center_pixel = look_up_image.getpixel((look_up_image.width // 2, look_up_image.height // 2))

#         self.assertNotEqual(level_center_pixel[:3], look_up_center_pixel[:3])


# class SkyboxWithObjectScene(f.Scene):
#     def __init__(self, width: int = 1280, height: int = 720):
#         base_dir = Path(__file__).resolve().parent
#         shader_dir = base_dir / "shaders"
#         position = f.Vector3(x=0.0, y=0.0, z=3.0)
#         target = f.Vector3(x=0.0, y=0.0, z=0.0)
#         up = f.Vector3(x=0.0, y=1.0, z=0.0)
#         self.cam = f.Camera(position=position, target=target, up=up)

#         super().__init__(
#             width=width,
#             height=height,
#             cam=self.cam,
#             vertex_shader_path=str(shader_dir / "lit_texture.vert"),
#             fragment_shader_path=str(shader_dir / "lit_texture.frag"),
#         )

#     def setup(self) -> None:
#         self.skybox = f.Skybox(camera=self.cam, radius=40.0)
#         self.set_skybox(self.skybox)

#         cube_transform = f.Transform()
#         cube_transform.translate(0.0, -1.0, -3.0)

#         cube_mesh = f.form.TexturedCubeMesh(size=1.0)
#         cube = f.RenderableObject(
#             mesh=cube_mesh,
#             transform=cube_transform,
#             material=f.Material(
#                 vertex_shader_path=self.vertex_shader_path,
#                 fragment_shader_path=self.fragment_shader_path,
#                 texture_path=str(Path(__file__).resolve().parent / "textures" / "box.jpg"),
#                 use_lighting=True,
#                 use_texture=True,
#             )
#         )
#         self.object_manager.add(cube)
    
#     def update(self) -> None:
#         ...

# class TestSkyboxWithObjectScene(unittest.TestCase):
#     def test_skybox_with_object_output(self) -> None:
#         scene = SkyboxWithObjectScene(width=800, height=600)
#         output_path = Path("skybox_with_object_scene.png")
#         scene.render_image(output_path=str(output_path))

#         with Image.open(output_path) as image:
#             center_pixel = image.getpixel((image.width // 2, image.height // 2))
#             top_pixel = image.getpixel((image.width // 2, 10))

#         self.assertNotEqual(center_pixel[:3], (26, 31, 41))
#         self.assertNotEqual(top_pixel[:3], center_pixel[:3])


# class CubeMapSkyboxScene(f.Scene):
#     def __init__(self, cube_map_faces: dict[str, str], width: int = 512, height: int = 512):
#         base_dir = Path(__file__).resolve().parent
#         shader_dir = base_dir / "shaders"
#         position = f.Vector3(x=0.0, y=0.0, z=3.0)
#         target = f.Vector3(x=0.0, y=0.0, z=2.0)
#         up = f.Vector3(x=0.0, y=1.0, z=0.0)
#         self.cam = f.Camera(position=position, target=target, up=up)
#         self.cube_map_faces = cube_map_faces

#         super().__init__(
#             width=width,
#             height=height,
#             cam=self.cam,
#             vertex_shader_path=str(shader_dir / "lit_texture.vert"),
#             fragment_shader_path=str(shader_dir / "lit_texture.frag"),
#         )

#     def setup(self) -> None:
#         self.set_skybox(f.Skybox(camera=self.cam, cube_map_faces=self.cube_map_faces))

#     def update(self) -> None:
#         self.cam.rotate(f.Vector3(x=0.0, y=1.0, z=0.0), 0.5)
#         self.scene_time += 1



# class TestCubeMapSkyboxScene(unittest.TestCase):
#     def test_cubemap_changes_with_camera_yaw(self) -> None:

#         face_paths = {
#             "right": str(Path(__file__).resolve().parent / "textures" / "negx.jpg"),
#             "left": str(Path(__file__).resolve().parent / "textures" / "posx.jpg"),
#             "top": str(Path(__file__).resolve().parent / "textures" / "posy.jpg"),
#             "bottom": str(Path(__file__).resolve().parent / "textures" / "negy.jpg"),
#             "front": str(Path(__file__).resolve().parent / "textures" / "posz.jpg"),
#             "back": str(Path(__file__).resolve().parent / "textures" / "negz.jpg"),
#         }
#         scene = CubeMapSkyboxScene(cube_map_faces=face_paths, width=320, height=240)

#         forward_path = Path("skybox_cubemap_forward.png")
#         scene.render_image(output_path=str(forward_path))
#         with Image.open(forward_path) as image:
#             forward_center = image.getpixel((image.width // 2, image.height // 2))

#         scene.cam.set_target(f.Vector3(x=4.0, y=0.0, z=3.0))
#         right_path = Path("skybox_cubemap_right.png")
#         scene.render_image(output_path=str(right_path))
#         with Image.open(right_path) as image:
#             right_center = image.getpixel((image.width // 2, image.height // 2))

#         # self.assertEqual(forward_center[:3], (32, 255, 255))
#         # self.assertEqual(right_center[:3], (255, 32, 32))
#         # self.assertNotEqual(forward_center[:3], right_center[:3])

# class TestCubeMaponGif(unittest.TestCase):
#     def test_cubemap_on_gif(self) -> None:
#         face_paths = {
#             "right": str(Path(__file__).resolve().parent / "textures" / "posx.jpg"),
#             "left": str(Path(__file__).resolve().parent / "textures" / "negx.jpg"),
#             "top": str(Path(__file__).resolve().parent / "textures" / "posy.jpg"),
#             "bottom": str(Path(__file__).resolve().parent / "textures" / "negy.jpg"),
#             "front": str(Path(__file__).resolve().parent / "textures" / "posz.jpg"),
#             "back": str(Path(__file__).resolve().parent / "textures" / "negz.jpg"),
#         }
#         scene = CubeMapSkyboxScene(cube_map_faces=face_paths, width=512, height=512)

#         scene.render_gif(output_path="skybox_cubemap.gif", duration=100, loop=0)

# if __name__ == "__main__":
#     unittest.main()