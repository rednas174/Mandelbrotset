# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 18:02:48 2020

@author: Sander
"""

import cupy as cp

def sumNum(num):
    if num == 0:
        return 0
    else:
        return num + sumNum(num-1)
    
def sumArr(a):
    new = cp.empty_like(a).flatten()
    dims = a.shape
    for i in range(new.flatten().size):
        new[i] = sumNum(i)
    return new.reshape(dims)

a = cp.arange(500).reshape(1,-1)
b = a.T - 1
c = sumArr(a)-sumArr(b)
print(cp.where(c == 666))

def lvl_27(inp1, inp2):
    pass