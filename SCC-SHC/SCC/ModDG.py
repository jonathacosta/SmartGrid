#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Geração Distribuída do condomínio
"""

import ModEDA
# import pandas as pd
import numpy as np


class DG:
    '''
    Classe contém métodos de cálculo de capacidade instalada do GD,
    quantidade de paineis, capacidade de geração de potência e rateio
    '''
    
    def __init__(self,ghi=2189,pot_mod=440,rend=0.8, detalhar=False):
        '''
        Método carrega varíaveis globais de irradiação, potência do modulo 
        fotovoltaico e rendimento. Como também, inicia os métodos de:
            * consumo-cond
            * dg
        '''
        self.ghi = ghi          # kWh/m² ao ano
        self.pot_mod = pot_mod  # Whp
        self.rend = rend        # 80%    
        if detalhar == True:
            self.consumo_cond(1)        
            self.dg_resumo(1)        

    def consumo_cond(self,detalhado=0):
        '''
        Método importa dados consolidados de consumo do condomínio de 
        100 casas e apresenta as médias de consumo e quartis.
        '''
        a=ModEDA.EDA()
        
        self.consumo_med = a.df_mes.consumo
        
        if detalhado == True:
            print('-'*50)
            print('\n1.Consumo acumulado de 30 dias em MWh:\n')      # Somatório dos valores diários de kWh
            print('-'*50)
            print('\n',self.consumo_med/1000)
            print('\n','-'*50,'\n\tDescritivo - quartis (kMWh):\n','-'*50)
            print(self.consumo_med.describe()/1000)
            print('-'*50)
    
  
    def dg_resumo(self,detalhado=False):            
        '''
        Método apresenta o resultado do cálculo da quantidade necessárioa de paineis 
        para gerar energia sob a condição mais crítica do condomínio.
        Todas as casas operando em consumo máximo mensal.
        '''
        x =  ModEDA.EDA().df.consumo.max() # Residencia com maior consumo diário
        consumo_cond_max = x*30*100        # 30 dias e 100 casas
        
        cap_ger_mod = np.round(self.pot_mod * self.ghi * self.rend /12000,2)        
        n_paineis = np.ceil(consumo_cond_max/cap_ger_mod)
        self.dg_total = np.round(n_paineis * self.pot_mod * self.ghi * self.rend/12000,2)        
        
        if detalhado == True:
            print('\n RESUMO')
            print('*'*10)
            print('',
            f"{np.round(consumo_cond_max/1000,2)} MWh : demanda energética mensal do condomínio. Condição de máximo consumo de cada casa!\n",
            f"{n_paineis} : quantidade necessária de paineis para atender esta demanda\n",
            f"{np.round(self.dg_total/1000,2)} MWh : capacidade de geração de energia com radiação diária de {np.round((self.ghi/365),3)} kWh/m²"
            )                     
            print('*'*10)      
            
    def dg_rat(self):            
          
          a=ModEDA.EDA()
          a.consumo_mensal_condominio()
          

class Forecast_DG:
    
    def Previsao_DG(self,detalhado=False):
        '''
        Previsão de GD mensal 
        '''
        a=DG(ghi=2189,pot_mod=440,rend=0.8, detalhar=detalhado)
        a.dg_resumo(1)   
#%%
#******************************************************************************
# AREA DE TESTES
#******************************************************************************

# a=DG()
# a.consumo_cond(1)
# a.dg_resumo(1)

# a.Previsao_DG(True)
