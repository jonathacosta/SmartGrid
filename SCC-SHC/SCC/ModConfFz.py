#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Método utiliza Lógica Fuzzy para definir um valor de conforto em 0 e 1.

"""

import skfuzzy as fuzz
import numpy as np   
from skfuzzy import control as ctrl
from random import randint,random
SEED=42


class Fz_Comfort:
    
    '''
    Classe aplica métodos para construir uma saída de conforto entre 0,1
    
    * Entrada:  Estado de humor, temperatura e humidade
    
    * Saída: Nível de conforto da carga
        
    '''
    
    def __init__(self,humor,temp,umidade,graf=0,lang=0):
        
        # Variáveis linguísticas
        self.temp_in = temp
        self.humor_in = humor
        self.umidade_in = umidade
        if lang==0:
        # Valores das variáveis linguísticas
            self.t = ['muito fria','fria','amena','quente','muito quente']        
            self.h = ['mau','intermediário','bom']        
            self.u = ['baixa','mediana','alta']
            self.c = ['baixo','médio','alto']
        else:    
            self.t = ['very cold','cold','mild','hot','very hot']        
            self.h = ['bad','intermediary','good']        
            self.u = ['low','median','high']
            self.c = ['low','medium','high']
            
        
        # Função de início da classe        
        self.Vars_Pert()
        self.Rules()        
        self.Comput()
        if graf==1:
            self.Grap_result()         
               
    def Vars_Pert(self):
        '''
        Método cria as variáveis de entrada e saida para o problema
        e atribui o mapeamento entre os valores nítidos e difusos
        utilizando a função de pertinencia
        * Humor       : mau, bom e ótimo. Escala 0 a 10.
        * Temperatura : fria, amena e quente. Escala 0 a 40.
        * Umidade     : baixa, média e alta. Escala 30 a 65.
        * Conforto    : baixo, médio e alto. Escala 0 a 10.
        
        Os efeitos da umidade sobre o clima são sentidos tanto nas temperaturas quanto 
        no regime de chuvas. A água, em razão de seu calor específico, tende a conservar 
        por mais tempo as temperaturas, fazendo com que haja uma menor variação delas, 
        ou seja, a amplitude térmica (diferença entre a maior e a menor temperatura) 
        é menor quanto maior for a umidade do ar. Além disso, em regiões mais úmidas 
        ou que estejam mais afetadas pela umidade, o regime de chuvas tende a ser maior, 
        pois a saturação do ar que provoca a condensação é mais frequente.
        
        umidade alta -> baixa variação de temperatura
        '''               
        #Entrada e pertinencia - 01
        self.temp = ctrl.Antecedent(np.arange(0, 41, 1), 'temperatura')  
        self.temp[self.t[0]] = fuzz.trapmf(self.temp.universe, [0,0,10,18])        
        self.temp[self.t[1]] = fuzz.gaussmf(self.temp.universe, 18,3)         
        self.temp[self.t[2]] = fuzz.gaussmf(self.temp.universe, 25,3)         
        self.temp[self.t[3]] = fuzz.gaussmf(self.temp.universe, 35,4)         
        self.temp[self.t[4]] = fuzz.gaussmf(self.temp.universe, 38,4)                
  
        #Entrada e pertinencia - 02
        self.umidade = ctrl.Antecedent(np.arange(35,76,1), 'umidade')
        # self.umidade.automf(names=self.u)
                
        self.umidade[self.u[0]] = fuzz.trapmf(self.umidade.universe, [0,0,40, 50])
        self.umidade[self.u[1]] = fuzz.trimf(self.umidade.universe, [40, 55, 70])
        self.umidade[self.u[2]] = fuzz.trapmf(self.umidade.universe, [60, 70, 75,75])
                
        #Entrada e pertinencia - 03
        self.humor = ctrl.Antecedent(np.arange(0,11,1), 'humor')
        self.humor[self.h[0]] = fuzz.trapmf(self.humor.universe, [0,0,3,5])
        self.humor[self.h[1]] = fuzz.trapmf(self.humor.universe, [3,5,6,8])
        self.humor[self.h[2]] = fuzz.trapmf(self.humor.universe, [6,8,10,10])
                            
        #Saída e pertinencia
        self.conf = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'conforto')  
        self.conf[self.c[0]] = fuzz.trapmf(self.conf.universe, [0.0, 0.0, 0.2,  0.4])
        self.conf[self.c[1]] = fuzz.trapmf(self.conf.universe, [0.2, 0.4, 0.6,  0.8])
        self.conf[self.c[2]] = fuzz.trapmf(self.conf.universe, [0.6, 0.8, 1.0, 1.0])
                        
    def Rules(self):

        self.rule1 = ctrl.Rule(
            (self.humor[self.h[0]] & self.temp[self.t[0]])
            ,self.conf[self.c[0]])
        
        self.rule2 = ctrl.Rule(
            (self.humor[self.h[0]] & self.temp[self.t[1]]) |
            (self.humor[self.h[0]] & self.temp[self.t[2]] & self.humor[self.h[0]])
            ,self.conf[self.c[1]])
        
        self.rule3 = ctrl.Rule(
            (self.humor[self.h[0]] & (self.temp[self.t[3]] | self.temp[self.t[4]])) |
            (self.humor[self.h[0]] & self.temp[self.t[2]] & (self.umidade[self.u[1]] |self.umidade[self.u[2]]) )
            ,self.conf[self.c[2]])
        
        # *****************************************************************************************
        self.rule4 = ctrl.Rule(
            (self.humor[self.h[1]] & (self.temp[self.t[0]] | self.temp[self.t[1]]) ) |
            (self.humor[self.h[1]] & self.temp[self.t[2]] & self.umidade[self.u[2]])
            ,self.conf[self.c[0]])
        
        self.rule5 = ctrl.Rule( 
            (self.humor[self.h[1]] & 
            (self.temp[self.t[2]] | self.temp[self.t[3]])  &
            (self.umidade[self.u[0]] |self.umidade[self.u[1]]) )
            ,self.conf[self.c[1]])
        
        self.rule6 = ctrl.Rule(
            (self.humor[self.h[1]] & (self.temp[self.t[4]])) |
            (self.humor[self.h[1]] & self.temp[self.t[3]] & self.umidade[self.u[2]])
            ,self.conf[self.c[2]])
        
        # *****************************************************************************************
        self.rule7 = ctrl.Rule(
            (self.humor[self.h[2]] & 
            (self.temp[self.t[0]]|
              self.temp[self.t[1]]|
              self.temp[self.t[2]]))
            ,self.conf[self.c[0]] )
        
        self.rule8 = ctrl.Rule(
            (self.humor[self.h[2]] & 
              (self.temp[self.t[3]] |self.temp[self.t[4]]) &
              (self.umidade[self.u[0]] |self.umidade[self.u[1]]) ) |
            (self.humor[self.h[2]] & self.temp[self.t[3]] & self.umidade[self.u[2]])
            ,self.conf[self.c[1]])
        
        self.rule9 = ctrl.Rule(
            (self.humor[self.h[2]]&
            self.temp[self.t[4]] &
            self.umidade[self.u[2]]),
            self.conf[self.c[2]])
        
        # *****************************************************************************************
        self.conf_ctrl = ctrl.ControlSystem([self.rule1, self.rule2, self.rule3,
                                              self.rule4,self.rule5,self.rule6,
                                              self.rule7,self.rule8,self.rule9])
        self.conf_simulador = ctrl.ControlSystemSimulation(self.conf_ctrl)    

    def Comput(self):
        
        self.conf_simulador.input['temperatura'] = self.temp_in
        self.conf_simulador.input['umidade'] = self.umidade_in
        self.conf_simulador.input['humor'] = self.humor_in      # Chamada pela label
                
        self.conf_simulador.compute()
                
    def Grap_result(self):
        #Resultados
        import matplotlib.pyplot as plt
        
        self.temp.view(sim=self.conf_simulador)
        plt.savefig('results/figuras/Fz_temp.png', dpi = 500)
        self.humor.view (sim=self.conf_simulador)
        plt.savefig('results/figuras/Fz_humor.png', dpi = 500)        
        self.umidade.view(sim=self.conf_simulador)
        plt.savefig('results/figuras/Fz_umid.png', dpi = 500)
        self.conf.view(sim=self.conf_simulador)
        plt.savefig('results/figuras/Fz_conf.png', dpi = 500)  
        
                    
class Fz_sim:
    
    ''' 
    Classe evoca métodos da classe Fz_Comfort para definir valores de conforto.
    Utiliza como input valores randomicos das 3 variáveis de entrada.
    '''    
    
    def Fuzificar(self,t=None,u=None,h=None,graf=0,imp_texto=0,lang=0): 
        np.random.seed(SEED)
        t = [t if t!=None else round(randint(0, 40)+random(),1)][0]   
        u = [u if u!=None else round(randint(0, 99)+random(),1)][0]    
        h = [h if h!=None else round(randint(0, 9)+random(),1)][0]            
                
        res = Fz_Comfort(humor = h, 
                          temp = t,
                          umidade = u,
                          graf = graf,
                          lang= lang,
                          ).conf_simulador.output['conforto']        
        if imp_texto == 1:
            print('Input:\n\tPercepção térmica:',t,
                  '| Percepção de umidade:',u,
                  '| Percepção estado de humor:',h,
                  '\n\tConforto atribuído:',res,'\n')     
                          
        return t,u,h,np.round(res,2)
        

# Área de testes        
# a=Fz_sim().Fuzificar(38,60,2,graf=1,imp_texto=1,lang=1)
# b=Fz_sim().Fuzificar(38,60,2,graf=0,imp_texto=1,lang=1)
# c=Fz_sim().Fuzificar()
# (t,u,h,omega) = Fz_sim().Fuzificar()

