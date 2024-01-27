from camera import PBSI as pbsi
from camera import photometry as phot

from piezo import BPC303 as bpc
from piezo import dither as dither

import os

# os.system('start /max cmd')
camera = pbsi.createCam()
pbsi.openCam(camera)
# pbsi.setSensitivity(camera)
pbsi.setHDR(camera)
frame = pbsi.generateFrame(camera, exposure_time=250)

import matplotlib.pyplot as plt

plt.figure()
plt.imshow(frame)
plt.show()

pbsi.closeCam(camera)

print('camera closed')
