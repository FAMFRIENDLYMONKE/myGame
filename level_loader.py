import pygame
from constants import *

def load_level_from_image(image_path):
    """Load level data from PNG image"""
    # Just use manual level for now to avoid scaling issues
    return create_manual_level()

def create_manual_level():
    """Create a simple working level"""
    platforms = [
        # Ground
        pygame.Rect(0, 550, SCREEN_WIDTH, 50),
        
        # Simple platforms
        pygame.Rect(200, 450, 150, 20),
        pygame.Rect(450, 350, 150, 20),
        pygame.Rect(150, 250, 150, 20),
        pygame.Rect(500, 150, 150, 20),
    ]
    
    collectibles = [
        pygame.Rect(250, 420, 16, 16),
        pygame.Rect(500, 320, 16, 16),
        pygame.Rect(200, 220, 16, 16),
        pygame.Rect(550, 120, 16, 16),
    ]
    
    spawn_point = (50, 500)
    
    return platforms, collectibles, spawn_point