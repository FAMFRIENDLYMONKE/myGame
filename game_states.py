import pygame
from constants import *
from level import Level

class GameState:
    def handle_event(self, event):
        pass
    
    def update(self, dt):
        pass
    
    def draw(self, screen):
        pass

class HomeScreen(GameState):
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.font = pygame.font.Font(None, 74)
        self.title_font = pygame.font.Font(None, 96)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.state_manager.change_state('menu')
    
    def draw(self, screen):
        screen.fill(BLACK)
        title = self.title_font.render("NotSoDangerousDave", True, WHITE)
        subtitle = self.font.render("Press SPACE to continue", True, GRAY)
        
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 100))
        screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, SCREEN_HEIGHT//2 + 50))

class MenuScreen(GameState):
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.font = pygame.font.Font(None, 48)
        self.selected = 0
        self.options = ["New Game", "Continue", "Multiplayer", "Level Builder"]
        self.enabled = [True, False, False, False]
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.enabled[self.selected]:
                    if self.selected == 0:  # New Game
                        self.state_manager.change_state('game')
    
    def draw(self, screen):
        screen.fill(BLACK)
        title = pygame.font.Font(None, 74).render("Main Menu", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        for i, option in enumerate(self.options):
            color = WHITE if self.enabled[i] else GRAY
            if i == self.selected and self.enabled[i]:
                color = BLUE
            
            text = self.font.render(option, True, color)
            y = 250 + i * 60
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y))

class GameScreen(GameState):
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.level = Level('Dangerous_Dave_Level_format.png')
        self.player = Player(*self.level.get_spawn_point())
        self.bullets = []
        self.collectibles = list(self.level.get_collectibles())
        self.score = 0
        self.timer = 0
        self.font = pygame.font.Font(None, 36)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state_manager.change_state('menu')
            elif event.key == pygame.K_SPACE and self.player.has_gun:
                self.bullets.append(Bullet(self.player.rect.centerx, self.player.rect.centery, self.player.facing))
    
    def update(self, dt):
        self.timer += dt
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys, self.level.get_platforms())
        
        for bullet in self.bullets[:]:
            bullet.update(dt)
            if bullet.rect.x < 0 or bullet.rect.x > SCREEN_WIDTH:
                self.bullets.remove(bullet)
        
        # Check collectible collisions
        for collectible in self.collectibles[:]:
            if self.player.rect.colliderect(collectible):
                self.collectibles.remove(collectible)
                self.score += 100
    
    def draw(self, screen):
        self.level.draw_background(screen)
        
        # Draw platforms
        for platform in self.level.get_platforms():
            pygame.draw.rect(screen, BLACK, platform)
        
        # Draw collectibles
        for collectible in self.collectibles:
            pygame.draw.rect(screen, RED, collectible)
        
        self.player.draw(screen)
        
        for bullet in self.bullets:
            bullet.draw(screen)
        
        # UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        timer_text = self.font.render(f"Time: {int(self.timer)}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(timer_text, (10, 50))

class Player:
    def __init__(self, x=100, y=400):
        self.rect = pygame.Rect(x, y, 32, 48)
        self.vel_y = 0
        self.on_ground = False
        self.has_gun = True  # Start with gun for testing
        self.facing = 1  # 1 for right, -1 for left
    
    def update(self, dt, keys, platforms):
        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED * dt
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED * dt
            self.facing = 1
        
        # Jumping
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = -JUMP_SPEED
            self.on_ground = False
        
        # Gravity
        self.vel_y += GRAVITY * dt
        self.rect.y += self.vel_y * dt
        
        # Platform collision
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:  # Falling
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.on_ground = True
        
        # Screen bounds
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - 100  # Reset if fall off screen
    
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)

class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 8, 4)
        self.direction = direction
    
    def update(self, dt):
        self.rect.x += BULLET_SPEED * self.direction * dt
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class GameStateManager:
    def __init__(self, screen):
        self.screen = screen
        self.states = {
            'home': HomeScreen(self),
            'menu': MenuScreen(self),
            'game': GameScreen(self)
        }
        self.current_state = 'home'
    
    def change_state(self, new_state):
        self.current_state = new_state
    
    def handle_event(self, event):
        self.states[self.current_state].handle_event(event)
    
    def update(self, dt):
        self.states[self.current_state].update(dt)
    
    def draw(self):
        self.states[self.current_state].draw(self.screen)