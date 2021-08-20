import matplotlib.pyplot as plt
import os
import Processing
import numpy as np
import constant as const
plt.switch_backend('agg')

Field = 'Bz'

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
    X = X/1e-6
    Y = Y/1e-6
    plt.figure(figsize=[4,3])
    im = plt.pcolormesh(X[::int(E.shape[1]/500),::int(E.shape[0]/500)],Y[::int(E.shape[1]/500),::int(E.shape[0]/500)],E[::int(E.shape[0]/500),::int(E.shape[1]/500)].T,cmap = plt.cm.bwr)#

    #im = plt.pcolormesh(X,Y,E.T,cmap = plt.cm.bwr)

    #,norm=mpl.colors.LogNorm())
    #plt.pcolormesh(X,Y,E.T,cmap=plt.cm.bwr)
    cbar = plt.colorbar()
    im.set_clim([-(np.abs(E)).max(),(np.abs(E)).max()])
    plt.xlabel('um')
    plt.ylabel('um')
    plt.xlim([0,400])
    plt.ylim([-200,200])
    #title = str(str(float(x)*const.dt_snapshot/1e-15) + 'fs')
    plt.title(title)
    plt.savefig(savedir,dpi=160,bbox_inches = 'tight')
    plt.close('all')

def plotFieldWrapper(E,x,title,Field):
    pngdir = const.gifdir + Field + 'Field/'
    os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    savedir = const.figdir + title + 'Field.jpg'
    plotE(E,x,title,savedir)

def main(x):
    ey ,title = Processing.getBz(x)
    plotFieldWrapper(ey,x,title,Field)

if __name__ == '__main__':
    x = 1500
    #pngdir = const.gifdir + 'BzThz/'
    #os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    #savedir = const.figdir +'_' + str(x) + 'THz.jpg'
    main(x)
