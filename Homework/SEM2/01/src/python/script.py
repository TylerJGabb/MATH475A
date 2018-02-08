import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal
import math

#Laziness here#########################################
sin = lambda a : np.sin(a)
cos = lambda a : np.cos(a)
exp = lambda a : np.exp(a)
abs = lambda a : np.abs(a)
sci = lambda num: '%.2E' % Decimal(num)
#######################################################

#useful predefined functions#####################################
analytical_solution = lambda t: (cos(t) + sin(t) - exp(t))/2
f = lambda t, x : x - sin(t)
E = lambda t, x: max(abs(analytical_solution(t) - x))
euler = lambda t, x, delta : x + f(t,x)*delta

def trap(xn,tn,tn_plus_1,delta):
	a = 1 - delta/2
	b = 1 + delta/2
	c = delta/2
	return (xn*b - c*(sin(tn) + sin(tn_plus_1)))/a

'''Returns the ending slope of a given curve'''
def slope(N_arr,E_arr,a=4,b=5):
	E1 = E_arr[a];
	E2 = E_arr[b]
	N1 = N_arr[a];
	N2 = N_arr[b]
	return (E2 - E1)/(N2-N1)
#################################################################

''' Adams Bashford 2nd Order'''
def AB2(N,firstGuessMethod):
	__AB2 = lambda x1,x2,t1,t2,delta : x2 + (delta/2)*( 3*f(t2,x2) - f(t1,x1))
	delta = np.pi/N;
	if firstGuessMethod == 'trap':
		x1 = trap(0,0,delta,delta)
	elif firstGuessMethod == 'euler':
		x1 = euler(0,0,delta)
	else:#special
		'''Find X1 via AB2 with N divisions between 0 and t1'''
		delta_subint = delta/N
		t_subint = np.arange(0,delta + delta_subint ,delta_subint)
		x_subint = [0,0]#start with simple forward euler
		i = 0;
		while len(x_subint) < len(t_subint):
			x1 = x_subint[-2]
			x2 = x_subint[-1]
			t1 = t_subint[i]
			t2 = t_subint[i+1]
			x_subint.append(__AB2(x1,x2,t1,t2,delta_subint))
			i += 1
		x1 = x_subint[-1];

	'''STAGE TWO: Begin AB2 With newly found X1'''
	x = [0,x1]
	t = np.arange(0,np.pi + delta, delta)
	i = 0;
	while len(x) < len(t):
		x1 = x[-2]
		x2 = x[-1]
		t1 = t[i]
		t2 = t[i+1]
		x.append(__AB2(x1,x2,t1,t2,delta))
		i += 1
	return (E(t,x),t,x)

'''
Adams Molton 3rd order
'''
def AM3(N):
	delta = np.pi/N
	'''For internal use only, AB3 method defined in function scope'''
	def __AM3(xmin,xn,tn,delta):
		#n-1 = 0, n = 1
		tmin = tn-delta
		tplus = tn+delta
		bneg = 5/12
		b0 = 2/3
		b1 = -1/12 #Don't fugg up this time mang
		a = 1-delta*bneg
		fn = f(tn,xn)
		fmin = f(tmin,xmin)
		term1 = delta * (-bneg*sin(tplus) + b0*fn + b1*fmin)
		return (xn + term1)/a


	'''STAGE ONE: To subinterval iteration with N intervals between 0 and t1 to find x1'''
	delta_subint = delta/N
	t_subint = np.arange(0,delta + delta_subint, delta_subint);
	x_subint = [0,0] #simple euler to start again
	i = 1
	while len(x_subint) < len(t_subint):
		x1 = x_subint[-2]
		x2 = x_subint[-1]
		t1 = t_subint[i]
		x_subint.append(__AM3(x1,x2,t1,delta_subint));
		i += 1
	x1 = x_subint[-1]
	x = [0,x1]
	t = np.arange(0,np.pi + delta, delta)
	i = 1;
	'''STAGE TWO: To regular interval iteration  with AM3 with newly found X1'''
	while len(x) < len(t):
		x1 = x[-2]
		x2 = x[-1]
		t1 = t[i]
		x.append(__AM3(x1,x2,t1,delta))
		i += 1
	return (E(t,x),t,x)
	

def orderOfDecade(decade,N_arr,E_arr):
	decade = int(decade)
	i = N_arr.index(decade);
	return str(abs(round(math.log(E_arr[i+9],10) - math.log(E_arr[i],10),3)))


def plotsComparative():
	N_arr = [n*10**m for n in range(1,10) for m in (2,3,4,5)]
	N_arr.sort()
	N_arr.append(1000000);
	E_trap = []
	E_euler = []
	E_special = []
	E_am3 = []
	print('aquiring data')
	for N in N_arr:
		print('N=',N)
		print('\tAB2_TRAP')
		E_trap.append(AB2(N,firstGuessMethod='trap')[0])
		print('\tAB2_EULR')
		E_euler.append(AB2(N,firstGuessMethod='euler')[0])
		print('\tAB2_SPECL')
		E_special.append(AB2(N,firstGuessMethod='special')[0])
		print('\tAM3_EULR')
		E_am3.append(AM3(N)[0])

	print('generating plots')

	decade = 10**3
	plt.plot(N_arr,E_trap,label='AB2_TRAP O=' + orderOfDecade(decade,N_arr,E_trap))
	plt.plot(N_arr,E_euler,label='AB2_EULR O=' + orderOfDecade(decade,N_arr,E_euler))
	plt.plot(N_arr,E_special,label='AB2_SPECL O=' + orderOfDecade(decade,N_arr,E_special))
	plt.plot(N_arr,E_am3,label='AM3_SPECL O=' + orderOfDecade(decade,N_arr,E_am3))
	plt.yscale('log')
	plt.xscale('log')
	plt.legend()
	plt.grid(True)
	plt.savefig('plotsComparative.png')


plotsComparative()
#plot_highResAM3()
