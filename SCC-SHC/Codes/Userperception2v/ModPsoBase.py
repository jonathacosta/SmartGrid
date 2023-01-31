#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
PSO calculate module

'''
import ModPopulation
import numpy as np
import copy
import ModComfortFunctions

class PsoBase:
    
    def __init__(self, w, c1, c2,ComfortFunction=0,omega=0):
         self.w = w
         self.c1 = c1
         self.c2 = c2
         self.nOfIterations = 1000
         self.funcao_conforto = ComfortFunction
         self.omega = omega         


    def initPopulation(self, popLength,loads):
        '''
         Method starts the PSO particle population (popLength).
         Each particle is a solution for scheduling the contained charges
         in the loads list.

        '''
        
        self.popLength = popLength
        nSubjects = len(loads)
      
        for i in range(popLength):
            pop = []
            for n in range(nSubjects):
                nAcio = np.size(loads[n].bestTimeInSamples)
                
                carga = ModPopulation.Population()
                
                horario_min = loads[n].minTimeInSamples
                horario_max = loads[n].maxTimeInSamples
                duracao = loads[n].durationInSamples
                
                pot_min = loads[n].avgPower
                pot_max = loads[n].avgPower
                        
                t0 = horario_min      	              # Early load cycle start time
                t1 = horario_max - sum(duracao)       # Latest possible time for end of load cycle
                
                proib = []
                h = np.zeros((nAcio))
                
                for j in range(nAcio):
                    signal = True
                    while(signal):
                        h[j] = round(t0 + (t1 - t0)*np.random.rand())
                        
                        ind = np.nonzero(proib==h[j])
                        if np.size(ind) == 0:
                            signal = False
                            
                    proib = np.hstack((proib, np.linspace(h[j]-sum(duracao)+1,
                                 h[j]+sum(duracao)-1,
                                 int(2*sum(duracao)-1)),0))
                h = np.sort(h)
                                
                multFact = (pot_min + (pot_max-pot_min)*np.random.rand())
                
                carga.startTime = h - 1
                carga.opPower = np.round(multFact*100)/100
                carga.v1 = np.zeros((nAcio))
                carga.v2 = np.zeros((nAcio))
                
                pop = np.append(pop,carga)
                
            if i==0:
                population = pop
            else:
                population = np.vstack([population,pop])
        
        self.population = population
        
    def diw(self, wstart, u, it):
        '''
         Method defines technique for changing weight of inertia w.
         DIW - Dynamic Inertia Weight
        '''
        w = wstart*pow(u, -it)
        return w
    
    def executePsoBase(self, 
                       targetCost, loads, sampleInterval,
                       tariff, peakLimit, alpha):
         '''
         - Method performs the search for a PSO solution
                         
              -Receive:
                 
                  (targetCost, loads, sampleInterval, tariff, peakLimit, alpha, w_type)
                  Now with the initPopulation attributes made in the previous step,
                  in another module.
                  pso.initPopulation(len(self.Loads), self.Loads)

              - Calculates:
                 
                  - w according to input data about type of w
                  - Solution fitness with calcFitness
                  -
                 
              -Returns:
                 
                  self.gbestFit = gbestFit
                  self.rest = REST
                  self.cost = cost
         '''
         (self.fitness, COST, DISCOMF, dmax, rest, tv) = self.calcFitness(targetCost,
                                                                          self.population,
                                                                          loads, 
                                                                          sampleInterval,
                                                                          tariff, 
                                                                          peakLimit,
                                                                          alpha)
         Si = np.zeros((self.popLength))
    
         gbestFit = np.max(self.fitness)
         imin = np.nonzero(self.fitness == gbestFit)[0]
         self.gBest = self.population[imin][:]
         self.pBest = self.population
         pbestFit = self.fitness
         REST = rest[imin]
         cost=[]
         it,conv = 1,0
         
         #Laço até convergência
         while ((it <  self.nOfIterations  and conv != self.popLength) or (REST!=1).all()):
             '''
             Set weight initialization type and by DIW technique
             '''
             w = self.diw(0.3, 1.00002, it)
             for j in range(self.popLength):
                 #Comparação dos fitness com gbest e pbest
                 if self.fitness[j] > gbestFit:
                     self.gBest = copy.deepcopy([self.population[j][:]])
                     gbestFit = copy.deepcopy(self.fitness[j])
                     self.lastIt = it
                     cost = COST[j]
                     REST = rest[j]
                
                 if self.fitness[j] > pbestFit[j]:
                     self.pBest[j][:] = copy.deepcopy(self.population[j][:])
                     pbestFit[j] = copy.deepcopy(self.fitness[j])
                     Si[j]=1
                 else:
                     Si[j] = 0
                    
                     
                 r1= np.random.rand()
                 r2= np.random.rand()
                               
                 nLoads = np.size(loads)
                                  
                 for i in range(nLoads):
                     duration = loads[i].durationInSamples
                     #Atualização da v1 e startTime
                     self.population[j][i].v1 = (w*self.population[j][i].v1 + 
                                                 self.c1*r1*(self.pBest[j][i].startTime - self.population[j][i].startTime) +
                                                 self.c2*r2*(self.gBest[0][i].startTime - self.population[j][i].startTime)
                                                 )
                     
                     self.population[j][i].startTime = np.round(self.population[j][i].startTime 
                                                                + self.population[j][i].v1 
                                                                )
                     #Limitação de startTime                       
                     limitMaxV1 = loads[i].maxTimeInSamples - sum(duration)
                                             
                     limitIndexMinV1 = np.nonzero( self.population[j][i].startTime < loads[i].minTimeInSamples)
                     
                     for k in range(np.size(limitIndexMinV1)):
                        self.population[j][i].startTime[limitIndexMinV1[0][k]] =  np.array([loads[i].minTimeInSamples])
                     
                     limitIndexMaxV1 = np.nonzero( self.population[j][i].startTime > limitMaxV1 )
                     for k in range(np.size(limitIndexMaxV1)):
                         self.population[j][i].startTime[limitIndexMaxV1[0][k]] =  np.array([limitMaxV1])                        
                
                 #calcula fitness e atualiza variável
                 (self.fitness, COST, DISCOMF, dmax, rest, tv) = self.calcFitness(targetCost,
                                                                                  self.population, 
                                                                                  loads, sampleInterval, tariff, 
                                                                                  peakLimit, alpha)
       
             it = it+1 #incrementa it
             conv = np.shape(np.nonzero(np.round((self.fitness[0])*1000)==np.round(self.fitness*1000)))[1]
             
             if(conv>self.popLength/2 and (REST!=1).all()):
                 self.initPopulation(self.popLength, loads)
                 (self.fitness, COST, DISCOMF, dmax, rest, tv) = self.calcFitness(targetCost, self.population,
                                                                                  loads, sampleInterval, tariff,
                                                                                  peakLimit, alpha)
         
                 gbestFit = np.max(self.fitness)
                 imin = np.nonzero(self.fitness==gbestFit)[0]
                 self.gBest = self.population[imin][:]
                 self.pBest = self.population
                 pbestFit = self.fitness
                 REST = rest[imin]
            
         self.gbestFit = gbestFit
         self.rest = REST
         self.cost = cost
                  
    def calcFitness(self, targetCost, population, LOADS, Ts, C, peakLimit, alpha):
         '''
         - Method evaluates the fitness of the solution and returns:
              - Receive:
                 
                  calcFitness(targetCost, SOLUTION, Loads, sampleInterval, rate, peak_limits, alpha)
             
              - Calculates:
                 
                  - Cost of the solution in calcCost
                  - Solution comfort in calcConfort
              - Returns:
                 Apt, exec_cost, discomf, DMAX, f3, TIME_VALUE
         '''
        
         (sizePop, n_loads) = np.shape(population)
         n_samples = (24*60)/Ts

         TIME_VALUE = np.zeros((int(n_samples), int(sizePop))) 
         exec_cost = np.zeros((int(sizePop), 1))

         discomf = np.zeros((int(sizePop), 1))
         
         for a in range(sizePop):
             #----------- Calcula o valor da potência de pico pra cada amostra
             for load in range(n_loads):
                 startPosition = population[a][load].startTime
                 
                 nAcio = np.size(LOADS[load].bestTimeInSamples)
                 for s in range(nAcio):
                     aux=0
                     DURATION = np.sum(LOADS[load].durationInSamples)
                     for sample in range(int(DURATION)):
                         TIME_VALUE[int(startPosition[s]) + aux][a] = (TIME_VALUE[int(startPosition[s])+aux][a] + 
                                                                       LOADS[load].peakPowerInSamples[sample])
                         aux = aux+1
                        
             exec_cost[a] = self.calcCost(population[a][:], LOADS, Ts, C)
             
             '''Defines the mathematical model of the comfort function '''
             discomf[a], DMAX = self.calcConfort(population[a][:],LOADS)            
             
         # Comparison with peak limit         
         f3 = np.zeros((sizePop,1))
         for a in range(sizePop):
             exceed = np.nonzero(TIME_VALUE[:,a] > peakLimit[0])
             for e in exceed[0]:
                 f3[a] = f3[a] + (TIME_VALUE[e,a] - peakLimit[0][e])
         
         f1 =(targetCost- exec_cost)/targetCost
         f2 = (discomf/np.sum(DMAX))
         f2 = f2/3.5               
         f3 = 1/(1+f3)
      
         Apt = (alpha)*f1 + (1-alpha)*f2 + f3  
         
         return Apt, exec_cost, discomf, DMAX, f3, TIME_VALUE
    
    def calcConsumption(self, subject, LOADS, Ts):
         '''
         -Method calculates the consumption in kWh of activating the loads according to
            user-defined trigger time preferences.

              - Returns the execution consumption of the load in the profile established by the client.
         '''                  
         exec_consump = 0
         for load in range(len(LOADS)):             
             startPosition = subject[load].startTime
             aux=0
             nAcio = np.size(LOADS[load].bestTimeInSamples)
             for s in range(nAcio):
                 DURATION = np.sum(LOADS[load].durationInSamples);
                 finalPosition = startPosition[s] + (DURATION);
                 load_consumption = 0
                 
                 #n=startPosition[s]
                 for n in range(int(startPosition[s]),int(finalPosition)):
                     load_consumption = load_consumption + (LOADS[load].
                                              avgPowerInSamples[int(n-startPosition[s])]*
                                              (Ts/60))                 
                 aux += load_consumption               
             exec_consump += aux
         return exec_consump
             
    def calcCost(self, subject, LOADS, Ts, C):
          '''
          - Method calculates the cost of activating the loads according to
             user-defined trigger time preferences.
              
               - targetCost:
                   - Receive: calcCost(target, Loads, sampleInterval, rate)
                   - Assign: calcCost(subject, LOADS, Ts, C)
               - Returns the execution cost of the load in the profile established by the client.
          '''                  
          exec_cost = 0
          for load in range(len(LOADS)):             
              startPosition = subject[load].startTime
              aux=0
              nAcio = np.size(LOADS[load].bestTimeInSamples)
              for s in range(nAcio):
                  DURATION = np.sum(LOADS[load].durationInSamples)
                  finalPosition = startPosition[s] + (DURATION)
                  load_cost = 0
                  
                  #n=startPosition[s]
                  for n in range(int(startPosition[s]),int(finalPosition)):
                      load_cost = load_cost + (LOADS[load].
                                               avgPowerInSamples[int(n-startPosition[s])]*
                                               (Ts/60) * C[0][n])                 
                  aux += load_cost               
              exec_cost += aux
                                        
          return exec_cost         

    def calcConfort(self, pop, cargas):
        '''- Method points to the comfort function used by PSO to
          calculate comfort and fitness.
        '''
        
        F=ModComfortFunctions.ComfortFunctions()
                
        if self.funcao_conforto == 1:  
            comfort,DMAX = F.F1_comfort(pop,cargas)
        
        if self.funcao_conforto == 2:  
            comfort,DMAX = F.F2_comfort(pop,cargas,self.omega)

        if self.funcao_conforto == 3:  
            comfort,DMAX = F.F3_comfort(pop,cargas)

        if self.funcao_conforto == 4:  
            comfort,DMAX = F.F4_comfort(pop,cargas,self.omega)
                        
            
        return comfort, DMAX 


