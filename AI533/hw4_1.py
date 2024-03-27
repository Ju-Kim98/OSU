#AI533 hw4 Q1: SARSA(λ) and Q-learning(λ)

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

def get_init_e():
    e = {}
    for x in range(4):
        for y in range(4):
            for a in actions:
                e[((x, y), a)] = 0
    return e


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


def SARSA_lambda(alpha, epsilon, lam):
    all_trials = []
    for trial in range(NUM_TRIALS):
        trial_rewards = []
        q = get_init_q()
        e = get_init_e()  # Initialize eligibility traces

        for ep in range(NUM_EPISODES):
            s = (0, 0)
            a = policy[s[0]][s[1]]
            reward_sum = 0

            for step in range(MAX_STEPS):
                s_prime = move_action(s, a)
                r = rewards[s_prime[0]][s_prime[1]]
                a_prime = get_epsilon_greedy_action(q, s_prime, epsilon)
                reward_sum += r

                delta = r + gamma * q[(s_prime, a_prime)] - q[(s, a)]
                e[(s, a)] += 1  # Increment eligibility trace

                for state, action in q.keys():
                    q[(state, action)] += alpha * delta * e[(state, action)]
                    e[(state, action)] *= gamma * lam  # Decay eligibility trace

                s, a = s_prime, a_prime
                if s == (3, 3):
                    break
            #trial_rewards.append(sum(rewards[s[0]][s[1]] for s in path))
            trial_rewards.append(reward_sum)

        all_trials.append(trial_rewards)
    return all_trials

def Q_learning_lambda(alpha, epsilon, lam):
    all_trials = []

    for trial in range(NUM_TRIALS):
        trial_rewards = []
        q = get_init_q()
        e = get_init_e()  # Initialize eligibility traces
    
        for ep in range(NUM_EPISODES):
            s = (0, 0)
            reward_sum = 0

            for step in range(MAX_STEPS):
                a = get_epsilon_greedy_action(q, s, epsilon)
                s_prime = move_action(s, a)
                r = rewards[s_prime[0]][s_prime[1]]
                reward_sum += r

                a_prime, _ = get_max_q_value(q, s_prime)

                a_star = a_prime if random.random() > epsilon else get_epsilon_greedy_action(q, s_prime, epsilon)
                delta = r + gamma * q[(s_prime, a_star)] - q[(s, a)]
                e[(s, a)] += 1  # Increment eligibility trace

                for state, action in q.keys():
                    q[(state, action)] += alpha * delta * e[(state, action)]
                    if a_star == action:
                        e[(state, action)] *= gamma * lam  # Decay eligibility trace
                    else:
                        e[(state, action)] = 0  # Reset eligibility trace

                s = s_prime
                if s == (3, 3):
                    break
            #trial_rewards.append(sum(rewards[s[0]][s[1]] for s in path))
            trial_rewards.append(reward_sum)

        all_trials.append(trial_rewards)
    return all_trials


def tune_hyperparams():
    best_alpha, best_epsilon, best_lambda = 0, 0, 0
    max_value = float('-inf')
      
    for alpha in [0.01, 0.1, 0.2, 0.5]:       
        for epsilon in [0.01, 0.1, 0.2, 0.5]: 
            for lam in [0, 0.1, 0.5, 0.99]:
                sarsa = np.average(SARSA_lambda(alpha, epsilon,lam))
                ql = np.average(Q_learning_lambda(alpha, epsilon, lam))
                average = np.average([sarsa, ql])

                print(f"{alpha=:0.2f}, {epsilon=:0.2f}, {lam=:0.1f}: Avg. reward {average:2.4f}")
                if average > max_value:
                    max_value = average
                    best_alpha, best_epsilon, best_lambda = alpha, epsilon, lam

    print(f"\nHighest average: {best_alpha=},{best_epsilon=},{best_lambda=}, max reward value= {max_value:2.4}\n")
    return best_alpha, best_epsilon, best_lambda

def plot_trials(sarsa, ql, alpha, epsilon):
    plt.clf()
    plt.title("Learning Curves: SARSA(λ), Q-learning(λ)")
    plt.xlabel("Episodes")
    plt.ylabel("Average Reward")

    sarsa = np.array(sarsa)
    ql = np.array(ql)

    sarsa_y, sarsa_err = [], []
    ql_y, ql_err = [], []
    for ep in range(NUM_EPISODES):
        sarsa_y.append(np.average(sarsa[:,ep]))
        sarsa_err.append(np.std(sarsa[:,ep]))

        ql_y.append(np.average(ql[:, ep]))
        ql_err.append(np.std(ql[:, ep]))
    
    plt.errorbar(list(range(NUM_EPISODES)), ql_y, ql_err, label="Q-Learning_lambda",  ecolor='r', capsize=5)
    plt.errorbar(list(range(NUM_EPISODES)), sarsa_y, sarsa_err, label="SARSA_ldambda", ecolor='g', capsize=5)


    plt.legend(loc='lower right', title='Algorithm')
    plt.show()

def main():
    alpha, epsilon, lam = tune_hyperparams()
    sarsa_rewards = SARSA_lambda(alpha, epsilon, lam)
    ql_rewards = Q_learning_lambda(alpha, epsilon, lam)
    plot_trials(sarsa_rewards, ql_rewards, alpha, epsilon)


if __name__ == '__main__':
    main()
