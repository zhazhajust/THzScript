import constant as const
import Processing
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')

def plotDensity(E,xNumber,savedir):


#def plotE(E,x,title,savedir):
    #pngdir = const.gifdir + 'Field/'
    #os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    #savedir = pngdir + title + 'Field.jpg'

    ###plotField####
    ################ 
    #plt.figure(figsize=[4,3])
    x = np.linspace(0,const.x_end/1e-6,const.Nx)
    y = np.linspace(0,const.y_lenth/1e-6,const.Ny)
    X,Y = np.meshgrid(x,y)
    plt.pcolormesh(X[::int(E.shape[1]/500),::int(E.shape[0]/500)],Y[::int(E.shape[1]/500),::int(E.shape[0]/500)],E[::int(E.shape[0]/500),::int(E.shape[1]/500)].T)#,cmap = plt.cm.bwr)
    #plt.pcolormesh(X,Y,E.T,cmap=plt.cm.bwr)
    plt.colorbar()
    plt.xlabel('um')
    plt.ylabel('um')
    title = str(str(int(xNumber)*const.dt_snapshot/1e-15) + 'fs')
    plt.title(title)
    plt.savefig(savedir,dpi=160,bbox_inches = 'tight')
    plt.close('all')

def main(x):
    ####
    pngdir = const.gifdir + Field +'ElectronDensity/'
    os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    savedir = pngdir + str(x) + 'ElectronDensity.jpg'
    ####
    E = Processing.getEDensity(x)
    plotDensity(E,x,savedir)
if __name__ == '__main__':
    x = 1000
    savedir = const.figdir + str(x) + 'ElectronDensity.jpg'
    E = Processing.getEDensity(x)
    plotDensity(E,x,savedir)

