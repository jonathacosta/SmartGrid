#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de configuração do SHC de cada casa.
Retorno de chamadas do Módulo SCC.
"""
import ModLoad,ModTariff,ModExecPSO

class SHC():
    '''
    Classe realiza a análise de consumo versus conforto aplicando agendamento de cargas
    via PSO com conforto Fuzzy.
    '''
    def __init__(self,sample_interval=5, tar=0, alfa=0, lst_cargas=0, 
                 conf_func=0,user_var=None ,graf=0, lang=0, casa = 0):
        '''
        Método init carrega variável global :
            -'sample_interval=5'
            - tarifas
            - cargas
            - picos de cargas
        '''       
        ''' Variáveis'''
        self.alfa = alfa             # Carrega alfa da relação custo-conforto
        self.exibe_graf = graf       # Exibe gráfico
        self.lang = lang             # Inglês= 1. português =0
        self.casa = casa             # Identifica o número da casa para o gráfico
        self.iteracoes = 3 	  	     # Define o total de iterações para o PSO
        self.conf_func = conf_func     # Define a função de conforto
        self.conf_alt = []		     # Armazena as variáveis linguísticas fuzzy 
        self.tab_cargas = lst_cargas # Identifica a tabela de cargas A,B ou C        
        self.user_var = user_var

        '''Módulo 01: tarifas e limite de pico de consumo para cargas não agendáveis'''
        if tar == 1: # set tarifa branca
            self.tarifa = ModTariff.Tariffs().Tariff_of_Use
        else:       # preset tarifa fixa
            self.tarifa = ModTariff.Tariffs().tariff_constant

        '''Módulo 02: Preenchimentos de objetos por amostragem com lista de cargas'''        
        if self.tab_cargas == 1:
            if lang == 1: # inglês
                self.cargas = ModLoad.DadosReferencia().cargas_lista1_en
            else:         # português
                self.cargas = ModLoad.DadosReferencia().cargas_lista1
        elif self.tab_cargas == 2: 
            self.cargas = ModLoad.DadosReferencia().cargas_lista2
        else:     
            self.cargas = ModLoad.DadosReferencia().cargas_lista3        
        
        '''Módulo 03:Valores de pico de carga por amostragem não agendáveis'''
        self.pico_cargas = ModLoad.Peak_ref().pico_cargas_nao_agendaveis
        
        '''Módulo 04: Execução do PSO'''
        self.Process_PSO()  
           

    def Process_PSO(self):
        '''
        Método de chamada para executar o PSO aplicando parametros do algoritmo e dos métodos sobre as cargas
        de modo que :
            * alfa [0,1] = [economia,conforto]
            * f = αf1 +(1−α)f2
        Para alfa = 0, o controlador obterá a melhor solução para os níveis de conforto do usuário conforme peso de alfa.
        Para alfa = 1, o controlador minimizará apenas os custos do consumo de eletricidade. De modo que haverá conforto, 
        pois as cargas serão acionadas, contudo esse não será um critério considerado pelo SHC para escolha dos horários.
        
        O método instancia o objeto 'sol' com os atributos da classe ExecPSO (dentro do módulo ModExecPSO). Seguidamente,
        é chamado o método que busca a melhor solução do PSO através de sol.PSO(), juntamente com as respostas
        gráficas para o referido valor de alfa.
        Isso é repetido para cada novo valor de alfa no laço 'for'.
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
# AREA DE TESTES
#******************************************************************************
# a=SHC()



