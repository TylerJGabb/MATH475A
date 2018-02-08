import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal

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
	t = np.arange(0,np.pi,delta)
	if firstGuessMethod == 'trap':
        x1 = trap(0,0,delta,delta)
	elif firstGuessMethod == 'euler':
		x1 = euler(0,0,delta)
	else:#special
		delta2 = delta/N
		t = list(np.arange(0,delta,delta2))
		t_end = list(np.arange(delta,np.pi,delta))
		t.extend(t_end)
		t = np.array(t)
		x1 = euler(0,0,delta2)
	x = [0,x1];
	i = 0;
	while len(x) < len(t):
		x1 = x[-2]
		x2 = x[-1]
		t1 = t[i]
		t2 = t[i+1]
		x.append(__AB2(x1,x2,t1,t2,delta))
		i += 1
	return (E(t,x),t,x)

'''Adams Molton 3rd order'''
def AM3(N):
	def __AM3(xmin,xn,tn,delta):
		#n-1 = 0, n = 1
		tmin = tn-delta
		tplus = tn+delta
		bneg = 5/12
		b0 = 2/3
		b1 = 1/12
		a = 1-delta*bneg
		fn = f(tn,xn)
		fmin = f(tmin,xmin)
		term1 = delta * (-bneg*sin(tplus) + b0*fn - b1*fmin)
		#After consulting wikipedia, it was determined the sign on
		#b1*fmin was incorrect, it was positive and needed to be negative
		return (xn + term1)/a
	delta = np.pi/N
	t = np.arange(0,np.pi,delta)
	x = [0,0.05]
	i = 1
	while len(x) < len(t):
		xmin = x[-2]
		xn = x[-1]
		tn = t[i]
		x.append(__AM3(xmin,xn,tn,delta))
		i += 1
	return (E(t,x),t,x)

def plot_highResAM3(data_only=False):
    N_arr = []
    E_am3 = []
    incr = 10
    n = 10
    while n <= 	1000000:
        N_arr.append(n)
        n += incr
        if len(str(n)) > len(str(incr)):
	        incr *= 10
			
    for N in N_arr:
        print('N=',N)
        E_am3.append(AM3(N)[0])
    if data_only:
        return (N_arr,E_am3)
    else:
        plt.plot(N_arr,E_am3,label='AM3_TRAP ' + sci(slope(N_arr,E_am3,27,36)))
        plt.yscale('log')
        plt.xscale('log')
        plt.legend()
        plt.grid(True)
        plt.savefig('highResAM3_' + str(N_arr[-1]) + '.png')

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
	plt.plot(N_arr,E_trap,label='AB2_TRAP ' + sci(slope(N_arr,E_trap,18,27)))
	plt.plot(N_arr,E_euler,label='AB2_EULR ' + sci(slope(N_arr,E_euler,18,27)))
	plt.plot(N_arr,E_special,label='AB2_SPECL ' + sci(slope(N_arr,E_special,18,27)))
	plt.plot(N_arr,E_am3,label='AM3_EULR ' + sci(slope(N_arr,E_am3,18,27)))
	plt.yscale('log')
	plt.xscale('log')
	plt.legend()
	plt.grid(True)
	plt.savefig('plotsComparative.png')



plotsComparative()
#plot_highResAM3()
