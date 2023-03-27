#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Geração Distribuída do condomínio
"""

import ModEDA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DG:
    '''
    Classe contém métodos de cálculo de capacidade instalada do GD,
    quantidade de paineis, capacidade de geração de potência e rateio
    '''
    
    def __init__(self,ghi=2206.4,mes=6,pot_mod=440,rend=0.8, detalhar=False):
        '''
        Método carrega varíaveis globais de irradiação, potência do modulo 
        fotovoltaico e rendimento. Como também, inicia os métodos de:
            * consumo-cond
            * dg
        '''
        # jan ... dez http://labren.ccst.inpe.br/atlas2_tables/CE_glo.html
                
        self.mes=mes
        self.ghi = np.array([5718, 5808, 5606, 4903, 5211, 5237, 5441, 5947, 6179, 6368, 6373, 5974])  # kWh/m² ao ano                
        self.rend = rend             # 80%    
        self.pot_mod = pot_mod       # Whp
        self.n_paineis = 0
        self.dg_mes = []
        
        # self.dg_proj_total(False)
        # self.dg_forest(False)
        # self.dg_rat()
        
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
    
  
    def dg_proj_total(self,detalhado=False):            
        '''
        Método apresenta o resultado do cálculo da quantidade necessária de paineis 
        para gerar energia sob a condição mais crítica do condomínio.
        Todas as casas operando em consumo máximo mensal.
        '''
        casas, dias = 100,30
        x =  ModEDA.EDA().df.consumo.mean() # Residencia com medio  ou maximo consumo diário
        consumo_dia_max = x
        dem_min = 30 # kWh.mes
        consumo_SHC_max = (consumo_dia_max*dias - dem_min)/dias
        '''
        consumo_SHC_max * 30 dias - 30 kWh de consumo minino)/30 dias
        '''
        ghi_proj = self.ghi.mean()/1000    # Para projeto usar média GHI diaria em kWh.dia/m²        
        p_ger = np.round(consumo_SHC_max / (ghi_proj * self.rend),2)   
        
        n_paineis = p_ger*1000 / self.pot_mod
        self.n_paineis = np.ceil(casas*n_paineis)
        
        
        if detalhado == True:
            print('*'*50)
            print('RESUMO por residência - SHC INVIDIDUAL')
            print('*'*50)
            print('',
            'Diária:\n',      
            f"{np.round(consumo_dia_max,2)} kWh - demanda energética individual de um SHC. Condição de médio (máximo) consumo!\n",              
            f'{dem_min/dias} kWh - demanda mínima de energia diária à concessionária\n',
            f'{np.round(consumo_SHC_max,2)} kWh- energia diária compensada via GD por créditos\n',            
            f'{np.round(self.pot_mod * n_paineis * ghi_proj/1000 *self.rend,2)} kWh - energia gerada pelos paineis'
            '\n\nMensal:\n',             
            f"{np.round(consumo_dia_max*dias,2)} kWh - demanda energética individual de um SHC. Condição de médio (máximo)  consumo!\n",              
            f'{dem_min} kWh - demanda mínima de energia mensal à concessionária\n',
            f'{np.round(consumo_SHC_max*dias,2)} kWh- energia mensal compensada via GD por créditos\n',        
            f'{np.round(self.pot_mod * n_paineis * ghi_proj/1000 *self.rend*dias,2)} MWh - energia gerada pelos paineis'
            '\n\nTotal de paineis:\n',
            f"{np.ceil(n_paineis)} - quantidade necessária de paineis para atender a demanda de uma única casa.\n",
            )
            
            print('*'*50)
            # 'Extrapolação condominal para 100 casas:\n'
            print('RESUMO - SCC com 100 casas - CONDOMÍNIO')                     
            print('*'*50)
            casas,dias = 100,30
            print('Extrapolação condominal para 100 casas:\n\n',
            'Diária:\n',      
            f"{np.round(casas*consumo_dia_max,2)} kWh - demanda energética diária do SCC. Condição de médio (máximo)  consumo!\n",              
            f'{casas*dem_min/dias} kWh - demanda mínima de energia diária à concessionária\n',
            f'{np.round(consumo_SHC_max,2)*casas} kWh- energia diária compensada via GD por créditos\n',
            '\nMensal:\n',             
            f"{np.round(consumo_dia_max*dias*casas,2)/1000} MWh - demanda energética individual de um SHC. Condição de médio (máximo)  consumo!\n",              
            f'{dem_min*casas/1000} MWh - demanda mínima de energia mensal à concessionária\n',
            f'{np.round(consumo_SHC_max*dias*casas,2)/1000} MWh- energia mensal compensada via GD por créditos\n',
            f'{np.round( (self.pot_mod * self.n_paineis * ghi_proj/1000 *self.rend*dias)/1000,2)} MWh - energia gerada pelos paineis'
            '\n\nTotal de paineis:\n',
            f"{self.n_paineis} - quantidade necessária de paineis para atender a demanda de {casas} casas.\n",
            )
            
    def dg_forest(self,detalhes=0):
        'self.n_paineis já considera 100 casas'
        dias=30
        
        for i in self.ghi:
            self.dg_mes.append(np.round((dias)* (self.pot_mod * self.n_paineis * i/1000 * self.rend)/1e3,2))
        self.dg_mes
        
        if detalhes==1:
            
            print('\nLista com projeção de GD ao longo do ano para o condomínio.\n',
                  'Lista considera diferentes valores de GHI, 100 casas , 30 dias.\n'
                  'Valores de GHI:\n',self.ghi,'\n',
                  'Total de paineis:',np.ceil(self.n_paineis),'.')
            print(f'Previsão de DG kWh.mes:\n {self.dg_mes}')
                       
              
    def dg_rat(self):            
          
          cond_cred = self.dg_mes[self.mes]  
          base=ModEDA.EDA().df          
          df=pd.DataFrame()          
          
          df=df.assign(mes = pd.DatetimeIndex(pd.to_datetime(base['data'],format="%Y-%m-%d")).month,
                       casa = base.casa,
                       consumo = base.consumo
                       )
          
          # Filtro mensal para rateio de DG
          flt=(df.mes==self.mes)          
          df = df[flt].groupby(by='casa').sum()    
          df = df.assign(pond=df.consumo.apply(lambda x: 
                                               1 if x < 50 else
                                               2 if x < 150 else
                                               5 if x < 300 else 
                                               6 if x < 350 else 
                                               7 if x < 400 else 
                                               8))                                   
          df['rat'] = cond_cred * df.pond/df.pond.sum()
          # df.consumo.plot(label='consumo')
          
          plt.plot(df.consumo,label='consumo')
          plt.plot(df.rat,label='creditos')
          plt.legend()
          
          print('Soma dos consumos no mês',df.consumo.sum())                     
          print('Soma dos créditos no mês',np.round(df.rat.sum(),2))
          print(df)
          # flt = (df.pond==2)
          # print(df[flt])              
#%%
#******************************************************************************
# AREA DE TESTES
#******************************************************************************
a=DG(mes=7,pot_mod=440)
a.dg_proj_total(0)
# print(a.n_paineis)
a.dg_forest(0)
a.dg_rat()

