from scipy.interpolate import interpn
import sdf
import constant as const
import numpy as np
import matplotlib.pyplot as plt
import os
import Processing
import colorbar
import math
plt.switch_backend('agg')

#cmap = colorbar.cmap_trans
####
####constant####
c = 299792458
pi = 3.1415926
delta_x=const.delta_x
delta_y=const.delta_y
#####
#####

#x = 2900

#Limit = 500


'''
def getBz(x):
    #savedir = const.figdir + 't' + str(x) + 'Ktheta.jpg'
    
    
    ####read sdf####
    sdfdir=const.sdfdir +str(x).zfill(const.filenumber)+".sdf"
    data=sdf.read(sdfdir,dict=True)
    Bz=data['Magnetic Field/Bz']
    bz=Bz.data
    #k_bz=np.fft.fft2(bz)
    return bz

def getKBz(bz):
    ####fourier transform#####
    k_bz2d=np.fft.fft2(bz)
    #fig,axs=plt.subplots(figsize=[4,3])
    #k0=2*pi/10.6e-6
    k0=2*pi*1e12/3e8
    kx=np.linspace(0,pi/delta_x/k0,int(const.Nx/2))
    ky=np.linspace(0,pi/delta_y/k0,int(const.Ny/2))
    Ky,Kx=np.meshgrid(ky,kx)
    Kxy=np.abs(k_bz2d[:int(const.Nx/2),:int(const.Ny/2)])#**2
    return Kx,Ky,Kxy
'''


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
    KKxy=KKxy[KKx>0]
    KKy=KKy[KKx>0]
    KKx=KKx[KKx>0]
    return KKx,KKy,KKxy

def getThetaK(KKx,KKy):
    ######theta , k generator####
    theta = np.arctan(KKy/KKx)
    K = np.sqrt(KKx**2+KKy**2)
    return theta,K

def plotPolar(theta,K,KKxy,Limit,savedir,cmap):
    #savedir = pngdir + + 'polar' + str(x) + 'Ktheta.jpg'
    #savedir = const.figdir + 'polar' + str(x) + 'Ktheta.jpg'
    ####plot####
    plt.subplot(projection = "polar")
    #plt.pcolormesh(Theta,K*c/2/pi/fthz,Value.T,cmap=plt.cm.jet)
    plt.scatter(theta[K<Limit],K[K<Limit],s=5,marker = ',',c=KKxy[K<Limit],cmap=cmap)#,alpha= 0.7)
    #plt.scatter(theta,K,s=0.1,marker = '.',c=KKxy,cmap=plt.cm.jet)
    
    plt.colorbar()
    plt.xlabel('THz')
    plt.ylabel('Theta')
    plt.savefig(savedir,dpi=160,bbox_inches = 'tight')

def getRofK(THzmin,THzmax):
    #R1 = 2 * pi / c / THzmin
    #R2 = 2 * pi / c / THzmax
    kmin = 2*pi*THzmin/c
    kmax = 2*pi*THzmax/c

    return kmin , kmax
def plotE(E,x,savedir,title):
    #const.figdir + str(x) + str(E) + 'Field.jpg'
    plt.figure(figsize=[4,3])
    x = np.linspace(0,const.x_end/1e-6,const.Nx)
    y = np.linspace(0,const.y_lenth/1e-6,const.Ny)
    X,Y = np.meshgrid(x,y)
    plt.pcolormesh(X[::int(E.shape[1]/500),::int(E.shape[0]/500)],Y[::int(E.shape[1]/500),::int(E.shape[0]/500)],E[::int(E.shape[0]/500),::int(E.shape[1]/500)].T)
    #plt.pcolormesh(X,Y,E.T,cmap=plt.cm.bwr)
    plt.colorbar()
    plt.xlabel('um')
    plt.ylabel('um')
    #title = str(str(float(x)*const.dt_snapshot/1e-15) + 'fs')
    plt.title(title)
    plt.savefig(savedir,dpi=160,bbox_inches = 'tight')
    plt.close('all')
def main(x,savedir):#,Limit,cmap):
    bz , title = Processing.getBz(x)
    limit_min = 0.1e12
    limit_max = 10e12
    R1 , R2  = getRofK(0.1e12,10e12)

    #####
    #delta_kx = 3.14 / const.delta_x / (const.Nx / 2) 
    #R1 = math.ceil(2 * pi * limit_min/c/delta_kx)
    #R2 = int(2 * pi * limit_max/c/delta_kx)

    print('R1,R2',R1,R2)
    ####Kpolar####
    ##############
    #Kx,Ky,Kxy = Processing.getKBz(bz)
    #KKx,KKy,KKxy = unravel(Kx,Ky,Kxy)
    #theta,K = getThetaK(KKx,KKy)

    KBz = np.fft.fft2(bz)
    KBz=Processing.Kfilter(KBz,R1,R2)
 

    BzTHz = np.fft.ifft2(KBz)
    BzTHz = BzTHz.real
    print('eff',np.sum(np.sum(np.square(BzTHz)))/np.sum(np.sum(np.square(bz))))
    #savedir = const.figdir + str(x) + str('BzTHz') + 'Field.jpg'
    #plotE(bz,x,savedir)
    plotE(BzTHz,x,savedir,title)
    #plotPolar(theta,K,KKxy,Limit,savedir,cmap)

if __name__ == '__main__':
    x = 1900
    #Limit = 30
    ####
    #iname = 'jet'

    #main(x)
    #KBz=Kfilter(KBz)
    #cmap = colorbar.getTransCmap(lambda x:(0.7 + (1/256*x) *0.3),iname)
    pngdir = const.gifdir + 'BzThz/'
    os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    savedir = const.figdir +'_' + str(x) + 'THz.jpg'
    #main(x,Limit,savedir,cmap)
    main(x,savedir)
