import torch
import torch.nn as nn
import torch.nn.functional as F

class SnakeNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(9, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 3)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)

    def get_state_from_core(self, core):
        hx, hy = core.snake[-1]

        # choose closest fruit
        if core.fruits:
            fx, fy = min(core.fruits, key=lambda f: abs(f[0]-hx)+abs(f[1]-hy))
        else:
            fx, fy = hx, hy

        dx = (fx - hx) / core.width_cells
        dy = (fy - hy) / core.height_cells

        danger_left, danger_forward, danger_right = self._get_dangers(core)

        state = torch.tensor([
            float(hx),
            float(hy),
            float(dx),
            float(dy),
            float(core.direction),
            float(len(core.snake)),
            float(danger_left),
            float(danger_forward),
            float(danger_right),
        ], dtype=torch.float32)

        return state

    def _get_dangers(self, core):
        """
        Compute danger_left, danger_forward, danger_right as 0/1
        based on potential collisions in those relative directions.
        """
        dir_now = core.direction
        hx, hy = core.snake[-1]

        # Map direction rotation
        left_dir = {1: 4, 2: 1, 3: 2, 4: 3}[dir_now]
        right_dir = {1: 2, 2: 3, 3: 4, 4: 1}[dir_now]
        forward_dir = dir_now

        danger_left = int(self._would_collide(core, hx, hy, left_dir))
        danger_forward = int(self._would_collide(core, hx, hy, forward_dir))
        danger_right = int(self._would_collide(core, hx, hy, right_dir))

        return danger_left, danger_forward, danger_right
    
    
    def _would_collide(self, core, hx, hy, direction):
        if direction == 1:
            nx, ny = hx, hy - 1
        elif direction == 2:
            nx, ny = hx + 1, hy
        elif direction == 3:
            nx, ny = hx, hy + 1
        elif direction == 4:
            nx, ny = hx - 1, hy
        else:
            nx, ny = hx, hy

        # Wall collision
        if nx < 0 or nx >= core.width_cells:
            return True
        if ny < 0 or ny >= core.height_cells:
            return True

        # Self collision
        if (nx, ny) in core.snake:
            return True

        return False

    def predict_action(self, state_tensor, epsilon=0.0):
        """
        epsilon-greedy: with prob epsilon, pick random action.
        """
        if epsilon > 0.0 and torch.rand(1).item() < epsilon:
            return torch.randint(0, 3, (1,)).item()

        with torch.no_grad():
            if state_tensor.dim() == 1:
                state_tensor = state_tensor.unsqueeze(0)  # [1, 9]
            q = self.forward(state_tensor)
            return torch.argmax(q, dim=1).item()

    def train_step(self, optimizer, batch, gamma=0.99):
        states, actions, rewards, next_states, dones = batch
        # states: [B, 9], actions: [B], rewards: [B], etc.

        q_values = self(states)                        # [B, 3]
        q_values = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)  # [B]

        with torch.no_grad():
            next_q_values = self(next_states).max(1)[0]                 # [B]
            targets = rewards + gamma * next_q_values * (1 - dones)

        loss = F.mse_loss(q_values, targets)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        return loss.item()

    def save(self, path: str):
        torch.save(self.state_dict(), path)

    @classmethod
    def load(cls, path: str):
        model = cls()
        model.load_state_dict(torch.load(path, map_location="cpu"))
        model.eval()
        return model