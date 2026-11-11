from __future__ import annotations

from dataclasses import dataclass

import numpy as np




# def bind(program, object, view_pos: np.ndarray) -> None:
# 	if "u_light.direction" in program:
# 		program["u_light.direction"].value = tuple(float(v) for v in self.direction)
# 	if "u_light.color" in program:
# 		program["u_light.color"].value = (
# 			float(self.color.r),
# 			float(self.color.g),
# 			float(self.color.b),
# 		)
# 	if "u_light.ambient_strength" in program:
# 		program["u_light.ambient_strength"].value = float(self.ambient_strength)
# 	if "u_light.diffuse_strength" in program:
# 		program["u_light.diffuse_strength"].value = float(self.diffuse_strength)
# 	if "u_light.specular_strength" in program:
# 		program["u_light.specular_strength"].value = float(self.specular_strength)
# 	if "u_view_pos" in program:
# 		program["u_view_pos"].value = tuple(float(v) for v in view_pos)