import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

if(len(sys.argv) < 2):
	print("USAGE: python script.py m")
	sys.exit(1)

M = int(sys.argv[1])
def main():
	file = open("duck.dat","r")
	lines = file.readlines()
	file.close()
	#populate the dataset
	data_set = [(float(data[0]),float(data[1])) for data in [line.strip().split() for line in lines]]
	size = len(data_set)

	f_vec = [point[1] for point in data_set];
	x_vec = [point[0] for point in data_set];

	#create the matrix for solving
	X = [[(x ** m) for m in range(0,M+1)] for x in x_vec]

	a = np.linalg.lstsq(X,f_vec)[0]
	
	p = np.poly1d(a[::-1]);

	test = np.arange(0,14,0.1)
	f_c = [p(x) for x in test]

	cs = CubicSpline(x_vec,f_vec,bc_type="natural")
	f_cs = [cs(x) for x in test]

	plt.plot(x_vec,f_vec,'ko',label="data set")
	plt.plot(test,f_cs,'b',label="cubic spline")
	plt.plot(test,f_c,'r',label="lsq fit order = " + str(M))

	plt.title("duck back approx for m = " + str(M))
	plt.legend()
	plt.ylim([0,3])
	plt.savefig("lsqfit_" + str(M) + ".png")
main()
