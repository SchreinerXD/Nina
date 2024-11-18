import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
FPS = 60

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

# Title image (scaled to 6x original size)
title_img = load_image('title.png', scale_factor=6)

# Play button images (scaled to 2x original size)
play_img = load_image('play_button.png', scale_factor=2)
play_hover_img = load_image('play_button_hover.png', scale_factor=2)

# Quit button images (scaled to 2x original size)
quit_img = load_image('quit_button.png', scale_factor=2)
quit_hover_img = load_image('quit_button_hover.png', scale_factor=2)

# Title position
title_rect = title_img.get_rect(center=(SCREEN_WIDTH // 2, 150))  # Centered at the top

# Button positions (adjust for increased size)
play_rect = play_img.get_rect(center=(SCREEN_WIDTH // 2, 400))  # Position play button
quit_rect = quit_img.get_rect(center=(SCREEN_WIDTH // 2, 550))  # Position quit button

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Opening Screen")
clock = pygame.time.Clock()

# Main loop
def main_menu():
    running = True
    while running:
        screen.blit(background_img, (0, 0))  # Draw the background
        screen.blit(title_img, title_rect.topleft)  # Draw the title

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw buttons and check hover
        if play_rect.collidepoint(mouse_pos):
            screen.blit(play_hover_img, play_rect.topleft)
        else:
            screen.blit(play_img, play_rect.topleft)

        if quit_rect.collidepoint(mouse_pos):
            screen.blit(quit_hover_img, quit_rect.topleft)
        else:
            screen.blit(quit_img, quit_rect.topleft)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(mouse_pos):
                    print("Play button clicked")  # Replace with your game function
                    running = False  # Exit the menu for now
                if quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

# Run the main menu
main_menu()
