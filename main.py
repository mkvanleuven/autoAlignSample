import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from time import sleep
import os
import sys

import camera.PBSI as pbsi
import camera.photometry as phot

import piezo.BPC303 as bpc
import piezo.dither as dither

'''
SET VALUES
'''
SN = '71281854'
exposure_ms = 250
num_iter = 30  # 2 * num_iter + 1
sleep_length = 10
frac = .95

## x
dx = .01
dVx = dx * 5  # 100 * dx / 20
chx = 3
x = [chx, dVx]

## y
dy = .01
dVy = dy * 5
chy = 2
y = [chy, dy, dVy]

## z
dz = 0.01
dVz = dz * 5
chz = 1
z = [chz, dVz]

channels = {'x': x, 'y': y, 'z': z}


def main():
    #os.system('start /max cmd')
    '''
    INITIALISE CAMERA
    '''
    camera = pbsi.createCam()
    pbsi.openCam(camera)
    pbsi.setSensitivity(camera)

    '''
    INITIALISE PIEZO
    '''
    piezo = bpc.BPC303(SN)
    num_channels = piezo._numChannels

    dither.correctChannel(piezo, *channels['z'], camera, num_iter, exposure_ms)
    dither.correctChannel(piezo, *channels['y'], camera, num_iter, exposure_ms)
    dither.correctChannel(piezo, *channels['x'], camera, num_iter, exposure_ms)
    dither.correctChannel(piezo, *channels['z'], camera, num_iter, exposure_ms)

    set_frame = pbsi.generateFrame(camera, exposure_ms)
    set_point = phot.getPeakIntensity(set_frame)

    '''
    DITHER LOOP
    '''

    while True:
        #  sleep(sleep_length)
        curr_frame = pbsi.generateFrame(camera, exposure_ms)
        curr_point = phot.getPeakIntensity(curr_frame)
        if curr_point < frac * set_point:
            print(f'Signal intensity is currently {curr_point}, below the {100 * frac} threshold from {set_point}.')
            # dither.correctChannel(piezo, *channels['z'], camera, num_iter, exposure_ms)
            # dither.correctChannel(piezo, *channels['y'], camera, num_iter, exposure_ms)
            # dither.correctChannel(piezo, *channels['x'], camera, num_iter, exposure_ms)
            # dither.correctChannel(piezo, *channels['z'], camera, num_iter, exposure_ms)

            dither.threePointDither(piezo, *channels['z'], camera, exposure_ms)
            dither.threePointDither(piezo, *channels['y'], camera, exposure_ms)
            dither.threePointDither(piezo, *channels['x'], camera, exposure_ms)
            dither.threePointDither(piezo, *channels['z'], camera, exposure_ms)

        elif curr_point > set_point:
            set_point = curr_point
            print(f'Signal intensity is currently {curr_point}, above the {100 * frac} threshold from {set_point}.')


if __name__ == '__main__':
    main()
