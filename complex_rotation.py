# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 11:32:39 2020

@author: Sander
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pyquaternion import Quaternion

for _ in range(100):
    plt.close()

coordinates = np.array([0,0,1])
circle = np.e ** (1j * np.linspace(0,2 * np.pi, 360))



def makeNewPlot(plotCircles = False):
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111, projection='3d')
    
    if plotCircles:
        ax.plot(np.zeros_like(circle.real), circle.real, circle.imag)
        ax.plot(circle.real, np.zeros_like(circle.real), circle.imag)
        ax.plot(circle.real, circle.imag, np.zeros_like(circle.real))
        
        plt.legend(["x", "y", "z"])
#ax.scatter(coordinates[0],coordinates[1],coordinates[2],c="b",marker="o")

    ax.set_xlim([-1,1])
    ax.set_ylim([-1,1])
    ax.set_zlim([-1,1])
    return (ax, fig)

def rotateObject(ob, axes, angle):
    # axes = [axes[0]*-1, axes[1]*-1, axes[2]]
    quaternion = Quaternion(axis=axes, angle=angle) # Rotate 120 about x=y=z
    rotated_object = np.empty_like(ob)
    for index in range(ob.shape[0]):
        rotated_object[index] = quaternion.rotate(ob[index])
    return rotated_object

ob = (np.array([[0,0,0],
               [0,0,1],
               [0,1,0],
               [0,1,1],
               [1,0,0],
               [1,0,1],
               [1,1,0],
               [1,1,1]]) - 0.5) * 2 / np.sqrt(3)

amp = 1

def plotObject(ob, ax, color = "r"):
    for coord in ob:
        ax.scatter(coord[0],coord[1],coord[2], c=color, marker=".")

ax, _ = makeNewPlot(plotCircles = True)
plotObject(ob, ax)

def plotBetween(ob, fig, axes, stepsize = 64, amount = 8, plotRotationAxes = False):
    if plotRotationAxes:
        fig.plot(np.linspace(-axes[0],axes[0]),np.linspace(-axes[1],axes[1]),np.linspace(-axes[2],axes[2]))
    for i in range(0,amount+1):
        ob_rotated = rotateObject(ob, axes, 2 * (np.pi/stepsize) * i)
        plotObject(ob_rotated, fig, color="y")
    plotObject(ob, fig, color="r")
    return ob_rotated


# plotBetween(ob, makeNewPlot(True), [1,0,0], 64, 8, plotRotationAxes = True)

# plotBetween(ob, makeNewPlot(True), [0,1,0], 64, 8, plotRotationAxes = True)

# plotBetween(ob, makeNewPlot(True), [0,0,1], 64, 8, plotRotationAxes = True)

print("yeet")
# a = 8
# ax = makeNewPlot(True)
# ob_rotated = rotateObject(ob, [1,0,0], 2 * np.pi/a)
# ob_rotated = rotateObject(ob_rotated, [0,1,0], 2 * np.pi/a)
# ob_rotated = rotateObject(ob_rotated, [0,0,1], 2 * np.pi/a)
# plotObject(ob_rotated, ax, color="r")




ax, fig = makeNewPlot(True)
new_ob = plotBetween(ob, ax, [-1,0,0], plotRotationAxes = True)
plotObject(new_ob, makeNewPlot(True)[0])
print("yoink")
fig.savefig("name.png", dpi=600)


