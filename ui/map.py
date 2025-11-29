import pygame
import random

from ui.colors.colors import steel_blue, black, light_green
from ui.snake import Snake

class Map:
    def __init__(self, window, gridsize = 30):
        self.window = window
        self.window_width = window.get_width()
        self.window_height = window.get_height()

        self.left = int(self.window_width * 0.025)
        self.right = int(self.window_width * 0.975)
        self.top = int(self.window_height * 0.025)
        self.bottom = int(self.window_height * 0.975)


        self.gridsize = gridsize
        self.width_grid_count = (self.right - self.left) / self.gridsize
        self.height_grid_count = (self.bottom - self.top) / self.gridsize

        self.current_fruit = []

    def draw_map(self):
        self.window.fill(black)
        pygame.draw.rect(
            self.window,
            steel_blue,
            (
                self.left,
                self.top,
                self.right - self.left,
                self.bottom - self.top
            )
        )

    def coord_to_grid_index(self, coord):
        x, y = coord
        col = int((x - self.left) // self.gridsize)
        row = int((y - self.top) // self.gridsize)
        cols = int(self.width_grid_count)
        return row * cols + col
    
    def grid_index_to_coord(self, index):
        cols = int(self.width_grid_count)
        row = index // cols
        col = index % cols
        x = self.left + col * self.gridsize
        y = self.top + row * self.gridsize
        return (x, y)

    def draw_fruit(self, snake: Snake):
        cols = int(self.width_grid_count)
        rows = int(self.height_grid_count)
        total_grids = cols * rows

        possible_grids = list(range(total_grids))

        snake_grid_indexes = [
            self.coord_to_grid_index(coord)
            for coord in snake.current_coord
        ]

        for idx in snake_grid_indexes:
            if idx in possible_grids:
                possible_grids.remove(idx)

        fruit_index = random.choice(possible_grids)
        fruit_x, fruit_y = self.grid_index_to_coord(fruit_index)
        center = (
            fruit_x + self.gridsize // 2,
            fruit_y + self.gridsize // 2
        )
        radius = self.gridsize // 2
        pygame.draw.circle(self.window, light_green, center, radius)
        self.current_fruit.append((fruit_x, fruit_y, fruit_index))