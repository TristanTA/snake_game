import pygame

from ui.colors.colors import light_red, steel_blue

class Snake:
    def __init__(self):
        self.direction = 2
        self.current_coord = None

    def draw_snake(self, map):
        if self.current_coord is None:
            self.current_coord = [(map.left, map.top)]
            pygame.draw.rect(map.window, light_red, (
                map.left,
                map.top,
                map.gridsize,
                map.gridsize
            ))

        else:
            head_x, head_y = self.current_coord[-1]
            grid = map.gridsize

            # Movement logic
            if self.direction == 1:       # UP
                new_x = head_x
                new_y = head_y - grid

            elif self.direction == 2:     # RIGHT
                new_x = head_x + grid
                new_y = head_y

            elif self.direction == 3:     # DOWN
                new_x = head_x
                new_y = head_y + grid

            elif self.direction == 4:     # LEFT
                new_x = head_x - grid
                new_y = head_y

            new_head = (new_x, new_y)

            # --- BORDER COLLISION ---
            if (
                new_x < map.left or
                new_x + grid > map.right or
                new_y < map.top or
                new_y + grid > map.bottom
            ):
                return "GAME_OVER"

            # --- SELF COLLISION ---
            if new_head in self.current_coord:
                return "GAME_OVER"


            self.current_coord.append(new_head)

            pygame.draw.rect(map.window, light_red, (new_x, new_y, grid, grid))

            center = (new_x + grid // 2, new_y + grid // 2)
            pygame.draw.circle(map.window, light_red, center, grid // 2)

            tail_x, tail_y = self.current_coord[0]
            pygame.draw.rect(map.window, steel_blue, (tail_x, tail_y, grid, grid))   # erase old tail
            self.current_coord.pop(0)
        return self.current_coord
    
    def grow_snake(self):
        pass