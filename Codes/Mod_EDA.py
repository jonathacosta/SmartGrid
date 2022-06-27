#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Código define métodos para a realização de análise exploratória de dados
de consumo energético do SCC.
@author: Jonatha Costa
"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class EDA:
    '''
    Classe contém métodos de análise exploratória de dados sobre o consumo 
    energético condominial.
    É utilizada como parâmetro para definir os modelo de distribuição de DG.
    Dados disponíveis em:  
    https://raw.githubusercontent.com/jonathacosta/SmartGrid/main/Datasets/results.csv
    '''
    def __init__(self):
        
        self.cores = ['mediumspringgreen','blue'] 
        # self.dados = pd.read_csv('results_back.csv')
        self.dados = pd.read_csv('https://raw.githubusercontent.com/jonathacosta/SmartGrid/main/Datasets/results.csv')
        self.preprocess()
        self.graficos()
        
        # self.basic_analyse()
        
    def preprocess(self):
        ''' 
        Método realiza o pré-processamento dos dados para a análise de consumo
        por casa durante uma semana.
        100 casas durante 7 dias =  700 registros.
        '''
        self.df = self.dados.copy()                               
        self.df.drop(self.df.columns[0],axis=1,inplace=True)
        
        dias=1
        
        lst_datas= pd.date_range('2022',freq='1s',periods=len(self.df))    
        
        self.df.set_index(lst_datas,inplace=True)
        lst_casas = (list(range(1,int(len(self.df)/dias)+1)))*dias
        self.df.insert(0, 'Casa', lst_casas)            
        self.df.cargas = self.df.cargas.astype('category')
        
        
    def graficos(self):
        plt.rcdefaults()
        self.graf_geral()        
        self.graf_hist()
        self.graf_boxplot1()
        self.graf_dispersao()
        self.graf_boxplot2()
        self.graf_3d()
        
        
    def graf_geral(self):
        '''
        Método exibe apreciação gráfica preliminar dos dados de consumo
        '''
       # *************************************************************
        # Gráfico de dados de preferências do usuário e agendamento do SHC
        
        self.df.groupby(self.df.Casa).target.sum().plot(label='Agendamento por preferências do usuário (target)',
                                                        legend='on',
                                                        color='red')
        
        self.df.groupby(self.df.Casa).custo_med.sum().plot(label='Agendamento pelo SHC (Custo_med)',
                                                        title='Resultados gerais: (custo total x casa x tipo de agendamento)',
                                                        grid=False,
                                                        ylabel='Custo semanal de agendamento',
                                                        xlabel='Casas do condomínio', 
                                                        figsize=(10,8),
                                                        legend='on',
                                                        color='blue')             
    
    def graf_hist(self):       
        '''
        Método exibe os gráficos de distribuição de custo médio em relação
        ao tipo de tarifa e ao tipo de conforto.
        '''
                
        plt.figure()
        plt.title('Distribuição das cargas')
        plt.hist(self.df.cargas, color = self.cores[1])
        plt.xlabel('Tipo de carga')
        plt.ylabel('Quantidade de casas')
        
        for l in self.df.cargas.unique():
                        
            # *************************************************************                                                
            # Gráfico de custo médio  x frequencia x Tarifa
            plt.figure(figsize=(16,4))
            plt.suptitle(f'Registro de dados semanais das casas condominiais: carga {l}')
            plt.subplot(1,3,1)
            plt.hist(self.df[(self.df.tarifa ==  'ToU') & (self.df.cargas ==  l)].custo_med,label='ToU',color = self.cores[0])
            plt.hist(self.df[(self.df.tarifa ==  'Fixa')& (self.df.cargas ==  l)].custo_med,label='Fixa',color = self.cores[1])
            plt.xlabel('Custo médio')
            plt.ylabel('Quantidade de casas')
            plt.legend(loc=1)
            plt.title("Dados: custo x casas x tarifa ")                  

            # *************************************************************                                                
            # Gráfico das distribuição do custo médio para casas com tarifa TOU
            # e Fixa conforto fuzzy e no-fuzzy
            
            for i,j in enumerate(['Fixa','ToU']):
                plt.subplot(1,3,i+2)
                
                plt.hist(self.df[  (self.df.tarifa == j) & 
                                   (self.df.conf_tip == 'Fuzzy') &
                                   (self.df.cargas ==  l)
                                   ].custo_med,label='Conf_Fuzzy',
                                    color = self.cores[0])
                
                plt.hist(self.df[  (self.df.tarifa == j) & 
                                   (self.df.conf_tip != 'Fuzzy') &
                                   (self.df.cargas ==  l)
                                   ].custo_med,label='Conf_no_fuzzy',
                                   color = self.cores[1])        
                plt.xlabel('Custo médio')
                plt.ylabel('Quantidade de casas')
                plt.title(f'Tarifa {j}: custo x casas x tipo de conforto')                  
                plt.grid=False
                plt.legend(loc= 0)
                                       
    
    def graf_boxplot1(self):
        
        '''
        Método exibe os gráficos de distribuição de custo médio em quartis
        por tarifa, tipo de conforto e alfa.
        Utilizando boxplot do seaborn           
        '''  
        for i in (self.df.cargas.unique()):                 
            dados = self.df[self.df.cargas == i]

            fig,axes = plt.subplots(1,2,figsize=(12,4))
            sns.boxplot(x ='alfa', y = 'custo_med', hue = 'tarifa',
                        palette = self.cores, data=dados, ax=axes[0])
            sns.boxplot(x='alfa', y= 'custo_med', hue = 'conf_tip',
                        palette = self.cores,data=dados, ax=axes[1])                                 
            plt.suptitle(f'Observações com cargas {i}')
            sns.despine(offset=3, trim=True)

            
    def graf_boxplot2(self):
        
        '''
        Método exibe os gráficos de distribuição de custo médio em quartis
        por tarifa, tipo de conforto e alfa.
        Utilizando boxplot do pandas
        '''         
       
        for i in (self.df.cargas.unique()):                 
            dados = self.df[self.df.cargas == i]
            
            fig,axes = plt.subplots(1,2,figsize=(12,4))        
            dados.boxplot(column='custo_med',by = ['alfa','tarifa'],ax = axes[0],rot=90)
            dados.boxplot(column='custo_med',by = ['alfa','conf_tip'],ax = axes[1],rot=90)
            plt.suptitle(f'Observações com cargas {i}')
                            

    def graf_dispersao(self):    
        '''
        Método exibe os gráficos de dispersão 
        Utilizando o pandas e plt
        '''  
        dados = self.df
        plt.figure()
        with plt.style.context('seaborn'): 
            #  Utilizando o matplotlib
            plt.scatter(y = dados.custo_med, x = dados.Casa ,
                        c = dados.target, s= dados.t_med*20, 
                        cmap = 'plasma',alpha=0.9)
            plt.ylabel('Custo médio')
            plt.xlabel('alfa')
            
            plt.colorbar()  
        plt.show()
        
        with plt.style.context('seaborn'):            
            #  Utilizando o pandas
            dados.plot.scatter(x='Casa',y='custo_med', 
                               s=dados.t_med*20,c='target',
                               cmap = 'plasma',alpha=0.9)
           
    def graf_3d(self):
        '''
        Método apresenta gráfico 3D.
        '''
        # from mpl_toolkits import mplot3d
           
        dados = self.df.copy(deep=True)
        dados.tarifa = dados.tarifa.apply(
                lambda x: x.replace('Fixa', '0').replace('ToU', '1')
                ).astype('int8')
        dados.conf_tip= dados.conf_tip.apply(
                lambda x: x.replace('No_fuzzy', '0').replace('Fuzzy', '1')
                ).astype('int8')
        
            
        plt.figure(figsize=(15,6))
        ax = plt.axes(projection="3d")
        
        x = dados.custo_med
        y = dados.conf_tip
        z = dados.alfa
        c = z
        
        ax.scatter3D(x, y, z, c = c, cmap='viridis')            
        plt.title('Custo x conforto x alfa')        
        ax.set_xlabel('Custo médio')
        ax.set_ylabel('Tipo de conforto')
        ax.set_zlabel('Alfa')        
        plt.show()   
        

         

        
    def basic_analyse(self):
        '''
        Método realiza análise preliminar do dataframe com dados de correlação
        entre variáveis.           
        '''
               
        dia=self.df
        dia=dia.resample('D').sum()
        
        print(dia)
        plt.figure(figsize=(12,6))
        plt.scatter(dia.index, dia.target, c = dia.custo_med, cmap='plasma', alpha=0.9 )
        plt.colorbar().set_label('custo_med (R$)')
        
        plt.grid()
        plt.xlabel('Diário')
        plt.ylabel('Consumo diário em intervalo semanal')
        plt.title('Consumo diário do condimínio de 100 casas')
        plt.show()
        
        # for year in range(dia.index.day[0], dia.index.day[-1]+1):
        #                 plt.axvline(pd.to_datetime(str('D')+'-01-01'),color='k',linestyle='--',alpha=0.5)    

        
        print(dia.groupby(dia.Casa).target.sum().sort_values(ascending=False))
        dia.groupby(dia.Casa).target.sum().plot()
    
        
        
if '__name__==main':
    a=EDA()
