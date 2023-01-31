#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Method uses Fuzzy Logic to define a comfort value in 0 and 1.

"""

import skfuzzy as fuzz
import numpy as np   
from skfuzzy import control as ctrl
from random import randint,random
SEED=42


class Fz_Comfort:
    
    '''
    Class applies methods to build a comfort output between 0.1
    
     * Input: temperature and humidity user perception
    
     * Output: Load comfort level
        
    '''
    
    def __init__(self,temp,umidade,graf=0,lang=0):
        
        # Variáveis linguísticas
        self.temp_in = temp        
        self.umidade_in = umidade
        if lang==0:
        # Valores das variáveis linguísticas
            self.t = ['muito fria','fria','amena','quente','muito quente']        
            self.u = ['baixa','mediana','alta']
            self.c = ['baixo','médio','alto']
        else:    
            self.t = ['very cold','cold','mild','hot','very hot']        
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
        Method creates the input and output variables for the problem
         and assigns the mapping between the sharp and fuzzy values
         using the membership function
         * Humor : bad, good and great. Scale 0 to 10.
         * Temperature: cold, mild and hot. Scale 0 to 40.
         * Humidity : low, medium and high. Scale 30 to 65.
         * Comfort : low, medium and high. Scale 0 to 10.
        
         The effects of humidity on climate are felt in both temperatures and
         in the rainfall regime. Water, because of its specific heat, tends to conserve
         temperatures for a longer time, causing a smaller variation in them,
         i.e. the thermal amplitude (difference between the highest and lowest temperature)
         is smaller the higher the humidity in the air. Furthermore, in wetter regions
         or that are more affected by humidity, the rainfall regime tends to be higher,
         because the air saturation that causes condensation is more frequent.
        
         high humidity -> low temperature variation
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
                
                            
        #Saída e pertinencia
        self.conf = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'conforto')  
        self.conf[self.c[0]] = fuzz.trapmf(self.conf.universe, [0.0, 0.0, 0.2,  0.4])
        self.conf[self.c[1]] = fuzz.trapmf(self.conf.universe, [0.2, 0.4, 0.6,  0.8])
        self.conf[self.c[2]] = fuzz.trapmf(self.conf.universe, [0.6, 0.8, 1.0, 1.0])
                        
    def Rules(self):

       
        # *****************************************************************************************
        self.rule4 = ctrl.Rule(
            (self.temp[self.t[0]] | self.temp[self.t[1]])  |
            (self.temp[self.t[2]] & self.umidade[self.u[2]])
            ,self.conf[self.c[0]])
        
        self.rule5 = ctrl.Rule( 
            (
            (self.temp[self.t[2]] | self.temp[self.t[3]])  &
            (self.umidade[self.u[0]] |self.umidade[self.u[1]]) )
            ,self.conf[self.c[1]])
        
        self.rule6 = ctrl.Rule(
            # (self.humor[self.h[1]] & 
            (self.temp[self.t[4]]) |
            (self.temp[self.t[3]] & self.umidade[self.u[2]])
            ,self.conf[self.c[2]])
        
        
        # *****************************************************************************************
        self.conf_ctrl = ctrl.ControlSystem([
                                             # self.rule1, self.rule2, self.rule3,
                                              self.rule4,self.rule5,self.rule6,
                                              # self.rule7,self.rule8,self.rule9
                                              ])
        self.conf_simulador = ctrl.ControlSystemSimulation(self.conf_ctrl)    

    def Comput(self):
        
        self.conf_simulador.input['temperatura'] = self.temp_in
        self.conf_simulador.input['umidade'] = self.umidade_in
        # self.conf_simulador.input['humor'] = self.humor_in      # Chamada pela label
                
        self.conf_simulador.compute()
                
    def Grap_result(self):
        #Resultados
        import matplotlib.pyplot as plt
        
        self.temp.view(sim=self.conf_simulador)
        plt.savefig('results/figuras/Fz_temp.png', dpi = 500)
        # self.humor.view (sim=self.conf_simulador)
        # plt.savefig('results/figuras/Fz_humor.png', dpi = 500)        
        self.umidade.view(sim=self.conf_simulador)
        plt.savefig('results/figuras/Fz_umid.png', dpi = 500)
        self.conf.view(sim=self.conf_simulador)
        plt.savefig('results/figuras/Fz_conf.png', dpi = 500)  
        
                    
class Fz_sim:
    
    ''' 
    Class invokes methods of the Fz Comfort class to set comfort values.
    It uses as input random values of the 3 input variables.
    '''    
    
    def Fuzificar(self,t=None,u=None,h=None,graf=0,imp_texto=0,lang=0): 
        np.random.seed(SEED)
        t = [t if t!=None else round(randint(0, 40)+random(),1)][0]   
        u = [u if u!=None else round(randint(0, 99)+random(),1)][0]    

                
        res = Fz_Comfort( temp = t,
                          umidade = u,
                          graf = graf,
                          lang= lang,
                          ).conf_simulador.output['conforto']        
        if imp_texto == 1:
            print('Input:\n\tThermal perception:',t,
                  '| Humidity perception:',u,
                  # '| Percepção estado de humor:',h,
                  '\n\t Assigned comfort:',res,'\n')     
                          
        return t,u,np.round(res,2)
        
# ******************************************
# Area of tests
# ******************************************
# a=Fz_sim().Fuzificar(38,60,graf=1,imp_texto=1,lang=1)
# b=Fz_sim().Fuzificar(38,60,graf=0,imp_texto=1,lang=1)
# Fz_sim().Fuzificar()

