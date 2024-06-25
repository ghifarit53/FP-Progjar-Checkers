import pygame
from constants import Constants, Colors

def play_vs_player(board, pos):
    if board.handle_click(pos):
        return True
    return False
