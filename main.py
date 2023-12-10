import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from time import sleep

import camera.PBSI as pbsi
import camera.photometry as phot

import piezo.BPC303 as bpc

'''
SET VALUES
'''
SN = '71281854'

def main():
    '''
    INITIALISE CAMERA
    '''
    camera = pbsi.createCam()
    pbsi.openCam(camera)

    '''
    INITIALISE PIEZO
    '''
    piezo = bpc.BPC303(SN)
    num_channels = piezo.getNumChannels()
    channels = range(1, num_channels + 1)

    '''
    
    '''

    while True:
        pass

    return

if __name__ == '__main__':
    main()