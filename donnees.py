#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 15:50:06 2018

@author: amarouani
"""

##Script permettant d'isoler la zone selectionnée selon le format choisi données-jours ou données-pixel
from matplotlib import cm

#taille de la carte initial
Z=[0,80,0,80]
#Limitationde la zone d'étude 
bord=[0, 47, 3, 56]
###ANNEES MANQUANTE SUR LES MESURE DE VOLUME THRESHOLD
#m=[]

###################################################################################

MAP_C=cm.rainbow
PATH = "/net/argos/data/vog/tarlod/50ans/"
import numpy as np
import init_donnees as id
import pandas as pd

###################################################################################

# Retrait des années manquante pour les variables IS MLD, JOUR et LOCALISATION X ET Y
#m=np.array(m)-63
#del_=[]
#for i in m:
#    del_.extend(np.arange(i*120,(i+1)*120))
keep=np.arange(6000)
#keep=np.delete(keep,del_)
#
#MLD=MLD[keep]
#IS=IS[keep]



nl=Z[1]-Z[0]+1
nc=Z[3]-Z[2]+1
nl2=bord[1]-bord[0]+1
nc2=bord[3]-bord[2]+1

###################################################################################

#On définit un mask
MASK_CURR = np.zeros((nl,nc))
for i in np.arange(bord[0],bord[1]+1):
    for j in np.arange(bord[2],bord[3]+1):
        MASK_CURR[i,j]=1

###################################################################################

# lecture de toute les données
MLD=id.__read_mld(PATH)
IS=id.__read_IS(PATH,1000)
v_10,v_11,v_12=id.__read_vol_thr(PATH)
jour=[]
for i in keep:
    jour.extend(np.repeat(i,nl2*nc2))
jour=np.array(jour)
#dens_0=id.__read_voldens(PATH, '29.10')
#dens_1=id.__read_voldens(PATH, '29.11')
#dens_2=id.__read_voldens(PATH, '29.12')
#dens_3=id.__read_voldens(PATH, '29.13')

LOC_X=(np.tile(np.arange(bord[0],bord[1]+1),nc2)).reshape(1,-1)
LOC_X=np.tile(LOC_X,len(keep))
LOC_Y=np.repeat(np.arange(bord[2],bord[3]+1),nl2).reshape(1,-1)
LOC_Y=np.tile(LOC_Y,len(keep))

###################################################################################

jour=np.array(jour).reshape(1,-1)[0]
MLD=id.mask_data(MLD, MASK_CURR)
v_10=id.mask_data(v_10, MASK_CURR)
v_11=id.mask_data(v_11, MASK_CURR)
v_12=id.mask_data(v_12, MASK_CURR)
IS=id.mask_data(IS, MASK_CURR)
MLD2=MLD.reshape(1,-1)[0]
IS2=IS.reshape(1,-1)[0]
v_10=v_10.reshape(1,-1)[0]
v_11=v_11.reshape(1,-1)[0]
v_12=v_12.reshape(1,-1)[0]

###################################################################################

donnee_pixel=np.concatenate((jour.reshape(-1,1),LOC_X.reshape(-1,1),LOC_Y.reshape(-1,1),MLD2.reshape(-1,1),IS2.reshape(-1,1),v_10.reshape(-1,1),v_11.reshape(-1,1),v_12.reshape(-1,1)),axis=1)
donnee_jours=[]
for i in np.arange(len(donnee_pixel[:,0])/(nc2*nl2)):
    donnee_jours.append(donnee_pixel[(i*(nc2*nl2)):((i+1)*(nc2*nl2)),3:].reshape(1,-1)[0])
donnee_jours=np.array(donnee_jours).reshape(len(donnee_pixel[:,0])/(nc2*nl2),-1)

###################################################################################
# on normalise les données
donnee_jours=id.centred(donnee_jours)
donnee_pixel[:,3:]=id.centred(donnee_pixel[:,3:])

LOC_X=(np.tile(np.arange(bord[0],bord[1]+1),nc2)).reshape(1,-1)
LOC_X=np.repeat(LOC_X,5)
LOC_Y=np.repeat(np.arange(bord[2],bord[3]+1),nl2).reshape(1,-1)
LOC_Y=np.repeat(LOC_Y,5)
VAR=np.tile(['MLD','IS','rho10','rho11','rho12'],nl2*nc2)
VAR2=['Y','X','Y','MLD','IS','rho10','rho11','rho12'] 


data_day=pd.DataFrame(donnee_jours,columns=[ str(i)+"-"+str(j)+"_"+h for i,j,h in zip(LOC_X,LOC_Y,VAR)])

data_pix=pd.DataFrame(donnee_pixel,columns=VAR2)
data_day.to_csv()
data_pix.to_csv()
