# clock.py

class TimeController:
    def __init__(self):
        self.current_scale = 0.0
        self.target_scale = 0.0
        self.speed = 6.0  # how fast time transitions

    def update(self, real_dt):
        # Smoothly move current_scale toward target_scale
        diff = self.target_scale - self.current_scale
        self.current_scale += diff * min(1, self.speed * real_dt)

        return real_dt * self.current_scale

    def freeze(self):
        self.target_scale = 0.0

    def normal(self):
        self.target_scale = 1.0

