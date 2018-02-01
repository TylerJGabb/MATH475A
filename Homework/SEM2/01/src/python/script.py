import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal

#Laziness here
sin = lambda a : np.sin(a)
cos = lambda a : np.cos(a)
exp = lambda a : np.exp(a)
abs = lambda a : np.abs(a)
sci = lambda num: '%.2E' % Decimal(num)

#useful predefined functions
analytical_solution = lambda t: (cos(t) + sin(t) - exp(t))/2
f = lambda t, x : x - sin(t)
E = lambda t, x: max(abs(analytical_solution(t) - x))
Euler_forward_single = lambda t, x, delta : x + f(t,x)*delta

def Trap_multi(xn,tn,tn_plus_1,delta):
	a = 1 - delta/2
	b = 1 + delta/2
	c = delta/2
	return (xn*b - c*(sin(tn) + sin(tn_plus_1)))/a

def AM3(x0,x1,t0,t1,delta):
	#n-1 = 0, n = 1
	bneg = 5/12
	b0 = 2/3
	b1 = 1/12
	a = 1-delta*bneg

	


''' Adams Bashford 2nd Order'''
def adams_bash_2(N,x1,power=1):
	AB2 = lambda x1,x2,t1,t2,delta : x2 + (delta/2)*( 3*f(t2,x2) - f(t1,x1))
	delta = np.pi/N**power;
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

def end_slope(N_arr,E_arr):
	E1 = E_arr[-2];
	E2 = E_arr[-1]
	N1 = N_arr[-2];
	N2 = N_arr[-1]
	return (E2 - E1)/(N2-N1)

def adams_molton_3(N):





def run_adams_bash_plot():
	E_trap_multi = []
	E_euler_forward = []
	N_arr = [10**(i+1) for i in range(6)]
	for N in N_arr:
		delta = np.pi/N;
		x1_trap = Trap_multi(0,0,delta,delta)
		x1_eulr = Euler_forward_single(0,0,delta)
		E_trap_multi.append(adams_bash_2(N,x1_trap))
		E_euler_forward.append(adams_bash_2(N,x1_eulr))
		print('ran',N,'x1_trap=',x1_trap,'x1_eulr=',x1_eulr)

	trap_slope = end_slope(N_arr,E_trap_multi)
	eulr_slope = end_slope(N_arr,E_euler_forward)

	plt.plot(N_arr,E_trap_multi,'r-',linewidth=2,label='Trapezoidal ' + sci(trap_slope))
	plt.plot(N_arr,E_euler_forward,'b-',linewidth=2,label='Forward Euler ' + sci(eulr_slope))
	plt.yscale('log')
	plt.xscale('log')
	plt.grid(True)
	plt.legend()
	plt.savefig('adams_bash2.png')
