import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Impact")
clock = pygame.time.Clock()

# Game state
game_active = False
score = 0

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create a simple spaceship shape
        self.image = pygame.Surface((50, 30))
        self.image.fill(GREEN)
        # Draw a triangle for the ship
        pygame.draw.polygon(self.image, WHITE, [(0, 15), (50, 0), (50, 30)])
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = SCREEN_HEIGHT // 2
        self.speed = 5
        self.bullets = pygame.sprite.Group()
        self.shoot_delay = 250  # milliseconds
        self.last_shot = pygame.time.get_ticks()
    
    def update(self):
        # Get keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        
        # Shoot bullets
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        # Update bullets
        self.bullets.update()
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.right, self.rect.centery)
            self.bullets.add(bullet)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.bullets.draw(surface)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speed = 10
    
    def update(self):
        self.rect.x += self.speed
        # Remove if it goes off-screen
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

def main():
    global game_active, score
    
    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_active:
                    # Start the game
                    game_active = True
                    score = 0
        
        # Fill the screen with black
        screen.fill(BLACK)
        
        if game_active:
            # Game logic and rendering will go here
            pass
        else:
            # Show start screen
            title_font = pygame.font.SysFont('Arial', 64)
            instruction_font = pygame.font.SysFont('Arial', 24)
            
            title_text = title_font.render('SPACE IMPACT', True, WHITE)
            instruction_text = instruction_font.render('Press SPACE to start', True, WHITE)
            
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))
            screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 300))
        
        # Update the display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
