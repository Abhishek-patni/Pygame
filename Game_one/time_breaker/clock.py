# clock.py

class TimeController:
    def __init__(self):
        # Current time multiplier (what is actually used)
        self.current_scale = 0.0

        # Desired time multiplier (where we want to go)
        self.target_scale = 0.0

        # How fast current_scale moves toward target_scale
        self.speed = 6.0

    def update(self, real_dt):
        # Smoothly interpolate toward target_scale
        diff = self.target_scale - self.current_scale
        self.current_scale += diff * min(1, self.speed * real_dt)

        # Return scaled time
        return real_dt * self.current_scale

    def freeze(self):
        # Freeze time
        self.target_scale = 0.0

    def normal(self):
        # Normal time flow
        self.target_scale = 1.0

    def surge(self):
        # Dash surge (time moves faster)
        self.target_scale = 1.8

