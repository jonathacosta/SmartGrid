#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 15:18:36 2022

@author: jrc
"""

import numpy as np

class ComfortFunctions:        
    

    def F1_comfort(self, population, LOADS):
         '''
         - Método calcula o conforto da solução conforme modelo proposto 
           por Santos,2019 e Albuquerquer,2018, em que:
             
             - Distância Dmax_m:
                 
                 Maior distância entre o melhor horário
                 selecionado pelo usuário(IBm) e os limites inicial e final do acionamento 
                 (ISm), (IEm), para uma dada carga m.
             
                 - Dmax_m = max(|I_Sm−I_Bm|, |I_Em−I_Bm|)
             
             - Desconforto é função de:
                 
                 Diferença entre o instante agendado pelo SHC(I_cm) e o instante escolhido 
                 pelo usuário(I_bm), multiplicado por C_lm, que é o nível de conforto atribuído 
                 a uma dada carga m.
                 
                 - C_lm : nível de conforto da carga
                 - I_Bm: melhor instante escolhido pelo usuário 
                 - I_Cm : Hora de início agendada para m-ésima carga pelo SHC
                 
                 - f_{DISC_m} = C_lm x | I_Cm - I_Bm |
            
            - Conforto total:
                - f2 = [ soma_m { Dmax_m  - f_DISC_m)} / soma_m(Dmax_m)
                        
            - Retorna:
                - Somatório de desconforto (f_DISC) em comfort
                - Somatório de distâncias máximas: DMAX                        
         '''
       
         DMAX = np.zeros(len(LOADS))   # Distância preset e usuário e do SHC
         comfort = 0
         
         for i in range(len(LOADS)):
             discomf_i = 0             # Disconforto da i-ésima carga
                   
             Dmax = np.maximum(
                 np.abs(LOADS[i].minTimeInSamples -
                        LOADS[i].bestTimeInSamples
                        ),
                 np.abs(LOADS[i].maxTimeInSamples -
                        LOADS[i].bestTimeInSamples
                        ))
             discomf_i = Dmax - (LOADS[i].comfortLevel* 
                            np.abs(population[i].startTime-
                                   LOADS[i].bestTimeInSamples))
             
             comfort += np.sum(discomf_i)
             
             DMAX[i] = np.sum(Dmax)
         
                    
         return comfort, DMAX
  
    
    def F2_comfort(self, population, LOADS, omega):
        
         '''
         - Método fuzifica o nível de relevância de conforto conforto das cargas
         '''         
                  
         for i in (LOADS):              # Altera o valor de relevância da carga                      
                 if i.comfortLevel > 0.7:                
                     i.comfortLevel = omega  
                                 
         comfort, DMAX = self.F1_comfort(population, LOADS)                                   
         
         
         return comfort, DMAX
     
    
    def F3_comfort(self, population, LOADS):
        
        '''
            Método calcula o conforto utilizando (Taguchi Loss Function) de
            'Residential power scheduling for demand response in smart grid'
            Ma,et Al, 2016
            
        '''
        
        DMAX = np.zeros(len(LOADS))
        confort = 0
        
        for i in range(len(LOADS)):
            conf = 0    
            Dmax = np.maximum(pow(LOADS[i].minTimeInSamples - LOADS[i].bestTimeInSamples,2), 
                              pow(LOADS[i].maxTimeInSamples - LOADS[i].bestTimeInSamples,2))
          
            conf = Dmax - LOADS[i].comfortLevel * pow( population[i].startTime - LOADS[i].bestTimeInSamples ,2)
    
            confort += np.sum(conf)
            DMAX[i] = np.sum(Dmax)
      
        return confort, DMAX      
  

    def F4_comfort(self, population, LOADS, omega):
      
       '''
       - Método fuzifica o nível de relevância de conforto conforto das cargas
       '''         
                
       for i in (LOADS):              # Altera o valor de relevância da carga                      
               if i.comfortLevel > 0.7:                
                   i.comfortLevel = omega  
                               
       comfort, DMAX = self.F3_comfort(population, LOADS)  
       return comfort, DMAX
