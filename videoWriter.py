# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 22:27:36 2020

@author: Sander
"""

import cv2
import numpy as np
import glob
import os
 
img_array = []
for i in range(1201):#for filename in sorted(os.listdir("C:/Users/Sander/mandlebrots_2/")):
    img = cv2.imread("./mandlebrots_3/"+ str(i) + ".png")
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
    if i == 1200:
        for _ in range(60):
            img_array.append(img)
        
 
 
out = cv2.VideoWriter('project2.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 60, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()