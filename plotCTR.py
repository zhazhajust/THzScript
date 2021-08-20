from EffFinal import *
from getCircle import *
import matplotlib.pyplot as plt
import Processing
import matplotlib as mpl
import sys
plt.switch_backend('agg')

pi = 3.1415926

datadir = savedir
#datadir = '/home/yujq/users/caijie/epoch2d/txt/MassLimit/new_a3_w9.1_n0.2/y50x300/318.0$mu m$TimeSequence.npy'
Field = Processing.Field

savedir = const.figdir + 'R' +str(int(R/1e-6)) + 'x' + str(int(point[0]/1e-6)) + Field

print(datadir,savedir)
#data = np.load(datadir)
#data = np.array(data)

R = 350e-6
if len(sys.argv) > 2:
    R = sys.argv[2]
    R = float(R)
maxY = (const.y_max - const.y_min)/2
if R > maxY:
    thetaMax = np.arcsin(maxY/R)
else:
    thetaMax = pi/2

def plotField(Theta,Time,data,savedir):
    Theta , Time = Theta*180/3.14 , Time/1e-15
    #plt.pcolormesh(theta,time,data,cmap = plt.cm.bwr)
    plt.pcolormesh(Theta[:,::10],Time[:,::10],data[:,::10],cmap = plt.cm.bwr)
    
    plt.colorbar()
    plt.title(savedir + 'Field.jpg')
    plt.savefig(savedir + 'Field.jpg',dpi=160)
    plt.close('all')

######
def getFreqs(data,theta):
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

    #theta = np.linspace(-thetaMax,thetaMax,NTheta)

    Theta,Freq = np.meshgrid(theta,freq)


    return Theta , Freq , XF

def plotFreqs(Theta,Freq,XF,savedir):
    Theta , Freq = Theta*180/3.14 , Freq/1e12
    #tmin = int(NTheta*75/90)
    #XF[Theta > 75] = 0
    #XF[Theta < -75] = 0
    #Freq[Theta > 75] = 0
    #Freq[Theta < -75] = 0
    #Theta[Theta < -75] = -0
    #Theta[Theta > 75] = 0
    #plt.pcolormesh(Theta,Freq,np.abs(XF),cmap = plt.cm.jet)
    XF[Freq>30] = 0
    plt.pcolormesh(Theta[:,::10],Freq[:,::10],np.abs(XF)[:,::10],cmap = plt.cm.jet)
    
    plt.colorbar()
    plt.xlabel('Theta')
    plt.ylabel('Freqncey[THz]')
    plt.ylim([0,30])
    plt.title(savedir + 'Freqs.jpg')
    #plt.xlim([-75,75])
    #plt.clim([0,50000])
    plt.savefig(savedir + 'Freqs.jpg',dpi=160)
    plt.close('all')

######
def THzFilter(Theta , Freq , XF):
    XF[np.abs(Freq)>10e12]=0
    XF[np.abs(Freq)<0.1e12]=0

    Bz = np.fft.irfft(XF,axis = 0)
    Bz = Bz.real
    return Bz

def plotTHz(Theta,Time,data,savedir):
    Theta , Time = Theta*180/3.14 , Time/1e-15
    plt.pcolormesh(Theta[:,::10],Time[:,::10],data[:,::10],cmap = plt.cm.bwr)
    plt.colorbar()
    plt.title(savedir + 'THz.jpg')
    plt.savefig(savedir + 'THz.jpg',dpi=160)
    plt.close('all')


def main():
    ####
    time = np.load(const.txtdir + 'Sequencetime.npy')
    #theta = np.linspace(-thetaMax,thetaMax,NTheta)
    #Theta , Time = np.meshgrid(theta,time)

    ####
    data = np.load(datadir)
    data = np.array(data)
    ###
    x0 = point[0]
    y0 = point[1]
    ###
    iterateY = np.arange(data.shape[1])

    
    indexY = iterateY[np.abs(iterateY * const.delta_y + const.y_min - y0) < R ]
    y = indexY * const.delta_y + const.y_min
    x = np.sqrt(R **2 - (y-y0)**2) + x0
    #indexX = int((np.sqrt(R **2 - (y-y0)**2) + x0)/delta_x)
    #y = indexY * const.delta_y + const.y_min - y0 < R
    theta = np.arctan((y-y0)/(x-x0))
    
    #Theta , Time = np.meshgrid(theta,time)

    data = data[:,np.abs(iterateY * const.delta_y + const.y_min - y0) < R]

    #Ttime = 1720e-15    
    
    #data = data[time > Ttime,:]
    #time = time[time > Ttime]
    #savedir = const.figdir + str(Ttime) + 'R' +str(int(R/1e-6)) + 'x' + str(int(point[0]/1e-6)) + Field
    
    

    Theta , Time = np.meshgrid(theta,time)

    iterateY = iterateY[np.abs(iterateY * const.delta_y + const.y_min - y0) < R ]


    #data = data[:,int(NTheta/4+1/2):int(-NTheta/4)]
    plotField(Theta,Time,data,savedir)    
    Theta , Freq , XF = getFreqs(data,theta)
    plotFreqs(Theta,Freq,XF,savedir)
    Bz = THzFilter(Theta , Freq , XF)

    Theta , Time = np.meshgrid(theta,time)
    plotTHz(Theta,Time,Bz,savedir)


if __name__ == '__main__':
    main()
