import argparse
import numpy as np

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--states")
    parser.add_argument("--parameters")
    parser.add_argument("--q")
    args = parser.parse_args()

    states_path = args.states
    parameters_path = args.parameters
    q = float(args.q)
    action_probs_a= {}
    action_probs_b= {}
    num_balls = 0
    num_actions = 5
    actions_a = [0,1,2,4,6]
    actions_b = [-1,0,1]
    possible_events =[-1,0,1,2,3,4,6]

    with open(states_path,'r') as file:
        lines = file.readlines()
        num_states = len(lines)
        states_to_int = dict(zip(sorted(list(map(lambda s: s.strip()+"0", lines)), reverse=True), range(0,num_states)))
        states1 = dict(zip(sorted(list(map(lambda s: s.strip()+"1", lines)), reverse=True), range(num_states,2*num_states)))
        states_to_int = {**states_to_int, **states1}
        int_to_states = {i:s for s,i in states_to_int.items()}
        balls = int(int_to_states[0][:2])
        runs = int(int_to_states[0][-3:-1])

        
    with open(parameters_path,'r') as file:
        lines = file.readlines()
        for i,line in enumerate(lines):
            if i!=0:
                values = line.strip().split(" ")
                action_probs_a[int(values[0])] = np.array(list(map(lambda s: float(s),values[1:])))

    for a in actions_a:
        action_probs_b[a] = np.array([q,(1-q)/2,(1-q)/2,0,0,0,0])


    transition_matrix = np.zeros((2*num_states+2,num_actions,2*num_states+2))
    reward_matrix = np.zeros((2*num_states+2, num_actions, 2*num_states+2))
    win_state = 2*num_states
    end_state = 2*num_states+1
    for s in range(num_states):
        bl = int(int_to_states[s][:2])
        rl = int(int_to_states[s][-3:-1])

        for a in range(len(actions_a)):
            for e in range(len(possible_events)):
                strike_b= False

                if possible_events[e]==1:
                    # non striker states
                    strike_b= True
                elif possible_events[e]==3:
                    # non striker states
                    strike_b= True
                if (bl-1)%6==0:
                    # when the over is completed
                    # strike for a will remain
                    strike_b= not strike_b

                rl1 = rl-possible_events[e]
                # print(rl1)
                if (bl==1 and rl1>0) or possible_events[e]==-1:
                    # return to losing state
                    transition_matrix[s,a,end_state] += action_probs_a[actions_a[a]][e]
                elif rl1<=0:
                    # return to winning state
                    transition_matrix[s,a,win_state] += action_probs_a[actions_a[a]][e]
                    reward_matrix[s,a,win_state] =1
                else:
                    nxt_state = str(bl-1).zfill(2) + str(rl1).zfill(2) + str(int(strike_b))
                    transition_matrix[s,a,states_to_int[nxt_state]] += action_probs_a[actions_a[a]][e]

    for s in range(num_states, 2*num_states):
        bl = int(int_to_states[s][:2])
        rl = int(int_to_states[s][-3:-1])
        
        for a in range(len(actions_a)):
            for e in range(len(possible_events)):
                strike_a= False

                if possible_events[e]==1:
                    # non striker states
                    strike_a= True
                if (bl-1)%6==0:
                    # when the over is completed
                    # strike for a will remain
                    strike_a= not strike_a

                rl1 = rl-possible_events[e]
                if (bl==1 and rl1>0) or possible_events[e]==-1:
                    # return to losing state
                    transition_matrix[s,a,end_state] += action_probs_b[actions_a[a]][e]
                elif rl1<=0: 
                    # return to winning state
                    transition_matrix[s,a,win_state] += action_probs_b[actions_a[a]][e]
                    reward_matrix[s,a,win_state] =1
                else:
                    nxt_state = str(bl-1).zfill(2) + str(rl1).zfill(2) + str(int((not strike_a)))
                    transition_matrix[s,a,states_to_int[nxt_state]] += action_probs_b[actions_a[a]][e]


    for a in range(len(actions_a)):
        transition_matrix[win_state,a,win_state]=1
        transition_matrix[end_state,a,end_state]=1


    print("numStates",2*num_states+2)
    print("numActions",len(actions_a))
    print("end",2*num_states,2*num_states+1)
    for s in range(2*num_states+2):
        for a in range(len(actions_a)):
            for s1 in range(2*num_states+1,-1,-1):
                if transition_matrix[s,a,s1]!=0:
                    print("transition",s,a,s1,reward_matrix[s,a,s1],transition_matrix[s,a,s1])

    print("mdptype","episodic")
    print("discount",1)


