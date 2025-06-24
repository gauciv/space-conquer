import pygame
import sys
import random
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize sound mixer

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

# Load images
def load_image(name):
    path = os.path.join('images', name)
    try:
        image = pygame.image.load(path)
        return image
    except pygame.error as e:
        print(f"Cannot load image: {path}")
        print(e)
        return pygame.Surface((30, 30))

# Load all game images
player_img = load_image('player_ship.png')
normal_enemy_img = load_image('normal_enemy.png')
fast_enemy_img = load_image('fast_enemy.png')
tank_enemy_img = load_image('tank_enemy.png')
bullet_img = load_image('bullet.png')
health_powerup_img = load_image('health_powerup.png')
speed_powerup_img = load_image('speed_powerup.png')
rapid_fire_powerup_img = load_image('rapid_fire_powerup.png')

# Create sounds directory if it doesn't exist
if not os.path.exists('sounds'):
    os.makedirs('sounds')

# Create simple sound files
def create_sound_files():
    try:
        # Create a simple shoot sound
        pygame.mixer.Sound.play = lambda self: None  # Temporarily disable sound playing
        shoot_sound = pygame.mixer.Sound(buffer=bytes([128] * 4410))  # 0.1s of silence
        shoot_sound.set_volume(0.3)
        shoot_sound.save('sounds/shoot.wav')
        
        # Create a simple explosion sound
        explosion_sound = pygame.mixer.Sound(buffer=bytes([128] * 22050))  # 0.5s of silence
        explosion_sound.set_volume(0.5)
        explosion_sound.save('sounds/explosion.wav')
        
        # Create a simple powerup sound
        powerup_sound = pygame.mixer.Sound(buffer=bytes([128] * 11025))  # 0.25s of silence
        powerup_sound.set_volume(0.4)
        powerup_sound.save('sounds/powerup.wav')
    except:
        print("Could not create sound files. Game will run without sound.")

# Try to create sound files
try:
    create_sound_files()
    # Load sounds
    shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
    explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')
    powerup_sound = pygame.mixer.Sound('sounds/powerup.wav')
    sound_enabled = True
except:
    sound_enabled = False

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
        # Use the player ship image
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = SCREEN_HEIGHT // 2
        self.speed = 5
        self.bullets = pygame.sprite.Group()
        self.shoot_delay = 250  # milliseconds
        self.last_shot = pygame.time.get_ticks()
        self.health = 3
        self.rapid_fire = False
        self.rapid_fire_timer = 0
    
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
        
        # Check rapid fire timer
        if self.rapid_fire:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer <= 0:
                self.rapid_fire = False
                self.shoot_delay = 250
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.right, self.rect.centery)
            self.bullets.add(bullet)
            
            # Add a second bullet if rapid fire is active
            if self.rapid_fire:
                bullet2 = Bullet(self.rect.right, self.rect.centery - 10)
                self.bullets.add(bullet2)
            
            # Play sound
            if sound_enabled:
                shoot_sound.play()
    
    def apply_powerup(self, powerup_type):
        if powerup_type == 'health':
            self.health += 1
        elif powerup_type == 'speed':
            self.speed += 1
        elif powerup_type == 'rapid_fire':
            self.rapid_fire = True
            self.shoot_delay = 100
            self.rapid_fire_timer = 300  # Lasts for 300 frames (5 seconds at 60 FPS)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.bullets.draw(surface)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
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
    def __init__(self, enemy_type='normal'):
        super().__init__()
        self.enemy_type = enemy_type
        
        if enemy_type == 'normal':
            self.image = normal_enemy_img
            self.health = 1
            self.speed = random.randint(3, 7)
            self.points = 10
        elif enemy_type == 'fast':
            self.image = fast_enemy_img
            self.health = 1
            self.speed = random.randint(8, 12)
            self.points = 15
        elif enemy_type == 'tank':
            self.image = tank_enemy_img
            self.health = 3
            self.speed = random.randint(2, 4)
            self.points = 25
        
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(0, 100)
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
    
    def update(self):
        self.rect.x -= self.speed
        # Remove if it goes off-screen
        if self.rect.right < 0:
            self.kill()

# Power-up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(['health', 'speed', 'rapid_fire'])
        
        if self.type == 'health':
            self.image = health_powerup_img
        elif self.type == 'speed':
            self.image = speed_powerup_img
        elif self.type == 'rapid_fire':
            self.image = rapid_fire_powerup_img
        
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(0, 100)
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.speed = 3
    
    def update(self):
        self.rect.x -= self.speed
        # Remove if it goes off-screen
        if self.rect.right < 0:
            self.kill()

def show_score(surface, score, health):
    font = pygame.font.SysFont('Arial', 24)
    score_text = font.render(f'Score: {score}', True, WHITE)
    health_text = font.render(f'Health: {health}', True, WHITE)
    surface.blit(score_text, (10, 10))
    surface.blit(health_text, (10, 40))

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
    powerups = pygame.sprite.Group()
    
    # Create player
    player = Player()
    all_sprites.add(player)
    
    # Create stars
    stars = [Star() for _ in range(50)]
    
    # Enemy spawn timer
    enemy_spawn_delay = 1000  # milliseconds
    last_enemy_spawn = pygame.time.get_ticks()
    
    # Power-up spawn timer
    powerup_spawn_delay = 10000  # milliseconds
    last_powerup_spawn = pygame.time.get_ticks()
    
    # Difficulty scaling
    difficulty_timer = 0
    enemy_types = ['normal']
    
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
                    powerups = pygame.sprite.Group()
                    player = Player()
                    all_sprites.add(player)
                    last_enemy_spawn = pygame.time.get_ticks()
                    last_powerup_spawn = pygame.time.get_ticks()
                    difficulty_timer = 0
                    enemy_types = ['normal']
        
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
            powerups.update()
            
            # Increase difficulty over time
            difficulty_timer += 1
            if difficulty_timer == 1200:  # After 20 seconds
                if 'fast' not in enemy_types:
                    enemy_types.append('fast')
            elif difficulty_timer == 3600:  # After 1 minute
                if 'tank' not in enemy_types:
                    enemy_types.append('tank')
            
            # Spawn enemies
            now = pygame.time.get_ticks()
            if now - last_enemy_spawn > enemy_spawn_delay:
                last_enemy_spawn = now
                enemy_type = random.choice(enemy_types)
                enemy = Enemy(enemy_type)
                enemies.add(enemy)
                all_sprites.add(enemy)
            
            # Spawn power-ups
            if now - last_powerup_spawn > powerup_spawn_delay:
                last_powerup_spawn = now
                powerup = PowerUp()
                powerups.add(powerup)
                all_sprites.add(powerup)
            
            # Check for bullet collisions with enemies
            hits = pygame.sprite.groupcollide(enemies, player.bullets, False, True)
            for enemy, bullets in hits.items():
                enemy.health -= len(bullets)
                if enemy.health <= 0:
                    score += enemy.points
                    enemy.kill()
                    # Play explosion sound
                    if sound_enabled:
                        explosion_sound.play()
            
            # Check for player collision with enemies
            if pygame.sprite.spritecollide(player, enemies, True):
                player.health -= 1
                # Play explosion sound
                if sound_enabled:
                    explosion_sound.play()
                if player.health <= 0:
                    game_active = False
            
            # Check for player collision with power-ups
            powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
            for powerup in powerup_hits:
                player.apply_powerup(powerup.type)
                # Play powerup sound
                if sound_enabled:
                    powerup_sound.play()
            
            # Draw
            all_sprites.draw(screen)
            player.draw(screen)
            
            # Show score and health
            show_score(screen, score, player.health)
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
