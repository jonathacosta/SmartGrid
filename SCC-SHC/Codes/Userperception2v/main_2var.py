#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comfort functions comparative module
"""
import numpy as np
import ModConfSHC
from tqdm import tqdm
np.random.seed(42)

class SHC_ComfortFunctions():
    '''
    - Class performs the PSO in a residence with a comparison between
       different comfort functions.
    '''
    
    def __init__(self,default=1,graf=0,lang=0,dias=0,
                 tar=None,alfa=None,carga=None,
                 Conf_Functions:list=[1,2],
                 user_variable:tuple=(20,65)
                 ):
        self.graf = graf        
        self.comfort_function=Conf_Functions
        self.comfort_func_data = []
        self.lang = lang
        self.user_var = user_variable
        
        if default == 1: 
            self.CompareComfort(tar,alfa,carga)
            self.Results(delta=dias)   
                                                               
    def CompareComfort(self,tar = 1, alfa = 0.25, carga = 4):
        
        '''
          Method configures the SHC of each residence using the SHC_conf.
         Calculate the individual schedule numbers with casa_agend.
         The individual list includes the values of the settings for: tariff, alpha,
         fuzzy and non-fuzzy comfort functions, and list of loads.
        '''
        alfa_sim=alfa
        for user_var_i in tqdm(self.user_var):            
            for tar,i in enumerate(['TC','ToU']):                
                for j in self.comfort_function:        
                    alfa = [0 if tar==0 else alfa_sim][0]                                             
                    conf_f = ModConfSHC.SHC(tar=tar, alfa=alfa,
                                            lst_cargas=carga,
                                            conf_func = j,
                                            user_var = user_var_i,
                                            graf=self.graf, 
                                            lang=self.lang)    
                                    
                    lst_cargas = ['Padrão A' if carga==1 else 'Padrão B' if carga==2 else 'Padrão C']         
                    
                    # Sincronizar conf e self.comfort_function - 
                    # Rótulo x quantidade
                    conf = ['No_fuzzy' if j==1 else 'Fuzzy' if j==2 else 'Taguchi' if j==3 else 'Fz_Taguchi']                              
                                    
                    conf_f.casa_agend.insert(0,i)
                    conf_f.casa_agend.insert(1,alfa)
                    conf_f.casa_agend.insert(2,conf[0])
                    conf_f.casa_agend.insert(3,str(lst_cargas[0]))            
                    self.comfort_func_data.append(conf_f.casa_agend)        


    def Results(self,delta=0):
       '''
        Method displays the graphical response of the Process PSO method simulation
        using Dataframe structure, and simulation results
        stored in conf_alt.
       '''           
       import pandas as pd
       from datetime import datetime, timedelta
       colunas = ['tarifa','alfa','f_confort','cargas',
                  'fit_min','fit_med','fit_max','std_dev',
                  'consumo','custo_min','custo_med','custo_max',
                  'target', 'conf_min','conf_med','conf_max',
                  't_med','temp','umidade','omega']
       
       results = pd.DataFrame(columns = colunas, data = self.comfort_func_data)           
       date = datetime.now() + timedelta(delta)
       lst_datas= pd.date_range(date.strftime('%Y-%m-%d %H:%m:%S')
                                  ,freq='1s',periods=len(results))    
       results.set_index(lst_datas,inplace=True)       
       lst_casas = list(range(1,(len(results))+1))
       results.insert(0, 'F-comfort', lst_casas)                   
       
       results.to_csv(f'results/results_{date}.csv')
       self.df = results.copy()   
#%%******************************************************************************
# Test area
#******************************************************************************
def sim_full():
    alfa=[ 0.25, 0.5, 0.75]
    for i in alfa:
        SHC_ComfortFunctions(default=1,
                           graf=0,lang=1,
                           tar=1,alfa=i,carga=1,
                           Conf_Functions=[1,2,3,4],
                           user_variable=([10,60],[30,65],[39,70])
                           )
sim_full()
