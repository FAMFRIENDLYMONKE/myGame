import pygame
from constants import *

class Level:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.platforms = []
        self.collectibles = []
        self.enemies = []
        self.spawn_point = (100, 400)
        self._parse_level()
    
    def _parse_level(self):
        # Parse the level image to create platforms and objects
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.image.get_at((x, y))
                
                # Black pixels = platforms
                if pixel[:3] == (0, 0, 0):
                    self.platforms.append(pygame.Rect(x * 2, y * 2, 2, 2))
                
                # Red pixels = collectibles
                elif pixel[:3] == (255, 0, 0):
                    self.collectibles.append(pygame.Rect(x * 2, y * 2, 16, 16))
                
                # Blue pixels = enemies
                elif pixel[:3] == (0, 0, 255):
                    self.enemies.append(pygame.Rect(x * 2, y * 2, 24, 24))
                
                # Green pixel = spawn point
                elif pixel[:3] == (0, 255, 0):
                    self.spawn_point = (x * 2, y * 2)
    
    def get_platforms(self):
        return self.platforms
    
    def get_collectibles(self):
        return self.collectibles
    
    def get_enemies(self):
        return self.enemies
    
    def get_spawn_point(self):
        return self.spawn_point
    
    def draw_background(self, screen):
        # Scale and draw the level image as background
        scaled_image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_image, (0, 0))