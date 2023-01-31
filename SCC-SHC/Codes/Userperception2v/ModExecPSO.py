#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
PSO modeling for load activation

ExecPSO Class:
     - Apply initial parameters to the PSO
    
     - Run PSO on PsoBase(self.w, self.c1, self.c2)
    
         - Initialize PSO variables
        
         - Calculates the cost of the user's preferred scenario (scenario chosen by the user)
        
         - Apply PSO in self.time loop

'''
import ModConfFz  
import numpy as np
import matplotlib.pyplot as plt
import time,ModPsoBase,ModPopulation
 

class ExecPSO:
    '''  
   Class creates objects for PSO execution applying to the mth loads.
        
     * Receives the base parameters for analysis
         self.alpha = alpha
         self.tarifa = fare
         self.Loads = Loads
         self.peak_limit = peak_limits
        
     * Applies initial parameters to PSO if not declared:
         self.w = 0.4
         self.c1 = 2
         self.c2 = 2
         self.iteration = 10000
         self.sampleInterval = 5     
                
    '''    
    
    def __init__(self,c1=2,c2=2,
                 alpha=0,iteration=1000,
                 tarifa=0, peak_limits=None,
                 sampleInterval=5, Loads:list=[],
                 Funcao_conforto=None,
                 user_var=None ):
        self.w = 'diw'
        self.c1 = c1
        self.c2 = c2
        self.alpha = alpha
        self.iteration = iteration
        self.tarifa = tarifa
        self.peak_limits = peak_limits
        self.sampleInterval = sampleInterval
        self.Loads = Loads        
        self.ComfortFunction = Funcao_conforto        
        self.dados_fz = ModConfFz.Fz_sim().Fuzificar(user_var[0],user_var[1])  # Gera valores t,u,w            
        # print(user_var)
    
    def PSO(self):
        '''
        Method applies the initial loads and comfort settings to the PSO.
        
         - Initialize PSO object with PSOBase class attributes
        
         - Calculates the cost of the user's preferred scenario (scenario chosen by the user)
        
             - Apply PSO in n-times loop
        '''       
      
        Custo = np.zeros((self.iteration))      # Vetor de custo das 'n' iterações
        Conforto = np.zeros((self.iteration))   # Vetor de iteraçõesConforto das 'n' 
        tempo = np.zeros((self.iteration))      # Vetor de tempo das 'n' iterações 
        gbest = np.zeros((self.iteration))      # Vetor de Posição global das 'n' iterações
        
    
        #Instancia o objeto pso com classe PsoBase(w,c1,c2)        
        omega = self.dados_fz[-1]
        pso = ModPsoBase.PsoBase(self.w, self.c1, self.c2,self.ComfortFunction,omega)       
        '''
        initial population
         Load initial values for all 'l' loads
             - Load initial time of 'l' loads with better sampling time
             - Stores in the 'target' list the attributes of each load with values of
             user preference.
             - Calculates the total cost of carrying out the loads according to the preference of the
             user, without identifying the loads, and stores it in targetCost.
             - targetCost will be used to calculate calcCost and calcFitness.
              is the result of the sum of (nominal_power) x (sampling time interval).
        '''
        target = []
        for l in (self.Loads):
            tg = ModPopulation.Population()
            tg.startTime = l.bestTimeInSamples 
            target = np.append(target,tg)
        targetCost = pso.calcCost(target, self.Loads, self.sampleInterval, self.tarifa)
        targetConsumption = pso.calcConsumption(target, self.Loads, self.sampleInterval)
        
        #Loop com nTimes execuções
        for k in range(self.iteration):
            ''' Search for the best solution in "self.Solucao" and best position and self.best ''' 
            start_time = time.time()
        
            ''' Initialize population with load attributes '''
            pso.initPopulation(len(self.Loads), self.Loads)
            # pso.initPopulation(10, self.Loads)
              
            ''' Search the solution in solution using the DIW technique for weight'''
            pso.executePsoBase(targetCost, self.Loads, self.sampleInterval, self.tarifa, 
                               self.peak_limits, self.alpha)
            Solucao = pso.gBest
            
            # Parâmetros da iteração 'n'
            tempo[k] = (time.time() - start_time)
            ''' Apt, exec_cost, discomf, DMAX, f3, TIME_VALUE '''            
            
            
            fitn, Custo[k], desconforto,T,U, timeValue_solution = pso.calcFitness(targetCost, Solucao, self.Loads, 
                                                                             self.sampleInterval, self.tarifa, 
                                                                             self.peak_limits, self.alpha,
                                                                             )
            
            Conforto[k] =  desconforto/sum(T)
            gbest[k] = fitn[0]   
            
        # print(Custo) # Verification
        self.melhores = gbest
        self.best = np.max(gbest)            
        self.Solucao = Solucao               
                
        self.lst = [f'{np.min(gbest):.3}',
                    f'{np.mean(gbest):.3}',
                    f'{np.max(gbest):.3}',
                    f'{np.std(gbest):.2}',
                    f'{(targetConsumption):.3}',
                    f'{np.min(Custo):.3}',
                    f'{np.mean(Custo):.4}',
                    f'{np.max(Custo):.4}',
                    f'{(targetCost):.4}',
                    f'{np.min(Conforto):.5}',
                    f'{np.mean(Conforto):.5}',
                    f'{np.max(Conforto):.5}',                                        
                    f'{np.mean(tempo):.3}',
                    f'{self.dados_fz[0]}',  # temperature     
                    f'{self.dados_fz[1]}',  # humidity
                    f'{self.dados_fz[2]}',  # omega
                    ]
        
    
        # self.Loads[-2].summary()  Verify comfort level for AF2 load.

      
              
    def GrafAgendCargas(self,casa = None,conf = None, tab_cargas = None, lang=None):
        '''
        Method displays the load distribution graph in 24 hours, as
         tradoff comfort x consumption.
         Final solution for the fare and times shown.
        '''
        
        if conf == 1:
            tag_conf = 'fuzzy'
        else:
            tag_conf = 'no-fuzzy'
        tabela_cargas = ['Padrão A' if tab_cargas==1 else 'Padrão B' if tab_cargas==2 else 'Padrão C']         
       
        
        # Faixa de amostragem diária
        amostragem_diaria = int(24*60 / self.sampleInterval) 
        # Faixa de gráfico
        xmin, xmax = 0, amostragem_diaria
        X = np.arange(0, amostragem_diaria)
        
        if lang==1:
             xlabel = 'Time[h]'
             ylabel = 'Demand [kW]'  
             tabela_cargas = ['Standard A' if tab_cargas==1 else 'Standard B' if tab_cargas==2 else 'Standard C']         

             
        else:             
            xlabel = 'Tempo [h]'
            ylabel = 'Demanda diária [kW]' 
            tabela_cargas = ['Padrão A' if tab_cargas==1 else 'Padrão B' if tab_cargas==2 else 'Padrão C']         
       
            
        # 'x' axis markers. Position and time value
        xticks1 = (np.arange(1,25)*amostragem_diaria/24)
        xticks2 = list(map(str,np.arange(1,len(xticks1)+1,1)))
 
        
        # Load names and colors
        lab = [str(self.Loads[i].name) for i in range(len(self.Loads))]
        color= ['r', 'g', 'b', 'y',
                'c', 'm', 'w','k',
                'gray','g']
    
        '''Mapa de cores disponível no endereço: https://matplotlib.org/2.0.2/examples/color/named_colors.html '''
        

        
        # Figura
        fig = plt.figure()        
        fig, ax = plt.subplots(figsize=(8,4),dpi=150)
        plt.axis([xmin,xmax,0,10])
        plt.grid(False)
        plt.plot(X,self.peak_limits[0][:],'-r',3)
        plt.xlabel(xlabel,fontsize= 9)
        plt.ylabel(ylabel,fontsize= 9)
        plt.xticks(xticks1, xticks2)      
        plt.style.use('ggplot') 
        plt.grid(True)
        #------------------------------------------------------------------
        
        valor_tempo = np.zeros(amostragem_diaria) 
        valor_tempo_aux = np.zeros(amostragem_diaria)  
          
        sol = (self.Solucao[0])       
        for a in range(len(sol)):
            startPosition = sol[a].startTime
            nAcio = np.size(self.Loads[a].bestTimeInSamples)
            for s in range(nAcio):
                aux=0
                duracao = np.sum(self.Loads[a].durationInSamples)
                for sample in range(int(duracao)):
                    valor_tempo[int(startPosition[s]) + aux] = valor_tempo[int(startPosition[s])+aux] + self.Loads[a].peakPowerInSamples[sample]
                    valor_tempo_aux[int(startPosition[s]) + aux] = valor_tempo[int(startPosition[s]) + aux]
                    aux = aux+1
            plt.plot(X,valor_tempo_aux, color[a],label=lab[a])
            ax.stackplot(X,valor_tempo_aux, colors=color[a],
                         alpha=0.7)
            valor_tempo_aux = np.zeros(amostragem_diaria)  

        tar = self.tarifa.mean() - self.tarifa[0][0]


        if lang==1:         
             a=['CT' if tar < 0.1 else 'ToU Tariff']
             plt.title(f'Schedule of loads - House {casa}:\n Table of loads {tabela_cargas[0]}, {a[0]}, Comfort {tag_conf} and alpha = {self.alpha}',fontsize= 11)      
             plt.plot(X,self.tarifa[0], 'grey',label=f'{a[0]}')
             plt.legend(loc='upper left')
             
        else:

        # Title, tariff profile and caption
            tar = self.tarifa.mean() - self.tarifa[0][0]
            a=['Tarifa Convencional' if tar < 0.1 else 'Tarifa Branca (ToU)']
            plt.title(f'Agendamento de cargas - Casa {casa}:\n Tabela de cargas {tabela_cargas[0]}, {a[0]}, Conforto {tag_conf} e alfa = {self.alpha}',fontsize=11)
            plt.plot(X,self.tarifa[0], 'grey',label=f'{a[0]}')
            plt.legend(loc='upper left')
        
            
# =============================================================================
# Área of test
# =============================================================================

