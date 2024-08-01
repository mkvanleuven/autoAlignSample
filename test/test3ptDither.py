import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kde
import time
import seaborn as sns

def quadratic(x, a, b, c):
    y = a * x * x + b * x + c
    return y


def create3Points():
    points = np.random.uniform(low=0.0, high=75.0, size=(3, 2))
    return points


def alg(points):
    p0 = points[0]
    p1 = points[1]
    p2 = points[2]

    x0, y0 = p0[0], p0[1]
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    a0 = y0 / (x0 - x1) / (x0 - x2)
    a1 = y1 / (x1 - x0) / (x1 - x2)
    a2 = y2 / (x2 - x0) / (x2 - x1)

    #  x_max = 1.5 * x1 - (a0 * x0 + a1 * x1 + a2 * x2) / (a0 + a1 + a2) / 2

    a = a0 + a1 + a2
    b = - a0 * (x1 + x2) - a1 * (x0 + x2) - a2 * (x0 + x1)
    c = a0 * x1 * x2 + a1 * x0 * x2 + a2 * x0 * x1

    popt = [a, b, c]

    return popt


def mat(points):
    p0 = points[0]
    p1 = points[1]
    p2 = points[2]

    x0, y0 = p0[0], p0[1]
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    M = [
        [x0 * x0, x0, 1],
        [x1 * x1, x1, 1],
        [x2 * x2, x2, 1]
    ]

    M_inv = np.linalg.inv(M)

    y = [y0, y1, y2]
    popt = M_inv @ y
    return popt


def main() -> None:
    i = 0
    time_alg = []
    time_mat = []
    lin = np.linspace(0, 75, 1000)

    while i < 1_000:
        i += 1
        points = create3Points()
        start = time.perf_counter()
        #  print(points)

        popt_alg = alg(points)
        t_a = time.perf_counter()

        popt_mat = mat(points)
        t_m = time.perf_counter()

        time_alg.append(t_a - start)
        time_mat.append(t_m - t_a)

        # plt.figure(dpi=200)
        # plt.plot(lin, quadratic(lin, *popt_alg), color='#3e3ab3')
        # for point in points:
        #     plt.plot(point[0], point[1], 'r.', markersize=15)
        #
        # plt.grid()
        # plt.show()

    plt.figure(dpi=200)
    plt.plot(time_alg, time_mat, 'rx')
    # plt.scatter(time_alg, time_mat, c=density)
    # sns.kdeplot(time_alg, time_mat, cmap='Reds', shade=True)
    plt.xlabel('Algebraic Solution')
    plt.ylabel('Matrix Solution')
    plt.axline((0, 0), slope=1, linestyle='dotted', label='Line of equal time')
    plt.legend()

    plt.figure(dpi=200)
    plt.hist(time_alg, bins=100)
    plt.title('Algebraic Solution')

    plt.figure()
    plt.hist(time_mat, bins=100)
    plt.title('Matrix Solution')
    print(np.mean(time_alg))
    print(np.std(time_alg))

    plt.show()
    return None


if __name__ == '__main__':
    main()
