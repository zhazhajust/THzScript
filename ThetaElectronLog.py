import matplotlib as mpl
#import constant as const
from Processing import *

def plotThetaE(x,savedir):#,cmap):
    Theta,K,Value = ThetaElectronLog(x,mode = 'log')
    #plt.pcolormesh(Theta,K,Value)#,norm=mpl.colors.LogNorm())
    #plt.subplot(projection = "polar")
    #im=plt.contourf(Theta,K,Value+1,cmap ='jet',norm=mpl.colors.LogNorm())
    im=plt.pcolormesh(Theta,K,Value+1,cmap ='jet',norm=mpl.colors.LogNorm())
    plt.xscale('log')
    #plt.scatter(K[:90,:90],Theta[:90,:90],s = 0.1,c=Value.T)
    plt.xlabel('Energe[MeV]')
    plt.ylabel('Theta')
    cbar = plt.colorbar()
    #im.set_clim([0,0.01])
    cbar.set_label('Cell Number Count')
    #plt.xlim([0,1e-15])
    plt.savefig(savedir)
    plt.close('all')

def main(x):
    savedir = const.figdir + 'ThetaE' + str(x) + 'KthetaLog.jpg'
    plotThetaE(x,savedir)#,cmap)

if __name__ == '__main__':
    x = 1900
    main(x)
