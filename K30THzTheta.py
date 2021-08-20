from scipy.interpolate import interpn
import sdf
import constant as const
import numpy as np
import matplotlib.pyplot as plt
import os
import Processing
import colorbar

plt.switch_backend('agg')

#cmap = colorbar.cmap_trans
####
####constant####
pi = 3.1415926
delta_x=const.delta_x
delta_y=const.delta_y
#####
#####




def unravel(Kx,Ky,Kxy):
    #######unravel########
    _1DKxy=Kxy.flatten()
    _1DKx=Kx.flatten()
    _1DKy=Ky.flatten()
    maxK = Kxy.max()
    KKxy=_1DKxy[_1DKxy>maxK/100]
    KKy=_1DKy[_1DKxy>maxK/100]
    KKx=_1DKx[_1DKxy>maxK/100]

    #KKx[KKx==0] = 1/np.inf

    #KKxy=KKxy[KKx!=0]
    #KKy=KKy[KKx!=0]
    #KKx=KKx[KKx!=0]

    return KKx,KKy,KKxy

def getThetaK(KKx,KKy):
    ######theta , k generator####
    #theta = np.arctan(KKy/KKx)
    #K = np.sqrt(KKx**2+KKy**2)

    K = np.sqrt(KKx**2+KKy**2)
    KKy[KKy==0] = 1/1e12
    KKx[KKx==0] = 1/1e12
    theta = np.arctan(KKy/KKx)
    #print(theta)
    return theta,K

def ThetaMax(theta,K,KKxy):
    Limit = 10
    #theta = theta[K<Limit]
    #K = K[K<Limit]
    #KKxy = KKxy[K<Limit]
    I = np.zeros(181)
    Phi = np.arange(-90,91,1)
    for i in range(len(theta)): 
            I[int(90 + theta[i]*180/pi)] += np.abs(KKxy[i])**2
            #I[int(theta[i]*180/pi)] += np.abs(KKxy[i])**2

    ######
    minTheta = 0
    maxTheta = 25 #degree
    #print(Phi)
    #print(I)
    ETotal = np.sum(I)
    I2 = I.copy()
    I2[np.abs(Phi)<minTheta] = 0
    I2[np.abs(Phi)>maxTheta] = 0
    #print(I)
    ETheta = np.sum(I2)
    print(ETheta,ETotal,ETheta/ETotal)


    return Phi,I


def drawMaxTheta(Phi,I,x,savedir,title):
    #savedir = pngdir + + 'polar' + str(x) + 'Ktheta.jpg'
    #savedir = const.figdir + 'polar' + str(x) + 'Ktheta.jpg'
    ####plot####
    #plt.subplot(projection = "polar")
    #plt.pcolormesh(Theta,K*c/2/pi/fthz,Value.T,cmap=plt.cm.jet)
    #plt.scatter(theta[K<Limit],K[K<Limit],s=5,marker = ',',c=KKxy[K<Limit],cmap=cmap)#,alpha= 0.7)
    #plt.scatter(theta,K,s=0.1,marker = '.',c=KKxy,cmap=plt.cm.jet)
    
    #plt.colorbar()

    plt.plot(Phi,I,'b.-')
    plt.xlabel('THeta')
    plt.ylabel('I')
    #plt.title(str(float(x)*const.dt_snapshot/1e-15) + 'fs')
    plt.title(title)
    plt.savefig(savedir,dpi=160,bbox_inches = 'tight')
    plt.close('all')

def main(x,Field,Limit,savedir):
    if Field == 'Bz':
        bz , title = Processing.getBz(x)
    if Field == 'Ey':
        bz ,title = Processing.getEy(x)
    #Kx,Ky,Kxy = Processing.getKBz(bz)
    Kx,Ky,Kxy = Processing.FFt(bz)
    Kx,Ky,Kxy = Processing.KTHz(Kx,Ky,Kxy)#,R1 = 0.1,R2 = 10) 
    KKx,KKy,KKxy = unravel(Kx,Ky,Kxy)
    theta,K = getThetaK(KKx,KKy)
    Phi,I = ThetaMax(theta,K,KKxy)

    drawMaxTheta(Phi,I,x,savedir,title)

if __name__ == '__main__':
    x = 1300
    Limit = 10
    ####
    pngdir = const.gifdir + 'MaxTheta/'
    os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    savedir = const.figdir + 'F' + str(Limit)+'polar' + str(x) + 'KMaxtheta.jpg'
    main(x,'Bz',Limit,savedir)
    #main(x,Limit)
