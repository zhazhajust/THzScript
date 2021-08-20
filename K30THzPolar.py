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
    #maxK = (Kxy[int(const.Nx/2):,int(const.Ny/2):]).max()
    maxK = Kxy[:int(const.Nx/2),:int(const.Ny/2)].max()
    KKxy=_1DKxy[_1DKxy>maxK/100]
    KKy=_1DKy[_1DKxy>maxK/100]
    KKx=_1DKx[_1DKxy>maxK/100]
    #KKx[KKx==0] = 1/np.inf
    print(KKxy.shape,KKx.shape,KKy.shape)
    #KKxy=KKxy[KKx>0]
    #KKy=KKy[KKx>0]
    #KKx=KKx[KKx>0]
    #KKx[KKx==0] = 1/np.inf
    print(KKxy.shape,KKx.shape,KKy.shape)
    return KKx,KKy,KKxy

def getThetaK(KKx,KKy):
    ######theta , k generator####
    #theta = np.arctan(KKy/KKx)
    #K = np.sqrt(KKx**2+KKy**2)
    
    K = np.sqrt(KKx**2+KKy**2)
    KKx[KKx==0] = 1/1e12
    KKy[KKy==0] = 1/1e12
    theta = np.arctan(KKy/KKx)
    #return theta,K
    return theta,K

def draw(theta,K,KKxy,x,Limit,savedir,title,cmap):
    #savedir = pngdir + + 'polar' + str(x) + 'Ktheta.jpg'
    #savedir = const.figdir + 'polar' + str(x) + 'Ktheta.jpg'
    ####plot####
    plt.subplot(projection = "polar")
    #plt.pcolormesh(Theta,K*c/2/pi/fthz,Value.T,cmap=plt.cm.jet)
    print(KKxy[K<Limit].max(),np.argmax(KKxy[K<Limit]))
    #plt.scatter(theta[K<Limit],K[K<Limit],s=5,marker = ',',c=KKxy[K<Limit],cmap=cmap)#,alpha= 0.7)
    plt.scatter(theta,K,s=5,marker = ',',c=KKxy,cmap=cmap)#,alpha= 0.7)
    #plt.scatter(theta,K,s=0.1,marker = '.',c=KKxy,cmap=plt.cm.jet)
    plt.colorbar()
    plt.xlabel('THz')
    plt.ylabel('Theta')
    #plt.title(str(float(x)*const.dt_snapshot/1e-15) + 'fs')
    plt.title(title)
    plt.savefig(savedir,dpi=160,bbox_inches = 'tight')
    plt.close('all')

def main(x,Limit,savedir,cmap):
    #bz ,title = Processing.getBz(x)
    bz ,title = Processing.getBz(x)
    Kx,Ky,Kxy = Processing.FFt(bz)
    Kx,Ky,Kxy = Processing.KTHz(Kx,Ky,Kxy)
    #Kx,Ky,Kxy = Processing.getKBz(bz)
    Kxy = np.abs(Kxy)
    print(Kxy.shape)
    KKx,KKy,KKxy = unravel(Kx,Ky,Kxy)
    theta,K = getThetaK(KKx,KKy)
    draw(theta,K,KKxy,x,Limit,savedir,title,cmap)

if __name__ == '__main__':
    x = 1200
    Limit = 10
    ####
    iname = 'jet'
    cmap = colorbar.getTransCmap(lambda x:(0.7 + (1/256*x) *0.3),iname)
    pngdir = const.gifdir + 'Kpolarpng/'
    os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    savedir = const.figdir + 'test' + str(Limit)+'KPolar' + str(x) + 'Ktheta.jpg'
    main(x,Limit,savedir,cmap)
    #main(x,Limit)
