# game.py

import pygame
from config import WIDTH, HEIGHT, FPS, BG_COLOR
from player.player import Player
from enemies.enemy import Enemy
from clock import TimeController


class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Create game window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TIME BREAKER")

        # Clock to control FPS
        self.clock = pygame.time.Clock()

        # Main game loop flag
        self.running = True

        # Global time controller (freeze / slow / normal)
        self.time = TimeController()

        # Create player at screen center
        self.player = Player(WIDTH // 2, HEIGHT // 2)

        # Create enemy
        self.enemy = Enemy(200, HEIGHT // 2)

    def run(self):
        # Main game loop
        while self.running:
            # Real time passed since last frame (seconds)
            real_dt = self.clock.tick(FPS) / 1000

            # Handle window events (quit, etc.)
            self.handle_events()

            # Update game logic
            self.update(real_dt)

            # Draw everything
            self.render()

        # Clean exit
        pygame.quit()

    def handle_events(self):
        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, real_dt):
        # Decide if time should flow based on player intent
        # Decide how time should behave
        if self.player.dashing:
            self.time.surge()        # Dash → time surge
        elif self.player.is_moving():
            self.time.normal()       # Movement → normal time
        else:
            self.time.freeze()       # Still → freeze time

        # Convert real time into game-controlled time
        game_dt = self.time.update(real_dt)

        # Update entities using GAME time
        self.player.update(game_dt)
        self.enemy.update(game_dt)

        # Check if player is hit by any bullet
        if self.check_death():
            self.reset()

    def check_death(self):
        # Get player collision rectangle
        player_rect = self.player.get_rect()

        # Check collision with each bullet
        for bullet in self.enemy.bullets:
            if player_rect.colliderect(bullet.get_rect()):
                return True  # Player died

        return False  # Player still alive

    def reset(self):
        # Recreate player (clears old state)
        self.player = Player(WIDTH // 2, HEIGHT // 2)

        # Recreate enemy (clears bullets)
        self.enemy = Enemy(200, HEIGHT // 2)

        # Freeze time after reset
        self.time.freeze()

    def render(self):
        # Clear screen
        self.screen.fill(BG_COLOR)

        # Draw game objects
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)

        # Draw time freeze overlay (polish)
        self.draw_time_overlay()

        # Update display
        pygame.display.flip()

    def draw_time_overlay(self):
        # Darken screen as time slows down
        intensity = int((1 - self.time.current_scale) * 120)

        if intensity <= 0:
            return

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(intensity)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

