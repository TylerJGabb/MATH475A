import numpy as np
import matplotlib.pyplot as plt

#Laziness here
sin = lambda a : np.sin(a)
cos = lambda a : np.cos(a)
exp = lambda a : np.exp(a)
abs = lambda a : np.abs(a)

#useful predefined functions
analytical_solution = lambda t: (cos(t) + sin(t) - exp(t))/2
f = lambda t, x : x - sin(t)
E = lambda t, x: max(abs(analytical_solution(t) - x))
Euler_forward_single = lambda t, x, delta : x + f(t,x)*delta


''' Adams Bashford 2nd Order'''
def adams_bash_2(N,x1):
	AB2 = lambda x1,x2,t1,t2,delta : x2 + (delta/2)*( 3*f(t2,x2) - f(t1,x1))
	delta = np.pi/N;
	t = np.arange(0,np.pi,delta)
	x = [0,x1];
	i = 0;
	while len(x) < len(t):
		x1 = x[-2]
		x2 = x[-1]
		t1 = t[i]
		t2 = t[i+1]
		x.append(AB2(x1,x2,t1,t2,delta))
		i += 1
	return E(t,x)
