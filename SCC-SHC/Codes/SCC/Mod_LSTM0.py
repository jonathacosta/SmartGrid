#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jonatha Costa
Basic code using Long Short Term Memory as a regressor using class
"""
import ModEDA
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dense,Dropout


class ModelLstm:
    def __init__(self,n_units=100,n_steps=3, n_features=1,
                 dropout_rate=0.2,activation='relu',optimizer='adam',
                 batch_size=16,epocas=100
                 ):        
        self.n_units = n_units             # cells        
        self.n_steps = n_steps             # dim from X.shape[1]
        self.n_features = n_features       # dim from X.shape[2]
        self.dropout_rate = dropout_rate   # Preventive gradiente vanish 
        self.activation = activation
        self.optimizer= optimizer
        self.batch_size = batch_size
        self.epochs = epocas
        
    def create_model(self,loss='mse',metrics=['mean_absolute_error']):
        '''model_sim
        Method creats a LSTM model based on main LSTM features''' 
        model = Sequential()
        model.add(LSTM(self.n_units, activation = self.activation, return_sequences=True, 
                       input_shape=(self.n_steps, self.n_features)))
        model.add(Dropout(self.dropout_rate))
        model.add(LSTM(self.n_units, activation = self.activation, return_sequences=True))
        model.add(Dropout(self.dropout_rate))
        model.add(LSTM(self.n_units, activation = self.activation))
        model.add(Dropout(self.dropout_rate))
        model.add(Dense(1))
        model.compile(optimizer=self.optimizer, loss=loss,metrics=metrics)
        # model.summary()        
        
        return model
    
    def FitLstmModel(self, X_train, y_train,                
                verbose=0,graph_train=0):
       
       model = self.create_model()
       history=model.fit(X_train, y_train, 
                         epochs=self.epochs, batch_size=self.batch_size, 
                         verbose=verbose)
       
       if graph_train==1:
           
           a=list(history.history.keys())           
           for i in range(len(a)):
               plt.plot(history.history[a[i]],label=a[i])                       
           plt.title('Erro do modelo no treino')
           plt.ylabel(f'{a}')
           plt.xlabel('epoch')
           plt.legend(loc='upper left')
           plt.show()        

       return model

    def evaluate(self, X_test, y_test, model):
        
        loss,accuray = model.evaluate(X_test, y_test, verbose=0)
        
        return loss,accuray

    def predict(self, X_test,model):
        y_pred = model.predict(X_test, verbose=0)
        
        return y_pred


class RedeLstm(ModelLstm):
    def __init_subclass__(self,data,**kwargs):
        pass
        
    def create_dataset(self, data):
        '''
        Method generate a dataset from a vector 
        Special case to LSTM regressor from a unique colunm vector
        n_steps works as a look_back
        
        X = X.shape[0], self.n_steps, self.n_features
        Y = Y.shape[0], self.n_steps
        '''
        
        X, y = [], []
        for i in range(self.n_steps, len(data)):
            X.append(data[i-self.n_steps:i, 0])
            y.append(data[i, 0])
        X, y = np.array(X), np.array(y)
        X = X.reshape(X.shape[0], self.n_steps, self.n_features)
        return X, y
    
    def DivTrainTest(self,per_train_test=0.80,data=None):
        '''
        Method separate dataset between train e test sets. '''
        
        # Cria os conjuntos de dados de treinamento e teste
        train_size = int(len(data)*per_train_test)
        train_size = train_size
        train_data = data[:train_size, :]        
        test_data = data[train_size:, :]
        
        return train_data, test_data
        
    def graph(self,y_test,y_pred):
        plt.plot(y_test, color = 'red', label = 'Dados reais')
        plt.plot(y_pred, color = 'blue', label = 'Previsões')
        plt.title('Previsão')
        plt.xlabel('--')
        plt.ylabel('--')
        plt.legend()
        plt.show()        
        
    def model_sim(self,data=np.arange(1000).reshape(-1,1),graph_train=0,graph_pred=0):
        
        train_data,test_data = self.DivTrainTest(data=data)        
        
        X_train, y_train = self.create_dataset(train_data)
        X_test, y_test = self.create_dataset(test_data)
        
        model=self.FitLstmModel(X_train, y_train,
                                graph_train=graph_train,verbose=0)
        
        loss,accuray = model.evaluate(X_train, y_train)
        
        return loss,accuray
        # y_pred=model.predict(X_test)
        # if graph_pred==1: self.graph(y_test, y_pred)
        # self.y_pred = y_pred
           
#%% My gridsearch
import time
from tqdm import tqdm

data = ModEDA.EDA().df.temp.values.reshape(-1,1)
sol=[]
n_steps = [10,20,30]
dropout_rate = [0.0, 0.1, 0.2]
n_units = [32,48,64,128]
activation = ['linear','relu']
optimizer=['adam','RMSprop']
batch_size = [16,32]
epocas =[50,100,150]
for i in tqdm(n_steps):
    for j in tqdm(dropout_rate):
        for k in n_units:
            for act in activation:
                for opt in optimizer:
                    for n_batch_size in batch_size:
                        for n_epocas in epocas:
                            t0=time.time() 
                            loss,accuracy = RedeLstm(n_units=k,
                                                     n_steps=i,
                                                     dropout_rate=j,
                                                     activation=act,
                                                     optimizer=opt,
                                                     batch_size=n_batch_size,
                                                     epocas = n_epocas
                                                     ).model_sim(data)
                            t1 = time.time()
                            sol.append([i,j,k,act,opt,n_batch_size,n_epocas,loss,accuracy,t1-t0])    
#%%    
import pandas as pd
df = pd.DataFrame(sol,columns=['n_steps','dropout','n_units','activation','optimizer','batch_size','epocas','loss','accuracy','time(s)'])
df.to_csv('results/df_gridsearch',index=True)
MelhorAcc = df.accuracy.idxmin()

print(f'\nO melhor loss está na linha {MelhorAcc},cujos hiperparâmetros são:\n')
print(df.loc[MelhorAcc])
print('Para análise de outras variáveis, como custo computacional, seguem os 10 melhores resultados de loss durante:\n')
print(df.sort_values(by='loss')[:10])






#%%


