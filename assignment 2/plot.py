from matplotlib import pyplot as plt
import subprocess
import os
import numpy as np
import random
from tqdm import tqdm

random.seed(0)

def get_V():
    with open("policy_file.txt",'r') as file:
        V = float(file.readlines()[0].split(" ")[0])
    return V

def get_rand_pol(states, state_dict):
    with open("rand_pol.txt",'w') as file:
        lines =[]
        for s in states:
            lines.append(state_dict[s]+"\n")
        
        file.writelines(lines)

rand_pol_dict = {x.split()[0]: x.split()[1] for x in open("data/cricket/rand_pol.txt").read().strip().split('\n')}

# plot 1
# balls = 15
# runs =30
# cmd_states = "python3","cricket_states.py","--balls", str(balls), "--runs", str(runs)
# f = open('cricket_state_list.txt','w')
# subprocess.call(cmd_states,stdout=f)
# states = [line.strip() for line in f.readlines()]
# f.close()

# get_rand_pol(states, rand_pol_dict)
# q_list= np.arange(0,1,0.1)
# v_list_optimal =[]
# v_list_rand = []

# for q in tqdm(q_list):
#     cmd_encoder = "python3","encoder.py","--states", "cricket_state_list.txt", "--parameters", "data/cricket/sample-p1.txt", "--q", str(q)
#     f = open('mdpfile.txt','w')
#     subprocess.call(cmd_encoder,stdout=f)
#     f.close()

#     cmd_planner = "python3","planner.py","--mdp", "mdpfile.txt"
#     f = open('policy_file.txt','w')
#     subprocess.call(cmd_planner,stdout=f)
#     f.close()

#     V = get_V()
#     v_list_optimal.append(V)

#     os.remove("policy_file.txt")
#     cmd_encoder = "python3","planner.py","--mdp", "mdpfile.txt","--policy","rand_pol1.txt"
#     f = open('policy_file.txt','w')
#     subprocess.call(cmd_encoder,stdout=f)
#     f.close()

#     V = get_V()
#     v_list_rand.append(V)

#     os.remove("mdpfile.txt")
#     os.remove("policy_file.txt")
    

# plt.plot(q_list,v_list_rand)
# plt.plot(q_list,v_list_optimal)
# plt.xlabel("runs")
# plt.ylabel("win probabilties")
# plt.savefig("plot1.png")

# plot 2
balls = 10
q =0.25
v_list_optimal = []
v_list_rand = []
for runs in tqdm(range(20,0,-1)):
    

    cmd_states = "python3","cricket_states.py","--balls", str(balls), "--runs", str(runs)
    f = open('cricket_state_list.txt','w')
    subprocess.call(cmd_states,stdout=f)
    f.close()
    
    f = open('cricket_state_list.txt','r')
    states = [line.strip() for line in f.readlines()]
    get_rand_pol(states, rand_pol_dict)
    f.close()

    cmd_encoder = "python3","encoder.py","--states", "cricket_state_list.txt", "--parameters", "data/cricket/sample-p1.txt", "--q", str(q)
    f = open('mdpfile.txt','w')
    subprocess.call(cmd_encoder,stdout=f)
    f.close()

    cmd_planner = "python3","planner.py","--mdp", "mdpfile.txt"
    f = open('policy_file.txt','w')
    subprocess.call(cmd_planner,stdout=f)
    f.close()

    V = get_V()
    v_list_optimal.append(V)

    os.remove("policy_file.txt")
    cmd_encoder = "python3","planner.py","--mdp", "mdpfile.txt","--policy","rand_pol.txt"
    f = open('policy_file.txt','w')
    subprocess.call(cmd_encoder,stdout=f)
    f.close()

    V = get_V()
    v_list_rand.append(V)

    os.remove("mdpfile.txt")
    os.remove("policy_file.txt")
    os.remove("cricket_state_list.txt")

plt.plot(range(20,0,-1),v_list_optimal, label="Optimal Policy")
plt.plot(range(20,0,-1),v_list_rand, label="Random Policy")
plt.xlabel("runs")
plt.ylabel("win probabilties")
plt.legend()
plt.savefig("plot2.png")

# plot 3
# runs = 10 
# q =0.25
# v_list_optimal = []
# v_list_rand = []
# for balls in tqdm(range(15,0,-1)):
    
#     cmd_states = "python3","cricket_states.py","--balls", str(balls), "--runs", str(runs)
#     f = open('cricket_state_list.txt','w')
#     subprocess.call(cmd_states,stdout=f)
#     states = [line.strip() for line in f.readlines()]
#     f.close()

    # f = open('cricket_state_list.txt','r')
    # states = [line.strip() for line in f.readlines()]
    # get_rand_pol(states, rand_pol_dict)
    # f.close()

#     cmd_encoder = "python3","encoder.py","--states", "cricket_state_list.txt", "--parameters", "data/cricket/sample-p1.txt", "--q", str(q)
#     f = open('mdpfile.txt','w')
#     subprocess.call(cmd_encoder,stdout=f)
#     f.close()

#     cmd_planner = "python3","planner.py","--mdp", "mdpfile.txt"
#     f = open('policy_file.txt','w')
#     subprocess.call(cmd_planner,stdout=f)
#     f.close()

#     V = get_V()
#     v_list_optimal.append(V)

#     os.remove("policy_file.txt")
#     cmd_encoder = "python3","planner.py","--mdp", "mdpfile.txt","--policy","rand_pol.txt"
#     f = open('policy_file.txt','w')
#     subprocess.call(cmd_encoder,stdout=f)
#     f.close()

#     V = get_V()
#     v_list_rand.append(V)

#     os.remove("mdpfile.txt")
#     os.remove("policy_file.txt")
#     os.remove("cricket_state_list.txt")

# plt.plot(range(15,0,-1),v_list_optimal)
# plt.plot(range(15,0,-1),v_list_rand)
# plt.xlabel("balls")
# plt.ylabel("win probabilties")
# plt.savefig("plot3.png")