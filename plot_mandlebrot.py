# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:50:01 2020

@author: Sander
"""
import numpy as np
import matplotlib.pyplot as plt

def function(num, complex_number):
    return num ** 2 + complex_number

def iterate(num, iterations):
    value = num
    for i in range(iterations):
        value = function(value, num)
        if np.abs(value) >= 2:
            return False
    return True

resolution = 50
bin_map = np.empty((resolution, resolution), dtype = np.uint8)
map_range = (-2,2,-2,2)
zoom = 0.5
offset_x = -1
offset_y = 0
m = np.meshgrid(np.linspace(map_range[0] * zoom + offset_x, \
                            map_range[1] * zoom + offset_x, bin_map.shape[0]), \
                np.linspace(map_range[2] * zoom - offset_y,\
                            map_range[3] * zoom - offset_y, bin_map.shape[0]))
m = m[0].astype(np.complex64) + 1j * m[1].astype(np.complex64)
print(m.shape)

for y in range(bin_map.shape[0]):
    print("Loading[")
    for x in range(bin_map.shape[1]):
        bin_map[y, x] = iterate(m[y,x], 25)
        
plt.imshow(bin_map*255, cmap = "gray")

    