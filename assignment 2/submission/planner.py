import argparse
import numpy as np
import re 
import sys
import pulp as pl


def get_Q(V,T,R, gamma):
    Q = np.zeros((T.shape[0], T.shape[1]))
    Q = np.sum(T[:,:,:]*(R[:,:,:]+gamma*V.reshape(1,-1)),axis=2)
    return Q

def get_policy(Q):
    pi= np.argmax(Q, axis=1)
    return pi
   

def policy_evaluation(pi, T, R, gamma, mdptype, end):
    num_states = T.shape[0]
    # print(num_states)
    problem = pl.LpProblem('LP', pl.LpMinimize)
    V = np.zeros(num_states)
    vars = [f"V_{i}" for i in range(num_states)]
    V_lp = pl.LpVariable.dicts("V",vars, cat="Continuous")
    # print(len(vars), T.shape, len(V_lp))

    # adding the objective function
    problem += pl.lpSum([V_lp[i] for i in vars])
    for s in range(num_states):
        # print(len(pi))
        # exit()
        problem += V_lp[vars[s]]-pl.lpSum([T[s,int(pi[s]),s1]*gamma*V_lp[vars[s1]] for s1 in range(num_states)]) >= pl.lpSum([T[s,int(pi[s]),s1]*R[s,int(pi[s]),s1] for s1 in range(num_states)])

    if mdptype=="episodic" and len(end)>0:
        # print(len(end))
        for e in end:
            # print(e)
            problem += (V_lp[vars[e]]==0)
    problem.solve(pl.PULP_CBC_CMD(msg=0))
    for s in range(num_states):
        V[s] = pl.value(V_lp[vars[s]])
    return V

def policy_improvement(pi, Q):
    stable_policy=True
    states = pi.shape[0]
    a = pi.copy()
    pi = np.argmax(Q,axis=1)
    if (pi!=a).any():
        stable_policy=False
    
    if stable_policy:
        return stable_policy

def value_iteration(num_states, transition_matrix, reward_matrix, discount):
    prev_V = np.zeros(num_states)
    V = np.zeros(num_states)
    while True:
        V = np.max(np.sum(transition_matrix[:,:,:]*(reward_matrix[:,:,:]+discount*prev_V.reshape(1,-1)), axis=2), axis=1)
        if np.sqrt(np.sum((V-prev_V)**2))<1e-9:
            break
        prev_V=V.copy()

    return V

def lp(num_states, num_actions, transition_matrix, reward_matrix, discount, mdptype, end):
    problem = pl.LpProblem('LP', pl.LpMinimize)
    V = np.zeros(num_states)
    vars = [f"V_{i}" for i in range(num_states)]
    V_lp = pl.LpVariable.dicts("V",vars, cat="Continuous")
    # adding the objective function
    problem += pl.lpSum([V_lp[i] for i in vars])
    for s in range(num_states):
        for a in range(num_actions):
            problem += V_lp[vars[s]]-pl.lpSum([transition_matrix[s,a,s1]*discount*V_lp[vars[s1]] for s1 in range(num_states)]) >= pl.lpSum([transition_matrix[s,a,s1]*reward_matrix[s,a,s1] for s1 in range(num_states)])
    
    if mdptype=="episodic" and len(end)>0:
        for e in end:
            problem += (V_lp[vars[e]]==0)
    problem.solve(pl.PULP_CBC_CMD(msg=0))
    for s in range(num_states):
        V[s] = pl.value(V_lp[vars[s]])
    
    return V

def hpi(num_states, num_actions, T, R, gamma, mdptype, end):
    pi = np.zeros(num_states)
    stable_policy = False
    while not stable_policy:
        V = policy_evaluation(pi,T,R,gamma, mdptype, end)
        Q = get_Q(V,T,R,gamma)

        # policy improvement step
        a = pi
        pi = get_policy(Q)
        if (a!=pi).any():
            stable_policy=False
        else:
            return V, pi


if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--mdp", help="specify the path to mdp")
    parser.add_argument("--algorithm", help="specify the algorithm to be used")
    parser.add_argument("--policy")
    args = parser.parse_args()

    num_states = None
    num_actions = None
    mdptype = None
    discount = None
    end = []
    transition_matrix = None
    reward_matrix = None
    policy = None

    path = args.mdp
    with open(path, 'r') as file:
        lines = file.readlines()
        for line_num, line in enumerate(lines):
            values = re.split(" +",line.strip())
            value_type = values[0]
            if value_type=="numStates":
                num_states = int(values[1])
            elif value_type=="numActions":
                num_actions = int(values[1])
                transition_matrix = np.zeros(( num_states, num_actions, num_states))
                reward_matrix = np.zeros(( num_states, num_actions, num_states))
            elif value_type=="end":
                end = list(map(int,values[1:]))
            elif value_type=="transition":
                s1 = int(values[1])
                ac = int(values[2])
                s2 = int(values[3])
                r = float(values[4])
                p = float(values[5])
                transition_matrix[s1,ac,s2] = p
                reward_matrix[s1,ac,s2] = r
            elif value_type=="mdptype":
                mdptype = values[1]
            elif value_type=="discount":
                discount = float(values[1])

    if args.policy is not None:
        with open(args.policy, 'r') as file:
            lines = file.readlines()
            policy = np.zeros(num_states)
            for idx, line in enumerate(lines):
                policy[idx] = int(line[0])

        V = policy_evaluation(policy, transition_matrix, reward_matrix, discount, mdptype, end)
        for s in range(num_states):
            print(V[s],policy[s])
        sys.exit(0)

    elif args.algorithm =="vi":
        V = value_iteration(num_states, transition_matrix, reward_matrix, discount)
        Q = get_Q(V,transition_matrix,reward_matrix,discount)
        pi = get_policy(Q)
        for s in range(num_states):
            print(V[s],pi[s])

            
    elif args.algorithm == "hpi":
        V , pi = hpi(num_states, num_actions, transition_matrix, reward_matrix, discount, mdptype, end)
        for s in range(num_states):
            print(V[s],pi[s])

    else:
        V = lp(num_states, num_actions, transition_matrix, reward_matrix, discount, mdptype, end)
        Q = get_Q(V,transition_matrix, reward_matrix, discount)
        pi = get_policy(Q)
        for s in range(num_states):
            print(V[s],pi[s])
            
            

