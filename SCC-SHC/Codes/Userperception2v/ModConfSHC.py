#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCC configuration module for each house. 
Callback from Module main.
"""
import ModLoad,ModTariff,ModExecPSO

class SHC():
    '''
    Class performs consumption versus comfort analysis applying load scheduling 
    via PSO with Fuzzy comfort.
    '''
    def __init__(self,sample_interval=5, tar=0, alfa=0, lst_cargas=0, 
                 conf_func=0,user_var=None, graf=0, lang=0, casa = 0):
        '''
        Init method loads global variable:
             -'sample_interval=5'
             - tariffs
             - residential loads
             - load spikes
        '''       
        ''' Variables'''
        self.alfa = alfa             # Carries cost-comfort alpha
        self.exibe_graf = graf       # Show graphic
        self.lang = lang             # English= 1,Portugguese =0
        self.casa = casa             # Identify number of house for graphic
        self.iteracoes = 30	  	     # Define PSO total of iterations
        self.conf_func = conf_func   # Define a comfort function
        self.conf_alt = []		     # Stores linguistic fuzzy variables 
        self.tab_cargas = lst_cargas # Identify table of loads A,B or C        
        self.user_var = user_var
        
        '''Module 01: tariffs and peak consumption limit for non-schedulable loads'''
        if tar == 1: # set ToU tariff
            self.tarifa = ModTariff.Tariffs().Tariff_of_Use
        else:        # preset Constante tariff
            self.tarifa = ModTariff.Tariffs().tariff_constant

        '''Module 02: Filling objects by sampling with list of loads'''
        if self.tab_cargas == 1:
            if lang == 1: # English
                self.cargas = ModLoad.DadosReferencia().cargas_lista1_en
            else:         # Portugueses
                self.cargas = ModLoad.DadosReferencia().cargas_lista1
                
        elif self.tab_cargas == 2: 
            self.cargas = ModLoad.DadosReferencia().cargas_lista2
        
        elif self.tab_cargas == 3:      
            self.cargas = ModLoad.DadosReferencia().cargas_lista3        
        
        else:     
            self.cargas = ModLoad.DadosReferencia().cargas_lista4
            
        
        '''Module 03: Non-schedulable sampling peak load values'''
        self.pico_cargas = ModLoad.Peak_ref().pico_cargas_nao_agendaveis
        
        '''Module 04: Implementation of the PSO'''
        self.Process_PSO()  
           

    def Process_PSO(self):
        '''        
        Call method to execute the PSO applying parameters of the algorithm and methods on the loads so that:
             * alpha [0,1] = [economy,comfort]
             * f = αf1 +(1−α)f2
        For alpha = 0, the controller will obtain the best solution for the user's comfort levels according to alpha weight. For alpha = 1, the controller will only minimize the electricity consumption costs. So there will be comfort, as the loads will be activated, however this will not be a criterion considered by the SHC for choosing the schedules.
        
        The method instantiates the 'sun' object with the attributes of the ExecPSO class (inside the ModExecPSO module). Next, the method that searches for the best PSO solution using sol.PSO() is called, together with the graphical responses for the aforementioned alpha value.
        This is repeated for each new alpha value in the 'for' loop.
        '''
                                          
        sol = ModExecPSO.ExecPSO(alpha = self.alfa, 
                                 tarifa = self.tarifa,
                                 iteration=self.iteracoes,
                                 peak_limits= self.pico_cargas, 
                                 Loads = self.cargas,
                                 Funcao_conforto  = self.conf_func,
                                 user_var = self.user_var
                                 )
        sol.PSO() 
        
        if self.exibe_graf == 1:
            sol.GrafAgendCargas(casa = self.casa, conf = self.conf_func,
                                lang = self.lang, tab_cargas = self.tab_cargas)        
        self.casa_agend = sol.lst         
        
#******************************************************************************
# Test area
#******************************************************************************
# a=SHC()



