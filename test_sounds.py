import pygame
import time
import sys

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Create a small window (needed for pygame to run)
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Sound Test")

# Load sounds
try:
    shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
    explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')
    powerup_sound = pygame.mixer.Sound('sounds/powerup.wav')
    
    print("Sound files loaded successfully!")
    
    # Play each sound with a delay
    print("Playing shoot sound...")
    shoot_sound.play()
    time.sleep(1)
    
    print("Playing explosion sound...")
    explosion_sound.play()
    time.sleep(1)
    
    print("Playing powerup sound...")
    powerup_sound.play()
    time.sleep(1)
    
    print("Sound test complete!")
    
except Exception as e:
    print(f"Error: {e}")

# Wait for user to close the window
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Display instructions
    font = pygame.font.SysFont('Arial', 16)
    text = font.render("Sound test complete. Close window to exit.", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(text, (20, 80))
    pygame.display.flip()

pygame.quit()
sys.exit()
