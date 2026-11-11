class FrameSchedule:
    def __init__(self, fps = 24):
        self.fps = fps
        self.callbacks = []
        # self.current_time = 0
        self.start_registry = {}
        
    def add_callback(self, start_time, callback):
        self.callbacks.append((start_time*self.fps, callback))
        self.start_registry[callback] = start_time
        self.sort_callbacks()

    def sort_callbacks(self):
        self.callbacks.sort(key=lambda x: x[0])
        self.callbacks = list(reversed(self.callbacks))

    def update(self, t, *args, **kwargs):
        for start_time, callback in self.callbacks:
            if start_time <= t:
                return callback(t, *args, **kwargs)
