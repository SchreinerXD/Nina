import pygame as pg
import sys
from random import randrange
import os

class Snake:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.body = [pg.rect.Rect([game.WINDOW_SIZE // 2, game.WINDOW_SIZE // 2, self.size, self.size])]
        self.direction = pg.Vector2(0, 0)
        self.new_block = False

        # Load both girl face images for animation, scaling them to the new size
        self.girl_face1 = pg.image.load(os.path.join(self.game.base_path, 'girl_face1.png'))
        self.girl_face1 = pg.transform.scale(self.girl_face1, (self.size, self.size))
        self.girl_face2 = pg.image.load(os.path.join(self.game.base_path, 'girl_face2.png'))
        self.girl_face2 = pg.transform.scale(self.girl_face2, (self.size, self.size))

        # Time to switch the images for girl face
        self.last_switch_time = pg.time.get_ticks()
        self.current_girl_face = self.girl_face1  # Start with the first girl face image

        # Load the two mask images for animation, scaling them to the new size
        self.mask1 = pg.image.load(os.path.join(self.game.base_path, 'mask1.png'))
        self.mask1 = pg.transform.scale(self.mask1, (self.size, self.size))
        self.mask2 = pg.image.load(os.path.join(self.game.base_path, 'mask2.png'))
        self.mask2 = pg.transform.scale(self.mask2, (self.size, self.size))

        # Time to switch the images for masks
        self.last_mask_switch_time = pg.time.get_ticks()
        self.current_mask = self.mask1  # Start with the first mask image

    def control(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and self.direction.y == 0:
                self.direction = pg.Vector2(0, -1)
            elif event.key == pg.K_s and self.direction.y == 0:
                self.direction = pg.Vector2(0, 1)
            elif event.key == pg.K_a and self.direction.x == 0:
                self.direction = pg.Vector2(-1, 0)
            elif event.key == pg.K_d and self.direction.x == 0:
                self.direction = pg.Vector2(1, 0)

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
        """Switch the girl face image every 2 seconds."""
        current_time = pg.time.get_ticks()
        if current_time - self.last_switch_time >= 2000:  # 2 seconds
            # Switch the girl face image
            self.current_girl_face = self.girl_face1 if self.current_girl_face == self.girl_face2 else self.girl_face2
            self.last_switch_time = current_time  # Reset the time counter

        # Switch the mask image every 1 second
        if current_time - self.last_mask_switch_time >= 1000:  # 1 second
            self.current_mask = self.mask1 if self.current_mask == self.mask2 else self.mask2
            self.last_mask_switch_time = current_time  # Reset the time counter

    def draw(self):
        for i, block in enumerate(self.body):
            if i == 0:  # Draw the animated girl face for the head
                self.game.screen.blit(self.current_girl_face, block.topleft)
            else:  # Draw the animated mask for the body
                self.game.screen.blit(self.current_mask, block.topleft)

class Food:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, self.size, self.size])
        self.rect.topleft = self.get_random_position()

        # Load both kitty face images for animation, scaling them to the new size
        self.food_image1 = pg.image.load(os.path.join(self.game.base_path, 'kitty_face1.png'))
        self.food_image1 = pg.transform.scale(self.food_image1, (self.size, self.size))
        self.food_image2 = pg.image.load(os.path.join(self.game.base_path, 'kitty_face2.png'))
        self.food_image2 = pg.transform.scale(self.food_image2, (self.size, self.size))

        # Time to switch the images for kitty face
        self.last_switch_time = pg.time.get_ticks()
        self.current_image = self.food_image1  # Start with the first image

    def get_random_position(self):
        """Ensure the food appears within visible screen bounds."""
        x = randrange(0, self.game.WINDOW_SIZE - self.size, self.size)
        y = randrange(0, self.game.WINDOW_SIZE - self.size, self.size)
        return x, y

    def update(self):
        """Switch the food image every 2 seconds."""
        current_time = pg.time.get_ticks()
        if current_time - self.last_switch_time >= 2000:  # 2 seconds
            # Switch the image
            self.current_image = self.food_image1 if self.current_image == self.food_image2 else self.food_image2
            self.last_switch_time = current_time  # Reset the time counter

    def draw(self):
        self.game.screen.blit(self.current_image, self.rect.topleft)

class Game:
    def __init__(self):
        pg.init()
        self.TILE_SIZE = 80  # Updated size to 80
        self.WINDOW_SIZE = 800  # Keep the screen size the same
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.running = True
        self.base_path = os.path.dirname(__file__)

        # Load background and music
        self.background_image = pg.image.load(os.path.join(self.base_path, 'background.png'))
        self.background_image = pg.transform.scale(self.background_image, (self.WINDOW_SIZE, self.WINDOW_SIZE))
        pg.mixer.music.load(os.path.join(self.base_path, 'background_music.mp3'))
        pg.mixer.music.play(-1)

        self.snake = Snake(self)
        self.food = Food(self)

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            self.snake.control(event)

    def update(self):
        self.snake.move()
        if self.snake.body[0].colliderect(self.food.rect):
            self.snake.add_block()
            self.food.rect.topleft = self.food.get_random_position()
        self.snake.check_collision()

        # Update the food and snake animations
        self.snake.update()
        self.food.update()

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.snake.draw()
        self.food.draw()
        pg.display.flip()

    def restart_game(self):
        self.__init__()

    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()
            self.clock.tick(10)

if __name__ == '__main__':
    game = Game()
    game.run()
