#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Módulo de soluções por iteração

Classe instancia objeto e guardar atributos de uma solução do SHC    
'''

import numpy as np

    
class DataPso:
    def __init__(self):
        pass


class Population(DataPso):
    '''
    Classe instancia objeto e guardar atributos de uma solução do SHC    
    '''   
    def __init__(self):
        DataPso.__init__(self)
        self.startTime = np.array([])
        self.opPower = np.array([])
        self.v1 = np.array([])
        self.v2 = np.array([])
        self.v3 = np.array([])

