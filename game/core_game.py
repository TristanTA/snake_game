import random

class CoreGame:
    def __init__(self, width_cells=30, height_cells=20, gridsize=30):
        self.width_cells = width_cells
        self.height_cells = height_cells
        self.gridsize = gridsize

        self.reset()

    def reset(self):
        self.direction = 2  # 1=UP,2=RIGHT,3=DOWN,4=LEFT
        self.snake = [(0, 0)]
        self.length = 1
        self.alive = True
        self.fruits = []
        self.tick_since_fruit = 0
        self.target_fruit_count = 1
        self.last_distance = None

        self.steps = 0
        self.level_timer = 0
        self.level_up_delay = 10000  # ms
        self.last_timestamp = 0

        return self.get_state()

    def step(self, action, timestamp_ms):
        reward = 0
        if not self.alive:
            return self.get_state(), 0.0, True

        self._apply_action(action)
        self._move_snake()

        # --- death penalty ---
        if self._check_collisions():
            self.alive = False
            return self.get_state(), reward, True

        hx, hy = self.snake[-1]

        # --- eat fruit reward ---
        length = len(self.snake)
        ate = self._check_eat_fruit()
        if ate:
            reward += (2 ** length)
            self.tick_since_fruit = 0
        else:
            self.tick_since_fruit += 1
            reward -= self.tick_since_fruit / 10

        if self.fruits:
            fx, fy = min(self.fruits, key=lambda f: abs(f[0]-hx) + abs(f[1]-hy))
        else:
            fx, fy = hx, hy

        dx_raw = fx - hx
        dy_raw = fy - hy
        distance = abs(dx_raw) + abs(dy_raw)

        # Distance shaping reward
        if self.last_distance is not None:
            if distance < self.last_distance:
                reward += 1.0 * length
            else:
                reward -= self.tick_since_fruit / 10

        if self.tick_since_fruit > 100:
            self.alive = False
            reward -= 100
            return self.get_state(), reward, True

        self.last_distance = distance

        self._update_fruit_spawn(timestamp_ms)

        self.steps += 1

        return self.get_state(), reward, False

    def _apply_action(self, action):
        dir = self.direction

        if action == 0:  # left
            if dir == 1: dir = 4
            elif dir == 2: dir = 1
            elif dir == 3: dir = 2
            elif dir == 4: dir = 3

        elif action == 2:  # right
            if dir == 1: dir = 2
            elif dir == 2: dir = 3
            elif dir == 3: dir = 4
            elif dir == 4: dir = 1

        # action == 1: straight → do nothing

        self.direction = dir

    def _move_snake(self):
        head_x, head_y = self.snake[-1]

        if self.direction == 1:
            new_head = (head_x, head_y - 1)
        elif self.direction == 2:
            new_head = (head_x + 1, head_y)
        elif self.direction == 3:
            new_head = (head_x, head_y + 1)
        elif self.direction == 4:
            new_head = (head_x - 1, head_y)

        self.snake.append(new_head)
        self.snake.pop(0)

    def _check_collisions(self):
        head_x, head_y = self.snake[-1]

        if head_x < 0 or head_x >= self.width_cells:
            return True
        if head_y < 0 or head_y >= self.height_cells:
            return True

        if len(self.snake) != len(set(self.snake)):
            return True

        return False

    def _check_eat_fruit(self):
        head = self.snake[-1]

        for f in self.fruits:
            if f == head:
                self.fruits.remove(f)
                self._grow_snake()
                return True
        return False

    def _grow_snake(self):
        tail = self.snake[0]
        self.snake.insert(0, tail)

    def _update_fruit_spawn(self, now):
        if now - self.last_timestamp >= self.level_up_delay:
            self.target_fruit_count += 1
            self.last_timestamp = now

        while len(self.fruits) < self.target_fruit_count:
            self._spawn_one_fruit()

    def _spawn_one_fruit(self):
        possible = [
            (x, y)
            for x in range(self.width_cells)
            for y in range(self.height_cells)
            if (x, y) not in self.snake and (x, y) not in self.fruits
        ]

        if not possible:
            return

        fruit = random.choice(possible)
        self.fruits.append(fruit)

    def get_state(self):
        return {
            "snake": self.snake[:],
            "direction": self.direction,
            "fruits": self.fruits[:],
            "alive": self.alive
        }