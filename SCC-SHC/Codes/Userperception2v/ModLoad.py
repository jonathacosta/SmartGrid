# -*- coding: utf-8 -*-
'''
Load modeling

Main class - basic class for modeling residential loads.

     sub-class 1 - flexible drive loads

     sub-class 2 - flexible power loads    
'''

import numpy as np

class DadosReferencia():
    '''
     * Class contains reference parameters for simulating different scenarios.
    
       * init method loads attributes from the Load method.
     
       * CargasCenarioPU method - loads reference loads for analysis.
      
       * Uses 5min sampling, self.sample_interval =5
    
     '''    
    def __init__(self):
        ''' 
        Loads the load objects of the reference scenario in L.
        
        '''
        self.CargasCenarioPU()
        self.CargasCenarioPU_en()
        self.CargasCenario2()
        self.CargasCenario3()
        self.CargasCenario4()

    
    def CargasCenarioPU(self):    
        '''
        - PU scenery reference loads
        
         - Run cargas[i].summary() to display payload details,
           i:int contained in range [0,9]
           Elements in Portuguese language 
         Return:
         -------
             loads = [ l1, l2, l3, l4, l5, l6, l7, l8, l9, l10 ]
        
        '''
        
        l1 = Loads('Bomba booster', 1, 7, 17, [8,16], [20], True, [2], [3], 0.1)
        l2 = Loads('Bomba piscina', 1, 7, 17, [8], [120], False, [0.75], [1.5], 0.1)             
        l3 = Loads('Maquina de lavar', 8, 7, 17, [8], [10, 10, 5, 10, 5, 5, 5, 10], False, [0.13,0.51,0.3,0.26,0.15,0.15,0.15,0.22], [0.7,0.51,0.3,0.26,0.15,0.15,0.15,0.3], 0.5)
        l4 = Loads('Lâmpadas externas', 1, 17, 24, [18], [270], False, [0.3], [0.3], 0.3);
        l5 = Loads('Lâmpadas internas', 1, 17, 23, [18], [270], False, [0.15],[0.3], 0.7);
        l6 = Loads('AC escritório', 14, 15, 24, [16,20], [10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], True, [1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3], [1.7,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3], 1);
        l7 = Loads('AC casal', 7, 17, 24, [20], [30, 20, 5, 5, 5, 5, 5], False, [2,2,2,2,2,2,2], [2.1,2.1,2.1,2.1,2,2,2], 1);
        l8 = Loads('AC F1', 1, 17, 24, [20], [240], False, [1.1], [1.2], 1);
        l9 = Loads('AC F2', 7, 17, 24, [20], [10, 10, 5, 5, 5, 5, 5], False, [0.9,0.9,0.9,0.9,0.9,0.9,0.9], [1.1,1.1,1.1,1.1,1.1,1.1,1.1], 1);
        l10 = Loads('Lava-louças', 5, 18, 22, [21], [5, 10, 15, 5, 10], False, [0.033,1.76,0.033,1.76,0.033], [0.033,1.76,0.033,1.76,0.033], 0.3);
            
        self.cargas_lista1 = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10]  
                         
    def CargasCenarioPU_en(self):    
        '''
        - PU scenery reference loads
        
         - Run cargas[i].summary() to display payload details,
           i:int contained in range [0,9]
           Elements in English language 
         Return:
         -------
             loads = [ l1, l2, l3, l4, l5, l6, l7, l8, l9, l10 ]
        
        '''
        
        
        l1 = Loads('Booster pump', 1, 7, 17, [8,16], [20], True, [2], [3], 0.1)
        l2 = Loads('Pool pump', 1, 7, 17, [8], [120], False, [0.75], [1.5], 0.1)             
        l3 = Loads('Washing machine', 8, 7, 17, [8], [10, 10, 5, 10, 5, 5, 5, 10], False, [0.13,0.51,0.3,0.26,0.15,0.15,0.15,0.22], [0.7,0.51,0.3,0.26,0.15,0.15,0.15,0.3], 0.5)
        l4 = Loads('External lights', 1, 17, 24, [18], [270], False, [0.3], [0.3], 0.3);
        l5 = Loads('Internal lights', 1, 17, 23, [18], [270], False, [0.15],[0.3], 0.7);
        l6 = Loads('Office AC', 14, 15, 24, [16,20], [10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], True, [1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3], [1.7,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3], 1);
        l7 = Loads('Couple AC', 7, 17, 24, [20], [30, 20, 5, 5, 5, 5, 5], False, [2,2,2,2,2,2,2], [2.1,2.1,2.1,2.1,2,2,2], 1);
        l8 = Loads('F1 AC', 1, 17, 24, [20], [240], False, [1.1], [1.2], 1);
        l9 = Loads('F2 AC', 7, 17, 24, [20], [10, 10, 5, 5, 5, 5, 5], False, [0.9,0.9,0.9,0.9,0.9,0.9,0.9], [1.1,1.1,1.1,1.1,1.1,1.1,1.1], 1);
        l10 = Loads('Dishwasher machine', 5, 18, 22, [21], [5, 10, 15, 5, 10], False, [0.033,1.76,0.033,1.76,0.033], [0.033,1.76,0.033,1.76,0.033], 0.3);
        self.cargas_lista1_en = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10]  
        
    def CargasCenario2(self):    
        '''
        - PU scenery reference loads using just 7 loads
        
         - Run cargas[i].summary() to display payload details,         
         Return:
         -------
             loads = [ l1, l2, l3, l4, l5, l6, l7]
    
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
        - PU scenery reference loads using just 4 loads
        
         - Run cargas[i].summary() to display payload details,         
         Return:
         -------
             loads = [ l1, l2, l3, l4]
    
        '''    
                
        l1 = Loads('Bomba booster', 1, 7, 17, [8,16], [20], True, [2], [3], 0.1)
        l2 = Loads('Bomba piscina', 1, 7, 17, [8], [120], False, [0.75], [1.5], 0.1)             
        l3 = Loads('lâmpadas externas', 1, 17, 24, [18], [270], False, [0.3], [0.3], 0.3);
        l4 = Loads('lâmpadas internas', 1, 17, 23, [18], [270], False, [0.15],[0.3], 0.7);
               
        self.cargas_lista3 = [l1, l2, l3, l4]  
        
    def CargasCenario4(self):    
        '''
        - PU scenery reference loads using just thermal loads
         - Run cargas[i].summary() to display payload details,         
         Return:
         -------
             loads = [ l1, l2, l3, l4, l5]
    
        '''     
                
        l1 = Loads('AC couples 1', 14, 15, 24, [16], [10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], True, [1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3], [1.7,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3,1.3], 1);
        l2 = Loads('AC couples 2', 7, 17, 24, [20], [30, 20, 5, 5, 5, 5, 5], False, [2,2,2,2,2,2,2], [2.1,2.1,2.1,2.1,2,2,2], 1);
        l3 = Loads('AC F1', 1, 19, 24, [20], [240], False, [1.1], [1.2], 1);        
        l4 = Loads('AC F2', 7, 17, 24, [20], [10, 10, 5, 5, 5, 5, 5], False, [0.9,0.9,0.9,0.9,0.9,0.9,0.9], [1.1,1.1,1.1,1.1,1.1,1.1,1.1], 1);
        l5 = Loads('AC F3', 7, 17, 24, [20], [10, 10, 5, 5, 5, 5, 5], False, [0.9,0.9,0.9,0.9,0.9,0.9,0.9], [1.1,1.1,1.1,1.1,1.1,1.1,1.1], 1);

        
        self.cargas_lista4 = [l1,l2,l3,l4,l5]     
        
        
        
        
class Loads(DadosReferencia):
    
    '''
    Class with general characteristics of a residential load.
     - Method init loads basic data of various loads of a residence.
         -------------------------------------------------- --------------------
             name - payload name\n
             nPhases - total activation phases\n
             minTime - minimum load start time\n
             maxTime - maximum load start time\n
             bestTime - minimum load operation time\n
             duration - duration time of connected load\n
             isMultiAcio - multi- or single-drive load status\n
             avgPower - load average power value\n
             peakPower - peak power value of the load\n
             comfortLevel - load comfort level assigned by the user between [0,1]\n
         -------------------------------------------------- --------------------
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
        Method displays information about the load assigned to an object.
         Run l1.summary()
        ''' 
        print('-'*50)
        print(f"Load: {object.name}\n\
              {object.nPhases} phase(s)\n\
              Minimum start time:{object.minTime}\n\
              Maximum start time:{object.maxTime}\n\
              Best start time:{object.bestTime}\n\
              Charge cycle time: {object.duration}\n\
              Load {'with' if object.isMultiAcio == True else 'without'} multi-drive!\n\
              Average load power(kW): {object.avgPower}\n\
              Max load power(kW): {object.peakPower}\n\
              Residential load comfort level: {object.comfortLevel}"
              )

    def fillPowerInSamples(self):
        '''
        Method creates objects of load characteristics, indexable by each variable.
        
         Populates Average Power and Peak Power arrays in dimensionality
         of daily sampling
        
         Uses 5min sampling, if not declared in the call
        '''            
       # Daily sampling
        amostragem_horaria = (60*1 / self.sample_interval) 
                        
        # Samples associated with load times    
        self.minTimeInSamples = self.minTime*amostragem_horaria
        self.maxTimeInSamples = self.maxTime*amostragem_horaria
        self.bestTimeInSamples = self.bestTime*amostragem_horaria
        self.durationInSamples = self.duration/self.sample_interval
        
        TOTAL_DURATION = np.sum(self.durationInSamples)
        self.TD = 7  # Week
        
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
        ''' Method loads the sampling interval to 5 min. 
        
        * Load hourly peak limits method
        '''
        self.sample_interval=sample_interval
        self.valor_limite=4
        
        self.horario_vale_gauss=19
        
        self.Peak()
        # self.ShowPeakCurve()
    
    def Peak(self):
        ''' 
        Method defines the representation of non-schedulable loads by an inverted Gaussian.
         centered at 7:30 pm with an amplitude of 1.0 kW to simulate a reduction in the
         demand considered.
        
         Parameters:
         ----------
         -peak_value : float, Daily consumption limit in kWh
        
         -time_vale_gauss : int, time value of gaussian valley
        '''
        from scipy import signal
       
        k=1                                            # Depth inverted gaussian
        passo = int(1*60/self.sample_interval)         # Time
        X = np.arange(1,3*passo+1)                     # Sections
        Y = signal.gaussian(np.size(X),7)*k            # Sign on the sections
        peak_limit = np.array(self.valor_limite * np.ones(passo*24)*1) # Daily 
        
        # Gaussian centroid manipulation
        a=self.horario_vale_gauss - 2                 # Star of the gaussian
        b=int(24-a-len(X)/passo)                      # End of the gaussian
        gaussiana_invertida = np.hstack(([np.zeros(a*passo)],  # Values
                                         [Y],
                                         [np.zeros(b*passo)]
                                         ))
    
        self.pico_cargas_nao_agendaveis = peak_limit - gaussiana_invertida
    
    def ShowPeakCurve(self):
        '''
        Method shows peak curve graphic
        '''
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10,5),dpi=150)
        plt.plot(self.pico_cargas_nao_agendaveis.ravel(),label='Limit consumption')
        plt.ylim(0, self.valor_limite+1)
        xticks1 = (np.arange(1,25)*(24*60/self.sample_interval)/24)
        xticks2 = list(map(str,np.arange(1,25,1)))
        plt.xticks(xticks1, xticks2 )              
        plt.ylabel("Peak of consumption(kwh)")
        plt.xlabel("Time (h)")       
        plt.grid(color='white')
        plt.legend()
        plt.style.use('ggplot')

#%% Area of tests
# =============================================================================
def test():
    a=Peak_ref()
    a.ShowPeakCurve()
    
def carg():
    b=DadosReferencia()    
    for i in b.cargas_lista1:
        i.summary()

# carg()  
# test()




