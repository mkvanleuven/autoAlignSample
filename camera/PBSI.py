'''
Teledyne Prime BSI Express camera controls
'''

from pyvcam import pvc
from pyvcam.camera import Camera
import numpy as np
import matplotlib.pyplot as plt


def createCam() -> Camera:
    '''
    Initialise and create camera object
    '''
    pvc.init_pvcam()
    camera = next(Camera.detect_camera())
    return camera


def openCam(camera) -> None:
    '''
    Open camera
    '''
    camera.open()
    return


def closeCam(camera) -> None:
    '''
    Close camera
    '''
    camera.close()
    return


def generateFrame(camera, exposure_time: int) -> np.ndarray:
    '''
    Get frame from camera with given exposure time. Returns numpy 2d array
    '''
    frame = camera.get_frame(exp_time=exposure_time)
    return frame


def getGain(camera) -> None:
    '''
    Get camera gain index
    '''
    return camera.gain


def setGain(camera, gain_index: int) -> None:
    '''
    Set camera gain index
    '''
    camera.gain = gain_index
    return