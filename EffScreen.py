import ScreenTHz as getTimeSequence
import constant as const
import Processing
import pandas as pd
import numpy as np
#import clib.addTimeSequence as addTimeSequence
####
Field = Processing.Field
Limit = Processing.Limit
savedir = getTimeSequence.savedir
print(savedir)
##########
R = getTimeSequence.R #200e-6
NTheta = 2 * const.Ny #1000#addTimeSequence.NTheta
##########
c = 299792458
pi = 3.1415926
dt = const.dt_snapshot
dx = const.delta_x
dy = const.delta_y
dl = pi/NTheta * R
##########
####
def getTotalEnerge():
    #MaxIndex = (const.las_t_fwhm1/const.dt_snapshot)*2

    #MaxIndex = int(const.x_spot/2/c/const.dt_snapshot)
    MaxIndex = Processing.MaxIndex
    filepath = const.txtdir + str(Field) + '_' +str(Limit) + 'THz' +'Ksqrt.csv'
    data =pd.read_csv(filepath)
    maxEnerge = data.iloc[0,2]
    return maxEnerge

def ForwardTHzFilter(data):
    #data = data[:,int(NTheta/4+1/2):int(-NTheta/4)]    
    print('data.shape',data.shape)
    XF = np.fft.fft(data,axis=0)
    print('Xf.shape',XF.shape)
    freq = np.fft.fftfreq(data.shape[0],d = dt)
    print('freq.shape',freq.shape)

    #theta = np.linspace(-3.14/2,3.14/2,int(NTheta/2))

    y = np.linspace(const.y_min,const.y_max,const.Ny)

    Y,Freq = np.meshgrid(y,freq)

    #data = data[np.abs(Theta)<pi/2]

    #XF = np.fft.rfft(data,axis=0)

    XF[np.abs(Freq)>10e12]=0
    XF[np.abs(Freq)<0.1e12]=0

    Bz = np.fft.ifft(XF,axis = 0)
    Bz = Bz.real

    #Bz = Bz[np.abs(Theta)<pi/2]
    return Bz

def getTHzEnerge(savedir):
    #data = np.load('test/test.npy')
    data = np.load(savedir,allow_pickle=True)
    data = np.array(data)
    #data = data[:,-pi/2:pi/2]

    ##########
    Bz = ForwardTHzFilter(data)
    #Bz = data
    THzEnerge = np.sum(np.sum(np.square(Bz))) * dt/(dx/c) #* dl/dy
    print('dt scale:',dt/(dx/c))
    ##########
    return THzEnerge

def main(savedir):
    Energe = getTotalEnerge()
    ####
    ####
    THzEnerge = getTHzEnerge(savedir)
    Eff = THzEnerge/Energe
    print(Eff)

if __name__ == '__main__':
    savedir = getTimeSequence.savedir
    main(savedir)


