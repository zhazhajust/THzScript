import matplotlib as mpl
#import constant as const
from Processing import *

def plot(x,savedir):
    indexEk,Ek1d = EnergeMap(x,mode = 'median',setName='subset_selected1',particle='electron2')
    plt.plot(indexEk,Ek1d)
    plt.yscale('log')
    plt.xlabel('Ek[MeV]')
    plt.ylabel('count')
    plt.xlim([0,12.5])
    plt.ylim([1,1e5])
    plt.savefig(savedir)
    plt.close('all')

def main(x):
    savedir = const.figdir + 'EnergeMap' + str(x) + '.jpg'
    plot(x,savedir)#,cmap)

if __name__ == '__main__':
    x = 800
    main(x)
