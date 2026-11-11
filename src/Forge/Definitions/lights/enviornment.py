
class EnviornmentEffect:
    def __init__(self, name: str, intensity: float):
        self.name = name
        self.intensity = intensity



class Enviornment:
    """Represents the environment of a scene, including lighting and other environmental effects."""
    
    def __init__(self):
        self.effects = []
        self.lights = []
        self.ambient_light = None

    def add_light(self, light):
        """Adds a light source to the environment."""
        self.lights.append(light)

    def set_ambient_light(self, color):
        """Sets the ambient light color for the environment."""
        self.ambient_light = color