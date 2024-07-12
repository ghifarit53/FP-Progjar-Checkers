import pygame
from constants import Constants
from board import Board

def draw_menu(surface):
    surface.fill(Colors.BLACK)
    font = pygame.font.SysFont('Arial', 50)
    text = font.render('Checkers', True, Colors.WHITE)
    surface.blit(text, (Constants.WIDTH // 2 - text.get_width() // 2, Constants.HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()

def main():
    pygame.init()
    aspect_ratio = Constants.WIDTH / Constants.HEIGHT  
    min_width, min_height = 300, 300
    surface = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Checkers')
    board = Board()
    clock = pygame.time.Clock()
    running = True
    in_menu = True

    while running:
        if in_menu:
            draw_menu(surface)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        in_menu = False
                elif event.type == pygame.VIDEORESIZE:
                    new_width = max(event.w, min_width)
                    new_height = max(event.h, min_height)
                    if new_width / new_height > aspect_ratio:
                        new_width = int(new_height * aspect_ratio)
                    else:
                        new_height = int(new_width / aspect_ratio)
                    surface = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // Constants.SQUARE_SIZE, x // Constants.SQUARE_SIZE
                    board.select_piece(row, col)
                elif event.type == pygame.VIDEORESIZE:
                    new_width = max(event.w, min_width)
                    new_height = max(event.h, min_height)
                    if new_width / new_height > aspect_ratio:
                        new_width = int(new_height * aspect_ratio)
                    else:
                        new_height = int(new_width / aspect_ratio)
                    surface = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

            board.draw(surface)
            pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
