import pygame

from ui.colors.colors import light_red, steel_blue

def draw_snake(window, params, current_coord = None, direction: int = 2):
    if current_coord is None:
        current_coord = [(params["left"], params["top"])]
        pygame.draw.rect(window, light_red, (
            params["left"],
            params["top"],
            params["grid_size"],
            params["grid_size"]
        ))

    else:
        head_x, head_y = current_coord[-1]
        grid = params["grid_size"]

        # Movement logic
        if direction == 1:       # UP
            new_x = head_x
            new_y = head_y - grid

        elif direction == 2:     # RIGHT
            new_x = head_x + grid
            new_y = head_y

        elif direction == 3:     # DOWN
            new_x = head_x
            new_y = head_y + grid

        elif direction == 4:     # LEFT
            new_x = head_x - grid
            new_y = head_y

        new_head = (new_x, new_y)

        # --- BORDER COLLISION ---
        if (
            new_x < params["left"] or
            new_x + grid > params["right"] or
            new_y < params["top"] or
            new_y + grid > params["bottom"]
        ):
            return "GAME_OVER"

        # --- SELF COLLISION ---
        if new_head in current_coord:
            return "GAME_OVER"


        current_coord.append(new_head)

        pygame.draw.rect(window, light_red, (new_x, new_y, grid, grid))

        center = (new_x + grid // 2, new_y + grid // 2)
        pygame.draw.circle(window, light_red, center, grid // 2)

        tail_x, tail_y = current_coord[0]
        pygame.draw.rect(window, steel_blue, (tail_x, tail_y, grid, grid))   # erase old tail
        current_coord.pop(0)

    return current_coord