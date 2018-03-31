import numpy as np

sin = np.sin
cos = np.cos
pi = np.pi

c0 = lambda x: x * sin(pi * x)


# For which value of delta does it look like BE converges


def generate_euler_D(N, Delta):
    D = []
    sub = [1, -2, 1]
    for i in range(N):
        if i == 0:
            row = [-2, 1, *([0] * (N - 3)), 1]
        elif i == N - 1:
            row = [1, *([0] * (N - 3)), 1, -2]
        else:
            row = [*([0] * (i - 1)), *sub, *([0] * (N - 3 - (i - 1)))]
        print(row)

