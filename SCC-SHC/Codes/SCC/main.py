#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de condomínio
"""

import ModSCC as cond
import ModCombine_csv
import ModEDA,ModDG

from tqdm import tqdm


class ManageSCC():
    
    def __init__(self,dias=365,casas=100,graf_agend=0,lang=0,atualizar=False):
        self.dias = dias
        self.casas = casas
        self.graf_agend = graf_agend
        self.lang = lang
        
        if atualizar == True:              # Gerar e combinar novas arquivos no SHC
            self.sim()                 # Gera arquivos do condomínio
            self.comb()                # Concatena os dados em único arquivo csv        
            self.EDA()                 # Analise os dados
            self.DG()
    
    def sim(self):   
        for i in tqdm(range(self.dias)):
            cond.SCC(graf=self.graf_agend,lang=self.lang,dias=i,casas=self.casas)        
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
       
    def DG(self):
        ModDG.Forecast_DG().Previsao_DG(1)
           
#******************************************************************************
# AREA DE TESTES
#******************************************************************************
#  Extração de gráficos específicos
a=ManageSCC(atualizar=1)
# a.sim()
# a.comb()

# a.sim()
# a=ManageSCC()
# a.comb()
# a.EDA() 
# # a.DG()

# Simulação geral
# ManageSCC(atualizar=1)
    
    




    