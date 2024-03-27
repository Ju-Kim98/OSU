#AI533 hw4 Q2: Actor-Critic

import matplotlib.pyplot as plt
import numpy as np
import random

np.set_printoptions(precision=4)
np.set_printoptions(suppress=True)

DEBUG = False

gamma = 0.95    
            
NUM_EPISODES = 100          # episode count in each trial
NUM_TRIALS = 100            # number of trials to run
MAX_STEPS = 1000            # stop episodes that do not reach goal before this many steps

actions = ['^', '>', 'v', '<']

policy = np.zeros((4, 4), dtype='U1')
policy = [
    ['v', 'v', '>', 'v'],
    ['v', '>', '>', 'v'],
    ['v', 'v', 'v', 'v'],
    ['>', '>', '>', 'o'],
]

rewards = [
    [-1, -10, -10, -1],
    [-1, -1, -1, -1],
    [-1, -5, -5, -1],
    [-1, -1, -1, 100],
]


def get_init_q():
    q = {}
    for x in range(4):
        for y in range(4):
            for a in actions:
                q[((x, y), a)] = 0

    return q


def get_move_dir(action):
    if action == '>':       
        moves = ['>', '^', 'v']
    elif action == 'v':     
        moves = ['v', '<', '>']
    elif action == '<':     
        moves = ['<', '^', 'v']
    if action == '^':       
        moves = ['^', '<', '>']

    prob = random.random()
    if prob <= 0.8:
        move = moves[0]
    elif prob <= 0.9:
        move = moves[1]
    else:
        move = moves[2]

    return move


def move_action(s, action):

    x, y = s
    if action == '>':
        y = min(y + 1, 3)
    elif action == '<':
        y = max(y - 1, 0)
    elif action == '^':
        x = max(x - 1, 0)
    elif action == 'v':
        x = min(x + 1, 3)
    else:
        raise Exception(f"Invalid action {action}")

    return x, y


def get_epsilon_greedy_action(q, s, epsilon):
   
    ep_val = random.random()
    if ep_val <= epsilon:           
        desired_action = random.choice(actions)
    else:
        desired_action, max_value = get_max_q_value(q, s)

    actual_action = get_move_dir(desired_action)

    if DEBUG:
        print(f"{ep_val=}, {desired_action=}, {actual_action=}")

    return actual_action


def get_max_q_value(q, s):
 
    max_value = float('-inf')
    poss_actions = []
    for action in actions:
        value = q[(s, action)]
        if value > max_value:
            poss_actions = [action]
            max_value = value
        elif value == max_value:
            poss_actions.append(action)

    action = random.choice(poss_actions)
    return action, max_value

# Additional functions needed for Actor-Critic
def actor_critic(num_episodes, gamma, alpha_theta, alpha_w):
    # Initialize policy parameters theta and state-value weights w randomly
    theta = np.random.rand(4, 4, len(actions))
    w = np.random.rand(4, 4)
    
    # To store reward history
    episode_rewards = []

    for e in range(num_episodes):
        # Initialize state (assuming starting state is fixed)
        s = (0, 0)
        I = 1  # eligibility trace
        total_reward = 0

        for step in range(MAX_STEPS):
            # Choose action using current policy
            probs = softmax(theta[s[0], s[1]])
            action = np.random.choice(actions, p=probs)
            action_index = actions.index(action)

            # Take action, observe new state and reward
            new_s = move_action(s, action)
            reward = rewards[new_s[0]][new_s[1]]

            # Estimate of V(s)
            v_s = w[s[0], s[1]]

            # Estimate of V(s') - Using TD(0)
            v_s_prime = w[new_s[0], new_s[1]]
            
            # TD Error δ
            td_error = reward + gamma * v_s_prime - v_s

            # Update critic weights w for V
            w[s[0], s[1]] += alpha_w * td_error * I

            # Update actor policy parameters θ
            theta[s[0], s[1], action_index] += alpha_theta * td_error * I * (1 - probs[action_index])

            # Update state and total reward
            s = new_s
            total_reward += reward

            # Update eligibility trace
            I *= gamma

            # Termination condition
            if reward == 100:
                break
        
        # Save total episode reward
        episode_rewards.append(total_reward)

    return episode_rewards

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)  # only difference

"""
hyperparameters tuning

1과 2가 그래프 모양이 다름, 2는 이전것들과 비슷함
"""
#ex3
def tune_actor_critic_hyperparameters():
    best_alpha_theta, best_alpha_w = 0, 0
    max_value = float('-inf')
    best_rewards_history = None

    # Explore the hyperparameter space
    for alpha_theta in [0.001, 0.01, 0.1, 0.2, 0.5]:
        for alpha_w in [0.001, 0.01, 0.1, 0.5, 0.99]:
            trial_rewards = [actor_critic(NUM_EPISODES, gamma, alpha_theta, alpha_w) for _ in range(NUM_TRIALS)]
            avg_rewards = np.mean(trial_rewards, axis=0)
            final_avg_reward = np.mean(avg_rewards[-10:])  # Consider average of the last 10 episodes for stability
            
            print(f"alpha_theta={alpha_theta:0.3f}, alpha_w={alpha_w:0.3f}: Final Avg. Reward {final_avg_reward:2.4f}")

            if final_avg_reward > max_value:
                max_value = final_avg_reward
                best_alpha_theta, best_alpha_w = alpha_theta, alpha_w
                best_rewards_history = np.array(trial_rewards)

    print(f"\nBest Hyperparameters: alpha_theta={best_alpha_theta}, alpha_w={best_alpha_w}, Max Average Reward={max_value:2.4f}\n")
    
    # Plotting the learning curve for the best hyperparameter combination
    avg_rewards = np.mean(best_rewards_history, axis=0)
    std_deviation_rewards = np.std(best_rewards_history, axis=0)

    plt.fill_between(range(NUM_EPISODES), avg_rewards - std_deviation_rewards, avg_rewards + std_deviation_rewards, alpha=0.3)
    plt.plot(range(NUM_EPISODES), avg_rewards, '-r')
    plt.xlabel('Episodes')
    plt.ylabel('Total Rewards')
    plt.title('Actor-Critic Learning Curve')
    plt.show()

    return best_alpha_theta, best_alpha_w

# Now call the function to tune the hyperparameters and plot the results
best_alpha_theta, best_alpha_w = tune_actor_critic_hyperparameters()


