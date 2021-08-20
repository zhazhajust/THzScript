from EffFinal import *
from getCircle import *
import matplotlib.pyplot as plt
import Processing
import matplotlib as mpl
import sys
from numba import njit
import matplotlib as mpl
from skimage import transform
import scipy.signal as signal
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
    plt.figure(figsize=[4,3])
    #plt.pcolormesh(theta,time,data,cmap = plt.cm.bwr)
    plt.pcolormesh(Theta[:,:],Time[:,:],data[:,:],cmap = plt.cm.bwr)
    
    plt.colorbar()
    plt.title(savedir.split('/')[-1] + 'Field')
    plt.savefig(savedir + 'Field.jpg',dpi=160)
    plt.close('all')

######
def getFreqs(data,theta,Nnumber=10000):
    '''
    XF = np.fft.rfft(data,axis=0)

    freq = np.fft.rfftfreq(data.shape[0],d = dt)

    theta = np.linspace(-3.14/2,3.14/2,NTheta)

    Theta,Freq = np.meshgrid(theta,freq)
    ######
    #Theta , Freq = Theta*180/3.14 , Freq/1e12

    data = data[:,int(NTheta/4):int(-NTheta/4)]
    '''
    XF = np.fft.rfft(data,n = Nnumber ,axis=0)
    #XF = np.fft.rfft(data,axis=0)
    #freq = np.fft.rfftfreq(data.shape[0],d = dt)

    freq = np.fft.rfftfreq(Nnumber,d = dt)

    #theta = np.linspace(-thetaMax,thetaMax,NTheta)

    Theta,Freq = np.meshgrid(theta,freq)


    return Theta , Freq , XF

@njit
def getIndex(theta):
    #intervalTheta = np.arange(-90,90,0.5)
    #theta = theta * 180 / pi
    intervalTheta = np.linspace(theta[0],theta[-1],1000)
    print(intervalTheta)

    indexT = theta * False

    for dtheta in intervalTheta:
        #dtheta = np.ones(theta.shape[0])*dtheta
        indexT[np.argmin(np.abs(theta - dtheta))] = True
        #print(np.argmin(theta - dtheta),'== true')
    indexT = np.where(indexT == 1 , True,False)
    return indexT

def interpFreq(Theta,Freq,Xf):
    #intervalTheta = np.arange(-90,90,0.5)
    #Theta , Freq = Theta*180/3.14 , Freq/1e12
    theta = Theta[0,:]
    intervalTheta = np.linspace(theta[0],theta[-1],500)
    #intervalFreq = np.arange(0,15,0.2)

    intervalFreq = Freq[:,0]

    grid_x , grid_y = np.meshgrid(intervalTheta,intervalFreq)
    #points = [Theta.flatten(),Freq.flatten()] 

    #print(Freq[:,0],Theta[0,:])
    points = np.stack([Theta.flatten(),Freq.flatten()],axis = -1)
    #points = np.vstack((Theta[:,0],Freq[0,:])).T
    values = Xf.flatten()
    grid_z2 = griddata(points,values,(grid_x,grid_y),method = 'cubic')

    return grid_z2 , intervalTheta , intervalFreq

def interpTime(Theta,Time,Xt):
    #intervalTheta = np.arange(-90,90,0.5)
    theta = Theta[0,:]
    intervalTheta = np.linspace(theta[0],theta[-1],500)
    intervalTime = Time[:,0]
    grid_x , grid_y = np.meshgrid(intervalTheta,intervalTime)
    #points = [Theta.flatten(),Freq.flatten()] 

    #print(Time[:,0],Theta[0,:])
    points = np.stack([Theta.flatten(),Time.flatten()],axis = -1)
    #points = np.vstack((Theta[:,0],Freq[0,:])).T
    values = Xt.flatten()
    grid_z2 = griddata(points,values,(grid_x,grid_y),method = 'cubic')

    return grid_z2 , intervalTheta , intervalTime


def plotFreqs(Theta,Freq,XF,savedir):
    Theta , Freq = Theta*180/3.14 , Freq/1e12
    ######
    
    freq = Freq[:,0]
    print(len(freq))
    index30 = len(freq[freq < 30])
    print('index',index30)
    #print(Booltheta)
    XF = XF[:index30,:]
    Theta = Theta[:index30,:]
    Freq = Freq[:index30,:]
    
    XF,Theta,Freq = interpFreq(Theta,Freq,XF)

    Theta , Freq = np.meshgrid(Theta , Freq)
    #XF = transform.resize(np.abs(XF), (1000, 2000),order=3)

    
    plt.figure(figsize=[4,3])
    #plt.pcolormesh(Theta[:,::10],Freq[:,::10],(np.abs(XF)[:,::10])**2,cmap = plt.cm.jet,shading ='gouraud',norm=mpl.colors.LogNorm())
    #plt.pcolormesh(Theta[:,::10],Freq[:,::10],(np.abs(XF)[:,::10])**2,cmap = plt.cm.jet,shading ='gouraud')

    plt.pcolormesh(Theta,Freq,(np.abs(XF))**2,cmap = plt.cm.jet,shading ='gouraud')#,norm=mpl.colors.LogNorm())
    #plt.contourf((np.abs(XXF))**2,50 ,alpha = 1 , cmap = plt.cm.jet)#,norm=mpl.colors.LogNorm())
    #plt.imshow((np.abs(XF)[:index30,indexT])**2 , interpolation = 'quadric', cmap = plt.cm.jet)#,norm=mpl.colors.LogNorm())
    plt.colorbar()
    plt.xlabel('Theta')
    plt.ylabel('Freqncey[THz]')
    plt.ylim([0,15])

    #plt.clim([0,8e8])
    plt.title(savedir.split('/')[-1] + 'Freqs')
    #plt.xlim([-75,75])
    #plt.clim([0,30000**2])
    plt.savefig(savedir + 'Freqs.jpg',dpi=160)
    plt.close('all')

def plotFreqsbak(Theta,Freq,XF,savedir):
    Theta , Freq = Theta*180/3.14 , Freq/1e12
    #tmin = int(NTheta*75/90)
    #XF[Theta > 75] = 0
    #XF[Theta < -75] = 0
    #Freq[Theta > 75] = 0
    #Freq[Theta < -75] = 0
    #Theta[Theta < -75] = -0
    #Theta[Theta > 75] = 0
    #plt.pcolormesh(Theta,Freq,np.abs(XF),cmap = plt.cm.jet)
    #Booltheta = np.where(np.mod(theta,pi/180)<0.1,True,False)

    #Theta = np.int(Theta*10)/10

    #Bool = []


    #indexT = Bool(indexT)

    #theta[intervalTheta]
    freq = Freq[:,0]
    print(len(freq))
    index30 = len(freq[freq < 30])
    print('index',index30)
    #print(Booltheta)
    XF = XF[:index30,:]
    Theta = Theta[:index30,:]
    Freq = Freq[:index30,:]
    XF[Freq > 30] = 0
    
    #XF[Freq < 0.1] = 0

    #XF = XF[Freq < 30]
    #Theta = Theta[Freq < 30]
    #Freq = Freq[Freq < 30]

    theta = Theta[0,:]
    print(theta)

    indexT = getIndex(theta)

    print(indexT)
    #plt.pcolormesh(Theta[:,np.mod(theta,pi/180)<0.25*pi/180],Freq[:,np.mo:q:d(theta,pi/180)<0.25*pi/180],np.abs(XF[:,np.mod(theta,pi/180)<0.25*pi/180])**2,cmap = plt.cm.jet,shading ='gouraud')

    print('shape',Theta.shape,Freq.shape,XF.shape)
    #plt.pcolormesh(Theta[:,::10],Freq[:,::10],(np.abs(XF)[:,::10])**2,cmap = plt.cm.jet,shading ='gouraud',norm=mpl.colors.LogNorm())
    #plt.pcolormesh(Theta[:,::10],Freq[:,::10],(np.abs(XF)[:,::10])**2,cmap = plt.cm.jet,shading ='gouraud')
    plt.pcolormesh(Theta[:index30,indexT],Freq[:index30,indexT],(np.abs(XF)[:index30,indexT])**2,cmap = plt.cm.jet,shading ='gouraud')#,norm=mpl.colors.LogNorm())
    #plt.contourf(Theta[:index30,indexT],Freq[:index30,indexT],(np.abs(XF)[:index30,indexT])**2,125 ,alpha = 1 , cmap = plt.cm.gist_earth)#,norm=mpl.colors.LogNorm())
    #plt.imshow((np.abs(XF)[:index30,indexT])**2 , interpolation = 'quadric', cmap = plt.cm.jet)#,norm=mpl.colors.LogNorm())
    plt.colorbar()
    plt.xlabel('Theta')
    plt.ylabel('Freqncey[THz]')
    plt.ylim([0,15])

    #plt.clim([0,3e9])
    plt.title(savedir.split('/')[-1] + 'Freqs')
    #plt.xlim([-75,75])
    #plt.clim([0,30000**2])
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
    plt.figure(figsize=[4,3])
    plt.pcolormesh(Theta[:,:],Time[:,:],data[:,:],cmap = plt.cm.bwr)#,shading ='gouraud')
    plt.colorbar()
    plt.title(savedir.split('/')[-1] + 'THz')
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
    ###################
    ####data filter####
    x0 = point[0]
    y0 = point[1]
    ###
    iterateY = np.arange(data.shape[1])

    
    indexY = iterateY[np.abs(iterateY * const.delta_y + const.y_min - y0) < R ]
    y = indexY * const.delta_y + const.y_min
    x = np.sqrt(R **2 - (y-y0)**2) + x0
    #indexX = int((np.sqrt(R **2 - (y-y0)**2) + x0)/delta_x)
    #y = indexY * const.delta_y + const.y_min - y0 < R
    global theta
    theta = np.arctan((y-y0)/(x-x0))
    
    #Theta , Time = np.meshgrid(theta,time)
    #data = data[data.shape[0]-time.shape[0]-1:-1,:]
    data = data[:,np.abs(iterateY * const.delta_y + const.y_min - y0) < R]

    #######
    #######
    #######
    #time.shape[0]
    #data = data[data.shape[0]-time.shape[0]-1:-1,:]

    #Ttime = 2810e-15
    #Ttime1 = 2166e-15  
    #print('time[0] + R/c',time[0] + R/c)
    #Ttime = float(time[0] + R/c) #2200e-15  
    #data = data[time < Ttime,:]
    #time = time[time < Ttime]

    #data = data[time > Ttime1,:]
    #time = time[time > Ttime1]

    #savedir = const.figdir + str(Ttime) + 'R' +str(int(R/1e-6)) + 'x' + str(int(point[0]/1e-6)) + Field

    #data = signal.medfilt2d(data, kernel_size=(1,101))
    
    theta = theta * 180/3.14
    indexT = getIndex(theta)
    data = data[:,indexT]
    theta = theta[indexT]
    theta = theta / 180*3.14

    data = signal.medfilt2d(data, kernel_size=(1,101))

    Theta , Time = np.meshgrid(theta,time)

    #data = signal.medfilt2d(data, kernel_size=(1,101))

    #iterateY = iterateY[np.abs(iterateY * const.delta_y + const.y_min - y0) < R ]

    #data = signal.medfilt2d(data, kernel_size=(1,101))
    #data , Theta,Time = interpTime(Theta,Time,data)

    #data = data[:,int(NTheta/4+1/2):int(-NTheta/4)]
    plotField(Theta,Time,data,savedir)    
    Theta , Freq , XF = getFreqs(data,theta)
    plotFreqs(Theta,Freq,XF,savedir)

    #XF = np.fft.rfft(data,axis=0)
    Theta , Freq , XF = getFreqs(data,theta,data.shape[0])
    Bz = THzFilter(Theta , Freq , XF)
    Theta , Time = np.meshgrid(theta,time)
    plotTHz(Theta,Time,Bz,savedir)


if __name__ == '__main__':
    main()
