import pygame
import sys
from game_states import GameStateManager
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("NotSoDangerousDave")
    clock = pygame.time.Clock()
    
    game_state_manager = GameStateManager(screen)
    
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game_state_manager.handle_event(event)
        
        game_state_manager.update(dt)
        game_state_manager.draw()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()