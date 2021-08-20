from EffScreen import *
import ScreenTHz
import matplotlib.pyplot as plt
import Processing
import matplotlib as mpl
import constant as const
plt.switch_backend('agg')

datadir = savedir
#datadir = '/home/yujq/users/caijie/epoch2d/txt/MassLimit/new_a3_w9.1_n0.2/y50x300/318.0$mu m$TimeSequence.npy'
Field = Processing.Field

savedir = const.figdir  + 'Screen'+ str(int(ScreenTHz.x_right/1e-6))+'um' + Field

print(datadir,savedir)
#data = np.load(datadir)
#data = np.array(data)

def plotField(theta,time,data):
    
    plt.pcolormesh(theta,time,data,cmap = plt.cm.bwr)
    plt.colorbar()
    plt.title(savedir + 'Field.jpg')
    plt.savefig(savedir + 'Field.jpg',dpi=160)
    plt.close('all')

######
def getFreqs(data):
    '''
    XF = np.fft.rfft(data,axis=0)

    freq = np.fft.rfftfreq(data.shape[0],d = dt)

    theta = np.linspace(-3.14/2,3.14/2,NTheta)

    Theta,Freq = np.meshgrid(theta,freq)
    ######
    #Theta , Freq = Theta*180/3.14 , Freq/1e12

    data = data[:,int(NTheta/4):int(-NTheta/4)]
    '''
    XF = np.fft.rfft(data,axis=0)

    freq = np.fft.rfftfreq(data.shape[0],d = dt)

    #theta = np.linspace(-3.14/2,3.14/2,int(NTheta/2))

    y = np.linspace(const.y_min,const.y_max,const.Ny)

    Y,Freq = np.meshgrid(y,freq)


    return Y , Freq , XF

def plotFreqs(Y,Freq,XF):
    #Theta , Freq = Theta*180/3.14 , Freq/1e12
    Freq = Freq/1e12
    Y = Y/1e-6
    #tmin = int(NTheta*75/90)
    #XF[Theta > 75] = 0
    #XF[Theta < -75] = 0
    #Freq[Theta > 75] = 0
    #Freq[Theta < -75] = 0
    #Theta[Theta < -75] = -0
    #Theta[Theta > 75] = 0
    XF[Freq > 30] = 0
    plt.pcolormesh(Y,Freq,np.abs(XF),cmap = plt.cm.jet)
    plt.colorbar()
    plt.xlabel('Y[$/mu m$]')
    plt.ylabel('Freqncey[THz]')
    plt.ylim([0,30])
    plt.title(savedir + 'Freqs.jpg')
    #plt.xlim([-75,75])
    plt.clim([0,50000])
    plt.savefig(savedir + 'Freqs.jpg',dpi=160)
    plt.close('all')

######
def THzFilter(Y , Freq , XF):
    XF[np.abs(Freq)>10e12]=0
    XF[np.abs(Freq)<0.1e12]=0

    Bz = np.fft.irfft(XF,axis = 0)
    Bz = Bz.real
    return Bz

def plotTHz(Y,Freq,data):
    plt.pcolormesh(data,cmap = plt.cm.bwr)
    plt.colorbar()
    plt.title(savedir + 'THz.jpg')
    plt.savefig(savedir + 'THz.jpg',dpi=160)
    plt.close('all')


def main():
    ####
    time = np.load(const.txtdir + 'Sequencetime.npy')
    #theta = np.linspace(-3.14/2,3.14/2,int(NTheta/2))
    y = np.linspace(const.y_min,const.y_max,const.Ny)
    
    Y , Time = np.meshgrid(y,time)

    ####
    data = np.load(datadir)
    data = np.array(data)
    #data = data[:,int(NTheta/4+1/2):int(-NTheta/4)]
    plotField(Y,Time,data)    
    Y , Freq , XF = getFreqs(data)
    plotFreqs(Y,Freq,XF)
    Bz = THzFilter(Y , Freq , XF)
    plotTHz(Y,Time,Bz)


if __name__ == '__main__':
    main()
