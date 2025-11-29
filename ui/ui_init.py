import pygame
import sys

from ui.map import Map
from ui.snake import Snake

class GameState:
    def __init__(self, WIDTH = 1200, HEIGHT = 600):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.map = Map(self.window)
        self.snake = Snake()
        self.clock = pygame.time.Clock()

    def start_ui(self):
        self.map.draw_map()
        pygame.display.flip()

        self.snake.draw_snake(self.map)
        pygame.display.flip()

        last_move_time = pygame.time.get_ticks()

        while True:
            MOVE_DELAY = 150
            now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.direction = 1
                    elif event.key == pygame.K_RIGHT:
                        self.snake.direction = 2
                    elif event.key == pygame.K_DOWN:
                        self.snake.direction = 3
                    elif event.key == pygame.K_LEFT:
                        self.snake.direction = 4
            
            if now - last_move_time > MOVE_DELAY:
                self.map.draw_fruit(self.snake)
                result = self.snake.draw_snake(self.map)
                if result == "GAME_OVER":
                    print("GAME OVER")
                    pygame.quit()
                    sys.exit()
                else:
                    self.snake.current_coord = result

                last_move_time = now

            pygame.display.update()
            self.clock.tick(60)