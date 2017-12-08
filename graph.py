from random import random

#generate graph with n vertices and d expected edges from each vertice
#and c is the number of colors
def generate(n, d):
	E = [[] for _ in range(n)]
	Adj = [set() for _ in range(n)]
	#probability of each edge
	p = float(d)/(n+1)
	#to index edges
	edgeno = -1
	#making sure there exist > 0 edges
	while(edgeno==-1):
		edgeno = -1
		for i in range(n):
			for j in range(i+1, n):
				if (random() < p):
					edgeno+=1
					#edges are bidirectional
					E[i].append((j, edgeno))
					E[j].append((i, edgeno))
					Adj[i].add(j)
					Adj[j].add(i)
					
	return Adj, E, edgeno+1
