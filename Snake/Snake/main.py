import pygame
import sys
import os
from random import randrange

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
FPS = 60
TILE_SIZE = 80  # Tile size for the game
WINDOW_SIZE = 800  # Window size for the game

# Base path for loading assets
BASE_PATH = os.path.dirname(__file__)

# Function to load and scale images
def load_image(filename, scale_factor=1):
    image_path = os.path.join(BASE_PATH, filename)
    image = pygame.image.load(image_path)
    if scale_factor != 1:
        image = pygame.transform.scale(
            image, (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor))
        )
    return image

# Load images
background_img = load_image('backgrounds.png', scale_factor=1)  # Background remains unchanged
title_img = load_image('title.png', scale_factor=6)  # Title image (scaled)
play_img = load_image('play_button.png', scale_factor=2)
play_hover_img = load_image('play_button_hover.png', scale_factor=2)
quit_img = load_image('quit_button.png', scale_factor=2)
quit_hover_img = load_image('quit_button_hover.png', scale_factor=2)

# Title position
title_rect = title_img.get_rect(center=(SCREEN_WIDTH // 2, 150))  # Centered at the top
play_rect = play_img.get_rect(center=(SCREEN_WIDTH // 2, 400))  # Position play button
quit_rect = quit_img.get_rect(center=(SCREEN_WIDTH // 2, 550))  # Position quit button

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Opening Screen")
clock = pygame.time.Clock()

# --- Game Code ---
class Snake:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.body = [pygame.rect.Rect([game.WINDOW_SIZE // 2, game.WINDOW_SIZE // 2, self.size, self.size])]
        self.direction = pygame.Vector2(0, 0)
        self.new_block = False

        # Load both girl face images for animation, scaling them to the new size
        self.girl_face1 = pygame.image.load(os.path.join(self.game.base_path, 'girl_face1.png'))
        self.girl_face1 = pygame.transform.scale(self.girl_face1, (self.size, self.size))
        self.girl_face2 = pygame.image.load(os.path.join(self.game.base_path, 'girl_face2.png'))
        self.girl_face2 = pygame.transform.scale(self.girl_face2, (self.size, self.size))

        # Time to switch the images for girl face
        self.last_switch_time = pygame.time.get_ticks()
        self.current_girl_face = self.girl_face1  # Start with the first girl face image

        # Load the two mask images for animation, scaling them to the new size
        self.mask1 = pygame.image.load(os.path.join(self.game.base_path, 'mask1.png'))
        self.mask1 = pygame.transform.scale(self.mask1, (self.size, self.size))
        self.mask2 = pygame.image.load(os.path.join(self.game.base_path, 'mask2.png'))
        self.mask2 = pygame.transform.scale(self.mask2, (self.size, self.size))

        # Time to switch the images for masks
        self.last_mask_switch_time = pygame.time.get_ticks()
        self.current_mask = self.mask1  # Start with the first mask image

    def control(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and self.direction.y == 0:
                self.direction = pygame.Vector2(0, -1)
            elif event.key == pygame.K_s and self.direction.y == 0:
                self.direction = pygame.Vector2(0, 1)
            elif event.key == pygame.K_a and self.direction.x == 0:
                self.direction = pygame.Vector2(-1, 0)
            elif event.key == pygame.K_d and self.direction.x == 0:
                self.direction = pygame.Vector2(1, 0)

    def move(self):
        if self.direction.length_squared() == 0:
            return

        body_copy = self.body[:-1] if not self.new_block else self.body[:]
        new_head = self.body[0].move(self.direction.x * self.size, self.direction.y * self.size)
        body_copy.insert(0, new_head)
        self.body = body_copy
        self.new_block = False

    def check_collision(self):
        if self.body[0].collidelist(self.body[1:]) != -1:
            self.game.restart_game()

        if self.body[0].left < 0 or self.body[0].right > self.game.WINDOW_SIZE or \
           self.body[0].top < 0 or self.body[0].bottom > self.game.WINDOW_SIZE:
            self.game.restart_game()

    def add_block(self):
        self.new_block = True

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_switch_time >= 2000:  # 2 seconds
            self.current_girl_face = self.girl_face1 if self.current_girl_face == self.girl_face2 else self.girl_face2
            self.last_switch_time = current_time

        if current_time - self.last_mask_switch_time >= 1000:  # 1 second
            self.current_mask = self.mask1 if self.current_mask == self.mask2 else self.mask2
            self.last_mask_switch_time = current_time

    def draw(self):
        for i, block in enumerate(self.body):
            if i == 0:
                self.game.screen.blit(self.current_girl_face, block.topleft)
            else:
                self.game.screen.blit(self.current_mask, block.topleft)

class Food:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pygame.rect.Rect([0, 0, self.size, self.size])
        self.rect.topleft = self.get_random_position()

        self.food_image1 = pygame.image.load(os.path.join(self.game.base_path, 'kitty_face1.png'))
        self.food_image1 = pygame.transform.scale(self.food_image1, (self.size, self.size))
        self.food_image2 = pygame.image.load(os.path.join(self.game.base_path, 'kitty_face2.png'))
        self.food_image2 = pygame.transform.scale(self.food_image2, (self.size, self.size))

        self.last_switch_time = pygame.time.get_ticks()
        self.current_image = self.food_image1

    def get_random_position(self):
        x = randrange(0, self.game.WINDOW_SIZE - self.size, self.size)
        y = randrange(0, self.game.WINDOW_SIZE - self.size, self.size)
        return x, y

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_switch_time >= 2000:  # 2 seconds
            self.current_image = self.food_image1 if self.current_image == self.food_image2 else self.food_image2
            self.last_switch_time = current_time

    def draw(self):
        self.game.screen.blit(self.current_image, self.rect.topleft)

class Game:
    def __init__(self):
        self.TILE_SIZE = TILE_SIZE
        self.WINDOW_SIZE = WINDOW_SIZE
        self.screen = pygame.display.set_mode([self.WINDOW_SIZE] * 2)
        self.clock = pygame.time.Clock()
        self.running = True
        self.base_path = os.path.dirname(__file__)

        self.background_image = pygame.image.load(os.path.join(self.base_path, 'background.png'))
        self.background_image = pygame.transform.scale(self.background_image, (self.WINDOW_SIZE, self.WINDOW_SIZE))
        pygame.mixer.music.load(os.path.join(self.base_path, 'background_music.mp3'))
        pygame.mixer.music.play(-1)

        self.snake = Snake(self)
        self.food = Food(self)

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.snake.control(event)

    def update(self):
        self.snake.move()
        if self.snake.body[0].colliderect(self.food.rect):
            self.snake.add_block()
            self.food.rect.topleft = self.food.get_random_position()
        self.snake.check_collision()

        self.snake.update()
        self.food.update()

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.snake.draw()
        self.food.draw()
        pygame.display.flip()

    def restart_game(self):
        self.__init__()

    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()
            self.clock.tick(10)

# --- Title Screen ---
def main_menu():
    running = True
    pygame.mixer.music.load(os.path.join(BASE_PATH, 'titlesong.mp3'))  # Load the title song
    pygame.mixer.music.play(-1, 0.0)  # Loop the title song indefinitely

    while running:
        screen.blit(background_img, (0, 0))  # Draw the background
        screen.blit(title_img, title_rect.topleft)  # Draw the title
        screen.blit(play_img, play_rect.topleft)  # Draw play button
        screen.blit(quit_img, quit_rect.topleft)  # Draw quit button

        # Event handling
        mouse_pos = pygame.mouse.get_pos()
        if play_rect.collidepoint(mouse_pos):
            screen.blit(play_hover_img, play_rect.topleft)
        else:
            screen.blit(play_img, play_rect.topleft)

        if quit_rect.collidepoint(mouse_pos):
            screen.blit(quit_hover_img, quit_rect.topleft)
        else:
            screen.blit(quit_img, quit_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(mouse_pos):
                    print("Play button clicked")
                    game = Game()
                    game.run()
                    running = False
                if quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(FPS)

# Run the main menu
main_menu()
