import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game  # Reference to the main game object
        self.type = e_type
        self.pos = list(pos)  # Position as a list [x, y] to be mutable
        self.size = size
        self.velocity = [0, 0]  # Initial velocity

    def update(self, movement=(0, 0)):
        # Update the position based on movement and velocity
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]  # Move horizontally
        self.pos[1] += frame_movement[1]  # Move vertically (none in this case)

    def render(self, surf):
        # Draw the entity's sprite at its position
        surf.blit(self.game.assets['player'], self.pos)
