import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from scipy import interpolate
#matplotlib.use('AGG')
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import sys, getopt
from matplotlib import cm
import os
#os.makedirs('test',exist_ok = True)
import math

plt.switch_backend('agg')
#imax
####const####
#############
dt = 10e-15
pi = math.pi
c = 3e8
#############
#############

def readData(datadir):
    #datadir + 'TracerX.csv'
    X = pd.read_csv(datadir + 'TracerX.csv')
    Y = pd.read_csv(datadir + 'TracerY.csv')
    Ey = pd.read_csv(datadir + 'TracerEy.csv')
    Ek = pd.read_csv(datadir + 'TracerEk.csv')
    Vy = pd.read_csv(datadir + 'TracerVy.csv')
    #Px = pd.read_csv(datadir + 'TracerPx.csv')
    #Py = pd.read_csv(datadir + 'TracerPy.csv')
    #data = pd.read_csv('TracerEy.csv')

    return X,Y,Vy,Ek

def trackParticle(value='ek',time = [0,-1],**kwargs):
    cmap=plt.get_cmap('rainbow')
    #fig, axs = plt.subplots(1, 1)
    fig, axs = plt.subplots(figsize=[4,3])
    #time=150
    #for key,value in kwargs:
    
    try:
        X = kwargs['X']
        Y = kwargs['Y']
        Ey = kwargs['Ey']
        Ek = kwargs['Ek']
        #Px = kwargs['Px']
        #Py = kwargs['Py']
        xlim = kwargs['xlim']
        ylim = kwargs['ylim']
        
    except:
        print('wrong read Dict')
        pass
    
    imax=Y.shape[1]
    tt = np.asarray(Y.iloc[:,0])
    #print(kwargs)
    #locals().update(kwargs)
    #print(X)
    for num in range(10,imax,int(imax/15)):
        # if (py[1228,num]>0):
        #   print(num)
        x = X.iloc[time[0]:time[1],num]#- Y.iloc[0,num]
        y = Y.iloc[time[0]:time[1],num]#Ey.iloc[0:110,num]
        x = np.asarray(x)/1e-6
        y = np.asarray(y)/1e-6
        ek =  Ek.iloc[time[0]:time[1],num]
        ek = np.asarray(ek)
        T = tt[time[0]:time[1]]
        dydx = eval(value)#t#(0.5 * (t[:-1] + t[1:]))
        #lines = [zip(x, y)]
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        #print(points)
        # Create a continuous norm to map from data points to colors
        norm = plt.Normalize(dydx.min(), dydx.max())
        lc = LineCollection(segments, cmap='jet')#, norm=norm)
        #lc = LineCollection(lines, cmap='rainbow', norm=norm)
        # Set the values used for colormapping
        lc.set_array(dydx)
        lc.set_linewidth(1)
        line = axs.add_collection(lc)
        axs.set_xlabel('x')
        axs.set_ylabel('y')
        

    axs.set_xlim(xlim)
    axs.set_ylim(ylim)

    plt.xlabel('um')
    plt.ylabel('um')
    cbar = fig.colorbar(line, ax=axs)
    #plt.savefig(Img_dir+'track_e'+'%04d'%num+'.png')
    cbar.set_label(value)
    #plt.close('all')
    plt.savefig(savedir + str(value)+str(time[0])+'_'+str(time[1])+'.jpg',dpi=160)
    plt.clf()
    plt.close('all')
    



def plotDensity(datadir,Xlim,Ylim):
    X,Y,Ey,Ek = readData(datadir)
    X = np.asarray(X)
    Y = np.asarray(Y)
    for n in range(0,X.shape[0],10):
        #if n == 140:
            plt.scatter(X[n,:],Y[n,:],s = 1,cmap= plt.cm.jet,alpha = 0.7)
            plt.xlim(Xlim)
            plt.ylim(Ylim)
            #plt.show()
            plt.savefig(datadir + 'test/density'+str(n)+'.jpg',bbox_inches='tight')
            plt.clf()
            plt.close('all')
            
def main(datadir,xlim,ylim):
    X,Y,Ey,Ek = readData(datadir) #[X,Y,Ey,Ek]
    #X = np.asarray(X)
    #Y = np.asarray(Y)
    try:
        PropertyDict = {'X':X,'Y':Y,'Ey':Ey,'Ek':Ek,'xlim':xlim,'ylim':ylim}
    except:
        PropertyDict = {'X':X,'Y':Y,'Ey':Ey,'Ek':Ek}
    #print(PropertyDict)
    global imax
    global savedir
    savedir = datadir
    trackParticle('ek',[0,int(FTime/10e-15)],**PropertyDict)
    #trackParticle('ek',[110,150],**PropertyDict)
    trackParticle('T',[0,int(FTime/10e-15)],**PropertyDict)
    #trackParticle('T',[110,150],**PropertyDict)
    return
    #plt.show()


def plotTracer(*args,**kwargs):
    
    font = {'family' : 'Times New Roman',
            #'color'  : 'black',  
            'weight' : 'normal',  
            'size'   : 15,  
            }  
    color='rainbow'
    index = 6
    ####
    ####
    #matplotlib.rc('font', **font)


    fig,ax=plt.subplots(figsize=(4,3))
    ax2=ax.twinx()
    ax3=ax.twinx()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(True)
    ax2.spines['top'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(True)
    ax3.spines['right'].set_visible(True)

    ###spines color
    ax3.spines['right'].set_color('green')
    ax2.spines['right'].set_color('red')
    labels=ax2.get_yticklabels()+ax3.get_yticklabels()
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    for tic in ax3.get_yticklabels():
        tic.set_color('g')
    ###

    ax3.spines['right'].set_position(('axes',1.2))

    i = args[0]
    x = np.array(args[1])
    #global curve_cof,curve_temp,curve_load
    for key,value in kwargs.items():
        #print(key,value)
        if key == 'Vy':
            global curve_cof
            curve_cof, = ax.plot(x,value, '-',label=str(key), color='black')
        if key == 'Ek':
            global curve_temp
            curve_temp, = ax2.plot(x, value, '-',label=str(key), color='red')
        if key == 'y':
            global curve_load
            curve_load, = ax3.plot(x,value, '-',label=str(key), color='green')
            
        if key == 'Datadir':
            datadir = value
            
    plt.legend(handles=[curve_cof,curve_temp,curve_load])
    
    #######
    #######
    #ax.set_ylabel('Ey[V/m]',fontdict=font)
    ax.set_ylabel('Ey[V/m]')
    #ax.set_xlabel('density[$n_c$]')
    ax.set_xlabel('Time [$fs$]')
    #ax.set_xlabel('spot[$w_0$]')
    ax2.set_ylabel('Ek',color='red')
    ax3.set_ylabel('Y[$um$]',color='g')

    ##

    #ax.xaxis.set_ticks([0,0.2,0.4,0.6,0.8])
    #ax2.xaxis.set_ticks([0,0.2,0.4,0.6,0.8])
    #ax3.xaxis.set_ticks([0,0.2,0.4,0.6,0.8])
    #ax.yaxis.set_ticks([3,6,9,12,15])
    #ax2.yaxis.set_ticks((0,2e11,4e11,6e11,8e11))
    #ax2.yaxis.set_ticks([0.5,1,1.5,2])
    #ax3.yaxis.set_ticks([0.5,1,1.5,2])

    ###

    #ax.set_ylim((0,15))

    #ax2.set_ylim((0,5))
    #ax3.set_ylim((0,10))
    #ax.set_xlim((150,636))

    for tic in ax3.get_yticklabels():
        tic.set_color('g')
    ###
    #plt.show()
    #fig.savefig('../fig/'+str(label[0])+'.png',format='png',dpi=400,bbox_inches = 'tight')
    #print(datadir)
    plt.savefig(datadir + 'test/'+str(i)+'.jpg',bbox_inches='tight')
    plt.clf()
    plt.close('all')

#######FFt########
##################


def getFFtData(t,y,dt_m,plot = 'true'):
    
    #tnew = np.cumsum(np.ones(t.shape)*10e-15)
    '''
    tnew = np.arange(0,t[-2],10e-15)
    plt.plot(tnew)
    f=interpolate.interp1d(t,y,kind="cubic")
    ynew = f(tnew)
    '''
    dt_m = 10e-15
    Xf = np.fft.rfft(y)
    freq = np.fft.rfftfreq(y.shape[0],d = dt_m)
    if plot == 'true':
        plt.plot(freq[freq > 0.1e12]/1e12,np.abs(Xf[freq > 0.1e12]))
        plt.xlim([0.1,10])
        #plt.show()
        plt.savefig(datadir + 'test/'+'FFt'+str(i)+'.jpg',bbox_inches='tight')
        plt.clf()
        plt.close('all')
    return freq , Xf

#####track particle######
#####################
def Particle(datadir):
    os.makedirs(datadir + 'test/',exist_ok = True)
    X,Y,Vy,Ek = readData(datadir)

    global imax
    imax=Y.shape[1]
    tt = np.asarray(Y.iloc[:,0])
    for i in range(10,imax,int(imax/100)):
        #i=
        '''
        plt.plot(Ey.iloc[:,i])
        plt.plot(np.asarray(Y.iloc[:,i])*1e16)
        plt.plot(np.asarray(Ek.iloc[:,i])*5e10)
        plt.ylim([-2e11,2e11])
        plt.savefig(datadir + 'test/'+str(i)+'.jpg')
        plt.clf()
        plt.close('all')
        '''
        plotTracer(i,tt,Vy=np.asarray(Vy.iloc[:,i]),y=np.asarray(Y.iloc[:,i])/1e-6,Ek=np.asarray(Ek.iloc[:,i]),Datadir = datadir)
        
        
    return

def CoordinateTransformation(theta,t,Vx,Vy):
    Vt = Vy * np.cos(theta) - Vx * np.sin(theta)

    #v = np.sqrt(Vx**2 + Vy**2)

    #v = Vx

    v = Vy * np.sin(theta) + Vx * np.cos(theta)

    #plt.plot(Vt)

    delta_t = 10e-15

    Doppler = np.sqrt((c + v)/(c - v))

    dt = delta_t * (1 - (v/c)**2)

    dt_m = np.sum(dt)/dt.shape[0]

    t = np.cumsum(dt)

    #print(t)
    '''
    for i in range(len(t)):
        x += vx[i] * dt
    v = x/t[-1]
    '''
    return Vt , t ,dt_m


##plot FFt of y###
##############
#os.makedirs(datadir + 'test',exist_ok = True)
#i = 700
def getFFt(datadir,theta,savedir):
    os.makedirs(datadir + 'test',exist_ok = True)
    X,Y,Ey,Ek = readData(datadir)
    Vy = pd.read_csv(datadir + 'TracerVy.csv')
    Vx = pd.read_csv(datadir + 'TracerVx.csv')
    
    global imax
    imax=Y.shape[1]
    t = np.asarray(Y.iloc[:,0])
    Y = Vy
    #####

    #####
    XfAll = 0
    freq = 0
    '''
    for i in range(10,imax,10):
        y=np.asarray(Y.iloc[:,i])/1e-6
        ######
        #theta = 0 * pi/180
        y,t ,dt_m= CoordinateTransformation(theta,t,np.asarray(Vx.iloc[:,i]),np.asarray(Vy.iloc[:,i]))
        #####
        freq , Xf = getFFtData(t,y,dt_m,plot = 'false')
        #XfAll += np.abs(Xf)
        XfAll += Xf
    '''
    y = 0
    t = 0
    for i in range(10,imax,10):
        
        ######
        #theta = 0 * pi/180
        Vt,t ,dt_m= CoordinateTransformation(theta,t,np.asarray(Vx.iloc[:int(FTime/10e-15),i]),np.asarray(Vy.iloc[:int(FTime/10e-15),i]))

        y += Vt
    
        #####
        freq , Xf = getFFtData(t,y,dt_m,plot = 'false')
        #XfAll += np.abs(Xf)
        XfAll += Xf

    XfAll = np.abs(XfAll)
    plt.figure(figsize=[4,3])
    im = plt.plot(freq/1e12,XfAll)
    plt.xlim([0.1,10])
    plt.xlabel('THz')
    plt.ylabel('dy')
    plt.savefig(savedir , dpi= 160)
    plt.show()
    return freq , XfAll

def plotFFtTrack(datadir):
    #datadir = 'y50x250/'
    XF=[]
    theta = 0 * pi/180
    freq,XfAll = getFFt(datadir,theta,savedir = datadir + 'FFtTrack.jpg')
    #XF.append(XfAll)

    #plt.pcolormesh(XF)
    #im.savefig('Vy10.jpg',dpi= 160)

if __name__ == '__main__':
    epochdir = '/home/yujq/users/caijie/epoch2d/' 
    
    FTime = 1200e-15

    DataDir = [epochdir + 'txt/MassLimit/tracer/y30x250/']
    Xlim = [[0,400]]
    Ylim = [[-40,40]]
    for datadir,xlim,ylim in zip(DataDir,Xlim,Ylim):
        os.makedirs(datadir + 'test/',exist_ok = True)
        main(datadir,xlim,ylim)
        plotFFtTrack(datadir)
        #plotDensity(i,xlim,ylim)
    for datadir in DataDir:
        Particle(datadir)
        
