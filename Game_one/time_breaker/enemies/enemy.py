# enemies/enemy.py

import pygame
from enemies.bullet import Bullet


class Enemy:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.size = 20
        self.speed = 150
        self.direction = 1  # 1 = right, -1 = left
        self.color = (255, 60, 60)
        self.bullets = []
        self.shoot_timer = 0.0
        self.shoot_interval = 1.0  # seconds


    def update(self, dt):
        # Movement
        self.pos.x += self.direction * self.speed * dt
        if self.pos.x < 100 or self.pos.x > 800:
            self.direction *= -1
        
        # Shooting logic
        self.shoot_timer += dt
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            bullet = Bullet(self.pos.x, self.pos.y + self.size // 2, self.direction)
            self.bullets.append(bullet)

        # Update bullets
        for bullet in self.bullets:
            bullet.update(dt)

    def draw(self, screen):
        pygame.draw.rect(
                screen,
                self.color,
                (self.pos.x, self.pos.y, self.size, self.size)
        )
        for bullet in self.bullets:
            bullet.draw(screen)

