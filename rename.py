# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 22:36:59 2020

@author: Sander
"""

import os

path = "C:/Users/Sander/mandlebrots_2/"
for filename in os.listdir(path):
    os.rename(path + filename, path + str(round(float(filename.replace(".png","")) * 2)) + ".png")
