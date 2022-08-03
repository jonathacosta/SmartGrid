#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Código define métodos para a realização de análise exploratória de dados
de consumo energético do SCC.
@author: Jonatha Costa
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class EDA:
    '''
    Classe contém métodos de análise exploratória de dados sobre o consumo 
    energético condominial.
    É utilizada como parâmetro para definir os modelo de distribuição de DG.
    Dados disponíveis em:  
    https://raw.githubusercontent.com/jonathacosta/SmartGrid/main/Datasets/results.csv
    '''
    def __init__(self,exibir_graf=0):                
        self.cores = ['mediumspringgreen','blue'] 
        self.dados = pd.read_csv('results/results_combined/results_full.csv')          
        self.preprocess()        
        if exibir_graf == 1:
            self.graf_eda()

    def graf_eda(self):
        '''
        Método realiza a chamada de gráficos distintos para EDA
        do SCC.
        '''
        self.hist_plt(1)        # Histograma diário
        self.hist_plt(30)       # Histograma mensal
        self.scatter_conf_TC_ToU()   # Scatter: conf x tarifa x casas
        
            
    def preprocess(self):
        ''' 
        Método realiza o pré-processamento dos dados para a análise de consumo
        100 casas 
        '''
        cargas_id = {
            'Padrão A':'Padrão A: 10 cargas',
            'Padrão B':'Padrão B: 7 cargas',
            'Padrão C':'Padrão C: 4 cargas'}           
        self.df=self.dados.copy()        
        self.df.rename(columns={self.df.columns[0]: 'data'},inplace=True)            
        self.df['cargas_alt'] = self.df['cargas'].map(cargas_id)
        self.df['econ 2'] = 100*(self.df['target']  - self.df['custo_med'])/ self.df['target']
            

    def hist_plt(self,dias=30):    
        dados = self.df.copy()
        dados = dados.iloc[:100*dias,:]    # Fatia das 100 primeiras casas - dia 01 do banco de dados
        
        # Modificando os valores do rótulo para eixo x.
        
        alfa=[ 0.3, 1]                
        plt.figure()
        plt.title('Distribuição de cargas entre as casas do condomínio')
        plt.hist(dados.cargas_alt, 
                 color = self.cores[1],
                 orientation='vertical',
                 cumulative=False,
                 histtype='barstacked', 
                 alpha=alfa[-1],
                 align='mid',
                 bins=6)
        if dias == 1:
            plt.ylabel(f'Total de registros de casas em {dias} dia')          
            plt.savefig('results/figuras/distr_cargas_1dia.png', dpi = 1000)
        else:
            plt.ylabel(f'Total de registros de casas em {dias} dias')          
            plt.savefig(f'results/figuras/distr_cargas_{dias}dias.png', dpi = 1000)        


    def scatter_conf_TC_ToU(self,casas=5):  
        
        '''
        Método apresenta o gráfico comparativo de dispersão entre 'n' casas.
        Se n = 5:
        -  5 com TC e fuzzy, 5 com TC e no-fuzzy
        -  5 com ToU e fuzzy, 5 com ToU e no-fuzzy        
            * carga - padrão A
            * tarifa - TC e ToU
        '''
        z=pd.DataFrame()             # Define o DF vazio para armazenar os recortes das linhas
        alfa = 0.25                  # Define um valor de alfa para ToU
        n=casas                      # Define a quantidade de casas de cada combinação de parâmetros 
        dados = self.df[self.df.cargas == 'Padrão A'].copy()  # Cria um df com carga padrão A

        for k in dados.tarifa.unique():                    # Lista as tarifas
            for i in dados.conf_tip.unique():              # Lista dos tipos de conforto
                if k == 'ToU':                             # Filtro com alfa para ToU
                    zn = dados[(dados.tarifa == k) & 
                               (dados.alfa==alfa) & 
                               (dados.conf_tip == i)
                               ].iloc[:n,:]
                else:
                    zn = dados[(dados.tarifa == k) & 
                               (dados.conf_tip == i)
                               ].iloc[:n,:]                            
                z=pd.concat([z,zn])                      # Concatena cada recorte no DF vazio   
        self.z = z.copy()                                # Permite acesso externo ad DF z                            
        for i in z.tarifa.unique():                      # Constroi o gráfico para cada tarifa
            xticks1 = np.arange(1,n+1)
            if i=='ToU': 
                alfa_str=str(alfa)
            else:
                alfa_str = '0,0'
            
            with plt.style.context('seaborn'):         
                plt.figure()    
                x1 = z[(z.tarifa==i) & (z.conf_tip == 'Fuzzy')]
                x2 = z[(z.tarifa==i) & (z.conf_tip == 'No_fuzzy')]
                plt.scatter(x = xticks1, y = x1['conf_med %'],color='blue',
                            s=50, marker='o', label = f'{i}, alfa = {alfa_str} e Fuzzy' )
                plt.scatter(x = xticks1, y = x2['conf_med %'], color='red',
                            s=30,marker = '+', label = f'{i}, alfa = {alfa_str} e No_fuzzy')                                                
                plt.ylabel('Conforto médio')
                plt.xlabel('Casas com a mesma quantidade de cargas (Padrão A - 10 cargas)')
                plt.xticks(xticks1)
                plt.ylim([0.8, 1.0])
                plt.legend(bbox_to_anchor=(0.15 ,3.1))
                plt.legend(frameon=True)
                plt.title(f'Conforto médio de {n} residencias com {i}')
                plt.savefig(f'results/figuras/eda_graf_geral_scatter_{i}_conf.png', dpi = 500)

        
#% ********SIMULAÇÕES***************************************************
# a=EDA()    
                       
