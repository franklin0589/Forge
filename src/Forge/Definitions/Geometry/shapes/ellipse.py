from Forge.Definitions import Point
from Forge.shared.utils import find_bezier_control_points
import math

class Ellipse:
    def __init__(self, focusA: Point, focusB: Point, major_axis_length: float, minor_axis_factor: float = 1.0):
        self.focusA = focusA
        self.focusB = focusB
        self.major_axis_length = major_axis_length
        self.minor_axis_factor = minor_axis_factor
        self.minor_axis_length = self.get_minor_axis_length() * self.minor_axis_factor

    def get_focal_distance(self):
        c = math.dist([self.focusB.x, self.focusB.y], [self.focusA.x, self.focusA.y]) / 2
        return c

    def get_minor_axis_length(self):
        c = self.get_focal_distance()
        return math.sqrt(self.major_axis_length**2 - (2*c)**2)
    
    def get_x(self, t):
        b = self.minor_axis_length
        c = self.get_focal_distance()
        constant = (self.focusA.x+self.focusB.x)/2 
        cosine_constant = self.major_axis_length /( 2 * c ) * (self.focusB.x -self.focusA.x)
        sine_constant = (b * (self.focusB.y -self.focusA.y))/(2*c)
        return constant + cosine_constant * math.cos(t) - sine_constant * math.sin(t)

    def get_y(self, t):
        b = self.minor_axis_length
        c = self.get_focal_distance()
        constant = (self.focusA.y+self.focusB.y)/2 
        cosine_constant = self.major_axis_length / (2 * c) * (self.focusB.y -self.focusA.y)
        sine_constant = (b * (self.focusB.x -self.focusA.x))/(2*c)
        return constant + cosine_constant * math.cos(t) + sine_constant * math.sin(t)

    def get_control_points(self):
        for t in range(4):
            angle = math.radians((t/4)*360)
            next_angle = math.radians(((t+1)/4)*360)
            start_point = (self.get_x(angle), self.get_y(angle))
            end_point = (self.get_x(next_angle), self.get_y(next_angle))
            sample_angle_A = (next_angle - angle) / 3 + angle
            sample_point_A = (self.get_x(sample_angle_A), self.get_y(sample_angle_A))
            sample_angle_B = 2 * (next_angle - angle) / 3 + angle   
            sample_point_B = (self.get_x(sample_angle_B), self.get_y(sample_angle_B))
            controlA, controlB = find_bezier_control_points(start_point, end_point, sample_point_A, sample_point_B, 0.3333, 0.6666)
            yield controlA, controlB, end_point