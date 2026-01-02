# core/camera.py

import pygame
import random

class Camera:
    def __init__(self, width, height):
        # Screen dimensions
        self.width = width
        self.height = height

        # Current zoom level (1 = normal)
        self.zoom = 1.0

        # Desired zoom level
        self.target_zoom = 1.0

        # How fast zoom interpolates
        self.zoom_speed = 5.0

        # Shake strength (0 = no shake)
        self.shake_strength = 0.0

    def update(self, dt):
        # Smooth zoom interpolation
        diff = self.target_zoom - self.zoom
        self.zoom += diff * min(1, self.zoom_speed * dt)

        # Reduce shake over time
        self.shake_strength *= 0.9

    def apply(self, surface):
        # Apply zoom by scaling the surface
        scaled_width = int(self.width * self.zoom)
        scaled_height = int(self.height * self.zoom)

        scaled_surface = pygame.transform.scale(
            surface, (scaled_width, scaled_height)
        )

        # Calculate shake offset
        offset_x = random.randint(-int(self.shake_strength), int(self.shake_strength))
        offset_y = random.randint(-int(self.shake_strength), int(self.shake_strength))

        # Center the camera
        x = (self.width - scaled_width) // 2 + offset_x
        y = (self.height - scaled_height) // 2 + offset_y

        return scaled_surface, (x, y)

    def zoom_in(self):
        # Zoom in slightly (freeze effect)
        self.target_zoom = 1.08

    def zoom_out(self):
        # Return to normal zoom
        self.target_zoom = 1.0

    def shake(self, strength=8):
        # Trigger camera shake
        self.shake_strength = strength

