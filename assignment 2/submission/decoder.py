import argparse
import numpy as np

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--states")
    parser.add_argument("--value-policy")
    args = parser.parse_args()


    actions_a = [0,1,2,4,6]
    actions_b = [-1,0,1]
    possible_events =[-1,0,1,2,3,4,6]

    with open(args.states,'r') as file:
        lines = file.readlines()
        num_states = len(lines)
        states_to_int = dict(zip(sorted(list(map(lambda s: s.strip()+"0", lines)), reverse=True), range(0,num_states)))
        states_to_int1 = dict(zip(sorted(list(map(lambda s: s.strip()+"1", lines)), reverse=True), range(num_states,2*num_states)))
        states_to_int = {**states_to_int, **states_to_int1}
        int_to_states = {i:s for s,i in states_to_int.items()}
        balls = int(int_to_states[0][:2])
        runs = int(int_to_states[0][-3:-1])

    with open(args.value_policy,'r') as file:
        lines = file.readlines()
        for s in range(num_states):
            print(int_to_states[s][:-1],actions_a[int(lines[s].split(" ")[1])],lines[s].split(" ")[0])
        


