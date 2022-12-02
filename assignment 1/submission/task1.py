"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the base Algorithm class that all algorithms should inherit
from. Here are the method details:
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

We have implemented the epsilon-greedy algorithm for you. You can use it as a
reference for implementing your own algorithms.
"""

import numpy as np
import math
# Hint: math.log is much faster than np.log for scalars

class Algorithm:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
    
    def give_pull(self):
        raise NotImplementedError
    
    def get_reward(self, arm_index, reward):
        raise NotImplementedError

# Example implementation of Epsilon Greedy algorithm
class Eps_Greedy(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # Extra member variables to keep track of the state
        self.eps = 0.1
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
    
    def give_pull(self):
        if np.random.random() < self.eps:
            return np.random.randint(self.num_arms)
        else:
            return np.argmax(self.values)
    
    def get_reward(self, arm_index, reward):
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value


# START EDITING HERE
# You can use this space to define any helper functions that you need
# END EDITING HERE

class UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        self.num_arms = num_arms # total number of arms in the multi armed bandit
        self.horizon = horizon # horizon 
        self.mu= np.zeros((num_arms,1)) # mean reward for each arm
        self.time = 1 # step count
        self.number_of_pulls = np.zeros((num_arms,1)) # number of arm pulls for each arm
        self.inf = float('inf')

    def give_pull(self):
        # START EDITING HERE
        chosen_arm = np.argmax(self.mu + 
                                    np.sqrt(np.divide(math.log(self.time),self.number_of_pulls,
                                                     np.ones_like(self.number_of_pulls)*self.inf,
                                                     where = self.number_of_pulls!=0
                                                    )
                                            )
                                )

        assert chosen_arm < self.num_arms
        self.time += 1
        return chosen_arm
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.mu[arm_index] = (reward+
                                    self.mu[arm_index]*self.number_of_pulls[arm_index])/(self.number_of_pulls[arm_index]+1)
        self.number_of_pulls[arm_index] += 1
        # END EDITING HERE

class KL_UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.num_arms = num_arms # total number of arms in the multi armed bandit
        self.horizon = horizon # horizon 
        self.mu= np.zeros(num_arms) # mean reward for each arm
        self.time = 1 # step count
        self.number_of_pulls = np.zeros(num_arms) # number of arm pulls for each arm
        self.inf = float('inf')
        # END EDITING HERE
    
    def KL(self, p, q):
        if p == 1:
            return p*np.log(p/q)
        elif p == 0:
            return (1-p)*np.log((1-p)/(1-q))
        else:
            return p*np.log(p/q) + (1-p)*np.log((1-p)/(1-q))

            
    def binary_search(self, target, pa):
        start = pa
        end = 1
        mid = (start+end)/2
        while start<end:
            mid = (start+end)/2
            value = self.KL(pa,mid)
            if abs(target - value) <0.01:
                return mid
            elif target> value:
                start = mid
            else:
                end = mid

        return mid


    # def give_q_arms(self):
    #     q_arm = np.zeros(self.num_arms)
    #     for i in range(0, self.num_arms):
    #         p_a = float(self.mu[i])
    #         rhs =  float((np.log(self.time)+3*np.log(np.log(self.time)))/self.number_of_pulls[i])
    #         q_arm[i] = self.get_q(rhs, p_a)
        
    #     return q_arm

    def give_q_arms(self):
        q_arm = np.zeros(self.num_arms)
        for i in range(0, self.num_arms):
            p_a = float(self.mu[i])
            target =  float((np.log(self.time))/self.number_of_pulls[i])
            q_arm[i] = self.binary_search(target, p_a)

        return q_arm
        
    def give_pull(self):
        # START EDITING HERE
        if self.time <= min(self.horizon, self.num_arms):
            return self.time-1
        ucb_kl = self.give_q_arms()
        chosen_arm = np.argmax(ucb_kl)
        return chosen_arm
        # END EDITING HERE

    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.time +=1
        self.mu[arm_index] = (reward+self.number_of_pulls[arm_index]*self.mu[arm_index])/(self.number_of_pulls[arm_index]+1)
        self.number_of_pulls[arm_index] += 1
        # END EDITING HERE


class Thompson_Sampling(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.num_arms = num_arms # total number of arms in the multi armed bandit
        self.horizon = horizon # horizon 
        self.successes = np.zeros(self.num_arms)
        self.failures = np.zeros(self.num_arms)
        self.time =1
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        x = np.random.beta(self.successes+1, self.failures+1)
        self.time += 1
        chosen_arm = np.argmax(x)
        return chosen_arm
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.successes[arm_index] += reward
        self.failures[arm_index] += (1-reward)
        # END EDITING HERE
