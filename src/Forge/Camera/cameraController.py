from Forge.Definitions.Camera import Camera
import Forge.Definitions as gadget


class CameraController:
    def __init__(self, camera: Camera, width: int, height: int):
        self.width = width
        self.height = height
        self.camera = camera


    def view_perspective(self, transform: gadget.Matrix4) -> gadget.Matrix4:
        """ Get the camera transform matrix """
        return transform * self.camera.get_mvp()

    def zoom(self, amount: float) -> None:
        """ Amount to zoom the camera by  """
        direction = (self.camera.target - self.camera.position)
        direction = direction.normalized()
        self.camera.position += direction * amount

    def rotate(self, axis: gadget.Vector3, angle_deg: float) -> None:
        """ Rotate the camera around the given axis by the specified angle in degrees """
        direction = (self.camera.target - self.camera.position).normalized()
        rotation = gadget.AQuaternion(axis, angle_deg).as_quaternion()
        rotated_direction = rotation.transform_vector(direction)
        self.camera.target = self.position + rotated_direction


    def rotate_x(self, angle_deg: float) -> None:
        """ Rotate the camera around the X-axis by the specified angle in degrees """
        self.rotate(gadget.X_AXIS, angle_deg)

    def rotate_y(self, angle_deg: float) -> None:
        """ Rotate the camera around the Y-axis by the specified angle in degrees """
        self.rotate(gadget.Y_AXIS, angle_deg)

    def rotate_z(self, angle_deg: float) -> None:
        """ Rotate the camera around the Z-axis by the specified angle in degrees """
        self.rotate(gadget.Z_AXIS, angle_deg)

    def move(self, direction: gadget.Vector3, amount: float) -> None:
        direction = direction.normalized()
        self.camera.position += direction * amount
        self.camera.target += direction * amount