import pgzrun
import random
import time

WIDTH = 800
HEIGHT = 600
PLAYER_SIZE = 25
PLAYER_SPEED = 5

player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT // 2 - PLAYER_SIZE // 2
game_over = False
score = 0
lasers = []

class Player:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = "green"
    
    def draw(self):
        screen.draw.filled_rect(self.hitbox(), self.color)
    
    def move(self):
        if not game_over:
            if keyboard.left or keyboard.a:
                self.x -= PLAYER_SPEED
            if keyboard.right or keyboard.d:
                self.x += PLAYER_SPEED
            if keyboard.up or keyboard.w:
                self.y -= PLAYER_SPEED
            if keyboard.down or keyboard.s:
                self.y += PLAYER_SPEED

            self.x = max(0, min(WIDTH - self.size, self.x))
            self.y = max(0, min(HEIGHT - self.size, self.y))
    
    def hitbox(self):
        return Rect((self.x, self.y), (self.size, self.size))

class Laser():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = "red"
        self.active = False
        self.active_start = 0
        self.warning = 0
        self.warning_duration = 0.75
    
    def draw(self):
        if self.active:
            screen.draw.filled_rect(self.hitbox(), self.color)
        elif time.time() - self.warning < self.warning_duration:
            if int((time.time() - self.warning) * 10) % 2 == 0:
                screen.draw.filled_rect(self.hitbox(), "yellow")
    
    def update(self):
        if not self.active and time.time() - self.warning >= self.warning_duration:
            self.active = True
            self.active_start = time.time()

        if self.active and time.time() - self.active_start > 1:
            return False
        return True
        
    def hitbox(self):
        return Rect((self.x, self.y), (self.width, self.height))

    def start_warning(self):
        self.warning = time.time()

player = Player(player_x, player_y, PLAYER_SIZE, PLAYER_SPEED)

def spawn_laser():
    for _ in range((score // 10) + 1):
        laser_type = random.choice(["Horizontal", "Vertical"])
        
        if laser_type == "Horizontal":
            laser = Laser(0, random.randint(0, HEIGHT - 10), WIDTH, 10)
        else:
            laser = Laser(random.randint(0, WIDTH - 10), 0, 10, HEIGHT)
        
        laser.start_warning()
        lasers.append(laser)

def draw():
    screen.clear()
    player.draw()
    
    for laser in lasers:
        laser.draw()
    
    screen.draw.text(str(score), center=(WIDTH//2, 25), fontsize=30, color="white")
    
    if game_over:
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="white")

def update():
    global score
    first_laser = True
    
    if not game_over:
        player.move()
        
        for laser in lasers[:]:
            if not laser.update():
                if first_laser:
                    score += 1
                    first_laser = False
                lasers.remove(laser)
        
        for laser in lasers:
            if laser.active and player.hitbox().colliderect(laser.hitbox()):
                end_game()

def end_game():
    global game_over
    game_over = True
    clock.unschedule(spawn_laser)

def update_lasers():
    spawn_laser()

clock.schedule_interval(spawn_laser, 2.1)

pgzrun.go()
