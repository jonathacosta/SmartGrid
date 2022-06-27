#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Modelagem do PSO para acionamento de cargas

Classe ExecPSO:
    - Aplica parâmetros inicias ao PSO
    
    - Executa PSO em PsoBase(self.w, self.c1, self.c2)
    
        - Inicializa variáveis do PSO
        
        - Calcula custo do cenário preferencial do usuário (cenário escolhido pelo usuário)
        
        - Aplica o PSO em laço de self.time 

'''

import time
import numpy as np
import ModPsoBase
import matplotlib.pyplot as plt

   
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


class ExecPSO:
    '''  
    Classe cria objetos para execução do PSO aplicando às m-ésima cargas.
        
    * Recebe os parâmetros de base para análise
        self.alpha = alpha   
        self.tarifa = tarifa                
        self.Loads = Loads
        self.peak_limit = peak_limits    
        
    * Aplica parâmetros iniciais ao PSO se não declarados :
        self.w = 0.4        
        self.c1 = 2
        self.c2 = 2        
        self.funcao_conf = 1        
        self.iteration = 10000       
        self.sampleInterval = 5        
                
    '''    
    
    def __init__(self,c1=2,c2=2,
                 alpha=0,iteration=10000,
                 tarifa=None, peak_limits=None,
                 sampleInterval=5, Loads:list=[],
                 funcao_conf=1):
        self.w = 'diw'
        self.c1 = c1
        self.c2 = c2
        self.alpha = alpha
        self.iteration = iteration
        self.tarifa = tarifa
        self.peak_limits = peak_limits
        self.sampleInterval = sampleInterval
        self.Loads = Loads
        self.funcao_conf = funcao_conf       
        
    def PSO(self):
        '''
        Método aplica as configurações iniciais de cargas e conforto ao PSO.
        
        - Inicializa objeto PSO com atributos da classe PSOBase
        
        - Calcula custo do cenário preferencial do usuário (cenário escolhido pelo usuário)
        
            - Aplica o PSO em laço de n-times 
        
        '''       
      
        Custo = np.zeros((self.iteration))      # Custo
        Conforto = np.zeros((self.iteration))   # Conforto
        tempo = np.zeros((self.iteration))      # Tempo
        gbest = np.zeros((self.iteration))      # Posição global
        
        
        #Instancia o objeto pso com classe PsoBase(w,c1,c2)        
        pso = ModPsoBase.PsoBase(self.w, self.c1, self.c2)       
        '''
        População inicial
        Carrega valores iniciais para todas as 'l' cargas 
            - Carrega tempo inicial das 'l' cargas com melhor time de amostragem
            - Guarda na lista 'target' os atributos de cada uma das cargas com valores de 
            preferencia do usuário.
            - Calcula o custo total de execução das cargas conforme preferência do 
            usuário, sem identificar as cargas, e armazena em targetCost.
            - targetCost será utilizado para calcular o calcCost e calcFitness.
             é o resultado do somatório de (potência_nominal) x (intervalo de tempo em amostragem). 
        '''
        target = []
        for l in (self.Loads):
            tg = Population()
            tg.startTime = l.bestTimeInSamples 
            target = np.append(target,tg)
        targetCost = pso.calcCost(target, self.Loads, self.sampleInterval, self.tarifa)
        targetConsumption = pso.calcConsumption(target, self.Loads, self.sampleInterval)
        
        #Loop com nTimes execuções
        for k in range(self.iteration):
            ''' Busca a melhor solução em "self.Solucao" e melhor posição e self.best '''
            start_time = time.time()
        
            ''' Inicializa população com atributos das cargas '''
            pso.initPopulation(len(self.Loads), self.Loads)
            # pso.initPopulation(10, self.Loads)
              
            ''' Busca a solução em solution utilizando a técnica de DIW para peso'''
            pso.executePsoBase(targetCost, self.Loads, self.sampleInterval, self.tarifa, 
                               self.peak_limits, self.alpha, self.funcao_conf)
            Solucao = pso.gBest
            
            # Parâmetros da iteração 'n'
            tempo[k] = (time.time() - start_time)
            ''' Apt, exec_cost, discomf, DMAX, f3, TIME_VALUE '''
            fitn, Custo[k], desconforto,T,U, timeValue_solution = pso.calcFitness(targetCost, Solucao, self.Loads, 
                                                                             self.sampleInterval, self.tarifa, 
                                                                             self.peak_limits, self.alpha,
                                                                             self.funcao_conf)
            Conforto[k] =  desconforto/sum(T)
            gbest[k] = fitn
        
        self.melhores = gbest
        self.best = np.max(gbest)            
        self.Solucao = Solucao
        
        
       
        self.lst = [f'{np.min(gbest):.3}',
                    f'{np.mean(gbest):.3}',
                    f'{np.max(gbest):.3}',
                    f'{np.std(gbest):.2}',
                    f'{(targetConsumption):.3}',
                    f'{np.mean(Custo):.3}',
                    f'{(targetCost):.3}',
                    f'{(targetCost - np.mean(Custo))/targetCost:.2%}',
                    f'{np.mean(Conforto):.2%}',f'{np.mean(tempo):.3}'                        
                    ]
              
    def GrafAgendCargas(self):
        '''
        Método exibe o gráfico de distribuição das cargas em 24h, conforme
        threshold conforto x consumo.
        Solução final para a tarifa e horários apresentados.
        '''
        # Faixa de amostragem diária
        amostragem_diaria = int(24*60 / self.sampleInterval) 
        # Faixa de gráfico
        xmin, xmax = 0, amostragem_diaria
        X = np.arange(0, amostragem_diaria)
        xlabel = 'Tempo [h]'
        ylabel = 'Consumo diário [kWh]' 
        # Marcadores de eixo 'x'. Posição e valor horário
        xticks1 = (np.arange(1,25)*amostragem_diaria/24)
        xticks2 = list(map(str,np.arange(1,25,1)))
        # Nomes e cores das cargas
        lab = [str(self.Loads[i].name) for i in range(len(self.Loads))]
        color = ['coral','blue','aqua', 'bisque','sienna','lime','yellow','turquoise','red','violet']        
        '''Mapa de cores disponível no endereço: https://matplotlib.org/2.0.2/examples/color/named_colors.html '''
        
        # Figura
        fig = plt.figure()        
        fig, ax = plt.subplots(figsize=(8,4),dpi=150)
        plt.axis([xmin,xmax,0,10])
        plt.grid(False)
        plt.plot(X,self.peak_limits[0][:],'-r',3)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(xticks1, xticks2 )      
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
            ax.stackplot(X,valor_tempo_aux, colors=color[a],alpha=0.7)
            valor_tempo_aux = np.zeros(amostragem_diaria)  

        # Título, perfil da tarifa e legenda
        tar = self.tarifa.mean() - self.tarifa[0][0]
        a=['Tarifa Constante' if tar < 0.1 else 'Tarifa Branca (ToU)']
        plt.title(f'Agendamento de cargas.\n{a[0]}, w={self.w} e alfa = {self.alpha}',fontsize=11)
        plt.plot(X,self.tarifa[0], 'grey',label=f'{a[0]}')
        plt.legend(loc='upper left')
        # fig.savefig('PerfilOtimizado.pdf')
            
#%% Área de test

def test():
    a=ExecPSO()
    a.GrafAgendCargas()

if __name__ == '__main__':
    # test()
    pass