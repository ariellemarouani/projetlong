# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

PATH = "/net/argos/data/vog/tarlod/50ans/"
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


import init_donnees as id
conv_=id.__read_mld(PATH)
x = np.linspace(0, 81, 81)
y = np.linspace(0, 81, 81)

X, Y = np.meshgrid(x, y)
vmin=np.min(-conv_)
u=0
for j in np.arange(50):
    conv_annee=conv_[(j*120):((j+1)*120)]
    annee=1963+j
    for i in np.arange(120):
        Z = conv_annee[i]
        fig = plt.figure(figsize=(20,20))
        ax = Axes3D(fig)
        surf=ax.plot_surface(X, Y, -Z,cmap=cm.summer,
                       linewidth=0, antialiased=False,alpha=0.5,vmin=vmin,vmax=0)
        ax.set_zlim(vmin,0)
        plt.title(str(annee)+" - "+str(i))
        fig.colorbar(surf, shrink=0.5, aspect=5)


        fig.savefig("images/"+str(u)+".png")
        u=u+1
