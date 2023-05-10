#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ModEDA
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM


class PrevLSTM:
    def __init__(self,passo=100):
       
        # Definindo variaveis globais
        self.data, self.base =[],[]    
        self.X_train, self.X_test = [],[]
        self.y_train, self.y_test = [],[]
        self.passo = passo 
   
        # Atualiza variaveis globais e processos sequenciais
        self.Database()            
        
        # Estrutra os atributos em sequências de comprimento passo (janela ou look_back)
        x,y = self.Datapreprocess()
        
        # Atualize as variáveis train-test
        self.DataTrainTest(X=x,y=y)
        
        # Controi a rede
        model=self.RedeLSTM()    
        
        # Treina a rede
        model.fit(self.X_train, self.y_train, epochs=100, batch_size=32)
        # Avalia o modelo
        score = model.evaluate(self.X_test, self.y_test, batch_size=32)
        print('Score: %.2f MSE',score)
        
        # Usa o modelo para prever valores futuros
        predictions = model.predict(self.X_test)
        
        # Imprime as previsões e os valores verdadeiros
        for i in range(10):
            print('Previsão: %.2f, Valor verdadeiro: %.2f' % (predictions[i], self.y_test[i]))
            
        
        plt.plot(self.y_test, color = 'red', label = 'Consumo real')
        plt.plot(predictions, color = 'blue', label = 'Previsões')
        plt.title('Previsão consumo residencial')
        plt.xlabel('Tempo')
        plt.ylabel('Valor kWh')
        plt.legend()
        plt.show()

    
    def Database(self,col='consumo', details=False):
        df = ModEDA.EDA().dados
        df_atrib = df[col].values
        
        if details == True:
            print('Base de dados importada!', df.info())
            print(f"\nUtilizada a coluna '{col}' para análise com LSTM.")
            
        self.data, self.base = df_atrib, df
    
   
    def Datapreprocess(self):
       
        X,y = [],[]
        for i in range(0,len(self.data) - self.passo):
            X.append(self.data[ i : i + self.passo ])
            y.append(self.data[ i + self.passo ])
        X,y = np.array(X),np.array(y)
        
        
        return X,y 

    def DataTrainTest(self,X,y,perc_test=0.8):
        
        # train_size = int(len(X) * perc_test)
        train_size = -100  # 100 Casas e um dia
        self.X_train, self.X_test = X[:train_size], X[train_size:]
        self.y_train, self.y_test = y[:train_size], y[train_size:]        
        
        
        
    def RedeLSTM(self,optimizer = 'rmsprop', loss = 'mean_squared_error',
                          metrics = ['mean_absolute_error'],
                          epocas=100,tamlote=32):
            regressor = Sequential()
            regressor.add(LSTM(units = 100, return_sequences = True, 
                                input_shape = (self.passo, 1)))
            regressor.add(Dropout(0.3))
            
            regressor.add(LSTM(units = 50, return_sequences = True))
            regressor.add(Dropout(0.3))
            
            regressor.add(LSTM(units = 50, return_sequences = True))
            regressor.add(Dropout(0.3))
            
            regressor.add(LSTM(units = 50))
            regressor.add(Dropout(0.3))
            
            regressor.add(Dense(units = 1, activation = 'linear'))
            
            regressor.compile(optimizer = optimizer, loss = loss,
                              metrics = metrics
                              )
            regressor.summary()
            
            return regressor    
   

import time
t0=time.time()    
PrevLSTM()
print(t0-time.time())




# from keras.models import Sequential
# from keras.layers import Dense, Dropout, LSTM
# from sklearn.preprocessing import MinMaxScaler
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import time


# class TS_Prev:
#     def __init__(self):
        
        
#         self.X_train_norm, self.normalizador = self.Dataset()
#         self.prev,self.val_real = self.AtribPrev()
#         self.regressor = self.RedeLSTM()
        
#         # t0=time.time()
#         self.regressor.fit(self.prev, self.val_real, 
#                            epochs = 10, batch_size = 32,
#                            )        
#         # print(f"Tempo decorrido: {time.time() - t0:.6f} segundos")
                
#         self.graf_test_prev()
        
#     def Dataset(self):
#         # Base de dados
#         base = pd.read_csv('petr4_treinamento.csv')
#         base = base.dropna()
#         X_train= base.iloc[:, 1:2].values
        
#         # Normalização da base de dados
#         norm = MinMaxScaler(feature_range=(0,1))
#         X_train_norm = norm.fit_transform(X_train)

#         return X_train_norm,norm
    
#     def AtribPrev(self,look_back=90):

#         prev , val_real = [],[]
#         for i in range(look_back, len(self.X_train_norm)):
#             prev.append(self.X_train_norm[i - look_back : i, 0])
#             val_real.append(self.X_train_norm[i, 0])
#         prev, val_real = np.array(prev), np.array(val_real)
#         prev = np.reshape(prev, (prev.shape[0], prev.shape[1], 1))
        
#         return prev, val_real

#     def RedeLSTM(self,optimizer = 'rmsprop', loss = 'mean_squared_error',
#                       metrics = ['mean_absolute_error'],
#                       epocas=100,tamlote=32):
#         regressor = Sequential()
#         regressor.add(LSTM(units = 100, return_sequences = True, 
#                            input_shape = (self.prev.shape[1], 1)))
#         regressor.add(Dropout(0.3))
        
#         regressor.add(LSTM(units = 50, return_sequences = True))
#         regressor.add(Dropout(0.3))
        
#         regressor.add(LSTM(units = 50, return_sequences = True))
#         regressor.add(Dropout(0.3))
        
#         regressor.add(LSTM(units = 50))
#         regressor.add(Dropout(0.3))
        
#         regressor.add(Dense(units = 1, activation = 'linear'))
        
#         regressor.compile(optimizer = optimizer, loss = loss,
#                           metrics = metrics
#                           )
#         regressor.summary()
        
#         return regressor
        
        
#     def TestPrev(self,look_back=90):    
#             base = pd.read_csv('petr4_treinamento.csv')
#             base_teste = pd.read_csv('petr4_teste.csv')
            
#             preco_real_teste = base_teste.iloc[:, 1:2].values            
#             base_completa = pd.concat((base['Open'], base_teste['Open']), axis = 0)
            
#             entradas = base_completa[len(base_completa) - len(base_teste) - look_back:].values
#             entradas = entradas.reshape(-1, 1)
#             entradas = self.normalizador.transform(entradas)
            
#             X_teste = []
#             for i in range(look_back, 112):
#                 X_teste.append(entradas[i-90:i, 0])
#             X_teste = np.array(X_teste)
#             X_teste = np.reshape(X_teste, (X_teste.shape[0], X_teste.shape[1], 1))
#             previsoes = self.regressor.predict(X_teste,verbose=False)

#             previsoes = self.normalizador.inverse_transform(previsoes)

#             return previsoes,preco_real_teste

#     def graf_test_prev(self):
#             previsoes,preco_real_teste = self.TestPrev()
                     
#             plt.plot(preco_real_teste, color = 'red', label = 'Preço real')
#             plt.plot(previsoes, color = 'blue', label = 'Previsões')
#             plt.title('Previsão de dados')
#             plt.xlabel('Tempo')
#             plt.ylabel('Valor Real')
#             plt.legend()
#             plt.show()


# # =============================================================================
# #%%Testes 
# # =============================================================================




















