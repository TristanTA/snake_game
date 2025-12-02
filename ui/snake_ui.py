import pygame

class SnakeUI:
    def __init__(self, core_game, scale=30):
        pygame.init()
        self.core = core_game
        self.scale = scale

        w = core_game.width_cells * scale
        h = core_game.height_cells * scale

        self.window = pygame.display.set_mode((w, h))
        self.clock = pygame.time.Clock()

        # Font for debug text
        self.font = pygame.font.SysFont("consolas", 18)

        # This gets set each frame externally
        self.debug_info = None

    def draw(self):
        self.window.fill((0, 0, 0))

        self._draw_snake()
        self._draw_fruits()
        self._draw_debug_text()  # <<< NEW

        pygame.display.update()

    def _draw_snake(self):
        for (x, y) in self.core.snake:
            pygame.draw.rect(
                self.window,
                (200, 50, 50),
                (x * self.scale, y * self.scale, self.scale, self.scale)
            )

    def _draw_fruits(self):
        for (x, y) in self.core.fruits:
            pygame.draw.circle(
                self.window,
                (100, 255, 100),
                (x * self.scale + self.scale//2, y * self.scale + self.scale//2),
                self.scale//2
            )

    # -------------------------------------------------------
    # DEBUG TEXT OVERLAY
    # -------------------------------------------------------
    def _draw_debug_text(self):
        """
        debug_info must be a dictionary of values provided by watch_ai.py.
        Example:
            {
                "state": state_tensor,
                "action": action
            }
        """
        if not self.debug_info:
            return

        # Convert model input tensor to list of floats for display
        state_values = self.debug_info.get("state", None)
        action = self.debug_info.get("action", None)

        if state_values is not None:
            state_values = [float(v) for v in state_values.tolist()]

        lines = []
        lines.append("=== AI DEBUG ===")
        if state_values:
            lines.append(f"Inputs: {state_values}")
        if action is not None:
            lines.append(f"Action: {action}")

        # Render each line
        y = 5
        for line in lines:
            surf = self.font.render(line, True, (255, 255, 255))
            self.window.blit(surf, (5, y))
            y += 20