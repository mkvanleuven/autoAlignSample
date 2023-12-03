from pyvcam import pvc 
from pyvcam.camera import Camera
import matplotlib.pyplot as plt

def createCam():
    pvc.init_pvcam()
    camera = next(Camera.detect_camera())
    return camera

def openCam(camera):
    camera.open()
    return

def generateFrame(camera, exposure_time):
    frame = camera.get_frame(exp_time = exposure_time)
    return frame

def showFrame(frame):
    plt.imshow(frame)