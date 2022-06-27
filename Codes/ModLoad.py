# -*- coding: utf-8 -*-
'''
Modelagem de cargas

Classe principal - classe basilar para modelagem de cargas residenciais.

    sub-classe 1 - cargas de acionamento flexível

    sub-classe 2 - cargas de potência flexível
    
'''

import numpy as np

class DadosReferencia():
    '''
    * Classe contém parâmetros de referência para simulação de cenários diversos.
    
      * Método init carrega atributos de do método Load.
     
      * Método CargasCenarioPU - carrega cargas de referência para análise.
      
      * Utiliza amostragem de 5min, self.sample_interval =5 
    
    '''
    
    def __init__(self):
        ''' Carrega os objetos da cargas do cenário de referência em L.
        
        '''
        self.CargasCenarioPU()
        self.CargasCenario2()
        self.CargasCenario3()

    
    def CargasCenarioPU(self):    
        '''
        - Cargas de referência do cenário PU
        
        - Execute cargas[i].summary() para exibir detalhes da carga, 
          i:int contido no intervalo [0,9]
            
        Return:
        ------- 
            cargas = [  l1, l2, l3, l4, l5, l6, l7, l8, l9, l10  ]            
        
        '''
        
        l1 = Loads('Bomba booster', 1, 7, 17, [8,16], [20], True, [2], [3], 0.1)
        l2 = Loads('Bomba piscina', 1, 7, 17, [8], [120], False, [0.75], [1.5], 0.1)             
        l3 = Loads('maquina de lavar', 8, 7, 17, [8], [10, 10, 5, 10, 5, 5, 5, 10], False, [0.13,0.51,0.3,0.26,0.15,0.15,0.15,0.22], [0.7,0.51,0.3,0.26,0.15,0.15,0.15,0.3], 0.5)
        l4 = Loads('lâmpadas externas', 1, 17, 24, [18], [270], False, [0.3], [0.3], 0.3);
        l5 = Loads('lâmpadas internas', 1, 17, 23, [18], [270], False, [0.15],[0.3], 0.7);
        l6 = Loads('AC office', 14, 15, 24, [16,20], [10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], True, [1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3], [1.7,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3], 1);
        l7 = Loads('AC couples', 7, 17, 24, [20], [30, 20, 5, 5, 5, 5, 5], False, [2,2,2,2,2,2,2], [2.1,2.1,2.1,2.1,2,2,2], 1);
        l8 = Loads('AC F1', 1, 17, 24, [20], [240], False, [1.1], [1.2], 1);
        l9 = Loads('AC F2', 7, 17, 24, [20], [10, 10, 5, 5, 5, 5, 5], False, [0.9,0.9,0.9,0.9,0.9,0.9,0.9], [1.1,1.1,1.1,1.1,1.1,1.1,1.1], 1);
        l10 = Loads('lava-louças', 5, 18, 22, [21], [5, 10, 15, 5, 10], False, [0.033,1.76,0.033,1.76,0.033], [0.033,1.76,0.033,1.76,0.033], 0.3);
            
        self.cargas_lista1 = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10]  
                         
    def CargasCenario2(self):    
        '''
        - Cargas de referência do cenário PU
        
        - Execute cargas[i].summary() para exibir detalhes da carga, 
          i:int contido no intervalo [0,9]
            
        Return:
        ------- 
            cargas = [  l11, l12, l21, l22, l31, l32, l41, l42, l43, l51, l52, l53  ]            
        
        '''
        
                
        l1 = Loads('maquina de lavar', 8, 7, 17, [8], [10, 10, 5, 10, 5, 5, 5, 10], False, [0.13,0.51,0.3,0.26,0.15,0.15,0.15,0.22], [0.7,0.51,0.3,0.26,0.15,0.15,0.15,0.3], 0.5)
        l2 = Loads('lâmpadas internas', 1, 17, 23, [18], [270], False, [0.15],[0.3], 0.7);
        l3 = Loads('AC office', 14, 15, 24, [16], [10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], True, [1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3], [1.7,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3], 1);
        l4 = Loads('AC couples', 7, 17, 24, [20], [30, 20, 5, 5, 5, 5, 5], False, [2,2,2,2,2,2,2], [2.1,2.1,2.1,2.1,2,2,2], 1);
        l5 = Loads('AC F1', 1, 19, 24, [20], [240], False, [1.1], [1.2], 1);
        l6 = Loads('AC F2', 1, 17, 24, [20], [240], False, [1.1], [1.2], 1);
        l7 = Loads('AC F3', 7, 17, 24, [20], [10, 10, 5, 5, 5, 5, 5], False, [0.9,0.9,0.9,0.9,0.9,0.9,0.9], [1.1,1.1,1.1,1.1,1.1,1.1,1.1], 1);
        
        
        self.cargas_lista2 = [l1, l2, l3, l4, l5, l6, l7]  

    def CargasCenario3(self):    
        '''
        - Cargas de referência do cenário PU
        
        - Execute cargas[i].summary() para exibir detalhes da carga, 
          i:int contido no intervalo [0,9]
            
        Return:
        ------- 
            cargas = [ l1, l2, l3, l4, l5, l6, l7 ]           
        
        '''       
                
        l1 = Loads('maquina de lavar', 8, 7, 17, [8], [10, 10, 5, 10, 5, 5, 5, 10], False, [0.13,0.51,0.3,0.26,0.15,0.15,0.15,0.22], [0.7,0.51,0.3,0.26,0.15,0.15,0.15,0.3], 0.5)
        l2 = Loads('lâmpadas internas', 1, 17, 23, [18], [270], False, [0.15],[0.3], 0.7);
        l3 = Loads('AC office', 14, 15, 24, [16], [10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], True, [1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3], [1.7,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3], 1);
        l4 = Loads('AC couples', 7, 17, 24, [20], [30, 20, 5, 5, 5, 5, 5], False, [2,2,2,2,2,2,2], [2.1,2.1,2.1,2.1,2,2,2], 1);
        l5 = Loads('AC F1', 1, 19, 24, [20], [240], False, [1.1], [1.2], 1);
        l6 = Loads('AC F2', 1, 17, 24, [20], [240], False, [1.1], [1.2], 1);
        l7 = Loads('AC F3', 7, 17, 24, [20], [10, 10, 5, 5, 5, 5, 5], False, [0.9,0.9,0.9,0.9,0.9,0.9,0.9], [1.1,1.1,1.1,1.1,1.1,1.1,1.1], 1);
        
        
        self.cargas_lista3 = [l1, l2, l3, l4, l5, l6, l7]  
        
        
class Loads(DadosReferencia):
    
    '''
    Classe com características gerais de uma carga residencial.
    - Método init carrega dados básicos de cargas diversas de uma residência.
        ----------------------------------------------------------------------
            name - nome da carga\n
            nPhases - total de fases de acionamento\n
            minTime - horário mínimo de início da carga\n
            maxTime - horário máximo de início da carga\n
            bestTime - mínimo tempo de operação da carga\n 
            duration - tempo de duração da carga ligado\n 
            isMultiAcio - status de carga multi ou mono-acionamento\n
            avgPower - valor de potência média da carga\n
            peakPower - valor de potência de pico da carga\n
            comfortLevel - nível de conforto da carga atribuído pelo usuário entre [0,1]\n               
        ----------------------------------------------------------------------
        '''            
    
    def __init__(self, 
                  name, nPhases, minTime, maxTime,  bestTime, 
                  duration, isMultiAcion, avgPower, peakPower, comfortLevel):

        self.name = np.array(name)
        self.nPhases = nPhases
        self.minTime = np.array(minTime)
        self.maxTime = np.array(maxTime)
        self.bestTime = np.array(bestTime)
        self.duration = np.array(duration)
        self.isMultiAcio = np.array(isMultiAcion)
        self.avgPower = np.array(avgPower)
        self.peakPower = np.array(peakPower)
        self.comfortLevel = np.array(comfortLevel)
        
        self.sample_interval=5
        self.fillPowerInSamples()
                     
    def summary(object):
        '''
        Método exibe informações sobre a carga atribuída a um objeto.
        Execute l1.summary()
        ''' 
        print('-'*50)
        print(f"Carga: {object.name}\n\
              {object.nPhases} fase(s)\n\
              Horário mínimo para início acionamento:{object.minTime}\n\
              Horário máximo para início acionamento:{object.maxTime}\n\
              Melhor horário para início acionamento:{object.bestTime}\n\
              Duração de ciclo da carga: {object.duration}\n\
              Carga {'com' if object.isMultiAcio == True else 'sem'} multiacionamento!\n\
              Potência média da carga(kW): {object.avgPower}\n\
              Potência máxima da carga(kW): {object.peakPower}\n\
              Nível de conforto da carga: {object.comfortLevel}"
              )

    def fillPowerInSamples(self):
        '''
        Método cria objetos das características cargas, indexáveis por cada variável.
        
        Preenche arrays de Potência média e com Potência de pico na dimensionalidade
        da amostragem diária
        
        Utiliza amostragem 5min, caso não seja declarada na chamada
        '''            
        # Amostragem diária
        amostragem_horaria = (60*1 / self.sample_interval) 
                        
        # Amostras associadas aos tempos das carga
        self.minTimeInSamples = self.minTime*amostragem_horaria
        self.maxTimeInSamples = self.maxTime*amostragem_horaria
        self.bestTimeInSamples = self.bestTime*amostragem_horaria
        self.durationInSamples = self.duration/self.sample_interval
        
        TOTAL_DURATION = np.sum(self.durationInSamples)
        self.TD = 7  # Semana
        
        PEAK = np.zeros((int(TOTAL_DURATION)))
        AVG = np.zeros((int(TOTAL_DURATION)))
        aux = 0
        
        for phase in range(self.nPhases):
            PEAK = PEAK + np.concatenate((np.zeros((aux)), 
                                          (self.peakPower[phase] * np.ones((int(self.durationInSamples[phase])))), 
                                          np.zeros((int(TOTAL_DURATION) - aux - int(self.durationInSamples[phase])))
                                          ),0)
            AVG = AVG + np.concatenate(( np.zeros((aux)),
                                        (self.avgPower[phase] * np.ones((int(self.durationInSamples[phase])))), 
                                        np.zeros((int(TOTAL_DURATION) - aux - int(self.durationInSamples[phase])))
                                        ),0)

            aux += int(self.durationInSamples[phase])
        self.peakPowerInSamples = np.concatenate( (PEAK , np.zeros((int(amostragem_horaria*24 - TOTAL_DURATION))) ), 0)
        self.avgPowerInSamples =  np.concatenate( (AVG , np.zeros((int(amostragem_horaria*24- TOTAL_DURATION))) ), 0)
    

class Peak_ref(DadosReferencia):
    
    def __init__(self,sample_interval=5):
        '''
        Método carrega a amostragem de intervalo par 5 min.
         * Carrega método de limites de pico horário
        '''
        self.sample_interval=sample_interval
        self.valor_limite=4
        
        self.horario_vale_gauss=19
        
        self.Peak()
        # self.ShowPeakCurve()
    
    def Peak(self):
        ''' 
        Método define a representação de cargas não agendáveis por uma gaussiana invertida.
        centrada às 19h30 com amplitude de 1,0 kW para simular uma redução no limite de 
        demanda considerado.
        
        Parâmetros:
        ----------
        -valor_pico : float, Limite de consumo diário em kWh
        
        -horario_vale_gauss : int, horário de valor de vale da gaussiana
        '''
        from scipy import signal
       
        k=1                                            # Profund. gaussiana invertida
        passo = int(1*60/self.sample_interval)         # Horário
        X = np.arange(1,3*passo+1)                     # Trechos
        Y = signal.gaussian(np.size(X),7)*k            # Sinal sobre os trechos
        peak_limit = np.array(self.valor_limite * np.ones(passo*24)*1) # Diário 
        
        # Manipulação do centróide da gaussiana
        a=self.horario_vale_gauss - 2                 #inicio_gaussiana
        b=int(24-a-len(X)/passo)                      #Término da gaussiana
        gaussiana_invertida = np.hstack(([np.zeros(a*passo)],  # Valores
                                         [Y],
                                         [np.zeros(b*passo)]
                                         ))
    
        self.pico_cargas_nao_agendaveis = peak_limit - gaussiana_invertida
    
    def ShowPeakCurve(self):
        '''
        Método exibe grafico da curva de Pico
        '''
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10,5),dpi=150)
        plt.plot(self.pico_cargas_nao_agendaveis.ravel(),label='Consumo limite')
        plt.ylim(0, self.valor_limite+1)
        xticks1 = (np.arange(1,25)*(24*60/self.sample_interval)/24)
        xticks2 = list(map(str,np.arange(1,25,1)))
        plt.xticks(xticks1, xticks2 )              
        plt.ylabel("Pico de consumo (kwh)")
        plt.xlabel("Tempo (h)")       
        plt.grid(color='white')
        plt.legend()
        plt.style.use('ggplot')

#%% Area de testes
# =============================================================================
def test():
    a=Peak_ref()
    a.ShowPeakCurve()
    
def carg():
    b=DadosReferencia()    
    for i in b.cargas_lista1:
        i.summary()
    
if __name__ == '__main__':
    carg()  
    test()
    pass
