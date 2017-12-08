import graph
from math import floor
from sa import sa
from qa import qa, qarev
import cycle
from bayesian_optimization import BayesianOptimization

def Bay_SA(t0, x):
	Adj, E, edgno = graph.generate(100, 20)
	sum = 0
	for _ in range(3):
		sum+= sa(100, E, 25, edgno, t0, 100, 1+int(floor(x)), 1+10-int(floor(x)))[0]
	return -sum

#FOR BAYESIAN OPTIMIZATION
bo = BayesianOptimization(Bay_SA,{'t0': (0.00000000001, 1), 'x': (0.0000000001, 10)})
bo.maximize(init_points=15, n_iter=45, kappa=2)
print(bo.res['max']) 

#floor(x) should converge to 0