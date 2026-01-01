# enemies/bullet.py

import pygame

class Bullet:
    def __init__(self, x, y, direction):
        self.pos = pygame.Vector2(x, y)
        self.radius = 5
        self.speed = 400
        self.direction = direction
        self.color = (255, 200, 50)

    def update(self, dt):
        self.pos.x += self.direction * self.speed * dt

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.pos.x), int(self.pos.y)),
            self.radius
        )

    def get_rect(self):
        # Returns a square collision box for the bullet
        return pygame.Rect(
                self.pos.x - self.radius,  # left
                self.pos.y - self.radius,  # top
                self.radius * 2,           # width
                self.radius * 2            # height
        )

