import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Ninas Mask Valley')
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()

        # Load background image
        self.background = pygame.image.load('Drawings/Desenhos/Capa/nina.png').convert()

        # Load button images (normal and hovered)
        self.play_button_normal = pygame.image.load('Data/Desenhos/Capa/Play/PlayOn.png').convert_alpha()
        self.play_button_hover = pygame.image.load('Drawings/Desenhos/Capa/Play/PlayPressed.png').convert_alpha()
        self.exit_button_normal = pygame.image.load('Drawings/Desenhos/Capa/Exit/ExitOn.png').convert_alpha()
        self.exit_button_hover = pygame.image.load('Drawings/Desenhos/Capa/Exit/ExitPressed.png').convert_alpha()

        # Set button positions
        self.play_button_rect = self.play_button_normal.get_rect(center=(960, 450))  # Center of the screen for Play
        self.exit_button_rect = self.exit_button_normal.get_rect(center=(960, 600))  # Center below Play

        # Game state
        self.in_menu = True

    def main_menu(self):
        while self.in_menu:
            self.screen.blit(self.background, (0, 0))  # Draw background

            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Check if hovering over Play button
            if self.play_button_rect.collidepoint(mouse_pos):
                self.screen.blit(self.play_button_hover, self.play_button_rect)
            else:
                self.screen.blit(self.play_button_normal, self.play_button_rect)

            # Check if hovering over Exit button
            if self.exit_button_rect.collidepoint(mouse_pos):
                self.screen.blit(self.exit_button_hover, self.exit_button_rect)
            else:
                self.screen.blit(self.exit_button_normal, self.exit_button_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Check for mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button_rect.collidepoint(mouse_pos):
                        self.start_game()
                    if self.exit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            self.clock.tick(60)

    def start_game(self):
        # This function will start the actual game
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Game logic here

            pygame.display.update()
            self.clock.tick(60)

    def run(self):
        self.main_menu()

# Run the game
if __name__ == '__main__':
    Game().run()
