import Forge.Definitions as gadget

class PointLight:
    def __init__(self, position: gadget.Vector3, color: gadget.Color):
        self._position: gadget.Vector3 = position
        self._color: gadget.Color = color
        self._ambient_strength: float = 0.18
        self._diffuse_strength: float = 0.9
        self._specular_strength: float = 0.4
        self._shininess: float = 32.0

    @property
    def position(self) -> gadget.Vector3:
        return self._position
    @position.setter
    def position(self, value: gadget.Vector3):
        self._position = value

    @property
    def color(self) -> gadget.Color:
        return self._color
    @color.setter
    def color(self, value: gadget.Color):
        self._color = value

    @property
    def ambient_strength(self) -> float:
        return self._ambient_strength
    @ambient_strength.setter
    def ambient_strength(self, value: float):
        self._ambient_strength = value
    
    @property
    def diffuse_strength(self) -> float:
        return self._diffuse_strength
    @diffuse_strength.setter
    def diffuse_strength(self, value: float):
        self._diffuse_strength = value

    @property
    def specular_strength(self) -> float:
        return self._specular_strength
    @specular_strength.setter
    def specular_strength(self, value: float):
        self._specular_strength = value

    @property
    def shininess(self) -> float:
        return self._shininess
    @shininess.setter
    def shininess(self, value: float):
        self._shininess = value
    