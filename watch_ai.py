import pygame
import torch

from game.core_game import CoreGame
from ui.snake_ui import SnakeUI
from model.snake_nn import SnakeNN

def watch_ai_play(model_path="snake_dqn_final.pth"):
    game = CoreGame(30, 20)
    ui = SnakeUI(game)

    model = SnakeNN.load(model_path)
    model.eval()

    running = True
    while running and game.alive:
        timestamp = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        state_tensor = model.get_state_from_core(game)
        action = model.predict_action(state_tensor, epsilon=0.0)

        # Step the game
        _, _, done = game.step(action, timestamp)

        # >>> NEW: deliver debug info to UI
        ui.debug_info = {
            "state": state_tensor.cpu(),
            "action": action
        }

        ui.draw()
        ui.clock.tick(12)

        if done:
            running = False


if __name__ == "__main__":
    watch_ai_play()