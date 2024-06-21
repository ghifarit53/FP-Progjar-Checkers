import pygame
from constants import Constants
from board import Board

def main():
    # Initialize Pygame
    pygame.init()
    aspect_ratio = Constants.WIDTH / Constants.HEIGHT  # Aspect ratio (width / height)
    min_width, min_height = 300, 300
    surface = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT), pygame.RESIZABLE)
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

            if event.type == pygame.VIDEORESIZE:
                # Calculate the new width and height to maintain the aspect ratio
                new_width = max(event.w, min_width)
                new_height = max(event.h, min_height)
                # Adjust dimensions to maintain the aspect ratio
                if new_width / new_height > aspect_ratio:
                    new_width = int(new_height * aspect_ratio)
                else:
                    new_height = int(new_width / aspect_ratio)
                surface = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)


        # Draw the board and update the display
        board.draw(surface)
        pygame.display.flip()

    pygame.quit()  # Quit Pygame

if __name__ == '__main__':
    main()
