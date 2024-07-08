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
    min_pipe_top = PIPE_GAP + 50  # Minimum distance from top to bottom of screen
    max_top_pipe_length = SCREEN_HEIGHT - min_pipe_top - PIPE_GAP - 50  # Maximum length of top pipe
    gap_start = random.randint(min_pipe_top, min_pipe_top + max_top_pipe_length - PIPE_GAP)
    
    top_pipe_height = gap_start
    bottom_pipe_y = gap_start + PIPE_GAP
    
   ed'])
    
    pipes.append(Pipe(xpos, top_pipe_height, top_pipe_height, color=pipe_color, inverted=True))  # Top pipe
    pipes.append(Pipe(xpos, bottom_pipe_y, SCREEN_HEIGHT - bottom_pipe_y, color=pipe_color))  # Bottom pipe
    
    return pipes

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Flappy Bird')

    .load('assets/sprites/background-night.png').convert()
    BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
    BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()
    BEGIN_IMAGE = pygame.transform.scale(BEGIN_IMAGE, (800, 600))  
    GAMEOVER_IMAGE = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
    GAMEOVER_IMAGE = pygame.transform.scale(GAMEOVER_IMAGE, (800, 400))  
   
    pygame.mixer.music.load(wing_sound)
    pygame.mixer.music.set_volume(0.5)

    
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
    pipe_frequency = 40
    frame_count = 0
    
    while begin:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                bird_group.sprite.bump()
                pygame.mixer.music.play()
                begin = False

        screen.blit(BACKGROUND, (0, 0))
        screen.blit(BEGIN_IMAGE, (340, 660))  # 
        
        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            ground = Ground(GROUND_WIDTH - 20)
            ground_group.add(ground)
        
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
                pygame.mixer.music.play()

        screen.blit(BACKGROUND, (0, 0))
        
        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            ground = Ground(GROUND_WIDTH - 20)
            ground_group.add(ground)

        if frame_count % pipe_frequency == 0:
            new_pipes = get_random_pipes(SCREEN_WIDTH * 2)
            pipe_group.add(new_pipes)

        for pipe in pipe_group.sprites():
            if not hasattr(pipe, 'scored') and pipe.rect.right < bird_group.sprite.rect.left:
                pipe.scored = True
                score += 5

        
        if score >= 150:
            bird_group.sprite.change_color('yellow')
        elif score >= 100:
            bird_group.sprite.change_color('red')

        bird_group.update()
        ground_group.update()
        pipe_group.update()

        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)

        font_size = 50
        flappy_font = pygame.font.Font('assets/font/Flappybird.ttf', font_size)
        score_surface_flappy = flappy_font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_surface_flappy, (10, 10))

        pygame.display.update()

        if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
            pygame.mixer.music.load(hit_sound)
            pygame.mixer.music.play()
            screen.blit(GAMEOVER_IMAGE, (340, 660)) 
            pygame.display.update()
            time.sleep(2)
            game_over = True
            break

        frame_count += 1

if __name__ == "__main__":
    main()
