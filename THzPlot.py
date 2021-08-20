from scipy.interpolate import interpn
import sdf
import constant as const
import numpy as np
import matplotlib.pyplot as plt
import os
import Processing
import colorbar
import math
import KTHzTheta
import KTHzPolar as Kpolar
import pandas as pd
import matplotlib as mpl
plt.switch_backend('agg')

#cmap = colorbar.cmap_trans
####
####constant####
c = 299792458
pi = 3.1415926
fs = 1e-15
delta_x=const.delta_x
delta_y=const.delta_y
#####
Limit = Processing.Limit #10
#####
def creatCSV(Field):
    df = pd.DataFrame(columns = ['index','ETHz','ETotal'])
    filepath = const.txtdir + str(Field) + '_' +str(Limit) + 'THz' +'Ksqrt.csv'
    #print(df)
    #if os.path.exists(filepath)==True:
    df.to_csv(filepath,mode = 'w', index = False)
    #os.remove(filepath)
    return



def plotE(E,x,title,savedir):
    #pngdir = const.gifdir + 'Field/'
    #os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    #savedir = pngdir + title + 'Field.jpg'

    ###plotField####
    ################ 
    #plt.figure(figsize=[4,3])
    #x = np.linspace(0,const.x_end/1e-6,const.Nx)
    #y = np.linspace(0,const.y_lenth/1e-6,const.Ny)
    x = np.linspace(const.x_min+const.delta_x/2,const.x_end-const.delta_x/2,const.Nx)
    y = np.linspace(const.y_min+const.delta_y/2,const.y_max-const.delta_y/2,const.Ny)


    X,Y = np.meshgrid(x,y)
    im = plt.pcolormesh(X[::int(E.shape[1]/500),::int(E.shape[0]/500)],Y[::int(E.shape[1]/500),::int(E.shape[0]/500)],E[::int(E.shape[0]/500),::int(E.shape[1]/500)].T,cmap = plt.cm.bwr)#

    #im = plt.pcolormesh(X,Y,E.T,cmap = plt.cm.bwr)

    #,norm=mpl.colors.LogNorm())
    #plt.pcolormesh(X,Y,E.T,cmap=plt.cm.bwr)
    cbar = plt.colorbar()
    im.set_clim([-(np.abs(E)).max(),(np.abs(E)).max()])
    plt.xlabel('um')
    plt.ylabel('um')
    #title = str(str(float(x)*const.dt_snapshot/1e-15) + 'fs')
    plt.title(title)
    plt.savefig(savedir,dpi=160,bbox_inches = 'tight')
    plt.close('all')

def plotELog(E,x,title,savedir):
    #pngdir = const.gifdir + 'Field/'
    #os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    #savedir = pngdir + title + 'Field.jpg'

    ###plotField####
    ################ 
    #plt.figure(figsize=[4,3])
    #x = np.linspace(0,const.x_end/1e-6,const.Nx)
    #y = np.linspace(0,const.y_lenth/1e-6,const.Ny)
    x = np.linspace(const.x_min+const.delta_x/2,const.x_end-const.delta_x/2,const.Nx)
    y = np.linspace(const.y_min+const.delta_y/2,const.y_max-const.delta_y/2,const.Ny)


    X,Y = np.meshgrid(x,y)
    im = plt.pcolormesh(X[::int(E.shape[1]/500),::int(E.shape[0]/500)],Y[::int(E.shape[1]/500),::int(E.shape[0]/500)],E[::int(E.shape[0]/500),::int(E.shape[1]/500)].T,cmap = plt.cm.bwr,norm=mpl.colors.LogNorm())
    #plt.pcolormesh(X,Y,E.T,cmap=plt.cm.bwr)
    cbar = plt.colorbar()
    im.set_clim([-(np.abs(E)).max(),(np.abs(E)).max()])
    plt.xlabel('um')
    plt.ylabel('um')
    #title = str(str(float(x)*const.dt_snapshot/1e-15) + 'fs')
    plt.title(title)
    plt.savefig(savedir,dpi=160,bbox_inches = 'tight')
    plt.close('all')
def KpolarWrapper(bz,x,title,Field):
    #Limit = 10
    ####
    iname = 'jet'
    cmap = colorbar.getTransCmap(lambda x:(0.7 + (1/256*x) *0.3),iname)
    pngdir = const.gifdir + Field +'Kpolarpng/'
    os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    savedir = pngdir +'THz' + str(Limit)+ 'polar' + str(x) + 'Ktheta.jpg'
    ##############


    #######transform######
    ######################
    #Kx,Ky,Kxy = Processing.getKBz(bz)
    Kx,Ky,Kxy = Processing.FFt(bz)
    ETotal = np.sum(np.sum(np.square(np.abs(Kxy))))/const.Nx/const.Ny
    Kx,Ky,Kxy = Processing.KTHz(Kx,Ky,Kxy,R1=0.1,R2 = Limit)
    ETHz = np.sum(np.sum(np.square(np.abs(Kxy))))/const.Nx/const.Ny
    ######
    #print(ETotal)
    #print('Eff:',ETHz/ETotal)
    #############################
    ######  add eff to csv  #####
    #############################
    cars = {'index':[x],
            'ETHz':[ETHz],
            'ETotal':[ETotal]
            }
    df = pd.DataFrame(cars, columns = ['index','ETHz','ETotal'])
    filepath = const.txtdir + str(Field) + '_' +str(Limit) + 'THz' +'Ksqrt.csv'
    #print(df)
    if os.path.exists(filepath)==True:
        df.to_csv(filepath,mode = 'a',header = False , index = False)
    else:
        df.to_csv(filepath,mode = 'a',index = False)
    #########


    KKx,KKy,KKxy = Kpolar.unravel(Kx,Ky,Kxy)
    theta,K = Kpolar.getThetaK(KKx,KKy)
    Kpolar.draw(theta,K,KKxy,x,Limit,savedir,title,cmap)

    #######
    Phi,I = KTHzTheta.ThetaMax(theta,K,KKxy)
    return Phi,I

def KTHzThetaWrapper(Phi,I,x,title,Field):
    pngdir = const.gifdir + Field +'MaxTheta/'
    os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    savedir = pngdir + str(Limit) +'THz_180' + 'polar' + str(x) + 'KMaxtheta.jpg'
    KTHzTheta.drawMaxTheta(Phi,I,x,savedir,title)


def plotFieldWrapper(E,x,title,Field):
    pngdir = const.gifdir + Field + 'Field/'
    os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    savedir = pngdir + title + 'Field.jpg'
    plotE(E,x,title,savedir)

def plotTHzWrapper(bz,R1,R2,x,title,Field):
    #KBz = np.fft.fft2(bz)
    #KBz=Processing.Kfilter(KBz,R1,R2)

    Kx,Ky,Kxy = Processing.FFt(bz)
    KBz = Processing.KFilter(Kx,Ky,Kxy,R1 = 0.1,R2 = 10)
    BzTHz = np.fft.ifft2(KBz)

    #KTotal = np.sum(np.sum(np.square(np.abs(Kxy))))
    #Kx,Ky,BzTHz = Processing.KTHz(Kx,Ky,Kxy)
    BzTHz = BzTHz.real
    #KTHz = np.sum(np.sum(np.square(np.abs(BzTHz))))
    #print('eff',KTHz/KTotal)

    BzTotal = np.sum(np.sum(np.square(bz)))
    BzTHzTotal = np.sum(np.sum(np.square(BzTHz)))
    #print('eff',BzTHzTotal/BzTotal)


    pngdir = const.gifdir + Field + 'THzField/'
    os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    savedir = pngdir + title + 'THzField.jpg'
    plotE(BzTHz,x,title,savedir)
    return BzTotal,BzTHzTotal


def main(x,Field = 'Bz'):
    if Field == 'Bz':
        bz , title = Processing.getBz(x)
    if Field == 'Ey':
        bz , title = Processing.getEy(x)
    if Field == 'Ez':
        bz , title = Processing.getEz(x)
    #plotE(bz,x,title)
    plotFieldWrapper(bz,x,title,Field)
    limit_min = 0.1e12
    limit_max = 10e12
    R1 , R2  = 0.1 , 10 #Processing.getRofK(0.1e12,10e12)

    #####
    #delta_kx = 3.14 / const.delta_x / (const.Nx / 2) 
    #R1 = math.ceil(2 * pi * limit_min/c/delta_kx)
    #R2 = int(2 * pi * limit_max/c/delta_kx)

    #print('R1,R2',R1,R2)
    ####Kpolar####
    ##############
    Phi , I = KpolarWrapper(bz,x,title,Field)
    #####KTHzTheta######
    ####################
    #Phi,I = KTHzTheta.ThetaMax(theta,K,KKxy)
    KTHzThetaWrapper(Phi,I,x,title,Field)
    #####plotKpolar#####
    ####################
    #KpolarWrapper(bz,x,title,Field)
    #KpolarWrapper(theta,K,KKxy,x,title,Field)
    ######plotTHz######
    ###################
    BzTotal , BzTHzTotal = plotTHzWrapper(bz,R1,R2,x,title,Field)
    '''
    try:
        filepath = const.txtdir + 'Fieldsqrd.csv'
        df = pd.read_csv(filepath, encoding=None) 
    except:
        filepath = const.txtdir + 'Fieldsqrd.csv'
        df = pd.read_csv(filepath, encoding=None)
    df.loc[x] = [BzTotal,BzTHzTotal]
    '''
if __name__ == '__main__':
    x = 1200
    #pngdir = const.gifdir + 'BzThz/'
    #os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    #savedir = const.figdir +'_' + str(x) + 'THz.jpg'
    main(x,Field = 'Bz')
