import random
from collections import deque
import torch

class ReplayBuffer:
    def __init__(self, capacity: int):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        """
        state, next_state: torch.tensor([9])
        action: int
        reward: float
        done: bool
        """
        self.buffer.append((
            state.detach(), # keep a copy, no grad
            int(action),
            float(reward),
            next_state.detach(),
            bool(done)
        ))

    def sample(self, batch_size: int):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.stack(states)                     # [B, 9]
        next_states = torch.stack(next_states)           # [B, 9]
        actions = torch.tensor(actions, dtype=torch.long)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.float32)  # 1.0 if done else 0.0

        return states, actions, rewards, next_states, dones

    def __len__(self):
        return len(self.buffer)
