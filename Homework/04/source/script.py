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


def makeOptimizedPlot(x_vec):
	fine = linspace(-10,10,500)
	f_vec = [f(x) for x in x_vec]
	lagrangian = [L(x,x_vec,f_vec) for x in fine];
	plt.plot(fine,[f(x) for x in fine],'k-',linewidth=2,label="f(x)")
	plt.plot(fine,lagrangian,label=("N="+str(6)))
	plt.plot(x_vec,f_vec,'ro',linewidth=2,label="data set");
	plt.ylim([-2,2]);

	errs = [abs(lagrangian[i] - f(fine[i])) for i in range(len(fine))]
	err = max(errs)
	i = errs.index(err)
	x = fine[i]
	lag = L(x,x_vec,f_vec)
	f_x = f(x)
	tupe = (f_x,lag)
	a = min(tupe);
	b = max(tupe);
	perc_err = 100*abs((f(x) - lag)/f_x)
	plt.plot([x,x],[a,b],'c:',label='max err='+str(perc_err)[:5]+'%',marker='d');

	name = "_".join([str(x) for x in x_vec])
	plt.legend();
	plt.savefig("optimized/optimized_" +name+ ".png")
	#10,7.5,3.7


def main():
    if(len(sys.argv) > 3):
        a1 = -float(sys.argv[1])
        a2 = -float(sys.argv[2])
        a3 = -float(sys.argv[3])
        a4 = -a3;
        a5 = -a2;
        a6 = -a1;
        x_vec = [a1,a2,a3,a4,a5,a6]
        makeOptimizedPlot(x_vec)
main()












#END OF FILE
