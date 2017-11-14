from matplotlib import pyplot as plt
from numpy import *;
import sys;

#define f(x)
f = lambda x: arctan(x)


#terms in the lagrangian
def l(i,x,x_vec):
	result = 1;
	for j in range(0,len(x_vec)):
		if j == i:
			continue
		result *= (x - x_vec[j])/(x_vec[i] - x_vec[j])
	return result


#the entire lagrangian
def L(x,x_vec,f_vec):
	result = 0;
	for i in range(0,len(x_vec)):
		result += f_vec[i]*l(i,x,x_vec)
	return result

def makeGenericPlots():
    fine = linspace(-11,11,500)

    for N in [2,4,6,16,32]:
        plt.figure()
        plt.plot(fine,[f(x) for x in fine],'k-',linewidth=2,label="f(x)")
        x_vec = [float(str(x)[:5]) for x in list(linspace(-10,10,N))]
        f_vec = [f(x) for x in x_vec]
        lagrangian = [L(x,x_vec,f_vec) for x in fine];
        plt.plot(fine,lagrangian,label=("N="+str(N)))
        plt.plot(x_vec,f_vec,'ro',linewidth=2,label="data set");
        plt.ylim([-2,2]);
        plt.legend();
        plt.savefig("lagrangian_10_"+str(N)+".png")




def main():
	makeGenericPlots()
main()

#END OF FILE
