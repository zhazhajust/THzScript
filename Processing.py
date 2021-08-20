from scipy.interpolate import interpn
from scipy.stats import gaussian_kde
import sdf
import constant as const
import numpy as np
import matplotlib.pyplot as plt
import os
from numba import njit
from scipy.interpolate import interp2d
from scipy.interpolate import griddata
import multiprocessing
from multiprocessing.managers import SharedMemoryManager
from multiprocessing import shared_memory
import pandas as pd
from clib.getTracerField import getTracerField
#from getTracerField import getTracerField

plt.switch_backend('agg')
####
####constant####
c = 299792458
pi = 3.1415926
MeV = 1.6021766208e-13
delta_x=const.delta_x
delta_y=const.delta_y
k0=2*pi*1e12/3e8
Nx = const.Nx
Ny = const.Ny
########
########

Field = 'Bz'
Limit = 10

MaxIndex = int(const.x_spot/2/c/const.dt_snapshot)
#########

def gridInterp(data):
    #points = 
    #values = 

    grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')
    #data = grid_z2(data)    
    return
def PoolMap2(func,*args):
    smm = SharedMemoryManager()
    smm.start()
    sl = []
    for i in range(len(args)):
        sl.append(smm.ShareableList(args[i]))
                
    #print('sl',sl)        
    pool = multiprocessing.Pool(processes=96)   #,initargs=(ss1,ss2))
    MapList = range(const.stop+const.step)
    results = pool.map(func,MapList)
    pool.close()
    pool.join()
    return results           

def PoolMap(func,*args):
    results = 0
    with SharedMemoryManager() as smm:
        sl = []
        for arg in args:
            shm = shared_memory.SharedMemory(create=True, size=arg.nbytes)
            arg_shm = np.ndarray(arg.shape, dtype=arg.dtype, buffer=shm.buf)
            arg_shm[:] = arg[:]
            #print(arg)
            #sl.append(smm.ShareableList(name = arg.shm.name))
            #a = shared_memory.ShareableList(arg)
            sl.append(shm.name)

        #sl = smm.ShareableList(range(2000))
        # Divide the work among two processes, storing partial results in sl

        pool = multiprocessing.Pool(processes=96)   #,initargs=(ss1,ss2))
        MapList = range(const.stop+const.step)
        results = pool.map(func,MapList,args = sl)
        pool.close()
        pool.join()

        #total_result = sum(sl)  # Consolidate the partial results now in sl
    return results

def flist():
    sdfdir = const.sdfdir
    listsdf=os.listdir(sdfdir)
    listsdf=[i.split('.') for i in listsdf]
    loop=[i for i in listsdf if i[1] == 'sdf']
    loop=np.array(loop)
    #loop=np.sort(loop)
    loop=loop[:,0]
    loop=np.sort(loop)
    print(loop)
    return loop

def getEff(Field = 'Bz'):
    data =pd.read_csv(const.txtdir+str(Field)+'Ksqrt.csv')
    index = data.iloc[:,0]
    a = data/data.iloc[0,2]
    eff = a.iloc[:,1]
    return index,eff

def getEDensity(x):
    sdfdir=const.sdfdir +str(x).zfill(const.filenumber)+".sdf"
    data=sdf.read(sdfdir,dict=True)
    ne=data['Derived/Number_Density/electron1'].data
    return ne

def getBz(x):
    #savedir = const.figdir + 't' + str(x) + 'Ktheta.jpg'
    ####read sdf####
    sdfdir=const.sdfdir +str(x).zfill(const.filenumber)+".sdf"
    data=sdf.read(sdfdir,dict=True)
    Bz=data['Magnetic Field/Bz']
    bz=Bz.data
    #k_bz=np.fft.fft2(bz)
    title = 'Bz' + str(int(int(x)*const.dt_snapshot/1e-15)) + 'fs'
    return bz , title
def getEy(x):
    #savedir = const.figdir + 't' + str(x) + 'Ktheta.jpg'
    ####read sdf####
    sdfdir=const.sdfdir +str(x).zfill(const.filenumber)+".sdf"
    data=sdf.read(sdfdir,dict=True)
    Bz=data['Electric Field/Ey']
    bz=Bz.data
    #k_bz=np.fft.fft2(bz)
    title = 'Ey' + str(int(int(x)*const.dt_snapshot/1e-15)) + 'fs'
    return bz ,title

def getEz(x):
    #savedir = const.figdir + 't' + str(x) + 'Ktheta.jpg'
    ####read sdf####
    sdfdir=const.sdfdir +str(x).zfill(const.filenumber)+".sdf"
    data=sdf.read(sdfdir,dict=True)
    Bz=data['Electric Field/Ez']
    bz=Bz.data
    #k_bz=np.fft.fft2(bz)
    title = 'Ez' + str(int(int(x)*const.dt_snapshot/1e-15)) + 'fs'
    return bz ,title

def TimeSequence(point,R):
    #theta = np.arange(-90,91)
    #x,y = point[0] + R*np.cos(theta) , point[1] + R*np.sin(theta)
    #x ,y = x/delta_x,(y - (const.y_min+delta_y/2))/delta_y
    #print(x,y)
    #stop = const.stop
    #step = 1
    #t = stop + step
    #TimeSequence= np.zeros((t,theta.shape[0]))
    theta = np.arange(-90,91)
    x,y = point[0] + R*np.cos(theta) , point[1] + R*np.sin(theta)
    x ,y = x/delta_x,(y - (const.y_min+delta_y/2))/delta_y
    results = PoolMap(getThetaTField,x,y,theta)

    return TimeSequence
'''
def getThetaTField(point,R):
    theta = np.arange(-90,91)
    x,y = point[0] + R*np.cos(theta) , point[1] + R*np.sin(theta)
    x ,y = x/delta_x,(y - (const.y_min+delta_y/2))/delta_y
    print(x,y)
    stop = const.stop
    step = 1
    t = stop + step
    #TimeSequence= np.zeros((t,theta.shape[0]))
    flist = range(stop+step)

    pool = multiprocessing.pool
    result = pool.map()
    for t in range(len(flist)):
        data , title = getBz(t)
        data = np.array(data)
        #TimeSequence = addFieldTheta(data,TimeSequence)
        for i in range(len(theta)):
            indexX ,indexY = int(x[i]),int(y[i])
            TimeSequence[t,int(theta[i]+90)]=data[indexX,indexY]
    return TimeSequence
'''

@njit
def addFieldTheta(data):#,TimeSequence):
        TimeSequence = []
        #theta = np.arange(-90,91)
        #x,y = point[0] + R*np.cos(theta) , point[1] + R*np.sin(theta)
        #x ,y = x/delta_x,(y - (const.y_min+delta_y/2))/delta_y
        arr = []
        for shmname in sl:
            shm0 = shared_memory.SharedMemory(name=shmname)
            arr.append(np.ndarray(buffer=existing_shm.buf))
        x = arr[0]
        y = arr[1]
        theta = arr[2]
        for i in range(len(theta)):
            indexX ,indexY = int(x[i]),int(y[i])
            TimeSequence.append(data[indexX,indexY])
        return TimeSequence

def getThetaTField(t):
    #pool.map()
    data , title = getBz(t)
    data = np.array(data)
    #####
    #theta = np.arange(-90,91)
    #x,y = point[0] + R*np.cos(theta) , point[1] + R*np.sin(theta)
    #x ,y = x/delta_x,(y - (const.y_min+delta_y/2))/delta_y
    TimeSequence = addFieldTheta(data)#,TimeSequence)
    return TimeSequence

def FFt(bz):
    ####fourier transform#####
    k_bz2d=np.fft.fft2(bz)
    k0=2*pi*1e12/c
    #kx = np.arange(const.Nx/2,const.Nx/2)*2*pi/(const.Nx*delta_x)/k0
    #ky = np.arange(const.Ny/2,const.Ny/2)*2*pi/(const.Ny*delta_y)/k0

    #kx = np.linspace(-pi/delta_x/k0,pi/delta_x/k0 - 2*pi/(delta_x*const.Nx)/k0,const.Nx)
    #ky = np.linspace(-pi/delta_y/k0,pi/delta_y/k0 - 2*pi/(delta_y*const.Ny)/k0,const.Ny)

    kx = np.fft.fftfreq(Nx,d = 1/(pi/delta_x/k0))
    ky = np.fft.fftfreq(Ny,d = 1/(pi/delta_y/k0))
    kx = np.fft.fftshift(kx)
    ky = np.fft.fftshift(ky)

    Ky,Kx=np.meshgrid(ky,kx)
    Kxy = np.fft.fftshift(k_bz2d)
    return Kx,Ky,Kxy


def FFtRight(bz,x):
    ####fourier transform#####

    xGrid = int((x - const.delta_x/2) / const.delta_x)
    print('xGrid:',xGrid)
    Nx = const.Nx - xGrid
    Ny = const.Ny
    bz = bz[xGrid:,:]    

    k_bz2d=np.fft.fft2(bz)
    k0=2*pi*1e12/c
    #kx = np.arange(const.Nx/2,const.Nx/2)*2*pi/(const.Nx*delta_x)/k0
    #ky = np.arange(const.Ny/2,const.Ny/2)*2*pi/(const.Ny*delta_y)/k0

    #kx = np.linspace(-pi/delta_x/k0 , pi/delta_x/k0 - 2*pi/(delta_x*Nx)/k0,Nx)
    #ky = np.linspace(-pi/delta_y/k0 , pi/delta_y/k0 - 2*pi/(delta_y*Ny)/k0,Ny)

    kx = np.fft.fftfreq(Nx,d = 1/(pi/delta_x/k0))
    ky = np.fft.fftfreq(Ny,d = 1/(pi/delta_y/k0))
    kx = np.fft.fftshift(kx)
    ky = np.fft.fftshift(ky)

    Ky,Kx=np.meshgrid(ky,kx)
    Kxy = np.fft.fftshift(k_bz2d)
    return Kx,Ky,Kxy

def FFtLeft(bz,x):
    ####fourier transform#####

    xGrid = int((x - const.delta_x/2) / const.delta_x)
    print(xGrid)
    Nx = xGrid - int(const.x_min/const.delta_x)
    Ny = const.Ny
    bz = bz[:xGrid,:]

    k_bz2d=np.fft.fft2(bz)
    k0=2*pi*1e12/c
    #kx = np.arange(const.Nx/2,const.Nx/2)*2*pi/(const.Nx*delta_x)/k0
    #ky = np.arange(const.Ny/2,const.Ny/2)*2*pi/(const.Ny*delta_y)/k0

    #kx = np.linspace(-pi/delta_x/k0 , pi/delta_x/k0 - 2*pi/(delta_x*Nx)/k0,Nx)
    #ky = np.linspace(-pi/delta_y/k0 , pi/delta_y/k0 - 2*pi/(delta_y*Ny)/k0,Ny)


    kx = np.fft.fftfreq(Nx,d = 1/(pi/delta_x/k0))
    ky = np.fft.fftfreq(Ny,d = 1/(pi/delta_y/k0))
    kx = np.fft.fftshift(kx)
    ky = np.fft.fftshift(ky)

    Ky,Kx=np.meshgrid(ky,kx)
    Kxy = np.fft.fftshift(k_bz2d)
    return Kx,Ky,Kxy


def getKBz(bz,Theta = '180'):
    ####fourier transform#####
    #k_bz2d=np.fft.fft2(bz)
    #fig,axs=plt.subplots(figsize=[4,3])
    #k0=2*pi/10.6e-6

    #k0=2*pi*1e12/3e8
    #kx=np.linspace(0,pi/delta_x/k0,int(const.Nx/2+1))
    #ky=np.linspace(0,pi/delta_y/k0,int(const.Ny/2+1))
    #kx = kx[0:int(const.Nx/2)]
    #ky = ky[0:int(const.Nx/2)]
    
    #Kx,Ky,Kxy = FFt(bz)
    if Theta == '90':
        Kxy=np.fft.fft2(bz)
        #fig,axs=plt.subplots(figsize=[4,3])

        k0=2*pi*1e12/3e8
        kx=np.linspace(0,pi/delta_x/k0,int(const.Nx/2+1))
        ky=np.linspace(0,pi/delta_y/k0,int(const.Ny/2+1))
        kx = kx[0:int(const.Nx/2)]
        ky = ky[0:int(const.Nx/2)]
        Ky,Kx=np.meshgrid(ky,kx)

        Kxy=np.abs(Kxy[:int(const.Nx/2),:int(const.Ny/2)])#**2
    if Theta == '180':
        Kx,Ky,Kxy = FFt(bz)
        ####shift####
        #Kx = np.fft.ifftshift(Kx)
        #Ky = np.fft.ifftshift(Ky)
        #Kxy = np.fft.ifftshift(Kxy)
        #####
        #Kx = Kx[:int(const.Nx/2),:int(const.Nx/2)]
        #Ky = Ky[:int(const.Nx/2),:int(const.Nx/2)]
        #Kxy= np.abs(Kxy[:int(const.Nx/2),:int(const.Nx/2)])

        #Kx = Kx[int(const.Nx/2):,:-1]
        #Ky = Ky[int(const.Nx/2):,:-1]
        Kxy=np.abs(Kxy)#**2


        #Kxy = np.fft.fftshift(k_bz2d)
        #Kxy = np.abs(Kxy)
    return Kx,Ky,Kxy

def getTracer(x,setName='subset_selected1',particle='electron2'):
    ParticleName = setName + '/' + particle

    sdfdir=const.sdfdir +str(x).zfill(const.filenumber)+".sdf"
    data = sdf.read(sdfdir,dict=True)
    ID = data['Particles/ID/' + ParticleName].data

    Py = data['Particles/Py/' + ParticleName].data
    Px = data['Particles/Px/' + ParticleName].data
    Vy = data['Particles/Vy/' + ParticleName].data
    Vx = data['Particles/Vx/' + ParticleName].data

    Ek = data['Particles/Ek/' + ParticleName].data
    X = data['Grid/Particles/' + ParticleName].data[0]
    Y = data['Grid/Particles/' + ParticleName].data[1]

    Ex = data['Electric Field/Ex'].data
    Ey = data['Electric Field/Ey'].data


    #Ex[X,Y]
    #Ey[X,Y]

    Px = np.array(Px)
    Py = np.array(Py)
    Ek = np.array(Ek)
    Ek = Ek/MeV

    t = x * const.dt_snapshot
    TracerEx, TracerEy = getTracerField(t,Ex, Ey, X, Y)

    return {'ID':ID , 'X':X , 'TracerEx':TracerEx, 'Px':Px , 'Y':Y , 'TracerEy':TracerEy , 'Py':Py , 'Ek':Ek , 'Vx':Vx,'Vy':Vy}

def EnergeMap(x,mode = 'median',setName='subset_selected1',particle='electron2'):
    sdfdir=const.sdfdir +str(x).zfill(const.filenumber)+".sdf"
    data = sdf.read(sdfdir,dict=True)
    ParticleName = setName + '/' + particle
    Py = data['Particles/Py/' + ParticleName].data
    Px = data['Particles/Px/' + ParticleName].data
    Ek = data['Particles/Ek/' + ParticleName].data
    Px = np.array(Px)
    Py = np.array(Py)
    Ek = np.array(Ek)
    Ek = Ek/MeV
    #Ek[Ek>np.median(Ek)] = 0
    #print(Ek.mean())
    Px[Px==0] = 1/np.inf
    median = np.median(Ek)
    Theta = np.arctan(Py/Px)
    if mode == 'median':
        '''
        Theta = Theta[Ek<2*median]
        Ek=Ek[Ek<2*median]
        '''
    binX,binY = 200,500
    H , theta , ek = np.histogram2d(Theta,Ek,bins = [binX,binY])
    print('H.shape',H.shape)
    Ek , Theta = np.meshgrid(ek,theta)
    Ek = Ek[:binX,:binY]
    Theta = Theta[:binX,:binY]

    Ek1d = np.sum(H,axis = 0)
    indexEk = Ek[0,:]
    return indexEk,Ek1d

def ThetaElectron(x,mode = 'median',setName='subset_selected1',particle='electron2'):
    sdfdir=const.sdfdir +str(x).zfill(const.filenumber)+".sdf"
    data = sdf.read(sdfdir,dict=True)
    '''
    Py = data['Particles/Py/subset_selected1/electron1'].data
    Px = data['Particles/Px/subset_selected1/electron1'].data
    Ek = data['Particles/Ek/subset_selected1/electron1'].data
    X = data['Grid/Particles/subset_selected1/electron1'].data[0]
    Y = data['Grid/Particles/subset_selected1/electron1'].data[1]
    '''
    ParticleName = setName + '/' + particle
    Py = data['Particles/Py/' + ParticleName].data
    Px = data['Particles/Px/' + ParticleName].data
    Ek = data['Particles/Ek/' + ParticleName].data
    X = data['Grid/Particles/' + ParticleName].data[0]
    Y = data['Grid/Particles/' + ParticleName].data[1]

    Px = np.array(Px)
    Py = np.array(Py)
    Ek = np.array(Ek)
    Ek = Ek/MeV
    #Ek[Ek>np.median(Ek)] = 0
    #print(Ek.mean())
    Px[Px==0] = 1/np.inf
    Theta = np.arctan(Py/Px)
    #####
    median = np.median(Ek)
    if mode == 'median':
        Theta = Theta[Ek<2*median]
        Ek=Ek[Ek<2*median]

    #Theta = Theta[Ek>Ek.mean()/1000]
    #Ek=Ek[Ek>Ek.mean()/1000]
    binX,binY = 200,500
    H , theta , ek = np.histogram2d(Theta,Ek,bins = [binX,binY])
    print('H.shape',H.shape)
    Ek , Theta = np.meshgrid(ek,theta)
    Ek = Ek[:binX,:binY]
    Theta = Theta[:binX,:binY]
    '''

    data = np.vstack([Theta, Ek])
    kde = gaussian_kde(data)
    ###
    theta = np.linspace(-pi/2.0,pi/2.0,90)
    ek = np.linspace(0,median*2.0,90)
    #print(theta,ek)
    Ek ,Theta = np.meshgrid(ek,theta)
    print(Ek.shape,Theta.shape)
    Z = kde.evaluate(np.vstack([Ek.ravel(),Theta.ravel()]))
    Z = Z.reshape(Ek.shape)
    '''
    return Ek , Theta , H


def ThetaElectronLog(x,mode = 'all',setName='subset_selected1',particle='electron2'):
    sdfdir=const.sdfdir +str(x).zfill(const.filenumber)+".sdf"
    data = sdf.read(sdfdir,dict=True)
    '''
    Py = data['Particles/Py/subset_selected1/electron1'].data
    Px = data['Particles/Px/subset_selected1/electron1'].data
    Ek = data['Particles/Ek/subset_selected1/electron1'].data
    X = data['Grid/Particles/subset_selected1/electron1'].data[0]
    Y = data['Grid/Particles/subset_selected1/electron1'].data[1]
    '''
    ParticleName = setName + '/' + particle
    Py = data['Particles/Py/' + ParticleName].data
    Px = data['Particles/Px/' + ParticleName].data
    Ek = data['Particles/Ek/' + ParticleName].data
    X = data['Grid/Particles/' + ParticleName].data[0]
    Y = data['Grid/Particles/' + ParticleName].data[1]

    Px = np.array(Px)
    Py = np.array(Py)
    Ek = np.array(Ek)
    #Ek = Ek/MeV
    #Ek[Ek>np.median(Ek)] = 0
    #print(Ek.mean())
    Px[Px==0] = 1/np.inf
    Theta = np.arctan(Py/Px)
    #####
    median = np.median(Ek)
    if mode == 'median':
        Theta = Theta[Ek<2*median]
        Ek=Ek[Ek<2*median]

    #Theta = Theta[Ek>Ek.mean()/1000]
    #Ek=Ek[Ek>Ek.mean()/1000]
    binX,binY = 200,500
    ####Log####
    Ek = np.log(Ek)
    ###########

    H , theta , ek = np.histogram2d(Theta,Ek,bins = [binX,binY])
    print('H.shape',H.shape)
    Ek , Theta = np.meshgrid(ek,theta)
    Ek = Ek[:binX,:binY]
    Theta = Theta[:binX,:binY]
    Ek = np.exp(Ek)
    Ek = Ek/MeV
    '''

    data = np.vstack([Theta, Ek])
    kde = gaussian_kde(data)
    ###
    theta = np.linspace(-pi/2.0,pi/2.0,90)
    ek = np.linspace(0,median*2.0,90)
    #print(theta,ek)
    Ek ,Theta = np.meshgrid(ek,theta)
    print(Ek.shape,Theta.shape)
    Z = kde.evaluate(np.vstack([Ek.ravel(),Theta.ravel()]))
    Z = Z.reshape(Ek.shape)
    '''
    return Ek , Theta , H

    #return Ek , Theta , Z

@njit
def getStreamData(X,Y,Px,Py,Ek,Sx,Sy):
    #####
    XLength = const.y_lenth #600e-6
    YLength = const.x_end #600e-6
    dx = 1/10 * XLength #60e-6
    dy = 1/10 * YLength #60e-6
    #####
    SPx = Sx.copy() * 0
    SPy = Sy.copy() * 0
    count = Sx.copy() * 0
    #countY = Sx.copy() * 0
    TotalEk = Sx.copy() * 0
    for i in range(len(X)):
        indexX = round((X[i] - const.x_min)/dx)
        indexY = round((Y[i] - const.y_min)/dy)
             
        count[indexY,indexX] += 1
        SPx[indexY,indexX] += Px[i] #/ countX[int(X[i]/dx)]
        SPy[indexY,indexX] += Py[i] #/ countY[int(Y[i]/dy)]
        TotalEk[indexY,indexX] += Ek[i]/count[indexY,indexX]
        '''
        
        count[int((Y[i]+YLength/2+dy/2)/dy),int(X[i]/dx)] += 1
        SPx[int((Y[i]+YLength/2+dy/2)/dy),int(X[i]/dx)] += Px[i] #/ countX[int(X[i]/dx)]
        SPy[int((Y[i]+YLength/2+dy/2)/dy),int(X[i]/dx)] += Py[i] #/ countY[int(Y[i]/dy)]
        TotalEk[int((Y[i]+YLength/2+dy/2)/dy),int(X[i]/dx)] += Ek[i]/count[int((Y[i]+YLength/2+dy/2)/dy),int(X[i]/dx)]
        '''
    return Sx,Sy,SPx,SPy,TotalEk,count


def StreamE(x,setName='subset_selected1',particle='electron2'):
    #####
    #XLength = 600e-6
    #YLength = 600e-6
    #dx = 60e-6
    #dy = 60e-6
    XLength = const.y_lenth #600e-6
    YLength = const.x_end #600e-6
    dx = 1/10 * XLength #60e-6
    dy = 1/10 * YLength #60e-6
    print('dx,dy',dx,dy)

    #dx = 10e-6
    #dy = 10e-6

    #####
    sx = np.arange(const.x_min,const.x_max + dx,dx)
    sy = np.arange(const.y_min,const.y_max + dy,dy)
    Sx ,Sy = np.meshgrid(sx,sy)
    ####
    sdfdir=const.sdfdir +str(x).zfill(const.filenumber)+".sdf"
    data = sdf.read(sdfdir,dict=True)
    ParticleName = setName + '/' + particle

    Py = data['Particles/Py/' + ParticleName].data
    Px = data['Particles/Px/' + ParticleName].data
    Ek = data['Particles/Ek/' + ParticleName].data  
    X = data['Grid/Particles/' + ParticleName].data[0]
    Y = data['Grid/Particles/' + ParticleName].data[1]

    #XLength = X.max() - X.min()
    #YLength = Y.max() - Y.min()
    Ek = np.array(Ek)
    Py = np.array(Py)
    Px = np.array(Px)
    X = np.array(X)
    Y = np.array(Y)
    Ek = Ek/MeV
    Sx,Sy,SPx,SPy,TotalEk,count = getStreamData(X,Y,Px,Py,Ek,Sx,Sy)
    return Sx,Sy,SPx,SPy,TotalEk,count

def getJxJy(x):
    sx = np.arange(const.x_min,const.x_max + dx,dx)
    sy = np.arange(const.y_min,const.y_max + dy,dy)
    Sx ,Sy = np.meshgrid(sx,sy)
    ####
    sdfdir=const.sdfdir +str(x).zfill(const.filenumber)+".sdf"
    data = sdf.read(sdfdir,dict=True)
    #ParticleName = setName + '/' + particle

    Jy = data['Particles/Py/' + ParticleName].data
    Jx = data['Particles/Px/' + ParticleName].data

    return Sx,Sy,Jx,Jy    

'''
def getStreamData(X,Y,Px,Py,Ek):
    sx = np.arange(0,600e-6+dx,dx)
    sy = np.arange(-300e-6,300e-6+dy,dy)
    Sx ,Sy = np.meshgrid(sx,sy)
    SPx = Sx.copy() * 0
    SPy = Sy.copy() * 0
    count = Sx.copy() * 0
    #countY = Sx.copy() * 0
    TotalEk = Sx.copy() * 0 
    for i in range(len(X)):
        #Sx[int(X[i]/1e-6)] += 1
        #countX[int(X[i]/dx)] += 1
        count[int((Y[i]+YLength/2+dy/2)/dy),int(X[i]/dx)] += 1
        SPx[int((Y[i]+YLength/2+dy/2)/dy),int(X[i]/dx)] += Px[i] #/ countX[int(X[i]/dx)]
        SPy[int((Y[i]+YLength/2+dy/2)/dy),int(X[i]/dx)] += Py[i] #/ countY[int(Y[i]/dy)]
        TotalEk[int((Y[i]+YLength/2+dy/2)/dy),int(X[i]/dx)] += Ek[i]/count[int((Y[i]+YLength/2+dy/2)/dy),int(X[i]/dx)]
    #SPx , SPy = np.meshgrid(sPx,sPy)
    return Sx,Sy,SPx,SPy,TotalEk,count
'''



def getRofK(THzmin,THzmax):
    #R1 = 2 * pi / c / THzmin
    #R2 = 2 * pi / c / THzmax
    kmin = 2*pi*THzmin/c
    kmax = 2*pi*THzmax/c

    return kmin , kmax


@njit
def KfilterBak(k_bz2,R1,R2):
    #k_bz2d=np.fft.fft2(bz)
    #delta_k=3.14/const.delta_x/(const.Nx/2)
    #k_bz2=k_bz*1
    #print("n",k_n[0],k_n[-1])
    #R1=k_n[0]
    #R2=k_n[-1]
    #delta_kx = pi/const.delta_x/(const.Nx/2)
    delta_kx = 2*pi / (const.Nx * const.delta_x)
    delta_ky = 2*pi / (const.Ny * const.delta_y)
    #delta_ky = pi/const.delta_y/(const.Ny/2)
    x1=(const.Nx)*delta_kx
    y1=(const.Ny)*delta_ky
    for i in range(0,const.Nx):
        for j in range(0,const.Ny):
            if np.sqrt((i*delta_kx)**2+(j*delta_ky)**2) > R2 and np.sqrt(((i*delta_kx)-x1)**2+(j*delta_ky)**2) > R2 and np.sqrt((i*delta_kx)**2+((j*delta_ky)-y1)**2) > R2 and np.sqrt(((i*delta_kx)-x1)**2+((j*delta_ky)-y1)**2) > R2:
                k_bz2[i,j]=0
            if np.sqrt((i*delta_kx)**2+(j*delta_ky)**2) < R1 or np.sqrt((i*delta_kx)**2+((j*delta_ky)-y1)**2) < R1 or np.sqrt(((i*delta_kx)-x1)**2+(j*delta_ky)**2) < R1 or np.sqrt(((i*delta_kx)-x1)**2+((j*delta_ky)-y1)**2) < R1:
                                k_bz2[i,j]=0


    return k_bz2
@njit
def KfilterN(k_bz2, R1, R2):
    x1 = const.Nx #- 1
    y1 = const.Ny #- 1
    delta_kx = 3.14 / const.delta_x / (const.Nx / 2)
    delta_ky = 3.14 / const.delta_y / (const.Ny / 2)
    for i in range(0, const.Nx):
        for j in range(0, const.Ny):
            if i**2 + (j * delta_ky / delta_kx)**2 > R2**2 and (i - x1)**2 + (j * delta_ky / delta_kx)**2 > R2**2 and i**2 + \
                       ((j - y1) * delta_ky / delta_kx)**2 > R2**2 and (i - x1)**2 + ((j - y1) * delta_ky / delta_kx)**2 > R2**2:
                k_bz2[i, j] = 0
            if i**2 + (j * delta_ky / delta_kx)**2 < R1**2 or i**2 + ((j - y1) * delta_ky / delta_kx)**2 < R1**2 or (
                i - x1)**2 + (j * delta_ky / delta_kx)**2 < R1**2 or (i - x1)**2 + ((j - y1) * delta_ky / delta_kx)**2 < R1**2:
                k_bz2[i, j] = 0
    return k_bz2

def KFilter(Kx,Ky,Kxy,R1 = 0.1,R2 = 10):
    K = np.sqrt(Kx**2 + Ky**2)
    Kxy[K>10]=0
    Kxy[K<0.1]=0
    Kxy = np.fft.ifftshift(Kxy)
    return Kxy

def KTHz(Kx,Ky,Kxy,R1 = 0.1,R2 = 10,bins=[1000,1000]):
    #K = np.sqrt(Kx**2 + Ky**2)
    #KTHz = Kxy[Kx<10 and Ky<10]
    #KTHz = Kxy[np.where(Kx<10 and Ky<10,True,False)]
    #Kx = Kx[Kx<10]
    #Ky = ky[Ky<10]
    kthz = Kxy[np.abs(Kx)<R2][np.abs(Ky[np.abs(Kx)<R2])<R2]
    kx = Kx[np.abs(Kx)<R2][np.abs(Ky[np.abs(Kx)<R2])<R2]
    ky = Ky[np.abs(Ky)<R2][np.abs(Kx[np.abs(Ky)<R2])<R2]
    #kx = Kx[:,0]
    #ky = Ky[0,:]
    #kx = kx[np.abs(kx)<10]
    #ky = ky[np.abs(ky)<10]
    #kx = Kx[:,0]
    #ky = Ky[0,:]
    kthz = np.abs(kthz)
    ###f = interp2d(np.hstack((kx,ky)),kthz)
    newkx = np.linspace(kx.min(),kx.max(),bins[0])
    newky = np.linspace(ky.min(),ky.max(),bins[1])
    #print(KTHz.shape)
    #print(kx,ky)
    ###NewKTHz = f(newkx,newky)

    #NewKTHz = griddata(np.hstack(kx,ky),kthz,)
    XX,YY = np.meshgrid(newkx,newky)
    K = np.sqrt(XX**2 + YY**2)
    #print(XX.shape)
    points = np.vstack((kx,ky)).T
    #print(points.shape)
    NewKTHz = griddata(points,kthz,(XX,YY),method='cubic')
    dS = (2*pi/(const.Ny*delta_y)/k0) * (2*pi/(const.Nx*delta_x)/k0)
    dSNew = (newkx[1]-newkx[0])*(newky[1]-newky[0])

    ###
    NewKTHz[K>R2]=0
    NewKTHz[K<R1]=0
    #Sum = np.sum(NewKHz**2)*dSNew/dS    
    ###
    NewKTHz = NewKTHz * np.sqrt(dSNew/dS)
    Sum = np.sum(NewKTHz**2)
    return XX,YY,NewKTHz#,dS,dSNew





def LeftWrapper(bz,Field,distance):
    KPolarTHzWrapper(bz,Field,distance,'Left')

def KPolarTHzWrapper(x,bz,Field,distance,direction):
    Limit = 10
    if direction == 'Left':
        Kx,Ky,Kxy = FFtLeft(bz,distance)
    if direction == 'Right':
        Kx,Ky,Kxy = FFtRight(bz,distance)
    if direction == 'All':
        Kx,Ky,Kxy = FFt(bz)
    ETotal = np.sum(np.sum(np.square(np.abs(Kxy))))/const.Nx/const.Ny
    Kx,Ky,Kxy = KTHz(Kx,Ky,Kxy,R1=0.1,R2 = Limit)
    ETHz = np.sum(np.sum(np.square(np.abs(Kxy))))/const.Nx/const.Ny
    ######
    #print(ETotal)
    #print('Eff:',ETHz/ETotal)
    #############################
    ######  add eff to csv  #####
    #############################
    cars = {'index':[x],
            'ETHz':[ETHz],
            'ETotal':[ETotal]
            }
    df = pd.DataFrame(cars, columns = ['index','ETHz','ETotal'])
    filepath = const.txtdir + str(Field) + direction + 'THz' +'Ksqrt.csv'
    #print(df)
    if os.path.exists(filepath)==True:
        df.to_csv(filepath,mode = 'a',header = False , index = False)
    else:
        df.to_csv(filepath,mode = 'a',index = False)
    #########
    return Kx,Ky,Kxy




def KThetaFilter(XX,YY,KTHz,minTheta,maxTheta):
    XX[XX == 0 ] = 1/1e12#np.inf
    YY[YY == 0 ] = 1/1e12
    Theta = YY/XX
    KTHz[np.abs(Theta)<minTheta] = 0
    KTHz[np.abs(Theta)>maxTheta] = 0
    Sum = np.sum(KTHz**2)
    return Sum

class Constant:
    def __init__(wkdir='Data'):
        wkdir = wkdir    
        data_name = case_name+"/"
        self.epochdir = '/home/yujq/users/caijie/epoch2d'
        self.sdfdir  =  epochdir+"/Data/"+data_name
        self.txtdir  =  epochdir+"/txt/"+data_name
        self.figdir  =  epochdir+"/fig/"+data_name
        self.gifdir  =  epochdir+"/gif/"+data_name
        self.pngdir  =  epochdir+"/gif/png/"
        self.loop = getflist(self,sdfdir)
        self.start=1
        self.stop=int(loop[-1])
        self.step=1
        print(self.stop)
        self.filenumber = len(str(loop[-1]))

    def getflist(self,sdfdir):
        a=os.listdir(sdfdir)
        a=[i.split('.') for i in a]
        loop=[i for i in a if i[1] == 'sdf']
        loop=np.array(loop)
        loop=loop[:,0]
        loop=np.sort(loop)
        return loop
    
