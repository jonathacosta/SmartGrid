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
    def __init__(self,exibir_graf=False): 
        '''
        Método inicia as configurações e chamadas da classe para o objeto
        instacionado externamente.
        '''       
        self.cores = ['mediumspringgreen','blue'] 
        self.dados = pd.read_csv('results/results_combined/results-full.csv')          
        self.preprocess() 
        self.preprocess_mes()

        if exibir_graf == True:
            self.graf_eda()

    def graf_eda(self):
        '''
        Método realiza a chamada de gráficos distintos para EDA
        do SCC.
        '''
        self.hist_plt(1)        # Histograma diário
        self.hist_plt(30)       # Histograma mensal
        self.scatter_conf_TC_ToU()   # Scatter: conf x tarifa x casas
        self.consumo_mensal_condominio()
        self.custo_mensal_condominio()
        self.consolidado()   
        
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

   
    def preprocess_mes(self):    
        '''
        Método cria um dataset com a coluna mês, e o somatório dss valores 
        de custo e consumo                
        '''
        df_mes = pd.DataFrame()
        df_mes["mes"] = pd.DatetimeIndex(pd.to_datetime(self.df['data'], format="%Y-%m-%d")).month
        df_mes['consumo'] = self.df['consumo']
        df_mes['custo_med'] = self.df['custo_med']
        df_mes = df_mes.groupby(by='mes').sum()
        self.df_mes = df_mes.copy()   
    

    def hist_plt(self,dias=30):
        '''
        Método cria histograma do conjunto de dados com subconjunto 
        diária de 100 casas
        Input = 100 * dias        
        '''
        dados = self.df.copy()
        dados = dados.iloc[:100*dias,:]        
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
                plt.scatter(x = xticks1, y = x1['conf_med'],color='blue',
                            s=50, marker='o', label = f'{i}, alfa = {alfa_str} e Fuzzy' )
                plt.scatter(x = xticks1, y = x2['conf_med'], color='red',
                            s=30,marker = '+', label = f'{i}, alfa = {alfa_str} e No_fuzzy')                                                
                plt.ylabel('Conforto médio')
                plt.xlabel('Casas com a mesma quantidade de cargas (Padrão A - 10 cargas)')
                plt.xticks(xticks1)
                plt.ylim([0.8, 1.0])
                plt.legend(bbox_to_anchor=(0.15 ,3.1))
                plt.legend(frameon=True)
                plt.title(f'Conforto médio de {n} residencias com {i}')
                plt.savefig(f'results/figuras/eda_graf_geral_scatter_{i}_conf.png', dpi = 500)


    def consumo_mensal_condominio(self,detalhado=0):
        '''
        Método analisa o consumo médio mensal do dataset.
        '''
        x = self.df.copy()
        x["mes"] = pd.DatetimeIndex(pd.to_datetime(x['data'], format="%Y-%m-%d")).month
        f= x.groupby(by='mes').sum().consumo
        
        if detalhado == 1:
            print('-'*50)
            print('\n1.Consumo acumulado de 30 dias em kWh:\n')      # Somatório dos valores diários de kWh
            print('-'*50)
            print('\n',f)
            print('\n','-'*50,'\n\tDescritivo - quartis:\n','-'*50)
            print(f.describe())
            print('-'*50)

            
        xticks1 = np.arange(1,13)
        with plt.style.context('seaborn'):     

            fig, ax1 = plt.subplots()                
            color ='blue'
            ax1.set_xlabel('Meses de observação')
            ax1.set_ylabel('Consumo mensal (kWh.mês)')                
            ax1.scatter(x = f.index, y = f,color=color,
                        s=100, marker='o', label = 'Consumo(kWh/mes)' )
            
            plt.ylim([f.mean()*0.6, f.mean()*1.2])
            plt.xticks(xticks1)
            plt.title('Consumo mensal do condomínio')            
            plt.savefig('results/figuras/eda_graf_consumo_mensal_condominio.png', dpi = 500)

        
    def custo_mensal_condominio(self,detalhado=0):
        '''
        Método analisa o custo médio mensal do dataset.
        '''
        x = self.df.copy()
        x["mes"] = pd.DatetimeIndex(pd.to_datetime(x['data'], format="%Y-%m-%d")).month
        f= x.groupby(by='mes').sum().custo_med
                        
        if detalhado == 1:
            print('\n1.Custo acumulado de 30 dias: mil R$:\n',f/1000)      # Somatório dos valores diários de kWh
        
            print(f.describe())

        if detalhado == 1:
            print('-'*50)
            print('\n1.Custo total do consumo acumulado de 30 dias em R$:\n')      # Somatório dos valores diários de kWh
            print('-'*50)
            print('\n',f)
            print('\n','-'*50,'\n\tDescritivo - quartis:\n','-'*50)
            print(f.describe())
            print('-'*50)
    
            
        xticks1 = np.arange(1,13)

        with plt.style.context('seaborn'):     

            fig, ax1 = plt.subplots()    
            
            color ='red'
            ax1.set_xlabel('Meses de observação')
            ax1.set_ylabel('R$ / mês')
            ax1.scatter(x = f.index, y = f,color=color,
                        s=100, marker='o', label = 'Custo R$' )            
            
            plt.ylim([f.mean()*0.6, f.mean()*1.2])
            plt.xticks(xticks1)
            plt.title('Faturamento mensal do condomínio')            
            plt.savefig('results/figuras/eda_graf_custo_geral.png', dpi = 500)

    def consolidado(self):
        '''
        Método apresenta o gráfico consolidado de custo e o consumo médio mensal do dataset.
        '''
        x = self.df.copy()
        x["mes"] = pd.DatetimeIndex(pd.to_datetime(x['data'], format="%Y-%m-%d")).month
        f = x.groupby(by='mes').sum().custo_med
        g = x.groupby(by='mes').sum().consumo
        xticks1 = np.arange(1,13)

        with plt.style.context('seaborn'):     

            fig, ax1 = plt.subplots()    
                        
            color ='blue'
            ax1.set_xlabel('Meses de observação')
            ax1.set_ylabel('Consumo em kWh.mês', color=color)
            ax1.set_ylim([g.mean()*.85, g.mean()*1.1])
            ax1.scatter(g.index,g,color=color,
                        s=100,marker='o', label='consumo')
            
            ax1.tick_params(axis='y', labelcolor=color)                                
            ax1.legend()
            plt.xticks(xticks1)
                                            
            ax2 = ax1.twinx()
            color = 'red'            
            ax2.set_ylabel('Custo em R$ / mês',color='black')            
            ax2.set_ylim([f.mean()*0.75, f.mean()*1.1])
            ax2.scatter(f.index, f, color=color, alpha=0.8,
                        s=100, marker='o', label = '\nCusto R$' )                                    
            ax2.tick_params(axis='y', labelcolor='black')
            ax2.legend()            
            plt.title('Consumo e custo mensal do condomínio')                        
            plt.savefig('results/figuras/eda_graf_consolidade_consumo_custo_geral.png', dpi = 500)    
        

#% ********SIMULAÇÕES***************************************************
# a=EDA()
# a.consumo_mensal_condominio(1)
# a.custo_mensal_condominio(1)
# a.consolidado()

                       
