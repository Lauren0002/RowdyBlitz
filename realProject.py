import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 850, 850
TITLE = "Rowdy Blitz"
GAME_DURATION = 60000  # 60 seconds in milliseconds

# pygame initialization
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Load the target image
target_image = pygame.image.load('target.png')
target_image = pygame.transform.scale(target_image, (50, 50))  # Adjust size as needed

# Player Class
#Load the player image
player_image = pygame.image.load('simple.png')
player_image = pygame.transform.scale(player_image, (50, 50))#Adjust size as needed

class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
            
        return False

def start_screen():
    win.fill((0, 0, 0))  # Fill the screen with black
    font_large = pygame.font.SysFont("Arial", 72)
    game_title_text = font_large.render("Rowdy Blitz", True, (255, 255, 255))
    game_title_rect = game_title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))

    font_small = pygame.font.SysFont("Arial", 36)
    start_text = font_small.render("Press SPACE to start", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))

    win.blit(game_title_text, game_title_rect)
    win.blit(start_text, start_rect)
    pygame.display.flip()

    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting_for_start = False


class Player(object):
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.image = player_image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def update(self):
        self.velX = 0
        self.velY = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed

        # Update position with velocity
        self.x += self.velX
        self.y += self.velY

        # Boundary checks
        if self.x < 0:  # Left boundary
            self.x = 0
        if self.x > WIDTH - self.rect.width:  # Right boundary
            self.x = WIDTH - self.rect.width
        if self.y < 0:  # Top boundary
            self.y = 0
        if self.y > HEIGHT - self.rect.height:  # Bottom boundary
            self.y = HEIGHT - self.rect.height

        #self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)
        self.rect.topleft = (self.x, self.y)

# Bullet Class
# Load the bullet image
bullet_image = pygame.image.load('Footballtwo.png')
bullet_image = pygame.transform.scale(bullet_image, (20, 20))  # Adjust the size as needed

class Bullet(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = bullet_image
        self.rect = self.image.get_rect(center=(x, y)) 
        self.speed = 8

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y
        #self.rect = pygame.Rect(int(self.x), int(self.y), 5, 10)

# Target Class
class Target(object):
    def __init__(self):
        self.image = target_image
        self.x = random.randint(50, WIDTH - 200)
        self.y = random.randint(50, HEIGHT - 200)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.speed = 3
        self.direction = random.choice(['left', 'right', 'up', 'down'])

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def update(self):
        if self.direction == 'left':
            self.x -= self.speed
            if self.x <= 0:
                self.direction = 'right'
        elif self.direction == 'right':
            self.x += self.speed
            if self.x >= WIDTH - 20:
                self.direction = 'left'
        elif self.direction == 'up':
            self.y -= self.speed
            if self.y <= 0:
                self.direction = 'down'
        elif self.direction == 'down':
            self.y += self.speed
            if self.y >= HEIGHT - 20:
                self.direction = 'up'

        self.rect = pygame.Rect(int(self.x), int(self.y), 20, 20)
        self.rect.x = self.x
        self.rect.y = self.y

# Points Class
class Points(object):
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 20)

    def draw(self, win):
        score_text = self.font.render("Score: {}".format(self.score), True, (255, 255, 255))
        win.blit(score_text, (10, 10))

def game_over_screen(score):
    win.fill((0, 0, 0))  # Fill the screen with black
    font = pygame.font.SysFont("Arial", 72)
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    
    font_small = pygame.font.SysFont("Arial", 48)
    go_runners_text = font_small.render(f"Go Runners! Score: {score}", True, (255, 255, 255))
    go_runners_rect = go_runners_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    
    win.blit(game_over_text, game_over_rect)
    win.blit(go_runners_text, go_runners_rect)
    pygame.display.flip()
    pygame.time.wait(6000)  # Display the screen for 3 seconds before exiting

# Player Initialization
player = Player(WIDTH / 2, HEIGHT - 50)
bullets = []
target = Target()  # Initial position of the target
points = Points()

# Record the start time
start_time = pygame.time.get_ticks()

#Initialize Pygame and Create Window
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

start_screen() #Show the start screen

# Main Loop
running = True
while running:
    elapsed_time = pygame.time.get_ticks() - start_time
    time_left = GAME_DURATION - elapsed_time
    if time_left <= 0:
        game_over_screen(points.score)
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.left_pressed = True
            if event.key == pygame.K_RIGHT:
                player.right_pressed = True
            if event.key == pygame.K_UP:
                player.up_pressed = True
            if event.key == pygame.K_DOWN:
                player.down_pressed = True
            if event.key == pygame.K_SPACE:
                # Shoot a bullet when the spacebar is pressed down
                bullet = Bullet(player.rect.centerx, player.rect.top)
                bullets.append(bullet)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.left_pressed = False
            if event.key == pygame.K_RIGHT:
                player.right_pressed = False
            if event.key == pygame.K_UP:
                player.up_pressed = False
            if event.key == pygame.K_DOWN:
                player.down_pressed = False

    player.update()
    target.update()

    #Check for collision between player and target
    if player.rect.colliderect(target.rect):
        game_over_screen(points.score) # Pass the current score to the game over screen
        break #Exit the game loop to end the game

        
    # Display time left
    seconds_left = max(0, time_left // 1000)  # Convert milliseconds to seconds, ensure non-negative
    font = pygame.font.SysFont("Arial", 30)
    timer_text = font.render(f"Time Left: {seconds_left} s", True, (255, 255, 255))
    win.blit(timer_text, (10, HEIGHT - 40))  # Position the timer text at the bottom-left corner

    #win.fill((12, 24, 36))
    pygame.display.flip()
    clock.tick(120) #Keep the game loop running at 60FPS

    win.fill((12, 24, 36))
    player.draw(win)


    # Update and draw bullets
    for bullet in bullets:
        bullet.update()
        bullet.draw(win)

    # Update and draw target
    target.update()
    target.draw(win)

    # Check for bullet collisions with the target
    for bullet in bullets[:]:  # Iterate over a copy of the bullets list
        if bullet.rect.colliderect(target.rect):
            print("Target Hit!")
            bullets.remove(bullet)  # Remove the bullet that hit the target
            target = Target()  # Reset target position
            points.score += 10  # Increment score

    # Draw score
    points.draw(win)

    # Update
    player.update()
    pygame.display.flip()

    clock.tick(120)

pygame.quit()
sys.exit()
