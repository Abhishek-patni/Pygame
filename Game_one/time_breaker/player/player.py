# player/player.py

import pygame
from config import PLAYER_COLOR

class Player:
    # initlize the game logic
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.size = 20
        self.speed = 300
        # Dash properties
        self.dashing = False          # Is player currently dashing?
        self.dash_time = 0.0          # Time spent in dash
        self.dash_duration = 0.15     # Dash lasts 0.15 seconds
        self.dash_cooldown = 0.5      # Cooldown before next dash
        self.cooldown_timer = 0.0     # Time since last dash
        self.base_speed = self.speed # Store normal speed

    # Update the value
    def update(self, dt):
        keys = pygame.key.get_pressed()
        # Update dash cooldown timer
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt
        # Start dash if SPACE is pressed and cooldown is ready
        if keys[pygame.K_SPACE] and self.cooldown_timer <= 0 and not self.dashing:
            self.dashing = True                 # Enter dash state
            self.dash_time = 0.0                # Reset dash timer
            self.speed = self.base_speed * 3    # Increase movement speed
            self.cooldown_timer = self.dash_cooldown
        # If currently dashing
        if self.dashing:
            self.dash_time += dt
            if self.dash_time >= self.dash_duration:
                self.dashing = False             # End dash
                self.speed = self.base_speed     # Restore normal speed
        # Normal movement logic
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
