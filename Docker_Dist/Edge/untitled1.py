# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 18:11:53 2023

@author: amarmorato
"""
import os.path as osp
import numpy as np

data = np.loadtxt("/home/andrea/Scrivania/Tesi/Docker_Dist/Edge/data.csv",delimiter=",", dtype=float)

np.random.shuffle(data)

numDevice = 3

numEl = data.shape[0]//numDevice

for i in range(numDevice):
    if i==numDevice-1:
        d = data[i*numEl:data.shape[0]]
    else:
        d = data[i*numEl:numEl + i*numEl]
    np.savetxt("data"+str(i)+".csv",d,delimiter=",")
