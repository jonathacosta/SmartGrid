#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de condomínio
"""

import ModSCC as cond
import ModCombine_csv
import ModEDA

from tqdm import tqdm


class ManageSCC():
    
    def __init__(self,dias=30):
        self.sim(dias=dias)        # Gera arquivos do condomínio
        self.comb()       # Concatena os dados em único arquivo csv
        self.EDA()        # Analise os dados
        pass
    def sim(self,dias=30):   
        for i in tqdm(range(dias)):
            cond.SCC(graf=0,dias=i,casas=100)        
        print('\nSimulação terminada!')
        
    def comb(self):
        try:
            ModCombine_csv.combine_csv()
            print('\nArquivos csv combinados!')
        except:       
            print('\nFalha na execução do módulo ModCombine_csv')
    
    def EDA(self):
        a=ModEDA.EDA()
        a.graf_eda()
   
#******************************************************************************
# AREA DE TESTES
#******************************************************************************
ManageSCC(dias=6*30)
  
    


        
    



