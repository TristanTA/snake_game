import pygame

from ui.colors.colors import steel_blue, black

def draw_map(window):
    window.fill(black)
    WIDTH, HEIGHT = window.get_size()

    pygame.draw.rect(window, steel_blue, (
        WIDTH * 0.025,
        HEIGHT * 0.025,
        WIDTH * 0.95,
        HEIGHT * 0.95
    ))

    left   = WIDTH * 0.025
    top    = HEIGHT * 0.025
    right  = WIDTH * 0.975
    bottom = HEIGHT * 0.975


    GRID_SIZE = 30

    params = {
        "left": left,
        "top": top,
        "right": right,
        "bottom": bottom,
        "grid_size": GRID_SIZE
    }
    return params