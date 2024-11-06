import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
PLAYER_SIZE = 25
PLAYER_SPEED = 5

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Laser")

# Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Game variables
player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT // 2 - PLAYER_SIZE // 2
game_over = False
score = 0
lasers = []

# Player class
class Player:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = GREEN
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.hitbox())
    
    def move(self, keys):
        if not game_over:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.x += PLAYER_SPEED
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.y -= PLAYER_SPEED
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.y += PLAYER_SPEED

            self.x = max(0, min(WIDTH - self.size, self.x))
            self.y = max(0, min(HEIGHT - self.size, self.y))
    
    def hitbox(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

# Laser class
class Laser:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = RED
        self.active = False
        self.active_start = 0
        self.warning = 0
        self.warning_duration = 0.75
    
    def draw(self):
        if self.active:
            pygame.draw.rect(screen, self.color, self.hitbox())
        elif time.time() - self.warning < self.warning_duration:
            if int((time.time() - self.warning) * 10) % 2 == 0:
                pygame.draw.rect(screen, YELLOW, self.hitbox())
    
    def update(self):
        if not self.active and time.time() - self.warning >= self.warning_duration:
            self.active = True
            self.active_start = time.time()

        if self.active and time.time() - self.active_start > 1:
            return False
        return True
        
    def hitbox(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def start_warning(self):
        self.warning = time.time()

# Initialize player
player = Player(player_x, player_y, PLAYER_SIZE, PLAYER_SPEED)

# Function to spawn lasers
def spawn_laser():
    for _ in range((score // 10) + 1):
        laser_type = random.choice(["Horizontal", "Vertical"])
        
        if laser_type == "Horizontal":
            laser = Laser(0, random.randint(0, HEIGHT - 10), WIDTH, 10)
        else:
            laser = Laser(random.randint(0, WIDTH - 10), 0, 10, HEIGHT)
        
        laser.start_warning()
        lasers.append(laser)

# Function to draw everything
def draw():
    screen.fill((0, 0, 0))
    player.draw()
    
    for laser in lasers:
        laser.draw()
    
    score_text = pygame.font.SysFont(None, 30).render(str(score), True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 25))
    
    if game_over:
        game_over_text = pygame.font.SysFont(None, 60).render("GAME OVER", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - game_over_text.get_height()//2))

# Function to update game state
def update():
    global score, game_over
    first_laser = True
    
    if not game_over:
        keys = pygame.key.get_pressed()
        player.move(keys)
        
        for laser in lasers[:]:
            if not laser.update():
                if first_laser:
                    score += 1
                    first_laser = False
                lasers.remove(laser)
        
        for laser in lasers:
            if laser.active and player.hitbox().colliderect(laser.hitbox()):
                game_over = True

# Main game loop
clock = pygame.time.Clock()
spawn_laser_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_laser_event, 2100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == spawn_laser_event:
            spawn_laser()
    
    update()
    draw()
    pygame.display.flip()
    clock.tick(60)