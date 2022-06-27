#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Módulo de cáculo do PSO

'''
import numpy as np
import copy
# import random as rd
# rd.seed(1)

class Population:
    '''
    Classe instancia objeto para de interesse à solução do SHC.    
    '''   
    def __init__(self):
        self.startTime = np.array([])
        self.opPower = np.array([])
        self.v1 = np.array([])
        self.v2 = np.array([])
        self.v3 = np.array([])


class PsoBase:
    
    def __init__(self, w, c1, c2, w_type=0):
         self.w = w
         self.c1 = c1
         self.c2 = c2
         self.w_type = w_type
         self.nOfIterations = 10000

    def initPopulation(self, popLength,loads):
        '''
        Método inicia a população de partículas do PSO (popLength).
        Cada partícula é uma solução para o agendamento das cargas contidas
        na lista loads.

        '''
        self.popLength = popLength
        nSubjects = len(loads)
      
        for i in range(popLength):
            pop = []
            for n in range(nSubjects):
                nAcio = np.size(loads[n].bestTimeInSamples)
                
                carga = Population()
                
                horario_min = loads[n].minTimeInSamples
                horario_max = loads[n].maxTimeInSamples
                duracao = loads[n].durationInSamples
                
                pot_min = loads[n].avgPower
                pot_max = loads[n].avgPower
                        
                t0 = horario_min      	              # Horário mais cedo de início de ciclo da carga
                t1 = horario_max - sum(duracao)        # Horário mais tarde possível para termino do ciclo da carga
                
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
        Método define técnica para mudança de peso de inércia w.
        DIW - Dynamic Inertia Weight
        '''
        w = wstart*pow(u, -it)
        return w
    
    def executePsoBase(self, targetCost, loads, sampleInterval, tariff, peakLimit, alpha, funcao_conf):
         '''
         - Método executa a busca de uma solução PSO
                         
             -Recebe:
                 
                 (targetCost, loads, sampleInterval, tariff, peakLimit, alpha,w_type)
                 Já com os atributos do initPopulation feito em etapa anterior, 
                 noutro modulo.
                 pso.initPopulation(10, self.Loads)

             - Calcula:
                 
                 - w conforme dado de entrada sobre tipo de w
                 - Aptidão da solução com calcFitness
                 - 
                 
             -Retorna:
                 
                 self.gbestFit = gbestFit
                 self.rest = REST
                 self.cost = cost
                 
         '''
         (self.fitness, COST, DISCOMF, dmax, rest, tv) = self.calcFitness(targetCost, self.population, loads, 
                                                                          sampleInterval, tariff, peakLimit, alpha,
                                                                          funcao_conf)
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
         while ((it <  self.nOfIterations  and conv!=self.popLength) or (REST!=1).all()):
             '''
             Define o tipo de inicialização do peso w pela técnica DIW
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
                 (self.fitness, COST, DISCOMF, dmax, rest, tv) = self.calcFitness(targetCost, self.population, 
                                                                                  loads, sampleInterval, tariff, 
                                                                                  peakLimit, alpha,funcao_conf)
       
             it = it+1 #incrementa it
             conv = np.shape(np.nonzero(np.round((self.fitness[0])*1000)==np.round(self.fitness*1000)))[1]
             
             if(conv>self.popLength/2 and (REST!=1).all()):
                 self.initPopulation(self.popLength, loads)
                 (self.fitness, COST, DISCOMF, dmax, rest, tv) = self.calcFitness(targetCost, self.population,
                                                                                  loads, sampleInterval, tariff,
                                                                                  peakLimit, alpha, funcao_conf)
         
                 gbestFit = np.max(self.fitness)
                 imin = np.nonzero(self.fitness==gbestFit)[0]
                 self.gBest = self.population[imin][:]
                 self.pBest = self.population
                 pbestFit = self.fitness
                 REST = rest[imin]
                 
         self.gbestFit = gbestFit
         self.rest = REST
         self.cost = cost
                  
    def calcFitness(self, targetCost, population, LOADS, Ts, C, peakLimit, alpha, funcao_conf):
         '''
         - Método avalia a aptidão da solução e retorna:
             - Recebe: 
                 
                 calcFitness(targetCost, SOLUTION, Loads, sampleInterval,tarifa, peak_limits, alpha)
             
             - Calcula:
                 
                 - Custo da solução em calcCost
                 - Conforto da solução em calcConfort
             - Retorna:
                 
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
             
             '''Escolha do modelo matemático da função de conforto '''
             if funcao_conf == 1: 
                 (discomf[a], DMAX) = self.calcConfort(population[a][:],LOADS)
             else:
                 (discomf[a], DMAX) = self.calcConfortTaguchi(population[a][:],LOADS)
   
         #Comparação com o pico limite
         f3 = np.zeros((sizePop,1))
         for a in range(sizePop):
             exceed = np.nonzero(TIME_VALUE[:,a] > peakLimit[0])
             for e in exceed[0]:
                 f3[a] = f3[a] + (TIME_VALUE[e,a] - peakLimit[0][e])
         
         f1 =(targetCost- exec_cost)/targetCost
         f2 = (discomf/np.sum(DMAX))
         f2 = f2/3.5               # Por que 3.5 no código original?
         f3 = 1/(1+f3)
      
         Apt = (alpha)*f1 + (1-alpha)*f2 + f3  

         return Apt, exec_cost, discomf, DMAX, f3, TIME_VALUE
    
    def calcConsumption(self, subject, LOADS, Ts):
         '''
         - Método calcula o consumo em kWh de acionamento das cargas conforme 
           preferências de horário de acionamento definidas pelo usuário.

             - Retorna o consumo de execução da carga no perfil estabelecido pelo cliente.
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
          - Método calcula o custo de acionamento das cargas conforme 
            preferências de horário de acionamento definidas pelo usuário.
              
              - targetCost:
                  - Recebe:  calcCost(target, Loads, sampleInterval, tarifa)             
                  - Atribui: calcCost(subject, LOADS, Ts, C)
              - Retorna o custo de execução da carga no perfil estabelecido pelo cliente.
          '''                  
          exec_cost = 0
          for load in range(len(LOADS)):             
              startPosition = subject[load].startTime
              aux=0
              nAcio = np.size(LOADS[load].bestTimeInSamples)
              for s in range(nAcio):
                  DURATION = np.sum(LOADS[load].durationInSamples);
                  finalPosition = startPosition[s] + (DURATION);
                  load_cost = 0
                  
                  #n=startPosition[s]
                  for n in range(int(startPosition[s]),int(finalPosition)):
                      load_cost = load_cost + (LOADS[load].
                                               avgPowerInSamples[int(n-startPosition[s])]*
                                               (Ts/60) * C[0][n])                 
                  aux += load_cost               
              exec_cost += aux
          return exec_cost 
        
     
    def calcConfort(self, population, LOADS):
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
  