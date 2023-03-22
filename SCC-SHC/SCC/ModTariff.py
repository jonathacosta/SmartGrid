#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
"""
Modelagem de tarifação

Modelos de tarifação de energia elétrica

Classe principal contém - periodicidade de amostragem para modelar custo

"""
import numpy as np

class Tariffs():
    '''
    Classe contém métodos que definem o custo em função das tarifas de estudo.
    -Necessário informar intervalo de amostragem para modelagem em minutos:
        Tariffs(sample_interval = 5)
        
        Sample_interval deve ser melhor que 60 min.
    -Método init carrega dados básicos das amostragem para tarifação.
        ------------------------------------------------------------       
        - Tarifa de custo contante
        - Tarifa branca
    '''
    def __init__(self,sample_interval=5):
        self.sample_interval = sample_interval    # amostragem de consumo em min
        self.Tariff_const()
        self.Tariff_ToU()
        # self.Graf_tariff()
    
    def Tariff_const(self,price=0.87345):
        '''
        Método retorna um vetor 'n' dimensional com valores do preço da tarifa.
         - 'n' é definido como a razão entre :(o total de minutos diários (60*24)) 
            e  a taxa de amostragem:(sample_interval)
         - 'reshape(1,-1)'é utilizado para vetorizar a saída para
            'n' colunas e 1 linha
        Parametros:
            price : float
        
            -Necessário informar o preço da tarifa
            
            -Tariff_const(price = 0.722495). DEFAULT
        Retorno
        -------
            Vetor de preços 'n' dimensional
            Tariff_const

        '''
        passo = int(24*60/self.sample_interval)    
        self.tariff_constant = price*np.ones(passo).reshape(1,-1)
        

    def Tariff_ToU(self,p1=0.56355,p2=0.88144,p3=1.42294):
        '''
        Método retorna um vetor 'n' dimensional com valores do preço da tarifa branca.
        Time of Use
         - 'n' é definido como a taxa de amostragem horária, em minutos:\n
             (1h*60min))/(sample_interval)
             
        Parametros
        ----------
        p1 : float. 
            Custo da tarifa branca no horário de 'FORA DE PONTA'            
            Das 1h às 17h e 23h às 24h (Ou das 23h às 17h do dia seguinte)
            
        p2 : float
            Custo da tarifa branca no horário de 'INTERMEDIÁRIO'
            Das 17h às 18h e das 21h às 22h
            
        p3 : float
            Custo da tarifa branca no horário de 'PONTA'
            Das 18h às 21h
        Valores default:    
            preco_fora_de_ponta = 0.56355,\n
            preco_intermediario = 0.88144,\n
            preco_de_ponta = 1.42294
        Retorno
        -------
            Vetor de preços 'n' dimensional
            ToU

        '''
        passo = int(1*60/self.sample_interval)    
        self.Tariff_of_Use = np.hstack(( 
            [p1*np.ones(17*passo)],
            [p2*np.ones(1*passo)],
            [p3*np.ones(3*passo)],
            [p2*np.ones(1*passo)],
            [p1*np.ones(2*(passo))]
            ))               
        


    def Graf_tariff(self):  
        '''
        Método exibe o gráfico das tarifas ToU e fixa
        '''
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10,5),dpi=150)
        xticks1 = (np.arange(1,25)*(24*60/self.sample_interval)/24)
        xticks2 = list(map(str,np.arange(1,25,1)))
        plt.xticks(xticks1, xticks2 )      
        plt.plot(self.Tariff_of_Use.ravel(),label='Tarifa Branca',color='b')
        plt.plot(self.tariff_constant.ravel(),label='Tarifa Fixa',color='y')
        plt.ylabel("R$/kwh")
        plt.xlabel("Tempo (h)")       
        plt.grid(color='white')
        plt.legend()
        plt.style.use('ggplot')

#%% Test space
def test():
    a=Tariffs()
    a.Graf_tariff()


# test()
