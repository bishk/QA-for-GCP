import graph
from math import floor
from sa import sa
from qa import qa, qarev
import cycle
from bayesian_optimization import BayesianOptimization

P = 10

'''
#Functions for Bayesian optimization
def Bay_qaw(t0, g0):
	Adj, E, edgno = graph.generate(100, 20)
	sum = 0
	for _ in range(10):
		sum+= qa(100, Adj, 25, edgno, t0, g0, 100, P, 1.0)[0]
	return -sum

def Bay_qaw0(t0, g0):
	Adj, E, edgno = graph.generate(100, 20)
	sum = 0
	for _ in range(10):
		sum+= qa(100, Adj, 25, edgno, t0, g0, 100, P, 0.00)[0]
	return -sum
#FOR BAYESIAN OPTIMIZATION
bo = BayesianOptimization(Bay_qaw,{'t0': (0.00000000001, 1), 'g0': (0.0000000001, 10)})
bo.maximize(init_points=15, n_iter=45, kappa=2)
print(bo.res['max']) 
'''


B = 0 #FOR TIME TAKEN

#QA forward vs QA backward
for _ in range(100):
	Adj, E, edgno = graph.generate(500, 200)
	print qa(500, Adj, 250, edgno, 0.62, 1.2, 1000, P, 1.0)[B], qarev(500, Adj, 250, edgno, 0.62, 1.2, 1000, P, 1.0)[B]

#should get similar results for both