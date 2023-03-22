#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
"""
Pricing modeling

Electricity pricing models

Main class contains - acceptance periodicity to model cost

"""
import numpy as np

class Tariffs():
    '''
    Class contains methods that define the cost as a function of study fees.
     -Necessary to inform sampling interval for modeling in minutes:
         Rates(sample_interval = 5)
        
         Sample_interval must be better than 60 min.
     -Init method loads basic sampling data for charging.
         -------------------------------------------------- ----------
         - Constant cost tariff
         - ToU tariff
    '''
    def __init__(self,sample_interval=5):
        self.sample_interval = sample_interval    # consumption sampling in min
        self.Tariff_const()
        self.Tariff_ToU()
        # self.Graf_tariff()
    
    def Tariff_const(self,price=0.87345):
        '''
        Method returns an 'n' dimensional vector with fare price values.
          - 'n' is defined as the ratio between :(the total daily minutes (60*24))
             and the sample rate:(sample_interval)
          - 'reshape(1,-1)' is used to vectorize the output to
             'n' columns and 1 row
         Parameters:
             price: float
        
             -It is necessary to inform the price of the tariff
            
             -Tariff_const(price = 0.722495). DEFAULT
         Return
         -------
             'n' dimensional pricing vector
             tariff_const

        '''
        passo = int(24*60/self.sample_interval)    
        self.tariff_constant = price*np.ones(passo).reshape(1,-1)
        

    def Tariff_ToU(self,p1=0.56355,p2=0.88144,p3=1.42294):
        '''
        Method returns an 'n' dimensional vector with white fare price values.
         Time of Use
          - 'n' is defined as the hourly sampling rate, in minutes:\n
              (1h*60min))/(sample_interval)
             
         parameters
         ----------
         p1 : float.
             Cost of the white fare during 'OFF PEAK' times
             From 1 am to 5 pm and from 11 pm to midnight (Or from 11 pm to 5 pm the next day)
            
         p2 : float
             Cost of the white tariff in the 'INTERMEDIATE' schedule
             From 17:00 to 18:00 and from 21:00 to 22:00
            
         p3: float
             Cost of the white fare at 'PONTA' time
             From 6 pm to 9 pm
         Default values:
             off-peak_price = 0.56355,\n
             intermediate_price = 0.88144,\n
             peak_price = 1.42294
         Return
         -------
             'n' dimensional pricing vector
             TOU

        '''
        passo = int(1*60/self.sample_interval)    
        self.Tariff_of_Use = np.hstack(( 
            [p1*np.ones(17*passo)],
            [p2*np.ones(1*passo)],
            [p3*np.ones(3*passo)],
            [p2*np.ones(1*passo)],
            [p1*np.ones(2*(passo))]
            ))               
        


    def Graf_tariff(self):  
        '''
        Method displays ToU and constant tariff chart        '''
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10,5),dpi=150)
        xticks1 = (np.arange(1,25)*(24*60/self.sample_interval)/24)
        xticks2 = list(map(str,np.arange(1,25,1)))
        plt.xticks(xticks1, xticks2 )      
        plt.plot(self.Tariff_of_Use.ravel(),label='ToU tariff',color='b')
        plt.plot(self.tariff_constant.ravel(),label='Constant tariff',color='y')
        plt.ylabel("R$/kwh")
        plt.xlabel("Time (h)")       
        plt.grid(color='white')
        plt.legend()
        plt.style.use('ggplot')

#%% Test space
def test():
    a=Tariffs()
    a.Graf_tariff()


# test()
