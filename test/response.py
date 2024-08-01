import matplotlib.pyplot as plt
import numpy as np
import camera.photometry as phot
import os
from PIL import Image

dir = '../2023-12-04'

#im = Image.open()

dir_list = os.listdir(dir)

dz = []
iz = []

for folder in dir_list:
    if 'x' not in folder and 'y' not in folder and '931' not in folder:
        dir_img = str(dir) + '\\' + str(folder) + '\\' + str(folder) + '_MMStack_Default.ome.tif'
        img = Image.open(dir_img)
        img = np.array(img)
        max = phot.getPeakIntensity(img)
        #print(max)
        split_folder = folder.split('_')[3]
        dz.append(float(split_folder))
        iz.append(max)

plt.figure('z', dpi=250)
plt.scatter(dz, iz)
plt.xlabel('dz (um)')
plt.ylabel('intensity')
#plt.title('intensity wrt change in z')
plt.axvline(0, color = 'k', linestyle = '--')
plt.grid()

dy = []
iy = []

for folder in dir_list:
    if 'y' in folder:
        dir_img = str(dir) + '\\' + str(folder) + '\\' + str(folder) + '_MMStack_Default.ome.tif'
        img = Image.open(dir_img)
        img = np.array(img)
        max = phot.getPeakIntensity(img)
        #print(max)
        split_folder = folder.split('_')[3]
        dy.append(float(split_folder))
        iy.append(max)

plt.figure('y', dpi=250)
plt.scatter(dy, iy)
plt.xlabel('dy (um)')
plt.ylabel('intensity')
#plt.title('intensity wrt change in y')
plt.axvline(0, color = 'k', linestyle = '--')
plt.grid()

dx = []
ix = []

for folder in dir_list:
    if 'x1' in folder:
        dir_img = str(dir) + '\\' + str(folder) + '\\' + str(folder) + '_MMStack_Default.ome.tif'
        img = Image.open(dir_img)
        img = np.array(img)
        max = phot.getPeakIntensity(img)
        #print(max)
        split_folder = folder.split('_')[2]
        dx.append(float(split_folder))
        ix.append(max)

plt.figure('x', dpi=250)
plt.scatter(dx, ix)
plt.xlabel('dx (um)')
plt.ylabel('intensity')
#plt.title('intensity wrt change in x')
plt.axvline(0, color = 'k', linestyle = '--')
plt.grid()

plt.show()