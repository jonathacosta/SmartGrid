#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Método utiliza Lógica Fuzzy para definir um valor de conforto em 0 e 1.
"""
import ModConfFz
import numpy as np
import matplotlib.pyplot as plt

class Superf_control:
    def __init__(self,graf_default=0,lang=0):
        '''
        Método init executa as rotinas para os gráficos de superfície
        considerando humor [1,5,9]
        '''
        
        self.graf_3d(lang=lang)    

    def f_humor(self):
        '''
        Método define a função f(temperatura,umidade) = conforto
        Utilizando um valor fixo 'h' para humor.
        '''
    
        temp, umid, conf = np.array([]),np.array([]),np.array([])      
        DIVs = 15
    
        for x in np.linspace(0, 40, DIVs):       # limites temp
            for y in np.linspace(0,100, DIVs):   # limites umidade
                conf_fz = ModConfFz.Fz_sim().Fuzificar(t=x,u=y)
                temp = np.append(temp,x)
                umid = np.append(umid,y)
                conf = np.append(conf,conf_fz[-1])
    
        return np.round(temp,2),np.round(umid,2),np.round(conf,2)
    
    def graf_3d(self,lang=0):        
        '''
        Método gera gráfico 3d com entrada:
            * humor: [0,10] 
            * tipo de humor = 'mau humor (1), humor intermediário (5), bom humor (9)'
        '''
        xs,ys,zs = self.f_humor()
        l = [1 if lang==1 else 0][0]    

        xlabel = ['temperatura percebida','Perceived temperature']
        ylabel = ['umidade percebida','Perceived humidity']
        zlabel = ['conforto level','Comfort level']
        
        # Classificação de humor para título do gráfico   
        titulo = [['Percepção do usuário','User perception'][l]]
        graf_title = [f"Conforto com variável '{titulo[0]}'",
                      f"Comfort for variable '{titulo[0]}' "]    
                
        with plt.style.context('seaborn'): 
            fig = plt.figure(figsize=(12,6))
            ax = fig.gca(projection ='3d')
            xx, yy = np.meshgrid(xs,ys)
            surf=ax.plot_trisurf(xs,ys,zs, vmin = 0, vmax = 1, 
                                 cmap='gnuplot2')
            ax.set_xlabel(xlabel[l])
            ax.set_ylabel(ylabel[l])
            ax.set_zlabel(zlabel[l])
            ax.set_title(graf_title[l], pad = 10)
            ax.set_zlim(0, 1)
            plt.tight_layout()
            fig.colorbar(surf, ax=ax)
            ax.view_init(elev=30., azim=-130)
            plt.savefig(f'results/figuras/conf_{titulo[0]}',
                        transparent=True,dpi = 300)
            
            plt.show()

# =============================================================================
# Área de testes
# =============================================================================
# Superf_control(lang=1)
