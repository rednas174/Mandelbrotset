# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:18:05 2020

@author: Sander
"""

import matplotlib.pyplot as plt
import time

r = 2.3

x = []
    
for r in range(200,400):
    y = []
    value = 0.4
    for _ in range(25):
        y.append(value)
        value = (r/100) * value * (1 - value)
    x.append(y)
    
for y in range(len(x)):
    plt.figure()
    plt.xlim(0,25)
    plt.ylim(0,1)
    plt.plot(x[y])
    plt.title("r = " + str(round(2+y/100, 2)))
    plt.pause(0.001)
    plt.close()