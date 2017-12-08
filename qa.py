from random import random, choice, shuffle, randint, sample
from copy import deepcopy
from math import exp, log, tanh
from time import time
from random import choice

#returns true with probability p
def flipCoin(p):
	#generate random number
    r = random()
    #if random number less than p, return true
    #else false
    return r < p
#initializes state randomly
def init(n, Adj, c, edgno):
	#state consists of list of set of color classes
	state = [set() for i in range(c)]
	#allocation of vertices to colors
	V = [None for i in range(n)]
	for i in range(n):
		allocated = randint(0, c-1)
		state[allocated].add(i)
		V[i] = allocated
	#F[v][color] = set of vertices that are in neighbour of v
	#and have color
	F = [[] for _ in range(n)]
	conflicted = set()
	for v in range(n):
		for C in range(c):
			F[v].append(len(Adj[v].intersection(state[C])))
		if F[v][V[v]] > 0:
			#if a vertice has neighbours which have 
			#same color as it, add it to the conflicted set
			conflicted.add(v)
	#return totalstate 
	return state, F, V, conflicted
#implements quantum annealing, returns time taken and number of iter
#ations taken to converge
def qa(n, Adj, c, edgno, t0, g0, it, P, scale):
	#for time keeping
	t1 = time()
	#setting all paremeters	
	T = t0
	G = g0
	#approximate bound on kinetic energy to compute exponential values
	#before for all possible values
	maxdeg = -float("inf")
	for v in Adj:
		k = len(v)
		if k > maxdeg:
			maxdeg = k
	Expdenom = []
	for i in range(-maxdeg, maxdeg+1):
		#to prevent math range error as python cannot store e^709+
		if float(i)/(P*T) > 709:
			Expdenom.append(float("inf"))
		else:
			Expdenom.append(exp(float(i)/(P*T)))
	#similar bound on the potential energy term
	maxdegnum = 4*(n-1)
	#initialising all phantoms
	phantoms = [init(n, Adj, c, edgno) for _ in range(P)]
	#list to shuffle order at every iteration
	order = [p for p in range(P)]
	while(G>0):
		shuffle(order)
		Jr = - scale*float(T)/2.0*log(tanh(float(G)/float(P*T)))
		#computing the numerator of the expnonential values here 
		#as it depends on J and J changes at every iteration
		Expnum = []
		for i in range(-maxdegnum, maxdegnum+1):
			#preventing math range error
			if Jr*float(i)/(T) > 709:
				Expnum.append(float("inf"))
			else:
				Expnum.append(exp(Jr*float(i)/(T)))
		for r in order:
			state = phantoms[r]
			colors, F, V, conflicted = state
			if(len(conflicted)==0):
				t2 = time()
				return t2- t1, it - float(it*G)/g0
			#choosing conflicting vertex at random
			v = sample(conflicted, 1)[0]
			#current color
			alpha = V[v]
			#new color
			beta = randint(0, c-1)
			dhpot = F[v][beta] - F[v][alpha]
			if dhpot < 0: 
				#changing state as switching
				#this is only place where we explicit 
				#compute all the values
				colors[alpha].remove(v)
				colors[beta].add(v)
				V[v] = beta
				if F[v][beta] == 0:
					conflicted.remove(v)
					if(len(conflicted)==0):
							t2 = time()
							return t2 - t1, it - float(it*G)/g0
				for neighbour in Adj[v]:
					F[neighbour][alpha]-=1
					F[neighbour][beta]+=1
					if F[neighbour][V[neighbour]]==0:
						conflicted.discard(neighbour)
						if(len(conflicted)==0):
							t2 = time()
							return t2 - t1, it - float(it*G)/g0
				phantoms[r] = colors, F, V, conflicted
			else:
				#first using bounds to check that could a switch even happen
				bound = 4*(len(colors[beta]) + len(colors[alpha]) - 1)
				number = random()
				if(float(dhpot)/P - Jr*(bound) < 0 or float(Expnum[bound + maxdegnum])/Expdenom[dhpot+maxdeg] > number):
					#if switch could happen, we compute the change in the kinetic part of H, using the fact that
					#only neighbouring terms contribute to it
					delta = 0
					#the mod 9 is to cyclically link the last state to the first state for symmetry
					succr = (r+1)%P
					predr = (r-1)%P
					for u in colors[alpha]:
						if u!=v:
							temp = 0
							#based on our Ising variables rules
							if phantoms[succr][2][u] == phantoms[succr][2][v]:
								temp += (-1)
							else:
								temp += 1
							if phantoms[predr][2][u] == phantoms[predr][2][v]:
								temp += (-1)
							else:
								temp += 1
							temp*=2
							delta+= temp
					for u in colors[beta]:
						temp = 0
						#based on our Ising variable rules
						if phantoms[succr][2][u] == phantoms[succr][2][v]:
							temp += (-1)
						else:
							temp += 1
						if phantoms[predr][2][u] == phantoms[predr][2][v]:
							temp += (-1)
						else:
							temp += 1
						temp*=2
						delta-= temp
					#now if change ''actually'' happens, we switch
					if (float(dhpot)/P - Jr*delta < 0 or float(Expnum[int(delta + maxdegnum)]/Expdenom[int(dhpot+maxdeg)]>number)):
						colors[alpha].remove(v)
						colors[beta].add(v)
						V[v] = beta
						if F[v][beta] == 0:
							conflicted.remove(v)
							if(len(conflicted)==0):
								t2 = time()
								return t2 - t1, it - float(it*G)/g0
						for neighbour in Adj[v]:
							F[neighbour][alpha]-=1
							F[neighbour][beta]+=1
							if F[neighbour][V[neighbour]]==0:
								conflicted.discard(neighbour)
								if(len(conflicted)==0):
									t2 = time()
									return t2 - t1, it - float(it*G)/g0
						phantoms[r] = colors, F, V, conflicted
		#decrement G
		G-=float(g0)/it
	return None
#implements quantum annealing but with g0 increasing over time, returns
#time taken to converge
def qarev(n, Adj, c, edgno, t0, g0, it, P, scale):
	#for time keeping
	t1 = time()
	#setting all paremeters	
	T = t0
	G = 0.00000000001
	#approximate bound on kinetic energy to compute exponential values
	#before for all possible values
	maxdeg = -float("inf")
	for v in Adj:
		k = len(v)
		if k > maxdeg:
			maxdeg = k
	Expdenom = []
	for i in range(-maxdeg, maxdeg+1):
		#to prevent math range error as python cannot store e^709+
		if float(i)/(P*T) > 709:
			Expdenom.append(float("inf"))
		else:
			Expdenom.append(exp(float(i)/(P*T)))
	#similar bound on the potential energy term
	maxdegnum = 4*(n-1)
	#initialising all phantoms
	phantoms = [init(n, Adj, c, edgno) for _ in range(P)]
	#list to shuffle order at every iteration
	order = [p for p in range(P)]
	while(G<g0):
		shuffle(order)
		Jr = - scale*float(T)/2.0*log(tanh(float(G)/float(P*T)))
		#computing the numerator of the expnonential values here 
		#as it depends on J and J changes at every iteration
		Expnum = []
		for i in range(-maxdegnum, maxdegnum+1):
			#preventing math range error
			if Jr*float(i)/(T) > 709:
				Expnum.append(float("inf"))
			else:
				Expnum.append(exp(Jr*float(i)/(T)))
		for r in order:
			state = phantoms[r]
			colors, F, V, conflicted = state
			if(len(conflicted)==0):
				t2 = time()
				return t2- t1
			#choosing conflicting vertex at random
			v = sample(conflicted, 1)[0]
			#current color
			alpha = V[v]
			#new color
			beta = randint(0, c-1)
			dhpot = F[v][beta] - F[v][alpha]
			if dhpot < 0: 
				#changing state as switching
				#this is only place where we explicit 
				#compute all the values
				colors[alpha].remove(v)
				colors[beta].add(	v)
				V[v] = beta
				if F[v][beta] == 0:
					conflicted.remove(v)
					if(len(conflicted)==0):
							t2 = time()
							return t2 - t1
				for neighbour in Adj[v]:
					F[neighbour][alpha]-=1
					F[neighbour][beta]+=1
					if F[neighbour][V[neighbour]]==0:
						conflicted.discard(neighbour)
						if(len(conflicted)==0):
							t2 = time()
							return t2 - t1
				phantoms[r] = colors, F, V, conflicted
			else:
				#first using bounds to check that could a switch even happen
				bound = 4*(len(colors[beta]) + len(colors[alpha]) - 1)
				number = random()
				if(float(dhpot)/P - Jr*(bound) < 0 or float(Expnum[bound + maxdegnum])/Expdenom[dhpot+maxdeg] > number):
					#if switch could happen, we compute the change in the kinetic part of H, using the fact that
					#only neighbouring terms contribute to it
					delta = 0
					#the mod 9 is to cyclically link the last state to the first state for symmetry
					succr = (r+1)%P
					predr = (r-1)%P
					for u in colors[alpha]:
						if u!=v:
							temp = 0
							#based on our Ising variables rules
							if phantoms[succr][2][u] == phantoms[succr][2][v]:
								temp += (-1)
							else:
								temp += 1
							if phantoms[predr][2][u] == phantoms[predr][2][v]:
								temp += (-1)
							else:
								temp += 1
							temp*=2
							delta+= temp
					for u in colors[beta]:
						temp = 0
						#based on our Ising variable rules
						if phantoms[succr][2][u] == phantoms[succr][2][v]:
							temp += (-1)
						else:
							temp += 1
						if phantoms[predr][2][u] == phantoms[predr][2][v]:
							temp += (-1)
						else:
							temp += 1
						temp*=2
						delta-= temp
					#now if change ''actually'' happens, we switch
					if (float(dhpot)/P - Jr*delta < 0 or float(Expnum[int(delta + maxdegnum)]/Expdenom[int(dhpot+maxdeg)]>number)):
						colors[alpha].remove(v)
						colors[beta].add(v)
						V[v] = beta
						if F[v][beta] == 0:
							conflicted.remove(v)
							if(len(conflicted)==0):
								t2 = time()
								return t2 - t1
						for neighbour in Adj[v]:
							F[neighbour][alpha]-=1
							F[neighbour][beta]+=1
							if F[neighbour][V[neighbour]]==0:
								conflicted.discard(neighbour)
								if(len(conflicted)==0):
									t2 = time()
									return t2 - t1
						phantoms[r] = colors, F, V, conflicted
		#incriment G
		G+=float(g0)/it
	return None
#returns the best value potential energy value currently in the P states
def minat(phantoms):
	#stores min potential energy value
	minval = float("inf")
	for colors, F, V, conflicted in phantoms:
		if len(conflicted)<minval:
			minval = len(conflicted)
	return minval