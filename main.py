import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from time import sleep
import os

import camera.PBSI as pbsi
import camera.photometry as phot

import piezo.BPC303 as bpc
import piezo.dither as dither

'''
SET VALUES
'''
SN = '71281854'
exposure_ms = 30
dx = .2
dV = dx * 5  # 100 * dx / 20
num_iter = 3 # 2 * num_iter + 1
sleep = 10
frac = .8


def main():
    os.system('start /max cmd')
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
    num_channels = piezo.getNumChannels()
    channels = range(1, num_channels + 1)

    for i in channels:
        dither.correctChannel(piezo, i, dV, num_iter, exposure_ms)

    set_frame = pbsi.generateFrame(camera, exposure_ms)
    set_point = phot.getPeakIntensity(set_frame)
    background = phot.mostCommon(set_frame)

    '''
    DITHER LOOP
    '''

    while True:
        sleep(sleep)
        curr_frame = pbsi.generateFrame(camera, exposure_ms)
        curr_point = phot.getPeakIntensity(curr_frame)
        if curr_point < frac * set_point:
            for i in channels:
                dither.correctChannel(piezo, i, dV, num_iter, exposure_ms)
    
    pbsi.closeCam(camera)

if __name__ == '__main__':
    main()