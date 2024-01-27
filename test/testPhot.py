import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
import camera.photometry as phot

image = np.loadtxt('../testData/d7um.csv', delimiter =',')

time1 = time.time()
image = phot.subtractBackground(image)
center = phot.getPeakIndex(image)
bbox = phot.getBbox(image, center, 0.1)
diameter = phot.getSpotDiameter(bbox)
peak = phot.getPeakIntensity(bbox)
print(peak)
print(diameter)
time2 = time.time()
print(time2 - time1)

fig, ax = plt.subplots()
ax.imshow(image)

ax.plot(center[1], center[0], 'rx', ms = 2)

bbox_rect = patches.Rectangle(bbox[0], diameter, diameter, alpha = 0.2, color = 'red')
ax.add_patch(bbox_rect)


plt.show()
