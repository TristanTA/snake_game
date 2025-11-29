import pygame
import sys

from ui.map import draw_map
from ui.snake import draw_snake

def start_ui():
    pygame.init()

    WIDTH, HEIGHT = 1200, 600
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    
    clock = pygame.time.Clock()

    params = draw_map(window)
    pygame.display.flip()

    current_coord = draw_snake(window, params)
    pygame.display.flip()

    last_move_time = pygame.time.get_ticks()
    direction = 2

    while True:
        MOVE_DELAY = 150
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = 1
                elif event.key == pygame.K_RIGHT:
                    direction = 2
                elif event.key == pygame.K_DOWN:
                    direction = 3
                elif event.key == pygame.K_LEFT:
                    direction = 4
        
        if now - last_move_time > MOVE_DELAY:
            result = draw_snake(window, params, current_coord, direction)
            if result == "GAME_OVER":
                print("GAME OVER")
                pygame.quit()
                sys.exit()
            else:
                current_coord = result

            last_move_time = now

        pygame.display.update()
        clock.tick(60)