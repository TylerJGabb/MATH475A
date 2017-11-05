import sys
import os
import numpy as np
from numpy.linalg import inv
from numpy import dot
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
CUBIC_SPLINE_NAME = "CubicSpline.png"

def main():
	#---------PREPARATION--------
	if(len(sys.argv) < 2):
		print("USAGE: python script.py m")
		print("OPTIONS: -v is verbose output")
		sys.exit(1)

	M = int(sys.argv[1])
	file = open("duck.dat","r")
	lines = file.readlines()
	file.close()

	#---------------------------
	#populate the dataset
	data_set = [(float(data[0]),float(data[1])) for data in [line.strip().split() for line in lines]]
	size = len(data_set)

	f_vec = [point[1] for point in data_set]
	x_vec = [point[0] for point in data_set]

	#create the matrix for solving
	X = np.array([[(x ** m) for m in range(0,M+1)] for x in x_vec])
	X_t = X.transpose()

	#solve the system X_t*X*a = X_t*f_vec
	A = dot(X_t,X)
	b = dot(X_t,f_vec)

	a = np.linalg.solve(A,b)

	#construct a polynomial with the data given
	p = np.poly1d(a[::-1]);

	#create test data with least squares fit
	test = np.arange(0,14,0.1)
	f_c = [p(x) for x in test]

	#create test data with lagrangian
	if M == 20: f_lag = [L(x,x_vec,f_vec) for x in test]


	plt.plot(x_vec,f_vec,'ko',label="data set")
	if M == 20: plt.plot(test,f_lag,'g:',label="lagrangian")
	plt.plot(test,f_c,'r',label="lsq fit order = " + str(M))

	plt.title("duck back approx for m = " + str(M))
	plt.legend()
	plt.ylim([-6,4])
	plt.savefig("python_lsq_" + str(M) + ".png")

	if len(sys.argv) > 2 and '-v' in sys.argv:
		for i in range(0,len(x_vec)):
			print(f_vec[i] - p(x_vec[i]), f_vec[i] - L(x_vec[i],x_vec,f_vec))

	if not os.path.isfile(CUBIC_SPLINE_NAME):
		fig2 = plt.figure()
		plt.plot(x_vec,f_vec,'ko',label="data set")
		cs = CubicSpline(x_vec,f_vec)
		f_cs = [cs(x) for x in test]
		plt.plot(test,f_cs,'b',label="cubic spline")
		plt.legend()
		plt.title("duck back cubic spline")
		plt.ylim([-6,4])
		plt.savefig(CUBIC_SPLINE_NAME)



def l(i,x,x_vec):
	result = 1;
	for j in range(0,len(x_vec)):
		if j == i:
			continue
		result *= (x - x_vec[j])/(x_vec[i] - x_vec[j])
	return result

def L(x,x_vec,f_vec):
	result = 0;
	for i in range(0,len(x_vec)):
		result += f_vec[i]*l(i,x,x_vec)
	return result

main()



















#
