import getTimeSequence
import constant as const
import Processing
import pandas as pd
import numpy as np
import os
from getCircle import point

#import clib.addTimeSequence as addTimeSequence
####
Field = Processing.Field
Limit = Processing.Limit
savedir = getTimeSequence.savedir
print(savedir)
##########
R = getTimeSequence.R #200e-6
NTheta = const.Ny #1000#addTimeSequence.NTheta
##########
c = 299792458
pi = 3.1415926
dt = const.dt_snapshot
dx = const.delta_x
dy = const.delta_y
dl = pi/NTheta * R
##########
####
def saveCSV(dataframe,filepath,create='False'):
    df = dataframe
    if create == 'True':
        df.to_csv(filepath,mode = 'w')#,header = False)
        return
    if os.path.exists(filepath)==True:
        df.to_csv(filepath,mode = 'a',header = False)# , index = False)
    else:
        df.to_csv(filepath,mode = 'a')#,index = False)
    #if exist:
    #    dfEy = pd.DataFrame(mode = 'a',index=n,head=False)#,columns=colums)
    return

def getTotalEnerge():
    #MaxIndex = (const.las_t_fwhm1/const.dt_snapshot)*2

    #MaxIndex = int(const.x_spot/2/c/const.dt_snapshot)
    MaxIndex = Processing.MaxIndex
    filepath = const.txtdir + str(Field) + '_' +str(Limit) + 'THz' +'Ksqrt.csv'
    data =pd.read_csv(filepath)
    maxEnerge = data.iloc[0,2]
    return maxEnerge

def ForwardTHzFilter(data):
    ##
    x0 = point[0]
    y0 = point[1]
    ##

    iterateY = np.arange(data.shape[1])


    indexY = iterateY[np.abs(iterateY * const.delta_y + const.y_min - y0) < R ]
    y = indexY * const.delta_y + const.y_min
    x = np.sqrt(R **2 - (y-y0)**2) + x0
    #indexX = int((np.sqrt(R **2 - (y-y0)**2) + x0)/delta_x)
    #y = indexY * const.delta_y + const.y_min - y0 < R
    theta = np.arctan((y-y0)/(x-x0))

    #d_theta = theta.copy()
    d_theta = theta[1:] - theta[:-1]
    #d_theta[-1] = d_theta[-2]
    
    #Theta , Time = np.meshgrid(theta,time)

    data = data[:,np.abs(iterateY * const.delta_y + const.y_min - y0) < R]

    dl = d_theta * R
    print('dl',dl)

    #data = data[:,int(NTheta/4+1/2):int(-NTheta/4)]    
    print('data.shape',data.shape)
    XF = np.fft.fft(data,axis=0)
    print('Xf.shape',XF.shape)
    freq = np.fft.fftfreq(data.shape[0],d = dt)
    print('freq.shape',freq.shape)

    #theta = np.linspace(-3.14/2,3.14/2,int(NTheta/2))

    Theta,Freq = np.meshgrid(theta,freq)

    #data = data[np.abs(Theta)<pi/2]

    #XF = np.fft.rfft(data,axis=0)

    XF[np.abs(Freq)>10e12]=0
    XF[np.abs(Freq)<0.1e12]=0

    Bz = np.fft.ifft(XF,axis = 0)
    Bz = Bz.real

    Tarr = np.ones(dl.shape[0]) * dt
    print('Tarr',Tarr.shape)
    #Tarr[0] = dt

    print(np.dot(np.square(Bz[:,:-1]),dl.T))

    THzEnerge = np.sum( np.dot(np.square(Bz[:,:-1]),dl.T) * dt )
    #print('THzEnerge')
    

    print('THzEnerge',THzEnerge)
    #Bz = Bz[np.abs(Theta)<pi/2]
    return THzEnerge

def getTHzEnerge(savedir):
    #data = np.load('test/test.npy')
    data = np.load(savedir)
    data = np.array(data)
    #data = data[:,-pi/2:pi/2]

    ##########
    Bz = ForwardTHzFilter(data)
    #Bz = data
    THzEnerge = Bz #np.sum(np.sum(np.square(Bz))) * dt * dl# * dt/(dx/c) * dl/dy
    print('dt,dl scale:',dt/(dx/c),dl/dy)
    print(dl,dt)
    ##########
    return THzEnerge

def main(savedir):
    Energe = getTotalEnerge() * dy * (dx/c)
    print('Energe',Energe)
    ####
    ####
    THzEnerge = getTHzEnerge(savedir)
    Eff = THzEnerge/Energe
    print(Eff)
    x = point[0]
    name = const.case_name.split('/')[-1] + 'R' + str(R) + 'x' +str(x)
    dataframe = pd.DataFrame(data=[Eff] ,index = [name] )#columns = ['index','ETHz','ETotal'])
    filepath = 'test/'  + 'Eff.csv'
    #for dataframe,filepath in zip(datadict,filedict):
        #if n == 0:
        #    saveCSV(dataframe,filepath,create = 'True')
        #    continue
    saveCSV(dataframe,filepath)

if __name__ == '__main__':
    savedir = getTimeSequence.savedir
    main(savedir)


