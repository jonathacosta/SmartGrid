#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 18:15:08 2022

@author: j
"""
import numpy as np
class Population:
    '''
    Classe instancia objeto para de interesse à solução do SHC.    
    '''   
    def __init__(self):
        self.startTime = np.array([])
        self.opPower = np.array([])
        self.v1 = np.array([])
        self.v2 = np.array([])
        self.v3 = np.array([])
