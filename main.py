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
BLUE = (0, 0, 255)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Impact")
clock = pygame.time.Clock()

# Game state
game_active = False
score = 0

# Star background
class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.randint(1, 3)
        
    def update(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = SCREEN_WIDTH
            self.y = random.randint(0, SCREEN_HEIGHT)
            
    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (self.x, self.y), self.size)

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

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(0, 100)
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.speed = random.randint(3, 7)
    
    def update(self):
        self.rect.x -= self.speed
        # Remove if it goes off-screen
        if self.rect.right < 0:
            self.kill()

def show_score(surface, score):
    font = pygame.font.SysFont('Arial', 24)
    score_text = font.render(f'Score: {score}', True, WHITE)
    surface.blit(score_text, (10, 10))

def game_over_screen():
    global game_active, score
    
    font_large = pygame.font.SysFont('Arial', 64)
    font_small = pygame.font.SysFont('Arial', 24)
    
    game_over_text = font_large.render('GAME OVER', True, RED)
    score_text = font_small.render(f'Final Score: {score}', True, WHITE)
    restart_text = font_small.render('Press SPACE to restart', True, WHITE)
    
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 350))

def main():
    global game_active, score
    
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    
    # Create player
    player = Player()
    all_sprites.add(player)
    
    # Create stars
    stars = [Star() for _ in range(50)]
    
    # Enemy spawn timer
    enemy_spawn_delay = 1000  # milliseconds
    last_enemy_spawn = pygame.time.get_ticks()
    
    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_active:
                    # Start/restart the game
                    game_active = True
                    score = 0
                    # Clear all sprites
                    all_sprites = pygame.sprite.Group()
                    enemies = pygame.sprite.Group()
                    player = Player()
                    all_sprites.add(player)
                    last_enemy_spawn = pygame.time.get_ticks()
        
        # Fill the screen with black
        screen.fill(BLACK)
        
        # Update and draw stars
        for star in stars:
            star.update()
            star.draw(screen)
        
        if game_active:
            # Update
            player.update()
            enemies.update()
            
            # Spawn enemies
            now = pygame.time.get_ticks()
            if now - last_enemy_spawn > enemy_spawn_delay:
                last_enemy_spawn = now
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)
            
            # Check for bullet collisions with enemies
            hits = pygame.sprite.groupcollide(enemies, player.bullets, True, True)
            for hit in hits:
                score += 10
            
            # Check for player collision with enemies
            if pygame.sprite.spritecollide(player, enemies, False):
                game_active = False
            
            # Draw
            all_sprites.draw(screen)
            player.draw(screen)
            
            # Show score
            show_score(screen, score)
        else:
            if score > 0:
                game_over_screen()
            else:
                # Show start screen
                title_font = pygame.font.SysFont('Arial', 64)
                instruction_font = pygame.font.SysFont('Arial', 24)
                
                title_text = title_font.render('SPACE IMPACT', True, WHITE)
                instruction_text = instruction_font.render('Press SPACE to start', True, WHITE)
                controls_text = instruction_font.render('Arrow keys to move, SPACE to shoot', True, WHITE)
                
                screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))
                screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 300))
                screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, 350))
        
        # Update the display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
