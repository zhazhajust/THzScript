from Processing import *
import matplotlib as mpl

x = 1900


savedir = const.figdir + 'XY_' + str(x) + 'Stream.jpg'

#def getStream(x):
#    Sx,Sy,SPx,SPy,Ek,count = StreamE(x)
#    return Sx,Sy,SPx,SPy,Ek,count



def plotStream(x,savedir):
    Sx,Sy,SPx,SPy,Ek,count = StreamE(x)
    speed = np.sqrt(SPx**2 + SPy**2)
    #lw = 5*speed/speed.max()
    lw = np.log(count+1)/np.log(count+1).max() + 0.5
    plt.streamplot(Sx*1e6,Sy*1e6,SPx,SPy,linewidth = lw ,color = Ek,cmap = 'jet')
    cbar = plt.colorbar()
    cbar.set_label('average energe[MeV]')
    plt.xlabel('$\mu m$')
    plt.ylabel('$\mu m$')
    plt.xlim([const.x_min*1e6,const.x_max*1e6])
    plt.ylim([const.y_min*1e6,const.y_max*1e6])
    plt.title(str(int(int(x)*const.dt_snapshot/1e-15))+'fs')
    plt.savefig(savedir,bbox_inches = 'tight')
    plt.close('all')
    return

def main(x):
    savedir = const.figdir + 'XY_' + str(x) + 'Stream.jpg'
    #Sx,Sy,SPx,SPy,Ek,count = getStream(x)
    plotStream(x,savedir)

if __name__ == '__main__':
    x = 1200
    main(x)
