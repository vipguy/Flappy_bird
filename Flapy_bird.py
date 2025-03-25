import pygame
import random
import time

# Constants
SCREEN_WIDTH = 1480
SCREEN_HEIGHT = 1920
SPEED = 30
GRAVITY = 3
GAME_SPEED = 15

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 425

PIPE_WIDTH = 200
PIPE_GAP = 350  
# Sound files
wing_sound = 'assets/audio/wing.wav'
hit_sound = 'assets/audio/hit.wav'

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color = 'blue'  # Initial color
        self.images = {
            'blue': [
                pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()
            ],
            'red': [
                pygame.image.load('assets/sprites/redbird-upflap.png').convert_alpha(),
                pygame.image.load('assets/sprites/redbird-midflap.png').convert_alpha(),
                pygame.image.load('assets/sprites/redbird-downflap.png').convert_alpha()
            ],
            'yellow': [
                pygame.image.load('assets/sprites/yellowbird-upflap.png').convert_alpha(),
                pygame.image.load('assets/sprites/yellowbird-midflap.png').convert_alpha(),
                pygame.image.load('assets/sprites/yellowbird-downflap.png').convert_alpha()
            ]
        }
        self.scaled_images = {color: [pygame.transform.scale(img, (100, 70)) for img in imgs] for color, imgs in self.images.items()}
        self.speed = SPEED
        self.current_image = 0
        self.image = self.scaled_images[self.color][self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.scaled_images[self.color][self.current_image]
        self.speed += GRAVITY
        self.rect.y += self.speed

    def bump(self):
        self.speed = -SPEED

    def change_color(self, color):
        self.color = color
        self.image = self.scaled_images[self.color][self.current_image]

class Pipe(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, height, color='green', inverted=False):
        super().__init__()
        self.color = color
        self.image = pygame.image.load(f'assets/sprites/pipe-{self.color}.png').convert_alpha()
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, height))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.bottom = ypos if inverted else ypos + height
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= GAME_SPEED

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        super().__init__()
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(x=xpos, y=SCREEN_HEIGHT - GROUND_HEIGHT)

    def update(self):
        self.rect.x -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect.right < 0

def get_random_pipes(xpos):
    pipes = []
    min_pipe_top = PIPE_GAP + 50
    max_top_pipe_length = SCREEN_HEIGHT - min_pipe_top - PIPE_GAP - 50
    gap_start = random.randint(min_pipe_top, min_pipe_top + max_top_pipe_length - PIPE_GAP)
    pipe_color = random.choice(['green', 'red'])
    
    pipes.append(Pipe(xpos, gap_start, gap_start, color=pipe_color, inverted=True))
    pipes.append(Pipe(xpos, gap_start + PIPE_GAP, SCREEN_HEIGHT - (gap_start + PIPE_GAP), color=pipe_color))
    
    return pipes

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Flappy Bird')

    BACKGROUND = pygame.image.load('assets/sprites/background-night.png').convert()
    BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
    BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()
    BEGIN_IMAGE = pygame.transform.scale(BEGIN_IMAGE, (800, 600))  
    GAMEOVER_IMAGE = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
    GAMEOVER_IMAGE = pygame.transform.scale(GAMEOVER_IMAGE, (800, 400))  

    bird_group = pygame.sprite.GroupSingle(Bird())
    ground_group = pygame.sprite.Group()
    pipe_group = pygame.sprite.Group()

    for i in range(2):
        ground = Ground(GROUND_WIDTH * i)
        ground_group.add(ground)

    clock = pygame.time.Clock()
    begin = True
    game_over = False
    score = 0
    frame_count = 0
    
    while begin:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                bird_group.sprite.bump()
                pygame.mixer.Sound(wing_sound).play()
                begin = False

        screen.blit(BACKGROUND, (0, 0))
        screen.blit(BEGIN_IMAGE, (340, 660))  
        ground_group.update()
        bird_group.draw(screen)
        ground_group.draw(screen)
        pygame.display.update()

    while not game_over:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                bird_group.sprite.bump()
                pygame.mixer.Sound(wing_sound).play()

        screen.blit(BACKGROUND, (0, 0))
        pipe_group.update()
        ground_group.update()
        bird_group.update()
        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)
        pygame.display.update()

if __name__ == "__main__":
    main()
