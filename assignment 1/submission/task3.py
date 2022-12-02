"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the AlgorithmManyArms class. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)
"""

import random
import numpy as np
import math

# START EDITING HERE
# You can use this space to define any helper functions that you need
# END EDITING HERE


class AlgorithmManyArms:
    def __init__(self, num_arms, horizon):
        self.eps = 1
        self.num_arms = num_arms
        self.horizon = horizon
        self.successes = np.zeros(num_arms)
        self.failuers = np.zeros(num_arms)
        self.idxs = np.array(random.sample(range(0, num_arms), int(math.sqrt(num_arms))))
        self.times = 1
        # Horizon is same as number of arms
    
    def give_pull(self):
        # START EDITING HERE
        betas = np.random.beta(self.successes[self.idxs]+1, self.failuers[self.idxs]+1)
        q_max = np.argmax(betas)
        return self.idxs[q_max]
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.successes[arm_index] += reward
        self.failuers[arm_index] += 1- reward
        self.times += 1
        # END EDITING HERE
