'''
Necessary functions to perform basic photometry on camera images
'''

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import time

'''
from collections import Counter
def most_common(lst):
    data = Counter(lst)
    return max(lst, key=data.get)
'''

def mostCommon(list) -> float:
    '''
    Returns the most common value from a numpy array. Works with ndarrays
    '''
    #find unique values in array along with their counts
    vals, counts = np.unique(list, return_counts=True)
    #find mode
    mode_value = np.argwhere(counts == np.max(counts))
    return vals[mode_value].flatten().min()

def subtractBackground(image) -> np.ndarray:
    '''
    Basic background subtraction based on the most common pixel value
    '''
    #flat = image.flatten()
    mc = mostCommon(image)

    return image - mc

def getPeakIntensity(image) -> float:
    '''
    Gets highest intensity value in the image
    '''
    max = image.max()
    return max

def getPeakIndex(image) -> np.array:
    '''
    Gets position of highest intensity value in the image. If multiple exist the average is returned
    '''
    max = getPeakIntensity(image)
    index = np.where(image == max)

    # average position if several peak indices
    x = round(np.mean(index[0]))
    y = round(np.mean(index[1]))
    avg_pos = np.array([x, y])
    return avg_pos

def step(image, startIndex, dir, threshold) -> np.array:
    '''
    Stepper function to travel from a starting point in a given direction until a threshold condition is reached
    '''
    dir_len = len(dir)
    if dir_len != 2:
        print(f"Direction list should be length 2, you gave me one of length {dir_len}, what am I supposed to do with this?")
        return
    
    x = startIndex[0]
    y = startIndex[1]

    dx = dir[0]
    dy = dir[1]

    len_x = len(image)
    len_y = len(image[0])

    while image[x][y] > threshold:
        if x <= 0 or x >= len_x or y <= 0 or y >= len_y:
            print('Reached image bounds.')
            break
        x += dx
        y += dy

    return np.array([x, y])

def getBbox(image, center, frac) -> np.ndarray:
    '''
    Gets the bounding box of a spot based on the stepper function
    '''
    max = getPeakIntensity(image)
    threshold = frac * max

    left_bound = step(image, center, [-1, 0], threshold)
    right_bound = step(image, center, [1, 0], threshold)
    top_bound = step(image, center, [0, -1], threshold)
    bottom_bound = step(image, center, [0, 1], threshold)

    topleft_bound = np.array([top_bound[1], left_bound[0]])
    bottomright_bound = np.array([bottom_bound[1], right_bound[0]])

    bbox = np.array([topleft_bound, bottomright_bound])

    return bbox

def getSpotDiameter(bbox) -> float:
    '''
    Get diameter of the spot based on averaging the two axes of the bounding box
    '''
    lr = bbox[1][0] - bbox[0][0]
    tb = bbox[1][1] - bbox[0][1]

    diameter = np.mean([lr, tb])
    return diameter