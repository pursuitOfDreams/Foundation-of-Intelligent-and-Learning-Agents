#! /usr/bin/python
from email import policy
import random,argparse,sys,subprocess,os
import numpy as np
import csv, argparse, os, re, signal, importlib, sys, io, time, shutil
from subprocess import Popen, PIPE
import func_timeout
random.seed(0)

oldstdout_fno = os.dup(sys.stdout.fileno())

class VerifyOutputPlanner:
    def __init__(self,algorithm,print_error):
        input_file_ls = ['data/mdp/test_c1.txt','data/mdp/test_c2.txt','data/mdp/test_ep1.txt','data/mdp/test_ep2.txt']
        algorithm_ls = list()
        if algorithm=='all':
            algorithm_ls+=['vi','hpi','lp']
        else:
            algorithm_ls.append(algorithm)
        marks_t1 = 0
        feedback = 'Task 1: '
        marks_per = {'hpi': 0.625, 'vi': 0.25, 'lp' : 0.625}    
        for algo in algorithm_ls:
            counter = 1    
            feedback += ' ' + algo + ': '
            for in_file in input_file_ls:
                correct = 0
                if algo == 'default':
                    cmd_planner = "python3","planner.py","--mdp",in_file
                else:
                    cmd_planner = "python3","planner.py","--mdp",in_file,"--algorithm",algo
                print(cmd_planner)
                counter+=1
                try:
                    cmd_output = subprocess.check_output(cmd_planner,universal_newlines=True)
                except Exception as e:
                    feedback += '+0 (error: '
                    feedback += str(e) 
                    feedback += ') '
                    continue
                try:
                    correct, mistake = self.verifyOutput(cmd_output,in_file,print_error)
                except Exception as e:
                    correct = 0
                    mistake = 1
                    feedback += '+0 (error: '
                    feedback += str(e) 
                    feedback += ') '
                    continue
                if (correct):
                    marks_t1 += marks_per[algo]
                    feedback += '+'+str(marks_per[algo])
                else:
                    feedback += '+0'
                    if (mistake):
                        feedback+= '(due to wrong output formatting/error in file) '
                    else:
                        feedback+= '(due to incorrect value function) '
    
        policy_eval_files = ['data/mdp/test_c1.txt', 'data/mdp/test_ep2.txt']
        policies = {'data/mdp/test_c1.txt':'data/mdp/test_peval1.txt', 'data/mdp/test_ep2.txt':'data/mdp/test_peval2.txt'}
        feedback += '  Policy evaluation' + ': '
        for in_file in policy_eval_files:
            policy_file = policies[in_file]
            cmd_planner = "python3","planner.py","--mdp",in_file, "--policy", policy_file
            try:
                cmd_output = subprocess.check_output(cmd_planner,universal_newlines=True)
            except Exception as e:
                feedback += '+0 (error: '
                feedback += str(e) 
                feedback += ') '
                continue
            print(cmd_planner)
            counter+=1                        
            try:
                correct, mistake = self.verifyOutput(cmd_output,in_file,print_error,True, policy_file.replace("test","ans"))
            except Exception as e:
                correct = 0
                mistake = 1
                feedback += str(e)

            if (correct):
                marks_t1 += 0.5
                feedback += '+0.5'
            else:
                feedback += '+0'
                if (mistake):
                    feedback+= '(due to wrong output formatting) '
                else:
                    feedback+= '(due to incorrect value function) '
        self.marks_t1 = marks_t1
        self.feedback = feedback
        
                    
            
            

    def verifyOutput(self,cmd_output,in_file,pe, pol_eval = False, sol_file = None):
        correct = 1
        if pol_eval==False:
            sol_file = in_file.replace("test","ans")


        base = np.loadtxt(sol_file,delimiter=" ",dtype=float)
        output = cmd_output.split("\n")
        nstates = base.shape[0]
        
        est = [i.split() for i in output if i!='']
        
        
        mistakeFlag = False
        #Check1: Checking the number of lines printed
        if not len(est)==nstates:
            print('wrong number of lines (file, correct):', len(est), nstates)
            mistakeFlag = True
            
        #Check2: Each line should have only two values
        for i in range(len(est)):
            if not len(est[i])==2:
                print('Instead of 2, terms in line: ', len(est[i]))
                mistakeFlag = True
                break
        
            
        pe_ls = ['no','NO','No','nO']
        if not mistakeFlag:
            print("Calculating error of your value function...")
            pass
        else:
            print("\nExiting without calculating error of your value function")
            return 0, mistakeFlag
        #calculating the error
        for i in range(len(est)):
            est_V = float(est[i][0]);base_V = float(base[i][0])
            print("%10.6f"%est_V,"%10.6f"%base_V,"%10.6f"%abs(est_V-base_V),end="\t")
            if abs(est_V-base_V) <= (10**-4):
                print("OK")
                pass
            else:
                correct = 0
                print("\tNot OK")
        if mistakeFlag:
            flag_ok = 0
        if not (mistakeFlag) or not (correct):
            print("ALL CHECKS PASSED!")
        else:
            print("You haven't printed output in correct format.")
        return correct, mistakeFlag
            

def run(states, p1_parameter, q):
    cmd_encoder = "python3","encoder.py","--parameters", p1_parameter, "--q", q, "--states",states
    # print("\n","Generating the MDP encoding using encoder.py")
    f = open('verify_attt_mdp','w')
    try:
        subprocess.call(cmd_encoder,stdout=f)
    except Exception as e:
        f.close()
        return 'Fail in calling encoder'
    f.close()

    cmd_planner = "python3","planner.py","--mdp","verify_attt_mdp"
    # print("\n","Generating the value policy file using planner.py using default algorithm")
    f = open('verify_attt_planner','w')
    try:
        subprocess.call(cmd_planner,stdout=f)
    except Exception as e:
        f.close()
        return 'Fail in calling planner'
    f.close()

    cmd_decoder = "python3","decoder.py","--value-policy","verify_attt_planner","--states",states 
    # print("\n","Generating the decoded policy file using decoder.py")
    try:
        cmd_output = subprocess.check_output(cmd_decoder,universal_newlines=True)
    except Exception as e:
        return 'Fail in calling decoder'

    os.remove('verify_attt_mdp')
    os.remove('verify_attt_planner')
    return cmd_output

def verifyOutput(states, output, in_file, q):
    correct = 1
    mistake = False
    output = output.split('\n')
    if '' in output:
        output.remove('')
    with open(states,'r') as file:
        lines = file.readlines()
    states = [line.strip() for line in lines]
    if len(output) != len(states):
        # print("\n","*"*10,f"Mistake: Expected {len(states)} policy lines, got {len(output)-1}")
        return 0, True
        sys.exit()
    
    policy_states=[]
    for idx,out in enumerate(output):
        terms = out.split(' ')
        if (terms[1] not in ['0','1','2','4','6']):
            # print("\n", terms[1], " is not a valid action")
            return 0, True
        if len(terms) !=3:
            # print("\n","*"*10,f"Mistake: In line {idx+1}, expected 3 terms , got {len(terms)}. {out}")
            return 0, True
            sys.exit()
        policy_states.append(terms[0])
        try:
            p = list(map(float,terms[1:]))
        except:
            # print("\n","*"*10,f"Mistake: In line {idx+1}, Number format excpetion. {out}")
            return 0, True
            sys.exit()
    
    states_intersection = set(states).intersection(set(policy_states))
    if len(states_intersection) != len(states):
        # print('States missing', set(states).difference(states_intersection))
        # print("\n","*"*10,f"Mistake: States in policy file and input states file do not match")
        return 0, True
        sys.exit()

    # print("Verifying policy and win probabilities")
    sol_file = in_file.replace("sample","sol")
    sol_file = 'data/cricket/ans_{' +in_file[-5]+'}_{'+q+'}'
    base = np.loadtxt(sol_file,delimiter=" ",dtype=float)
    
    for i in range(len(output)):
        terms = output[i].split(' ')
        est_V = float(terms[2])
        base_V = float(base[i][2])
        # est_A = int(terms[1])
        # base_A = int(base[i][1])
        print("%10.6f"%est_V,"%10.6f"%base_V,"%10.6f"%abs(est_V-base_V),end="\t")
        if abs(est_V-base_V) > (10**-2):
            correct = 0
            print(terms[0], end=' ')
            print("\t Value function not OK")
        else:
            print(' OK')

    return correct, mistake
    
    # print("All OK")

def task1():
    list_re = os.listdir()
    algo = VerifyOutputPlanner('all','no')
    # return algo.marks_t1, str(list_re)
    return algo.marks_t1, algo.feedback

def task2():
    in_file_ls = ['data/cricket/test-1.txt', 'data/cricket/test-2.txt', 'data/cricket/test-2.txt', 'data/cricket/test-4.txt', 'data/cricket/test-5.txt']
    states = 'data/cricket/cricket_state_list.txt'
    q = ['0.25', '0.00', '1.00', '0.00', '0.50']
    i = 0

    marks = 0
    feedback = ' Task 2: '
    for in_file in in_file_ls:
        print ("Running for ", states, ' with policy', in_file, ' and q = ', q[i])
        output = run(states,in_file,q[i])
        if  len(output)<1 or output[0] == 'F':
            feedback += output
            return 0, feedback
        correct, mistake = verifyOutput(states, output, in_file, q[i])
        if (correct):
            marks += 1
            feedback += '+1'
        else:
            feedback += '+0'
            if (mistake):
                feedback+= '(due to wrong output formatting) '
            else:
                feedback+= '(due to incorrect value function) '
        i+=1
    return marks, feedback



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', type = int, default= 3)
    parser.add_argument("--algorithm",type=str,default="default")
    parser.add_argument("--pe",type=str,default="yes")
    parser.add_argument("--states",type=str,help="File with valid states of the player", default="NA")
    parser.add_argument("--parameters",type=str,help="File with valid environment parameters", default="NA")
    parser.add_argument("--q",type=str,help="Weakness of player B", default="0.25")
    parser.add_argument('--sheet', type=str, required=False, default = '',help='Path of grading sheet')
    args = parser.parse_args()

    #print(args)
    #sys.exit(0)
    if(args.task == 1):
        #algo = VerifyOutputPlanner(args.algorithm,args.pe)
        task1()
    elif (args.task == 2):
        task2()
    elif (args.task == 3):
        marks1, feed1 = func_timeout.func_timeout(40 * 60, task1, ())
        marks2, feed2 = func_timeout.func_timeout(20 * 60, task2, ())
        marks = marks1 + marks2
        feedback = feed1+ feed2
        print(marks, feedback)
        
