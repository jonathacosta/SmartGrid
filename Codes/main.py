#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main code to SHC using PSO multiobjetive
@author: Costa, Jonatha, jun 2022
V4 Main throught POO with comfort fuzzy function
"""
import ModLoad
import ModTariff
import ModExecPSO
import ModConfFz
from tqdm import tqdm
import numpy as np
np.random.seed(42)


class SCC:
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
    
    def __init__(self):
        self.condominio=[]
        self.condominio_casas()
        self.Results()
      
    def SHC_conf(self):
        '''
        Método define as configurações de SHC para uma casa do condomínio 
        através de escolha aleatória entre:
            * tarifa: branca ou fixa
            * valor de alfa entre [0, 0.25, 0.5, 0.75, 1.0]
            * utilização de conforto fuzzy ou no-fuzzy
            * Lista de cargas agendáveis l1,l2,l3
            * 
        '''
        tarifa = np.random.randint(0,2)
        lst_alfa=[0, 0.25, 0.5, 0.75, 1.0]
        if tarifa == 1:
            alfa = lst_alfa[np.random.randint(0,5)]                
        else:
            alfa = 0
        conf_fz = np.random.randint(0,2)
        lst_cargas = np.random.randint(0,3)        
                
        return tarifa, alfa, conf_fz, lst_cargas
             
                        
    def condominio_casas(self):
        
        '''
        Método configura o SHC de cada residencia utilizando o SHC_conf.
        Calcula os números do agendamento individual com o casa_agend.
        Inclui a lista individual os valores das configurações de: tarifa, alfa,
        conforto fuzzy e no-fuzzy, e lista de cargas.
        Total de 100 casas condominiais.
        '''
        for i in tqdm(range(100)):
            (a,b,c,d) = self.SHC_conf()
            casa_n = SHC(tar=a,alfa=b,conf_fz=c,lst_cargas=d)            
            
            tar = ['Fixa' if a==0 else 'ToU']           
            conf = ['No_fuzzy' if c==0 else 'Fuzzy']              
            lst_cargas = ['L1' if d==1 else 'L2' if d==2 else 'L3']         
            casa_n.casa_agend.insert(0,tar[0])
            casa_n.casa_agend.insert(1,b)
            casa_n.casa_agend.insert(2,conf[0])
            casa_n.casa_agend.insert(3,str(lst_cargas[0]))
            self.condominio.append(casa_n.casa_agend)            
            
        
    def Creditos_DG(self):
        pass
   
           
    def Results(self,graf=0):
       '''
       Método exibe a resposta gráfica da simulação do método Process PSO
       utilizando estrutura de Dataframe, e os resultados das simulações 
       armazenados em Cenario e em conf_alt.
       '''           
       import pandas as pd
       colunas = ['tarifa','alfa','conf_tip','cargas',
                  'fit_min','fit_med','fit_max','std_dev',
                  'consumo','custo_med','target','econ',
                  'conf_med','t_med']
       
       self.df = pd.DataFrame(columns = colunas, data = self.condominio)           
       lst_datas= pd.date_range(pd.to_datetime('today').strftime('%Y-%m-%d %H:%m:%S')
                                 ,freq='1s',periods=len(self.df))
          
       self.df.set_index(lst_datas,inplace=True)       
       lst_casas = list(range(1,(len(self.df))+1))
       self.df.insert(0, 'Casa', lst_casas)            
       self.df.cargas = self.df.cargas.astype('category')
       data=pd.to_datetime('today').strftime('%Y-%m-%d')
       self.df.to_csv(f'results_{data}.csv')       
       print(f'Resultados com {SHC().iteracoes} iterações.\n\n',self.df)
       
       
       
       if graf==1:
           self.sol.GrafAgendCargas()   

class SHC:
    '''
    Classe realiza a análise de consumo versus conforto aplicando agendamento de cargas
    via PSO com conforto Fuzzy.
    '''
    def __init__(self,sample_interval=5,tar=0,alfa=0, lst_cargas=0, conf_fz=0):
        '''
        Método init carrega variável global :
            -'sample_interval=5'
            - tarifas
            - cargas
            - picos de cargas
        '''       
        ''' Variáveis'''
        self.alfa = alfa
        self.Cenario=[]			    # Aux
        self.iteracoes=30 		    # Iterações PSO
        self.conf_fz=conf_fz		# Conforto fuzzy
        '''Módulo 01: tarifas e limite de pico de consumo para cargas não agendáveis'''
        if tar == 1: # set tarifa branca
            self.tarifas = ModTariff.Tariffs().Tariff_of_Use
        else:       # preset tarifa fixa
            self.tarifas = ModTariff.Tariffs().tariff_constant
        '''Módulo 02: Preenchimentos de objetos por amostragem com lista de cargas'''
        
        if lst_cargas == 1: 
            self.cargas = ModLoad.DadosReferencia().cargas_lista1
        elif lst_cargas == 2: 
            self.cargas = ModLoad.DadosReferencia().cargas_lista2
        else:     
            self.cargas = ModLoad.DadosReferencia().cargas_lista3        
        
        '''Módulo 03: Conforto fuzzy'''
        if self.conf_fz == 1: self.Fz_Conf_cargas()        
        '''Módulo 04:Valores de pico de carga por amostragem não agendáveis'''
        self.pico_cargas = ModLoad.Peak_ref().pico_cargas_nao_agendaveis
        '''Módulo 05: Execução do PSO'''
        self.Process_PSO()  
        
    def Fz_Conf_cargas(self):
        '''
        Método recebe um objeto (carga) e atualiza o atributo (comfort level)
        em função de humor do usuário-admin, temperatura e umidade
        Entrada: objeto comfortlevel_in
        Saída : objeto comfortlevel_out
        '''     
        self.conf_alt=[]
        for i in (self.cargas):
            if i.comfortLevel >= 0.5:                
                a = (float(i.comfortLevel))
                i.comfortLevel = ModConfFz.Fz_sim().Fuzificar()
                self.conf_alt.append([i,a,i.comfortLevel])       
          
    def Process_PSO(self):
        '''
        Método de chamada para executar o PSO aplicando parametros do algoritmo e dos métodos sobre as cargas
        de modo que :
            * alfa [0,1] = [economia,conforto]
            * f = αf1 +(1−α)f2
        Para alfa = 0, o controlador obterá a melhor solução para os níveis de conforto do usuário conforme peso de alfa.
        Para alfa = 1, o controlador minimizará apenas os custos do consumo de eletricidade. De modo que haverá conforto, 
        pois as cargas serão acionadas, contudo esse não será um critério considerado pelo SHC para escolha dos horários.
        
        O método instancia o objeto 'sol' com os atributos da classe ExecPSO (dentro do módulo ModExecPSO). Seguidamente,
        é chamado o método que busca a melhor solução do PSO através de sol.PSO(), juntamente com as respostas
        gráficas para o referido valor de alfa.
        Isso é repetido para cada novo valor de alfa no laço 'for'.
        '''                                  
        sol = ModExecPSO.ExecPSO(alpha = self.alfa, 
                                 tarifa = self.tarifas,
                                 iteration=self.iteracoes,
                                 peak_limits= self.pico_cargas, 
                                 Loads = self.cargas)
        sol.PSO()
        self.casa_agend = sol.lst
                                           
        
if '__name__==main':
    a=SCC()
    



