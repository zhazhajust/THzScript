import getTimeSequence
import constant as const
import Processing
import pandas as pd
import numpy as np
import getStartSequence
####
Field = Processing.Field
Limit = Processing.Limit
savedir = getStartSequence.savedir
##########
R = getTimeSequence.R #200e-6
NTheta = 600
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
    MaxIndex = Processing.MaxIndex
    filepath = const.txtdir + str(Field) + '_' +str(Limit) + 'THz' +'Ksqrt.csv'
    data =pd.read_csv(filepath)
    maxEnerge = data.iloc[0,2]
    return maxEnerge

def THzFilter(data):
    XF = np.fft.rfft(data,axis=0)

    freq = np.fft.rfftfreq(data.shape[0],d = dt)

    theta = np.linspace(-3.14/2,3.14/2,NTheta)

    Theta,Freq = np.meshgrid(theta,freq)

    XF[np.abs(Freq)>10e12]=0
    XF[np.abs(Freq)<0.1e12]=0

    Bz = np.fft.irfft(XF,axis = 0)
    Bz = Bz.real
    return Bz

def getTHzEnerge(savedir):
    #data = np.load('test/test.npy')
    data = np.load(savedir)
    data = np.array(data)
    ##########
    #Bz = THzFilter(data)
    Bz = data
    THzEnerge = np.sum(np.sum(np.square(Bz))) * dt/(dx/c)# * dl/dy
    #Bz = data
    print('dt,dl scale:',dt/(dx/c),dl/dy)
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
    savedir = getStartSequence.savedir
    main(savedir)


