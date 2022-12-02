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

def get_rand_pol(states, state_dict,actions_to_int):
    with open("rand_pol.txt",'w') as file:
        lines =[]
        for s in states:
            lines.append(str(actions_to_int[int(state_dict[s])])+"\n")
        
        file.writelines(lines)

actions_to_int = {action: i for i,action in enumerate([0,1,2,4,6])}
rand_pol_dict = {x.split()[0]: x.split()[1] for x in open("data/cricket/rand_pol.txt").read().strip().split('\n')}

# plot 1
balls = 15
runs =30
cmd_states = "python3","cricket_states.py","--balls", str(balls), "--runs", str(runs)
f = open('cricket_state_list.txt','w')
subprocess.call(cmd_states,stdout=f)
f.close()

f = open('cricket_state_list.txt','r')
states = [line.strip() for line in f.readlines()]
f.close()

get_rand_pol(states, rand_pol_dict,actions_to_int)
q_list= np.arange(0,1,0.1)
v_list_optimal =[]
v_list_rand = []

for q in tqdm(q_list):
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
    

plt.plot(q_list,v_list_optimal,color ="red",label="Optimal Policy")
plt.plot(q_list,v_list_rand,color="green",label="Random Policy")
plt.xlabel("value of q")
plt.ylabel("win probabilties")
plt.legend()
plt.savefig("plot1.png")