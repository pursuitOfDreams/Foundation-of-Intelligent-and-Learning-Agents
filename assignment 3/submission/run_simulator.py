from importlib.resources import path
from gym_driving.assets.car import *
from gym_driving.envs.environment import *
from gym_driving.envs.driving_env import *
from gym_driving.assets.terrain import *

import time
import pygame, sys
from pygame.locals import *
import random
import math
import argparse

# Do NOT change these values
TIMESTEPS = 1000
FPS = 30
NUM_EPISODES = 10

class Task1():

    def __init__(self):
        """
        Can modify to include variables as required
        """
        super().__init__()

    def next_action(self, state):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED
        """

        action_acc = None
        action_steer = None
        delta_angle = 2
        delta_x = 40
        # Replace with your implementation to determine actions to be taken
        
        # if the current x and y coordinate is in the range -15 and 15 make the acc 0


        # if  -delta_x < self.y < delta_x: 
        #     if abs(self.angle) < delta_angle:
        #         action_acc = 4
        #         action_steer = 1
        #     elif (self.angle+360)%360 >= 180 and (self.angle+360)%360 < 360:
        #         action_acc = 2
        #         action_steer = 2
        #     else:
        #         action_acc = 2
        #         action_steer = 0
        # elif self.y <= -delta_x:
        #     if abs((self.angle+360)%360-90) < delta_angle:
        #         action_acc = 4
        #         action_steer = 1
        #     elif (self.angle+360)%360 >= 90+delta_angle and (self.angle+360)%360 < 270:
        #         action_acc= 2
        #         action_steer = 0
        #     else:
        #         action_acc = 2
        #         action_steer = 2
        # else:
        #     if abs((self.angle+360)%360-270) < delta_angle:
        #         action_acc = 4
        #         action_steer = 1
        #     elif (self.angle+360)%360 <= 270+delta_angle and (self.angle+360)%360 > 90:
        #         action_acc = 2
        #         action_steer = 2
        #     else:
        #         action_acc = 2
        #         action_steer = 0


        if self.y < 0 : 
            if abs((self.angle+360)%360 -self.theta) < delta_angle:
                action_acc = 4  
                action_steer = 1
            else:
                if ((self.angle+360)%360 -self.theta) > delta_angle:
                    action_acc = 2
                    action_steer = 0
                else:
                    action_acc = 2
                    action_steer = 2
        else:
            if abs((self.angle+360)%360 -self.theta) < delta_angle:
                action_acc = 4  
                action_steer = 1
            else:
                if ((self.angle+360)%360 -self.theta) > delta_angle:
                    action_acc = 2
                    action_steer = 0
                else:
                    action_acc = 2
                    action_steer = 2


            


        action = np.array([action_steer, action_acc])  

        return action

    def controller_task1(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
    
        ######### Do NOT modify these lines ##########
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        simulator = DrivingEnv('T1', render_mode=render_mode, config_filepath=config_filepath)

        time.sleep(3)
        ##############################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):
        
            ######### Do NOT modify these lines ##########
            
            # To keep track of the number of timesteps per epoch
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset()
            
            # Variable representing if you have reached the road
            road_status = False
            ##############################################

            # The following code is a basic example of the usage of the simulator
            for t in range(TIMESTEPS):
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                self.x = state[0]
                self.y = state[1]
                self.velocity = state[2]
                self.angle = state[3]

                if t==0:
                    self.theta = math.degrees(np.arctan(((350-self.x)/abs(self.y+1e-8))))
                    if self.y > 0:
                        self.theta += 268
                    else:
                        self.theta = 90 -self.theta


                action = self.next_action(state)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)

                
                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            # Writing the output at each episode to STDOUT
            print(str(road_status) + ' ' + str(cur_time))
            # print("True 0")

class Task2():

    def __init__(self):
        """
        Can modify to include variables as required
        """

        super().__init__()
        self.r =[[] for i in range(5)]

    def next_action(self, state):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED

        You can modify the function to take in extra arguments and return extra quantities apart from the ones specified if required
        """

        # Replace with your implementation to determine actions to be taken
        delta_y1 = 25
        delta_y = 40
        delta_x = 35
        quad_no = None
        if self.x > 0 and self.y > 0:
            quad_no = 1
        elif self.x > 0 and self.y < 0:
            quad_no = 4
        elif self.x< 0 and self.y >0 :
            quad_no = 2
        else:
            quad_no = 3

        delta_angle = 2

        if -delta_y < self.y < delta_y:
            
            if abs(self.angle) < delta_angle :
                action_acc = 4
                action_steer = 1
            elif (self.angle+360)%360 < 360 and (self.angle+360)%360 > 180:
                action_acc = 2
                action_steer = 2
            else:
                action_acc = 2
                action_steer = 0
        else:
            if (quad_no ==3 or quad_no == 4)  and self.y > self.r[quad_no][1] + 50 +delta_y1:
                # go straight nothing to do 
                
                if abs((self.angle+360)%360-90) < delta_angle:
                    action_acc = 4
                    action_steer = 1
                elif (self.angle+360)%360 >= 90+delta_angle and (self.angle+360)%360 < 270:
                    action_acc= 2
                    action_steer = 0
                else:
                    action_acc = 2
                    action_steer = 2
            elif (quad_no ==1 or quad_no == 2) and self.y < self.r[quad_no][1]- 50 -delta_y1 :
                if abs((self.angle+360)%360-270) < delta_angle:
                    action_acc = 4
                    action_steer = 1
                elif (self.angle+360)%360 <= 270+delta_angle and (self.angle+360)%360 > 90:
                    action_acc = 2
                    action_steer = 2
                else:
                    action_acc = 2
                    action_steer = 0
            else:
                if self.x < self.r[quad_no][0]-50-delta_x:
                    # print("here")
                    if (quad_no==3 or quad_no==4):
                        if abs((self.angle+360)%360-90) < delta_angle:
                            action_acc = 4
                            action_steer = 1
                        elif (self.angle+360)%360 >= 90+delta_angle and (self.angle+360)%360 < 270:
                            action_acc= 2
                            action_steer = 0
                        else:
                            action_acc = 2
                            action_steer = 2
                    else:
                        if abs((self.angle+360)%360-270) < delta_angle:
                            action_acc = 4
                            action_steer = 1
                        elif (self.angle+360)%360 <= 270-delta_angle and (self.angle+360)%360 > 90:
                            action_acc = 2
                            action_steer = 2
                        else:
                            action_acc = 2
                            action_steer = 0

                elif self.x > self.r[quad_no][0]+50+delta_x:
                    # print("here1")
                    if (quad_no==3 or quad_no==4):
                        if abs((self.angle+360)%360-90) < delta_angle:
                            action_acc = 4
                            action_steer = 1
                        elif (self.angle+360)%360 >= 90+delta_angle and (self.angle+360)%360 < 270:
                            action_acc= 2
                            action_steer = 0
                        else:
                            action_acc = 2
                            action_steer = 2
                    else:
                        if abs((self.angle+360)%360-270) < delta_angle:
                            action_acc = 4
                            action_steer = 1
                        elif (self.angle+360)%360 <= 270-delta_angle and (self.angle+360)%360 > 90:
                            action_acc = 2
                            action_steer = 2
                        else:
                            action_acc = 2
                            action_steer = 0
                else:
                    # print("here2")
                    # move ahead till you cross the 
                    if abs(self.angle) < delta_angle:
                        action_acc = 4
                        action_steer = 1
                    elif (self.angle+360)%360 < 360 and (self.angle+360)%360 > 180:
                        action_acc = 2
                        action_steer = 2
                    else:
                        action_acc = 2
                        action_steer = 0


        action = np.array([action_steer, action_acc])  

        return action

    def controller_task2(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
        
        ################ Do NOT modify these lines ################
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        time.sleep(3)
        ###########################################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):

            ################ Setting up the environment, do NOT modify these lines ################
            # To randomly initialize centers of the traps within a determined range
            ran_cen_1x = random.randint(120, 230)
            ran_cen_1y = random.randint(120, 230)
            ran_cen_1 = [ran_cen_1x, ran_cen_1y]

            ran_cen_2x = random.randint(120, 230)
            ran_cen_2y = random.randint(-230, -120)
            ran_cen_2 = [ran_cen_2x, ran_cen_2y]

            ran_cen_3x = random.randint(-230, -120)
            ran_cen_3y = random.randint(120, 230)
            ran_cen_3 = [ran_cen_3x, ran_cen_3y]

            ran_cen_4x = random.randint(-230, -120)
            ran_cen_4y = random.randint(-230, -120)
            ran_cen_4 = [ran_cen_4x, ran_cen_4y]

            ran_cen_list = [ran_cen_1, ran_cen_2, ran_cen_3, ran_cen_4]            
            eligible_list = []

            # To randomly initialize the car within a determined range
            for x in range(-300, 300):
                for y in range(-300, 300):

                    if x >= (ran_cen_1x - 110) and x <= (ran_cen_1x + 110) and y >= (ran_cen_1y - 110) and y <= (ran_cen_1y + 110):
                        continue

                    if x >= (ran_cen_2x - 110) and x <= (ran_cen_2x + 110) and y >= (ran_cen_2y - 110) and y <= (ran_cen_2y + 110):
                        continue

                    if x >= (ran_cen_3x - 110) and x <= (ran_cen_3x + 110) and y >= (ran_cen_3y - 110) and y <= (ran_cen_3y + 110):
                        continue

                    if x >= (ran_cen_4x - 110) and x <= (ran_cen_4x + 110) and y >= (ran_cen_4y - 110) and y <= (ran_cen_4y + 110):
                        continue

                    eligible_list.append((x,y))

            self.r[1] = ran_cen_1
            self.r[2] = ran_cen_3
            self.r[3] = ran_cen_4
            self.r[4] = ran_cen_2
            # print(self.r)

            simulator = DrivingEnv('T2', eligible_list, render_mode=render_mode, config_filepath=config_filepath, ran_cen_list=ran_cen_list)
        
            # To keep track of the number of timesteps per episode
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset(eligible_list=eligible_list)
            ###########################################################

            # The following code is a basic example of the usage of the simulator
            road_status = False

            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                    
                
                self.x = state[0]
                self.y = state[1]
                self.velocity = state[2]
                self.angle = state[3]
                
                # if (t==0):
                #     print(self.x, self.y , self.angle)
                
                # print(self.x, self.y, self.angle)
                action = self.next_action(state)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)

                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            print(str(road_status) + ' ' + str(cur_time))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config filepath", default=None)
    parser.add_argument("-t", "--task", help="task number", choices=['T1', 'T2'])
    parser.add_argument("-r", "--random_seed", help="random seed", type=int, default=0)
    parser.add_argument("-m", "--render_mode", action='store_true')
    parser.add_argument("-f", "--frames_per_sec", help="fps", type=int, default=30) # Keep this as the default while running your simulation to visualize results
    args = parser.parse_args()

    config_filepath = args.config
    task = args.task
    random_seed = args.random_seed
    render_mode = args.render_mode
    fps = args.frames_per_sec

    FPS = fps

    random.seed(random_seed)
    np.random.seed(random_seed)

    if task == 'T1':
        agent = Task1()
        agent.controller_task1(config_filepath=config_filepath, render_mode=render_mode)

    else:

        agent = Task2()
        agent.controller_task2(config_filepath=config_filepath, render_mode=render_mode)
