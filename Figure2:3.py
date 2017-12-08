import graph
from math import floor
from sa import sa
from qa import qa, qarev
import cycle
from bayesian_optimization import BayesianOptimization

P = 10

'''
Functions for Bayesian optimization
def Bay_qa(t0, g0):
	Adj, E, edgno = graph.generate(100, 20)
	sum = 0
	for _ in range(10):
		sum+= qa(100, Adj, 25, edgno, t0, g0, 100, P, 1.0)[0]
	return -sum
def Bay_sa(t0):
	Adj, E, edgno = graph.generate(100, 20)
	sum = 0
	for _ in range(10):
		sum+= sa(100, E, 25, edgno, t0, 1000, 1, 1)[0]
	return -sum
def Bay_psa(t0):
	Adj, E, edgno = graph.generate(100, 20)
	sum = 0
	for _ in range(10):
		sum+= sa(100, E, 25, edgno, t0, 1000, P, 1)[0]
	return -sum
def Bay_ba(t0):
	Adj, E, edgno = graph.generate(100, 20)
	sum = 0
	for _ in range(10):
		sum+= sa(100, E, 25, edgno, t0, 1000, 1, P)[0]
	return -sum
#FOR BAYESIAN OPTIMIZATION
bo = BayesianOptimization(FUNCTION TO OPTIMIZE,{'t0': (0.00000000001, 1), 'g0': (0.0000000001, 10)})
bo.maximize(init_points=15, n_iter=45, kappa=2)
print(bo.res['max']) 
'''

#Toggle below to compare time taken or numbe of iterations (Figure 2 and 3)
#B = 0 #FOR TIME TAKEN
#B = 1 #FOR NUMBER OF ITERATIONS

#QA vs SA vs PSA vs BA
for _ in range(100):
	Adj, E, edgno = graph.generate(100, 20)
	print qa(100, Adj, 25, edgno, 0.35, 0.75, 100, P, 1.0)[B], sa(100, E, 25, edgno, 0.35, 1000, 1, 1)[B], sa(100, E, 25, edgno, 0.35, 1000, P, 1)[B], sa(100, E, 25, edgno, 0.35, 1000, 1, P)[B] 
