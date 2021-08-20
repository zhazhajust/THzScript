import matplotlib as mpl
#import constant as const
from Processing import *

def plotThetaE(x,savedir):#,cmap):
    Ek,Theta,Value = ThetaElectron(x,mode = 'median')
    #plt.pcolormesh(Theta,K,Value)#,norm=mpl.colors.LogNorm())
    #plt.subplot(projection = "polar")
    #im=plt.pcolormesh(Theta[:90,:90],K[:90,:90],Value/Value.max(),cmap ='jet',shading='gouraud')
    im = plt.contourf(Ek[:90,:90],Theta[:90,:90]*180/pi,Value/Value.max(),cmap ='jet')
    #plt.scatter(K[:90,:90],Theta[:90,:90],s = 0.1,c=Value.T)
    plt.xlabel('Energe[MeV]')
    plt.ylabel('Theta')
    plt.title(str(int(int(x)*const.dt_snapshot/1e-15))+'fs')
    cbar = plt.colorbar()
    #im.set_clim([0,0.01])
    cbar.set_label('Cell Number Count')
    #plt.xlim([0,1e-15])
    plt.savefig(savedir)
    plt.close('all')

def main(x):
    savedir = const.figdir + 'ThetaE' + str(x) + 'median.jpg'
    plotThetaE(x,savedir)#,cmap)

if __name__ == '__main__':
    x = 1200
    main(x)
