import random
import torch

from game.core_game import CoreGame
from model.snake_nn import SnakeNN
from model.replay_buffer import ReplayBuffer

def train_ai():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = SnakeNN().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    buffer = ReplayBuffer(capacity=100_000)

    gamma = 0.50
    batch_size = 64
    num_episodes = 4000
    epsilon_start = 1.0
    epsilon_end = 0.05
    epsilon_decay = num_episodes / 4 # linear over episodes

    for episode in range(num_episodes):
        game = CoreGame(30, 20)
        state = model.get_state_from_core(game).to(device)
        done = False
        total_reward = 0.0

        # Linear epsilon schedule
        epsilon = max(
            epsilon_end,
            epsilon_start - (epsilon_start - epsilon_end) * (episode / epsilon_decay)
        )

        while not done:
            # Epsilon-greedy action
            action = model.predict_action(state.cpu(), epsilon=epsilon)

            # No real time in headless mode; timestamp can be a step counter or 0
            _, reward, done = game.step(action, timestamp_ms=0)
            next_state = model.get_state_from_core(game).to(device)

            buffer.push(state.cpu(), action, reward, next_state.cpu(), done)
            state = next_state
            total_reward += reward

            # Learn from replay buffer
            if len(buffer) >= batch_size:
                batch = buffer.sample(batch_size)
                # move tensors to device
                batch = [b.to(device) for b in batch]
                loss = model.train_step(optimizer, batch, gamma=gamma)

        print(f"Episode {episode} | Epsilon {epsilon:.3f} | Reward {total_reward:.1f} | Length {len(game.snake)}")

        # Save occasionally
        if (episode + 1) % 100 == 0:
            model.save(f"snake_dqn_ep{episode+1}.pth")

    # Final save
    model.save("snake_dqn_final.pth")

if __name__ == "__main__":
    train_ai()