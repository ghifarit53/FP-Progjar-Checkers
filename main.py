import pygame
from constants import Constants
from board import Board

def main():
    # Initialize Pygame
    pygame.init()
    WIN = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
    pygame.display.set_caption('Checkers')

    # Create the board
    board = Board()
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)  # Set the frame rate to 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the game loop if the user quits

        # Draw the board and update the display
        board.draw(WIN)
        pygame.display.flip()

    pygame.quit()  # Quit Pygame

if __name__ == '__main__':
    main()
