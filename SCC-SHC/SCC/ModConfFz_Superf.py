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
        
        if graf_default==1:
            for i in [1,5,9]:
                self.graf_3d(h=i,lang=lang)    

    def f_humor(self,h=2):
        '''
        Método define a função f(temperatura,umidade) = conforto
        Utilizando um valor fixo 'h' para humor.
        '''
    
        temp, umid, conf = np.array([]),np.array([]),np.array([])      
        DIVs = 50
    
        for x in np.linspace(0, 40, DIVs):       # limites temp
            for y in np.linspace(0,100, DIVs):   # limites umidade
                conf_fz = ModConfFz.Fz_sim().Fuzificar(t=x,u=y,h=h)
                temp = np.append(temp,x)
                umid = np.append(umid,y)
                conf = np.append(conf,conf_fz[-1])
    
        return np.round(temp,2),np.round(umid,2),np.round(conf,2)
    
    def graf_3d(self,h=1,lang=0):        
        '''
        Método gera gráfico 3d com entrada:
            * humor: [0,10] 
            * tipo de humor = 'mau humor (1), humor intermediário (5), bom humor (9)'
        '''
        xs,ys,zs = self.f_humor(h=h)
        l = [1 if lang==1 else 0][0]    

        xlabel = ['temperatura','temperature']
        ylabel = ['umidade','humidity']
        zlabel = ['conforto','comfort']
        
        # Classificação de humor para título do gráfico   
        titulo = [['mau_humor','bad_mood'][l] if h<3.5 
                  else ['humor_intermediario','intermediate_mood'][l]
                  if h<7 else ['bom_humor','good_mood'][l]
                  ] 
        graf_title = [f"Conforto com variável '{titulo[0]}' - h={h}",
                      f"Comfort for variable '{titulo[0]}' - h={h}"]    
                
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
            plt.savefig(f'results/figuras/conf_{titulo[0]}',
                        transparent=True,dpi = 300)
            ax.view_init(elev=30., azim=-130)
            plt.show()

# =============================================================================
# Área de testes
# =============================================================================
# a=Superf_control(lang=1)
# a.graf_3d(h=8)
Superf_control(graf_default=True,lang=True)