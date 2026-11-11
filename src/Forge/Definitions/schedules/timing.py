from typing import Callable

class Timing:
    def __init__(self, max_duration, start, dest):
        self.max_duration = max_duration
        self.start = start
        self.dest = dest
        self.easing = lambda t: t  # Default linear easing function

    def set_easing(self, easing_func:Callable):
        self.easing = easing_func

    def duration_within(self, current_time):
        dur = current_time / self.max_duration 
        return self.easing(dur)
        
    def interpolate(self, current_time):
        t = self.duration_within(current_time)
        return self.start + t * (self.dest - self.start)