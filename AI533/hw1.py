#AI533 HW1 JuKim
# Q5.Value Iteration & Policy Iteration at Gird world

import numpy as np
import random

# Scenario constants
WATER_STATES = [9, 10]
WILDFIRE_STATES = [1, 2]
GOAL_STATE = 15
WATER_REWARD = -5
WILDFIRE_REWARD = -10
GOAL_REWARD = 100
DEFAULT_REWARD = -1
SUCCESS_PROB = 0.8
SLIDE_PROB = 0.1
DISCOUNT_FACTOR = 0.9  # Assuming a discount factor for this MDP

# Grid dimensions and action configurations
GRID_ROWS = 4
GRID_COLS = 4

# Utility and policy iteration configuration
MAX_ITER = 1000
print_intermediate = False

np.set_printoptions(precision=4, suppress=True)

def get_start_state():
    util = np.zeros((GRID_ROWS, GRID_COLS))
    util[3, 3] = GOAL_REWARD  # goal state reward
    for water_state in WATER_STATES:
        util[water_state // GRID_COLS, water_state % GRID_COLS] = WATER_REWARD
    for wildfire_state in WILDFIRE_STATES:
        util[wildfire_state // GRID_COLS, wildfire_state % GRID_COLS] = WILDFIRE_REWARD
    return util

# Get the value of the requested cell, return None if it is outside the grid
def get_val(util, x, y):
    if x < 0 or y < 0 or x > len(util) - 1 or y > len(util[0]) - 1:
        return None
    return util[x, y]

# Given a util value matrix, print the direction of the highest reward
def print_path(util):
    policy_dir = np.zeros((4, 4), dtype='U1')

    for x in range(len(util)):
        for y in range(len(util[0])):
            value = util[x, y]
            max_value = value

            right = get_val(util, x, y + 1)
            left = get_val(util, x, y - 1)
            up = get_val(util, x - 1, y)
            down = get_val(util, x + 1, y)

            # UP, RIGHT, DOWN, LEFT, zero: just stay
            policy_dir[x, y] = '0'
            if right and right >= max_value:
                policy_dir[x, y] = 'Right'
                max_value = right
            if left and left >= max_value:
                policy_dir[x, y] = 'Left'
                max_value = left
            if up and up >= max_value:
                policy_dir[x, y] = 'Up'
                max_value = up
            if down and down >= max_value:
                policy_dir[x, y] = 'Down'
                max_value = down

    print(policy_dir)

# Return the max value, check the move
def get_updated_value(x, y, util, gamma): 
    if (x, y) == (0, 1) or (x, y) == (0, 2):    #Fire
        return -10
    if (x, y) == (2, 1) or (x, y) == (2, 2):    #water
        return -5
    if (x, y) == (3, 3):    #Goal state
        return 100
    
    # reward of negative 1 for each movement
    cell = -1
    if y < len(util[0]) - 1:
        val_right = util[x, y + 1]
    else:
        val_right = cell
    if x > 0:
        val_up = util[x - 1, y]
    else:
        val_up = cell
    if x < len(util) - 1:
        val_down = util[x + 1, y]
    else:
        val_down = cell
    if y > 0:
        val_left = util[x, y - 1]
    else:
        val_left = cell

    move_right = 0.8 * (cell + gamma * val_right) + 0.1 * (cell + gamma * val_up) + 0.1 * (cell + gamma * val_down)
    move_up = 0.8 * (cell + gamma * val_up) + 0.1 * (cell + gamma * val_left) + 0.1 * (cell + gamma * val_right)
    move_down = 0.8 * (cell + gamma * val_down) + 0.1 * (cell + gamma * val_left) + 0.1 * (cell + gamma * val_right)
    move_left = 0.8 * (cell + gamma * val_left) + 0.1 * (cell + gamma * val_up) + 0.1 * (cell + gamma * val_down)

    return max(move_right, move_left, move_up, move_down)


def value_iteration(max_error, gamma):
    util = get_start_state()            # initial value of all states
    threshold = max_error * (1 - gamma) / gamma     #considering value matrix equivalent

    for t in range(MAX_ITER):
        next_util = np.copy(util)
        
        max_change = 0
        for x in range(4):
            for y in range(4):
                next_util[x, y] = get_updated_value(x, y, util, gamma)
                change = abs(next_util[x, y] - util[x, y])
                max_change = max(max_change, change)

        if print_intermediate:
            print(f"\nAfter time step {t}")
            print(next_util)
            print(f"{max_change=}, {threshold=}")

        util = next_util

        if max_change <= threshold:
            break
    max_value_vi = np.max(util)        

    return util, max_value_vi

# 4x4 grid with dircection
def get_random_policy():
    policy = np.zeros((4, 4), dtype='U1')
    directions = ['Up', 'Right', 'Down', 'Left']

    for x in range(len(policy)):
        for y in range(len(policy[0])):
            policy[x, y] = directions[random.randint(0, len(directions) - 1)]

    return policy


def are_policies_the_same(policy_1, policy_2):
    for x in range(len(policy_1)):
        for y in range(len(policy_1[0])):
            if policy_1[x, y] != policy_2[x, y]:
                return False

    return True

# compute the opti value
def get_updated_value_from_policy(x, y, util, gamma, policy):
    if (x, y) == (0, 1) or (x, y) == (0, 2):
        return -10
    if (x, y) == (2, 1) or (x, y) == (2, 2):
        return -5
    if (x, y) == (3, 3):
        return 100
    
    dir = policy[x, y]

    cell = -1 # util[x, y]
    if y < len(util[0]) - 1:
        val_right = util[x, y + 1]
    else:
        val_right = cell
    if x > 0:
        val_up = util[x - 1, y]
    else:
        val_up = cell
    if x < len(util) - 1:
        val_down = util[x + 1, y]
    else:
        val_down = cell
    if y > 0:
        val_left = util[x, y - 1]
    else:
        val_left = cell

    move_right = 0.8 * (cell + gamma * val_right) + 0.1 * (cell + gamma * val_up) + 0.1 * (cell + gamma * val_down)
    move_up = 0.8 * (cell + gamma * val_up) + 0.1 * (cell + gamma * val_left) + 0.1 * (cell + gamma * val_right)
    move_down = 0.8 * (cell + gamma * val_down) + 0.1 * (cell + gamma * val_left) + 0.1 * (cell + gamma * val_right)
    move_left = 0.8 * (cell + gamma * val_left) + 0.1 * (cell + gamma * val_up) + 0.1 * (cell + gamma * val_down)

    if dir == 'R':
        return move_right
    elif dir == 'D':
        return move_down
    elif dir == 'L':
        return move_left
    elif dir == 'U':
        return move_up
    else:
        raise Exception(f'Policy gave garbage direction: {dir}')

# Get hughest util from the neighbor direction
def get_dir_of_max_neighbor(x, y, util):
    max = -100

    val_right = get_val(util, x, y + 1)
    val_left = get_val(util, x, y - 1)
    val_up = get_val(util, x - 1, y)
    val_down = get_val(util, x + 1, y)

    if val_right and val_right > max:
        dir = 'R'
        max = val_right
    if val_left and val_left > max:
        dir = 'L'
        max = val_left
    if val_up and val_up > max:
        dir = 'U'
        max = val_up
    if val_down and val_down > max:
        dir = 'D'
        max = val_down
    
    return dir


def policy_iteration(max_error, gamma):
    util = get_start_state()
    policy = get_random_policy()    # initalize random policy
    threshold = max_error * (1 - gamma) / gamma     #considering value matrix equivalent
    iter_cnt = 0        # number of iterations in value convergence

    # until no change in policy
    while True:
        # until the util values converge
        while True:
            next_util = np.copy(util)
            max_change = 0

            for x in range(4):
                for y in range(4):
                    # update the util value using the current policy (not best move like VI)
                    next_util[x, y] = get_updated_value_from_policy(x, y, util, gamma, policy)
                    change = abs(next_util[x, y] - util[x, y])
                    max_change = max(max_change, change)
            iter_cnt += 1

            if print_intermediate:
                print(next_util)
                print(f"{iter_cnt=}, {max_change=}, {threshold=}")

            util = next_util
            # break out when util val converges
            if max_change <= threshold:
                break

        # for each state, update the policy to move to the state with the highest reward
        new_policy = np.copy(policy)
        for x in range(4):
            for y in range(4):
                new_policy[x, y] = get_dir_of_max_neighbor(x, y, next_util)

        if print_intermediate:
            print(new_policy)
            print(f"{max_change=}, {threshold=}")

        # if there was no change in the policy, we can exit the outer loop
        if are_policies_the_same(policy, new_policy):
            break

        policy = np.copy(new_policy)
        max_value_pi = np.max(util)

    return util, policy, max_value_pi

def main():
    max_error = 0.0001
    
    print("=============================================================\n")

    print("Policy and Optimal Value in Value Iteration for gamma=0.3:")
    util, max_value_vi = value_iteration(max_error=max_error, gamma=0.3)
    print_path(util)
    print(util)
    print("\n")
    
    print("=============================================================\n")
    print("Policy and Optimal Value in Value Iteration for gamma=0.95:")
    util, max_value_vi = value_iteration(max_error=max_error, gamma=0.95)
    print_path(util)
    print(util)
    print("\n")

    print("=============================================================\n")
    print("Policy and Optimal Value in Policy Iteration for gamma=0.95:")
    util, policy, max_value_pi = policy_iteration(max_error=max_error, gamma=0.95)
    print_path(util)
    print(util)
    
    print("\n")
    
if __name__ == '__main__':
    main()