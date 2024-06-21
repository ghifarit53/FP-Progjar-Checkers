import pygame
from constants import Constants, Colors
from board import Board
from game import handle_player_turn, handle_ai_turn
from menu import draw_menu

def main():
    pygame.init()
    aspect_ratio = Constants.WIDTH / Constants.HEIGHT
    min_width, min_height = 300, 300
    surface = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Checkers')

    font = pygame.font.Font(None, 74)
    board = Board()
    clock = pygame.time.Clock()
    running = True
    game_mode = None
    ai_turn = False
    player_turn = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                new_width = max(event.w, min_width)
                new_height = max(event.h, min_height)
                if new_width / new_height > aspect_ratio:
                    new_width = int(new_height * aspect_ratio)
                else:
                    new_height = int(new_width / aspect_ratio)
                surface = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_mode is None:
                    pos = pygame.mouse.get_pos()
                    pvp_rect, pvai_rect = draw_menu(surface, font)
                    if pvp_rect.collidepoint(pos):
                        game_mode = "pvp"
                    elif pvai_rect.collidepoint(pos):
                        game_mode = "pvai"
                else:
                    pos = pygame.mouse.get_pos()
                    if game_mode == "pvp":
                        player_turn = handle_player_turn(board, surface, player_turn)
                    elif game_mode == "pvai":
                        player_turn = handle_player_turn(board, surface, player_turn)
                        if not player_turn:
                            ai_turn = True

        if game_mode is None:
            draw_menu(surface, font)
        else:
            if game_mode == "pvai" and not player_turn and ai_turn:
                ai_turn = handle_ai_turn(board, surface, ai_turn)
                if not ai_turn:
                    player_turn = True

            board.draw(surface)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()