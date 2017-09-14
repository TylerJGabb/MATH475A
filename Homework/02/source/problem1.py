import matplotlib.pyplot as plt
import math as M



def algo1(x):
    """
    Returns an array of 200 terms, each a sucessive iterative approximation
    for e raised to the power of x. uses "Algorithm I"
    """
    terms = []
    s = 1
    t = x
    N_values = list(range(1,201))
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
    for n in range(200,0,-1):
        s = s * x / n + 1
        terms.append(s)

    return terms

def main():
    """
    The main Function
    """
    pos_50_algo_1_list = algo1(50)
    pos_50_algo_2_list = algo2(50)

    neg_50_algo_1_list = algo1(-50)
    neg_50_algo_2_list = algo2(-50)

    x = plt.figure(1)
    plt.plot([abs(x - M.exp(50)) for x in pos_50_algo_1_list],'r--',label="Algo I",linewidth=2.5)
    plt.plot([abs(x - M.exp(50)) for x in pos_50_algo_2_list],'b--',label="Algo II",linewidth=2.5)
    plt.legend(loc='best')
    plt.title('Error in value at iteration For +50')
    plt.yscale('log')
    x.show()

    y = plt.figure(2)
    plt.plot([abs(x - M.exp(-50)) for x in neg_50_algo_1_list],'r--',label="Algo I",linewidth=2.5)
    plt.plot([abs(x - M.exp(-50)) for x in neg_50_algo_2_list],'b--',label="Algo II",linewidth=2.5)
    plt.legend(loc='best')
    plt.title('Error in value at iteration For -50')
    plt.yscale('log')
    y.show()

    raw_input()


main()   