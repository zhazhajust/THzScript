from EffFinal import *
from getCircle import *
import matplotlib.pyplot as plt
import Processing
import matplotlib as mpl
import sys
import pandas as pd
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
def plotField(Theta,Time,data,savedir):
    Theta , Time = Theta*180/3.14 , Time/1e-15
    #plt.pcolormesh(theta,time,data,cmap = plt.cm.bwr)
    plt.pcolormesh(Theta[:,::10],Time[:,::10],data[:,::10],cmap = plt.cm.bwr)
    
    plt.colorbar()
    plt.title(savedir + 'Field.jpg')
    plt.savefig(savedir + 'Field.jpg',dpi=160)
    plt.close('all')

######
def getFreqs(data,theta,Nnumber=5000):
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
    #freq = np.fft.rfftfreq(data.shape[0],d = dt)

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
    #Booltheta = np.where(np.mod(theta,pi/180)<0.1,True,False)

    

    #print(Booltheta)
    XF[Freq>30] = 0
    #plt.pcolormesh(Theta[:,np.mod(theta,pi/180)<0.25*pi/180],Freq[:,np.mod(theta,pi/180)<0.25*pi/180],np.abs(XF[:,np.mod(theta,pi/180)<0.25*pi/180])**2,cmap = plt.cm.jet,shading ='gouraud')

    print('shape',Theta.shape,Freq.shape,XF.shape)
    #plt.pcolormesh(Theta[:,::10],Freq[:,::10],(np.abs(XF)[:,::10])**2,cmap = plt.cm.jet,shading ='gouraud',norm=mpl.colors.LogNorm())
    plt.pcolormesh(Theta[:,::10],Freq[:,::10],(np.abs(XF)[:,::10])**2,cmap = plt.cm.jet,shading ='gouraud')
    plt.colorbar()
    plt.xlabel('Theta')
    plt.ylabel('Freqncey[THz]')
    plt.ylim([0,30])
    plt.title(savedir + 'Freqs.jpg')
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
    global theta
    theta = np.arctan((y-y0)/(x-x0))
    d_theta = theta[1:] - theta[:-1]
    dl = d_theta * R
    Tarr = np.ones(dl.shape[0]) * dt

    #Theta , Time = np.meshgrid(theta,time)

    data = data[:,np.abs(iterateY * const.delta_y + const.y_min - y0) < R]

    #I_theta = np.sum(np.square(data),axis = 1)

    
    ####
    ####
    Ttime = 2220e-15    
    data_forward = data[time > Ttime,:]
    #time = time[time < Ttime]
    #savedir = const.figdir + str(Ttime) + 'R' +str(int(R/1e-6)) + 'x' + str(int(point[0]/1e-6)) + Field
    
    ####
    ####

    #ITHz_theta = np.sum(np.square(data),axis = 1)



    #Theta , Time = np.meshgrid(theta,time)

    #iterateY = iterateY[np.abs(iterateY * const.delta_y + const.y_min - y0) < R ]


    #data = data[:,int(NTheta/4+1/2):int(-NTheta/4)]
    #plotField(Theta,Time,data,savedir)    
    Theta , Freq , XF = getFreqs(data,theta)
    #plotFreqs(Theta,Freq,XF,savedir)

    Thetaforward , Freqforward , XFforward = getFreqs(data_forward,theta)
    freqs = Freq[:,0]
    freqsF = Freqforward[:,0]
    d_f = freqs[1]-freqs[0]
    #I_freqs = np.sum(np.square(np.abs(XF)),axis = 1)
    I_freqs = np.dot(np.square(np.abs(XF)[:,:-1]),dl.T) * d_f/dl.shape[0]/freqs.shape[0]
    #Iforward_theta = np.sum(np.square(np.abs(XFforward)),axis = 1)
    Iforward_theta = np.dot(np.square(np.abs(XFforward)[:,:-1]),dl.T) * d_f/dl.shape[0]/freqs.shape[0]

    Eff = np.sum(Iforward_theta)/np.sum(I_freqs)

    print(Eff)

    x = point[0]
    name = const.case_name.split('/')[-1] + 'R' + str(R) + 'x' +str(x)

    dataframe = pd.DataFrame(data=[Eff] ,index = [name] )#columns = ['index','ETHz','ETotal'])
    filepath = 'test/'  + 'Effproprotion.csv'
    #for dataframe,filepath in zip(datadict,filedict):
        #if n == 0:
        #    saveCSV(dataframe,filepath,create = 'True')
        #    continue
    saveCSV(dataframe,filepath)

    plt.plot(freqs[freqs < 10e12]/1e12, I_freqs[freqs < 10e12],label = 'I')
    plt.plot(freqsF[freqsF < 10e12]/1e12, Iforward_theta[freqsF < 10e12],label = 'IForward')
    plt.legend()
    plt.xlim([0,10])
    plt.savefig('test/I_freqs.jpg',dpi=160)
    plt.clf()
    plt.close('all')
    #XF = np.fft.rfft(data,axis=0)
    
    #Theta , Freq , XF = getFreqs(data,theta,data.shape[0])

    #Bz = THzFilter(Theta , Freq , XF)

    #Theta , Time = np.meshgrid(theta,time)
    #plotTHz(Theta,Time,Bz,savedir)


if __name__ == '__main__':
    main()
