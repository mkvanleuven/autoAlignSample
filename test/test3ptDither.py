import random
import numpy as np
import matplotlib.pyplot as plt
import time

from piezo.dither import threePointDither, tpdMat


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
    linspace = np.linspace(0, 75, 1000)
    time_alg = []
    time_mat = []

    while i < 1000:
        i += 1
        points = create3Points()
        start = time.perf_counter_ns()
        #  print(points)

        popt_alg = alg(points)
        t_a = time.perf_counter_ns()

        popt_mat = mat(points)
        t_m = time.perf_counter_ns()

        time_alg.append(t_a - start)
        time_mat.append(t_m - t_a)
        # plt.figure()
        # for point in points:
        #     plt.plot(point[0], point[1], 'rx')
        # plt.plot(linspace, quadratic(linspace, *popt))
        # plt.show()

    plt.figure()
    #  plt.plot(time_alg, time_mat, 'rx')
    plt.scatter(time_alg, time_mat, 'rx')
    plt.xlabel('Algebraic Solution')
    plt.ylabel('Matrix Solution')
    plt.axline((0, 0), slope=1, linestyle='dotted')
    plt.show()
    return None


if __name__ == '__main__':
    main()
