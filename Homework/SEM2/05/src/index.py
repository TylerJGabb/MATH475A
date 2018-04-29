import math
import numpy as np
import time
import matplotlib.pyplot as plt


class URandoGenerator:
    def __init__(self, alpha, beta, m):
        self.a = alpha
        self.b = beta
        self.m = m
        self.x0 = None
        self.x = self.x0

    def seed(self, seed):
        self.x = seed

    def next(self):
        self.x = (self.a * self.x + self.b) % self.m
        return (2 * self.x / self.m) - 1

    def reset(self):
        self.x = self.x0

    def generate(self, count):
        return [self.next() for i in range(count)]


def do_histo_plot(seq, title=""):
    title = "histo_" + title
    nums = seq
    hist, bins = np.histogram(nums, bins=100)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.title(title)
    plt.savefig(title)
    plt.show()


def get_auto_correlation(seq, m, distance=500, title=""):
    title = "correlation_" + title
    # k_vals = range(distance)
    # func = [sum([seq[n] * seq[(n + k) % m] for n in range(m)]) / m for k in k_vals]
    # plt.plot(k_vals, func)
    dft = np.fft.fft(seq)
    idft = np.fft.ifft([(abs(q) ** 2) / m for q in dft]).real
    x = np.arange(0, 2 ** 16)
    plt.plot(x, idft, linestyle='', marker='o', markersize=3)
    plt.title(title)
    plt.savefig(title)
    plt.show()


def gaussian(pts):
    m = 2 ** 16
    X = URandoGenerator(4 * 17 + 1, 31, m)
    Y = URandoGenerator(4 * 19 + 1, 67, m)
    X.seed(503)
    Y.seed(244)
    x_vals = X.generate(pts)
    y_vals = Y.generate(pts)
    points = \
        [
            (x_vals[i], y_vals[i]) for i in range(pts)
            if x_vals[i] ** 2 + y_vals[i] ** 2 <= 1
        ]
    r_vals = \
        [math.sqrt((points[i][0] ** 2 + points[i][1] ** 2)) for i in range(len(points))]

    theta_vals = \
        [math.acos(points[i][0] / r_vals[i]) for i in range(len(points))]

    N1 = \
        [2 * math.sqrt(-math.log(r_vals[i])) * math.cos(theta_vals[i]) for i in range(len(points))]

    N2 = \
        [2 * math.sqrt(-math.log(r_vals[i])) * math.cos(theta_vals[i]) for i in range(len(points))]

    N = [*N1, *N2]

    hist, bins = np.histogram(N, bins=100)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width, color='blue', label='results')

    plt.xlim([-5, 5])
    # plt.scatter([p[0] for p in points], [p[1] for p in points])
    vals = np.arange(-5, 5, 0.01)
    f = lambda x: np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi)
    plt.plot(vals, (max(hist)/0.40)*f(vals), 'k-', linewidth=2, label='normal density func')
    plt.legend()
    title = "Gaussian Distribution Histogram"
    plt.title(title)
    plt.savefig(title)
    plt.show()


def main():
    # m = 2 ** 16  # the only prime factor of this is 2
    # a = 16 + 1  # 16 % 4 == 0 and 16 % 2 == 0. Add one to 16 to obtain an appropriate alpha
    # b = 19  # 19 shares no prime factors with M
    # rng = URandoGenerator(a, b, m)  # make the rando generator
    # rng.seed(42)  # the answer to everything
    # seq = rng.generate(rng.m)
    # do_histo_plot(seq)
    # get_auto_correlation(seq, m=m, distance=100)
    gaussian(20000)


main()
