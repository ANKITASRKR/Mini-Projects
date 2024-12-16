import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
GREEN = (34, 139, 34)

# Game Constants
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 50
PIPE_GAP = 150
FPS = 60

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
bird_image = pygame.image.load("HTML.web sample/buffering/intern/download.jpeg")
bird_image = pygame.transform.scale(bird_image, (40, 40))

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)

# Bird Class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.image = bird_image

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Pipe Class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP)

    def update(self):
        self.x -= 3
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)

    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0

# Game Loop
bird = Bird()
pipes = [Pipe(SCREEN_WIDTH + i * 200) for i in range(3)]
score = 0
running = True

def reset_game():
    global bird, pipes, score
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * 200) for i in range(3)]
    score = 0

while running:
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()

    # Update bird
    bird.update()

    # Update pipes
    for pipe in pipes:
        pipe.update()
        if pipe.is_off_screen():
            pipes.remove(pipe)
            pipes.append(Pipe(SCREEN_WIDTH))
            score += 1

    # Collision detection
    for pipe in pipes:
        if bird.y < 0 or bird.y > SCREEN_HEIGHT:
            reset_game()
        if pipe.top_rect.colliderect((bird.x, bird.y, 40, 40)) or pipe.bottom_rect.colliderect((bird.x, bird.y, 40, 40)):
            reset_game()

    # Draw elements
    bird.draw()
    for pipe in pipes:
        pipe.draw()

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)
