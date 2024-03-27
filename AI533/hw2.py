#AI533 hw2 Q3 - Ju

import numpy as np
import matplotlib.pyplot as plt

class GridWorld:
    def __init__(self):
        self.grid_size = 4
        self.num_states = self.grid_size ** 2
        self.start_state = 0
        self.goal_state = 15
        self.wildfire_states = [1, 2] 
        self.water_states = [9, 10]
        self.reward_for_states = np.full(self.num_states, -1.0)
        for state in self.wildfire_states:
            self.reward_for_states[state] = -10
        for state in self.water_states:
            self.reward_for_states[state] = -5
        self.reward_for_states[self.goal_state] = 100

        self.actions = ['left', 'up', 'right', 'down']
        self.action_effects = [-1, -self.grid_size, 1, self.grid_size]

        self.success_prob = 0.8
        self.slip_prob = 0.1

    def step(self, state, action):
        if state == self.goal_state:
            return state, 0

        action_index = self.actions.index(action)
        move = self.action_effects[action_index]
        next_state = state + move

        if np.random.rand() < self.success_prob:
            pass
        else:
            if np.random.rand() < 0.5:
                slip_direction = (action_index - 1) % 4
            else:
                slip_direction = (action_index + 1) % 4
            next_state += self.action_effects[slip_direction]

        next_state_row = next_state // self.grid_size
        next_state_col = next_state % self.grid_size
        current_state_row = state // self.grid_size
        current_state_col = state % self.grid_size
        if next_state_row < 0 or next_state_row >= self.grid_size or next_state_col < 0 or next_state_col >= self.grid_size:
            next_state = state
        elif (current_state_col == 0 and next_state_col == self.grid_size - 1) or \
             (current_state_col == self.grid_size - 1 and next_state_col == 0):
            next_state = state

        # Get the reward for the current state
        reward = self.reward_for_states[next_state]

        return next_state, reward

    def generate_episode(self, policy):
        state = self.start_state
        episode = []
        while state != self.goal_state:
            action = policy[state]
            next_state, reward = self.step(state, action)
            episode.append((state, action, reward))
            state = next_state
        episode.append((state, "Goal", self.reward_for_states[state]))
        return episode

# Update the fixed policy
fixed_policy = {i: 'right' if i % 4 < 3 else 'down' for i in range(16)}

env = GridWorld()

# Ep generate, state visits count
episodes = []
state_visit_counts = np.zeros(env.num_states, dtype=int)
for _ in range(30):
    episode = env.generate_episode(fixed_policy)
    episodes.append(episode)
    for (state, _, _) in episode:
        state_visit_counts[state] += 1

for i, ep in enumerate(episodes):
    print(f"Episode {i+1}:")
    for step in ep:
        print(f"    {step}")
    print()

plt.figure(figsize=(10, 8))
plt.bar(range(env.num_states), state_visit_counts)
plt.xlabel('State')
plt.ylabel('Number of Visits')
plt.title('Histogram of number of thimes each state is visited across 30 Ep')
plt.xticks(range(env.num_states), [f's{i}' for i in range(env.num_states)])
plt.show()
