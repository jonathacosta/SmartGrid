#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de condomínio
"""
import numpy as np
import ModConfSHC

np.random.seed(42)
class SCC():
    '''
    Classe gerencia a geração e distribuição de energia renovável entre as 
    casas(SHC) de um condomínio de 30 casas.
    Hiperparâmetros combináveis entre as casas:
        * Total créditos de energia renovável(DG)
        * Escolha de parâmetros de casa entre:
            - cargas
            - tarifas
            - limiares de conforto  x econonimia
            - conforto fuzzy e no-fuzzy
    
    '''
    
    def __init__(self,graf=0,dias=0,casas=1000):
        self.graf = graf        
        self.casas = casas
        self.condominio_dados=[]               
       
        self.condominio_casas()
        self.Results(delta=dias)        
                              
    def SHC_conf(self,casa_id):
        '''
        Método define as configurações de SHC para uma casa do condomínio 
        através de escolha aleatória entre:
            * Tarifa: branca ou fixa
            * Valor de alfa (conforto x custo) entre [0, 0.25, 0.5, 0.75, 1.0]
            * Utilização de conforto fuzzy ou no-fuzzy
            * Lista de cargas agendáveis Padrão A,Padrão B e Padrão C
            * Parâmetro 'casa_id' força tarifa fixa às 50 primeiras casas
              e ToU para as demais
        '''
        
        if casa_id < 50:
            tarifa, alfa = 0, 0
        else:
            tarifa = 1
            lst_alfa=[0, 0.25, 0.5, 0.75, 1.0]        
            alfa = lst_alfa[ np.random.randint(0,5) ]                
        
        conf_fz = np.random.randint(0,2)
        lst_cargas = np.random.randint(1,4)         
        
        return (tarifa, alfa, conf_fz, lst_cargas)
                                                              
 
    def condominio_casas(self):
        
        '''
        Método configura o SHC de cada residencia utilizando o SHC_conf.
        Calcula os números do agendamento individual com o casa_agend.
        Inclui a lista individual os valores das configurações de: tarifa, alfa,
        conforto fuzzy e no-fuzzy, e lista de cargas.
        Total de 100 casas condominiais.        
        '''
        for i in (range(self.casas)):              
            (a,b,c,d) = self.SHC_conf(i)                            
            casa_i = ModConfSHC.SHC(tar=a, alfa=b, conf_fz=c, lst_cargas=d, 
                         graf=self.graf, casa = i+1)            
            
            tar = ['TC' if a==0 else 'ToU']           
            conf = ['No_fuzzy' if c==0 else 'Fuzzy']              
            lst_cargas = ['Padrão A' if d==1 else 'Padrão B' if d==2 else 'Padrão C']         
            
            casa_i.casa_agend.insert(0,tar[0])
            casa_i.casa_agend.insert(1,b)
            casa_i.casa_agend.insert(2,conf[0])
            casa_i.casa_agend.insert(3,str(lst_cargas[0]))            
            self.condominio_dados.append(casa_i.casa_agend)        


    def Results(self,delta=0):
       '''
       Método exibe a resposta gráfica da simulação do método Process PSO
       utilizando estrutura de Dataframe, e os resultados das simulações 
       armazenados em conf_alt.
       '''           
       import pandas as pd
       from datetime import datetime, timedelta
       colunas = ['tarifa','alfa','conf_tip','cargas',
                  'fit_min','fit_med','fit_max','std_dev',
                  'consumo','custo_med','target','conf_med %',
                  't_med','temp', 'umidade', 'humor',
                  'omega','rel_alt']
       
       results = pd.DataFrame(columns = colunas, data = self.condominio_dados)           
       data = datetime.now() + timedelta(delta)
       lst_datas= pd.date_range(data.strftime('%Y-%m-%d %H:%m:%S')
                                 ,freq='1s',periods=len(results))    
       results.set_index(lst_datas,inplace=True)       
       lst_casas = list(range(1,(len(results))+1))
       results.insert(0, 'casa', lst_casas)                   
       data=data.strftime('%Y-%m-%d')
       
       results.to_csv(f'results/results_{data}.csv')
       # print(f'Resultados para {ModConfSHC.SHC().iteracoes} iterações.',results)
       self.df = results.copy()   
#******************************************************************************
# AREA DE TESTES
#******************************************************************************
        
        
    



