import camera.PBSI as pbsi
import camera.photometry as phot

import piezo.BPC303 as bpc

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from time import sleep


def dither(piezo, channel, dV, camera, num_iter, exposure_time):  # -> tuple[np.array, np.array]
    V_init = piezo.get_voltage(channel)
    iter = -num_iter
    V_array = []
    I_array = []
    voltage = V_init - dV * num_iter
    while iter <= num_iter:
        piezo.set_voltage(channel, voltage)
        sleep(0.1)
        frame = pbsi.generateFrame(camera, exposure_time)
        # frame = phot.subtractBackground(frame)
        peak = phot.getPeakIntensity(frame)

        V_array.append(voltage)
        voltage += dV
        iter += 1

        I_array.append(peak)

    return V_array, I_array


def Gaussian(x, a, b, c, u) -> float:
    y = a + b * np.exp(- c * (x - u) * (x - u))
    return y


def fitGaussian(V, I):  # -> tuple[np.array, np.ndarray]
    a0 = 100
    b0 = max(I)
    # c0 = 1. # this can be optimised - currently using 1. as a placeholder value
    u0i = I.index(max(I))
    u0 = V[u0i]
    c0_denom = (V[u0i] - u0) ** 2 - (V[u0i - 1] - u0) ** 2
    c0 = np.log(I[u0i] / I[u0i - 1]) / c0_denom
    p0 = [a0, b0, c0, u0]
    popt, pcov = curve_fit(Gaussian, V, I, p0)
    return popt, pcov


def correctChannel(piezo, channel, dV, camera, num_iter, exposure_time) -> None:
    V, I = dither(piezo, channel, dV, camera, num_iter, exposure_time)
    plt.plot(V, I)
    I_max = max(I)
    I_max_index = I.index(I_max)
    uopt = V[I_max_index]
    piezo.set_voltage(channel, uopt)
    print(f'Channel {channel} has been moved to position {uopt}')  # with error {u_sigma}.')
    # plt.plot(V, Gaussian(V, *popt))
    # plt.show()
    return


def threePointDither(piezo, channel, dV, camera,
                     exposure_time) -> None:  # this can definitely be improved using matrices lol, will do that tomorrow
    V_init = piezo.get_voltage()
    delta = dV

    x1 = V_init
    x0 = x1 - delta
    x2 = x1 + delta

    frame = pbsi.generateFrame(camera, exposure_time)
    y1 = phot.getPeakIntensity(frame)

    piezo.set_voltage(channel, x0)
    frame = pbsi.generateFrame(camera, exposure_time)
    y0 = phot.getPeakIntensity(frame)

    piezo.set_voltage(channel, x2)
    frame = pbsi.generateFrame(camera, exposure_time)
    y2 = phot.getPeakIntensity(frame)

    a0 = y0 / (x0 - x1) / (x0 - x2)
    a1 = y1 / (x1 - x0) / (x1 - x2)
    a2 = y2 / (x2 - x0) / (x2 - x1)

    if (a0 + a1 + a2) > 0:
        return

    x_max = 1.5 * x1 - ((a0 * x0 + a1 * x1 + a2 * x2) / (a0 + a1 + a2) / 2)
    piezo.set_voltage(x_max)

    return
