# game.py

import pygame
from config import WIDTH, HEIGHT, FPS, BG_COLOR
from player.player import Player
from enemies.enemy import Enemy
from clock import TimeController
from core.camera import Camera


class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Main window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TIME BREAKER")

        # Clock for FPS control
        self.clock = pygame.time.Clock()

        # Game loop flag
        self.running = True

        # Global time controller
        self.time = TimeController()

        # Camera system
        self.camera = Camera(WIDTH, HEIGHT)

        # World surface (everything is drawn here first)
        self.world_surface = pygame.Surface((WIDTH, HEIGHT))

        # Player and enemy
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        self.enemy = Enemy(200, HEIGHT // 2)

    def run(self):
        # Main game loop
        while self.running:
            # Real delta time (seconds)
            real_dt = self.clock.tick(FPS) / 1000

            # Handle quit events
            self.handle_events()

            # Update game logic
            self.update(real_dt)

            # Render frame
            self.render()

        pygame.quit()

    def handle_events(self):
        # Process pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, real_dt):
        # ----- TIME DECISION LOGIC -----
        if self.player.dashing:
            self.time.surge()          # Dash → time surge
        elif self.player.is_moving():
            self.time.normal()         # Moving → normal time
        else:
            self.time.freeze()         # Still → freeze time

        # Convert real time to game-controlled time
        game_dt = self.time.update(real_dt)

        # Update entities using GAME time
        self.player.update(game_dt)
        self.enemy.update(game_dt)

        # Check death
        if self.check_death():
            self.reset()

        # ----- CAMERA LOGIC -----
        self.camera.update(real_dt)

        # Zoom reacts to time state
        if self.time.current_scale < 0.2:
            self.camera.zoom_in()
        else:
            self.camera.zoom_out()

        # Dash causes camera shake
        if self.player.dashing:
            self.camera.shake(10)

    def check_death(self):
        # Player collision box
        player_rect = self.player.get_rect()

        # Check bullet collisions
        for bullet in self.enemy.bullets:
            if player_rect.colliderect(bullet.get_rect()):
                return True

        return False

    def reset(self):
        # Reset player and enemy
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        self.enemy = Enemy(200, HEIGHT // 2)

        # Freeze time after reset
        self.time.freeze()

    def render(self):
        # Clear world surface
        self.world_surface.fill(BG_COLOR)

        # Draw game objects onto world surface
        self.player.draw(self.world_surface)
        self.enemy.draw(self.world_surface)

        # Draw freeze overlay onto world surface
        self.draw_time_overlay(self.world_surface)

        # Apply camera transform
        final_surface, position = self.camera.apply(self.world_surface)

        # Clear screen
        self.screen.fill((0, 0, 0))

        # Draw camera-transformed scene
        self.screen.blit(final_surface, position)

        # Update display
        pygame.display.flip()

    def draw_time_overlay(self, surface):
        # Darken screen as time slows
        intensity = int((1 - self.time.current_scale) * 120)

        if intensity <= 0:
            return

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(intensity)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

