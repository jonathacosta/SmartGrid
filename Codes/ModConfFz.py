#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Método utiliza Lógica Fuzzy para definir um valor de conforto em 0 e 1.
Pesquisa: https://www.youtube.com/watch?v=LF8A8EGk-4c
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from random import randint,random

class Fz_Comfort():
    
    '''
    Classe aplica métodos para construir uma saída de conforto entre 0,1
    
    * Entrada:  Estado de humor, temperatura e humidade
    
    * Saída: Nível de conforto da carga
        
    '''
    
    def __init__(self,humor,temp,umidade,graf=0):
        
        # Variáveis linguísticas
        self.temp_in = temp
        self.humor_in = humor
        self.umidade_in = umidade
        
        # Valores das variáveis linguísticas
        self.t = ['muito fria','fria','amena','quente','muito quente']        
        self.h = ['mau','neutro','bom']        
        self.u = ['baixa','mediana','alta']
        self.c = ['baixo','médio','alto']
        # Função de início da classe        
        self.Vars_Pert()
        self.Rules()        
        self.Comput()
        if graf==1:
            self.Grap_result() 
        else:
            None
        
               
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
        self.temp.view(sim=self.conf_simulador,)
        self.humor.view (sim=self.conf_simulador)        
        self.umidade.view(sim=self.conf_simulador)
        self.conf.view(sim=self.conf_simulador)
        pass

class Fz_sim(Fz_Comfort):
    
    ''' 
    Classe evoca métodos da classe Fz_Comfort para definir valores de conforto.
    Utiliza como input valores randomicos das 3 variáveis de entrada.
    '''
    def __init__(self, 
                 temp = round(randint(0, 40)+random(),1),
                 umid = round(randint(0, 101),1),
                 humor = round(randint(0, 9)+random(),1)
                 ):
        self.h = humor  
        self.t = temp
        self.u = umid
        
    def Fuzificar(self,graf=0,imprimir=0):
        
        res = Fz_Comfort(self.h,self.t,self.u,graf).conf_simulador.output['conforto']
        # res=1
        if imprimir == 1:
            print('Input:\n\tPercepção térmica:',self.t,'| Percepção de umidade:',self.u,'| Percepção estado de humor:',self.h,
                  '\n\tConforto atribuído:',res,'\n')     
        else:
            None
        return res
        
#%% =============================================================================
# Área de test
# =============================================================================

def val(): 
        temp = round(randint(0, 40)+random(),1)
        umid = round(randint(0, 101),1)
        humor = round(randint(0, 9)+random(),1)
        return temp,umid,humor

def simulador(graf_out=0):
    L=[[20,40,9],[25,45,5],[38,60,2]]
    L=[[38,65,2]]
    for i in L:
        [a,b,c] = i
        Fz_sim(a,b,c).Fuzificar(graf_out,1)

if __name__ == "__main__":
    simulador(1)
    pass
