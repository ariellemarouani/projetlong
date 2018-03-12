from matplotlib import cm

Z=[0,80,0,80]
MAP_C=cm.rainbow
PATH = "/net/argos/data/vog/tarlod/50ans/"
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image

# Create a 1024x1024x3 array of 8 bit unsigned integers
import init_donnees as id

def filtre_median(matrix,nl,nc,bord,nb):
    res=np.array(matrix)
    pixels=[]
    for i in np.arange(bord,nl-bord+1):
        for j in np.arange(bord,nc-bord+1):
            curr=list(matrix[(i-bord):(i+bord+1),j])
            del curr[bord]
            curr.extend(list(matrix[i,(j-bord):(j+bord+1)]))
            m=np.median(curr)
            r=res[i,j]
            if(r!=m):
                pixels.append([nb,i,j,r])
            res[i,j]=m
            
    return res,pixels


nl=Z[1]-Z[0]+1
nc=Z[3]-Z[2]+1

conv_=id.__read_mld(PATH)
MAX=MAX_81_81 #truc à importer depuis l'explorateur de variable
MAX_LISSE,pixs=filtre_median(MAX,nl,nc,1,1)

mat=MAX_LISSE
lim=600
bord_g=[]
for i in np.arange(nl):
    j=0
    while mat[i,j]<lim and j<(nc-1):
        j=j+1
        
    bord_g.append(j)
        
bord_g=min(bord_g)
        
bord_d=[]
for i in np.arange(nl):
    j=nc-1
    while mat[i,j]<lim and j>0:
        j=j-1
    bord_d.append(j)
bord_d=max(bord_d)   

bord_h=[]
for j in np.arange(nc):
    i=0
    while mat[i,j]<lim and i<(nl-1): 
        i=i+1
    bord_h.append(i)
bord_h=min(bord_h)
        
bord_b=[]
for j in np.arange(nc):
    i=nl-1
    while mat[i,j]<lim and i>0:
        i=i-1
    bord_b.append(i)

bord_b=max(bord_b)   

buff=bord_b
bord_b=bord_h
bord_h=buff

print(bord_b,bord_h,bord_d,bord_g)

x = np.linspace(Z[0],Z[1],nl)
y = np.linspace(Z[2],Z[3],nc)
X, Y = np.meshgrid(x, y)

CARRE_X=list(np.repeat(bord_g,bord_h-bord_b+1))
CARRE_X.extend(np.arange(bord_g,bord_d+1))
CARRE_X.extend(np.repeat(bord_d,bord_h-bord_b+1))
CARRE_X.extend(np.arange(bord_g,bord_d+1))

CARRE_Y=list(np.arange(bord_b,bord_h+1))
CARRE_Y.extend(np.repeat(bord_h,bord_d-bord_g+1))
CARRE_Y.extend(np.arange(bord_b,bord_h+1))
CARRE_Y.extend(np.repeat(bord_b,bord_d-bord_g+1))
fig = plt.figure(figsize=(15,15))
ax = Axes3D(fig)
surf=ax.plot_surface(X, Y, -MAX,cmap=MAP_C,
                     linewidth=0, antialiased=False,alpha=0.5)

fig.colorbar(surf, shrink=0.5, aspect=5)
ax.set_title("Maximum de convection pour la zone ("+str(Z[0])+","+str(Z[1])+"),("+str(Z[2])+","+str(Z[3])+")",fontsize= 30)

fig.savefig("images/"+str(Z[0])+"_"+str(Z[1])+"-"+str(Z[2])+"_"+str(Z[3])+"3D.png")


GRAD=(MAX-np.min(MAX))/(np.max(MAX)-np.min(MAX))

fig, axes = plt.subplots()
axes.imshow(-GRAD, aspect='auto', cmap=MAP_C)
axes.plot(CARRE_X,CARRE_Y,color='black')
fig.colorbar(surf, shrink=0.5, aspect=5)
ax.set_title("Maximum de convection pour la zone ("+str(Z[0])+","+str(Z[1])+"),("+str(Z[2])+","+str(Z[3])+")",fontsize= 30)
fig.savefig("images/"+str(Z[0])+"_"+str(Z[1])+"-"+str(Z[2])+"_"+str(Z[3])+"2D.png")


AIR=[]
for lim in np.arange(0,2501,100):
    bord_g=[]
    for i in np.arange(nl):
        j=0
        while mat[i,j]<lim and j<(nc-1):
            j=j+1
        
        bord_g.append(j)
        
    bord_g=min(bord_g)
        
    bord_d=[]
    for i in np.arange(nl):
        j=nc-1
        while mat[i,j]<lim and j>0:
            j=j-1
        bord_d.append(j)
    bord_d=max(bord_d)   
    
    bord_h=[]
    for j in np.arange(nc):
        i=0
        while mat[i,j]<lim and i<(nl-1): 
            i=i+1
        bord_h.append(i)
    bord_h=min(bord_h)
            
    bord_b=[]
    for j in np.arange(nc):
        i=nl-1
        while mat[i,j]<lim and i>0:
            i=i-1
        bord_b.append(i)
    
    bord_b=max(bord_b)   
    
    buff=bord_b
    bord_b=bord_h
    bord_h=buff
    AIR.append((bord_h-bord_b)*(bord_d-bord_g))
    
    x = np.linspace(Z[0],Z[1],nl)
    y = np.linspace(Z[2],Z[3],nc)
    X, Y = np.meshgrid(x, y)
    
    CARRE_X=list(np.repeat(bord_g,bord_h-bord_b+1))
    CARRE_X.extend(np.arange(bord_g,bord_d+1))
    CARRE_X.extend(np.repeat(bord_d,bord_h-bord_b+1))
    CARRE_X.extend(np.arange(bord_g,bord_d+1))
    
    CARRE_Y=list(np.arange(bord_b,bord_h+1))
    CARRE_Y.extend(np.repeat(bord_h,bord_d-bord_g+1))
    CARRE_Y.extend(np.arange(bord_b,bord_h+1))
    CARRE_Y.extend(np.repeat(bord_b,bord_d-bord_g+1))
    
    fig, axes = plt.subplots()
    axes.imshow(-GRAD, aspect='auto', cmap=MAP_C)
    plt.title("Zone contenant les MLD > "+str(lim)+"m")

    axes.plot(CARRE_X,CARRE_Y,color='black')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    fig.savefig("images/zone/zone"+str(lim)+".png")
    plt.show()

plt.plot(np.arange(0,2501,100),AIR)
plt.xlabel('MDL la plus petite')
plt.ylabel('Air de la zone')
plt.savefig("images/coude.png")

q3=[]
vect=np.array([abs(i) for i in PIXELFILTRE[:,3]])
for p in np.arange(100):
    q3.append(np.percentile(vect, p))

plt.plot(np.arange(100),q3)
plt.xlabel("Percentiles")
plt.ylabel("Ecart entre la MLD de base\net apres filtre median")
plt.savefig("images/quartile.png")

plt.hist(vect[vect>=q3[90]], bins=1000)
plt.xlabel("Ecart entre la MLD de base et apres filtre median")
plt.ylabel("Nombre de points")
plt.savefig("images/histo.png")

a=0
for i in vect:
    if i>=100:
        a+=1
b=a/11691197.
