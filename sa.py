from random import random, choice, shuffle, sample, randint
from copy import deepcopy
from math import exp
from time import time

#returns true with probability p
def flipCoin(p):
	#generate random number
    r = random()
    #if random number less than p, return true
    #else false
    return r < p
#initializes state randomly
def init(n, E, c, edgno):
	#assigns random color to each vertex
	V = [randint(0, c-1) for _ in range(n)]
	#init all variables
	isling = [None for _ in range(edgno)]
	conflict = set()
	conflictedmatrix = [set() for _ in range(n)]
	hpot = 0
	#setup variables based on V
	for i in range(n):
		for neighbour, number in E[i]:
			#to increase effeciency
			if (neighbour > i):
				if V[i] == V[neighbour]:
					isling[number] = -1
					hpot += 1
					if i not in conflict:
						conflict.add(i)
					if neighbour not in conflict: 
						conflict.add(neighbour)
					conflictedmatrix[i].add(neighbour)
					conflictedmatrix[neighbour].add(i)
				else:
					isling[number] = 1
	#return init state
	return V, isling, conflict, hpot, conflictedmatrix
#returns best of k successors to state
def successor(state, E, c, k):
	minhpot = (float("inf"), None)
	#generating k successors
	for _ in range(k):
		V, isling, conflict, hpot, conflictedmatrix = deepcopy(state)
		#chosing vertex from conflicted set
		i = sample(conflict, 1)[0]
		conflict.discard(i)
		V[i] = randint(0, c-1)
		#updating state for successor
		for neighbour, number in E[i]:
			if isling[number] == -1:
				if V[i] != V[neighbour]:
					isling[number] = 1
					hpot -= 1
					conflictedmatrix[i].remove(neighbour)
					conflictedmatrix[neighbour].remove(i)
					if len(conflictedmatrix[neighbour]) == 0:
						conflict.remove(neighbour)
				else:
					conflict.add(i)
			else:
				if V[i] == V[neighbour]:
					isling[number] = -1
					hpot += 1
					if i not in conflict:
						conflict.add(i)
					if neighbour not in conflict: 
						conflict.add(neighbour)
					conflictedmatrix[i].add(neighbour)
					conflictedmatrix[neighbour].add(i)
		nex = (V, isling, conflict, hpot, conflictedmatrix)
		#selecting successor with minimum potential energy
		if hpot <= minhpot[0]:
			minhpot = (hpot, nex)
	#returns state of chosen successor
	return minhpot[1]				
#implements the simulated annealing and returns time and number 
#of iterations taken to converge to solution
def sa(n, E, c, edgno, t0, it, P, k):
	#for timekeeping
	t1 = time()
	#generates P initial states
	states = [init(n, E, c, edgno) for _ in range(P)]
	T = t0
	while(T>0):
		for r in range(len(states)):
			state = states[r]
			omegap= successor(state, E, c, k)
			dhpot = omegap[3] - state[3]
			#simualted annealing condition
			if dhpot < 0  or flipCoin(exp(-float(dhpot)/float(T))):
				state = omegap
				states[r] = omegap
			#if solved GCP, return time taken
			if state[3]==0:
				t2 = time()
				return t2 - t1, it - float(it*T)/t0 
		#decrement temperature parameterss
		T-=float(t0)/it
	return None
#returns the best value potential energy value currently in the P states
def minat(phantoms):
	#stores min potential energy value
	minval = float("inf")
	for (V, isling, conflict, hpot, conflictedmatrix) in phantoms:
		if len(conflict)<minval:
			minval = len(conflict)
	return minval