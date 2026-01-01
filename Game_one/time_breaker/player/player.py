# player/player.py

import pygame
from config import PLAYER_COLOR

class Player:
    # initlize the game logic
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.size = 20
        self.speed = 300
    # Update the value

    def update(self, dt):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(
            keys[pygame.K_d] - keys[pygame.K_a],
            keys[pygame.K_s] - keys[pygame.K_w]
        )
        if direction.length() > 0:
            direction = direction.normalize()
        self.pos += direction * self.speed * dt

    # The game that make changes
    def draw(self, screen):
        pygame.draw.rect(
            screen,
            PLAYER_COLOR,
            (self.pos.x, self.pos.y, self.size, self.size)
        )

    # This report the intent and control the logic
    def is_moving(self):
        keys = pygame.key.get_pressed()
        return (
            keys[pygame.K_w] or
            keys[pygame.K_a] or
            keys[pygame.K_s] or
            keys[pygame.K_d]
        )
    
    def get_rect(self):
        # Returns the player's collision rectangle
        return pygame.Rect(
                self.pos.x,     # left
                self.pos.y,     # top
                self.size,      # width
                self.size       # height
        )


#player to work 
