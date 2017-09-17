import matplotlib.pyplot as plt
import math as M
import sys
VAL = int(sys.argv[1]);
ITERS = int(sys.argv[2]);
def main():
    """
    The main Function
    """
    if len(sys.argv) < 3:
        print("Usage: python3 problem1.py POWER ITERATIONS")
        exit(1)
 
    pos_50_algo_1_list = algo1(VAL)
    pos_50_algo_2_list = algo2(VAL)

    neg_50_algo_1_list = algo1(-VAL)
    neg_50_algo_2_list = algo2(-VAL)

    x = plt.figure(1)
    plt.plot([abs(x - M.exp(VAL)) for x in pos_50_algo_1_list],'r--',label="Algo I",linewidth=2.5)
    plt.plot([abs(x - M.exp(VAL)) for x in pos_50_algo_2_list],'b--',label="Algo II",linewidth=2.5)
    plt.legend(loc='best')
    plt.title('Error in value at iteration For +' + str(VAL))
    plt.yscale('log', basex=10);
    x.show()

    y = plt.figure(2)
    plt.plot([abs(x - M.exp(-VAL)) for x in neg_50_algo_1_list],'r--',label="Algo I",linewidth=2.5)
    plt.plot([abs(x - M.exp(-VAL)) for x in neg_50_algo_2_list],'b--',label="Algo II",linewidth=2.5)
    plt.legend(loc='best')
    plt.title('Error in value at iteration For -' + str(VAL))
    plt.yscale('log', basex=10);
    y.show()

    input()

def algo1(x):
    """
    Returns an array of 200 terms, each a sucessive iterative approximation
    for e raised to the power of x. uses "Algorithm I"
    """
    terms = []
    s = 1
    t = x
    N_values = list(range(1,ITERS + 1))
    for n in N_values:
        s = s + t
        t = t * x / (n + 1)
        terms.append(s)

    return terms

def algo2(x):
    """
    Returns an array of 200 terms, each a sucessive iterative approximation
    for e raised to the power of x. uses "Algorithm II"
    """
    terms = []
    s = 1
    for n in range(ITERS,0,-1):
        s = (s * x / n) + 1
        terms.append(s)

    return terms



main()



   
