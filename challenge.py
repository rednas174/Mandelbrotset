# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 22:13:21 2020

@author: Sander
"""

import numpy as np

starting_list = list((np.random.random(500)*100).astype(np.uint64))
asdf = 0
def sort_thingy(arr, decimal):
    global asdf
    temp = [[],[],[],[],[],[],[],[],[],[]]
    for item in arr:
        asdf += 1
        i = str(int(((item)/(10**(decimal)))%10))
        temp[int(i)].append(item)
    return temp

def recursive_sort(array, bit = 19):
    if bit == -1 or type(array) != list:
        return array
    array = sort_thingy(array, bit)
    while [] in array:
        array.remove([])
    
    for i in range(len(array)):
        if len(array[i]) == 1:
            array[i] = array[i][0]
    for i in range(len(array)-1,-1,-1):
        if type(array[i]) == list:
            array = array[:i] + recursive_sort(array[i], bit-1) + array[i+1:]

    if type(array) != list:
        array = [array]
    return array



temp = recursive_sort(starting_list, 1)
print("output:\n",temp)
print(temp == sorted(starting_list))
print(asdf)
