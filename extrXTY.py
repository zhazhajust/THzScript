# -- coding: utf-8 --
import sys
import multiprocessing
from multiprocessing import shared_memory
import constant as const
from matplotlib import colors, ticker, cm
from numpy import ma
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import math
import sdf
import matplotlib
import math
matplotlib.use('agg')

savedir = const.txtdir  # "./txt/a0_1_2e-2/"
savename = "XtMatr.npy"
fftdir = const.figdir  # "./fig/a0_1_2e-2/"
###
dirsdf = const.sdfdir   # '../Data/a0_1_2e-2/'
dirsize = const.filenumber  # 4
x_interval = 100
y_interval = 1
xStartDistance = sys.argv[2]
xStart = int(float(xStartDistance)/const.delta_x/x_interval)
xEnd = int(max((xStart + const.Nx/x_interval) , const.stop/x_interval))
Xarr = const.delta_x * x_interval * np.arange(xStart,xEnd+2)
print('Xarr.shape',Xarr.shape)
print('start end',xStart , xEnd)
def extract(n):
    #### header data ####
    print('n:'+str(n))
    # xt = np.frombuffer(global_arr_shared, np.double).reshape(SHAPE)
    xt = np.ndarray(ss1, dtype=ss2, buffer=shm.buf)  # xt[X,T,Y]
    data = sdf.read(dirsdf+str(n).zfill(dirsize)+".sdf", dict=True)
    header = data['Header']
    time = header['time']
    # E_y0=data['Electric Field/Ey'].data[:,int(y)]
    #E = data['Electric Field/Ey'].data[:,::int(y_interval)]
    E = data['Magnetic Field/Bz'].data[:,::int(y_interval)]
    if  n  <  start_move_number:
        for x in range(xStart,xEnd+1):
            a=int(x*x_interval)
            d_n=int((1e15*delta_x*a/c)/dt)
            if n-d_n > 0 and n-d_n < t_size :# [fs]
                xt[x-xStart,n-d_n,:]=E[a-1,:] #/bxunit            
    else:
        # for x in range(1,int(xgrid/x_interval)+1):
        for x in range(xStart,xEnd+1):
            a=int(x*x_interval)
            if a-c*(time-window_start_time)/delta_x >= 0 and a-c*(time-window_start_time)/delta_x < gridnumber-1:
    # [fs]
                d_n=int((1e15*delta_x*a/c)/dt)
                xt[x-xStart,n-d_n,:]=E[int(round(a-c*(time-window_start_time)/delta_x)),:]  #/bxunit
    return "OK"+str(n)
                   # else:bz.append(0)
                   # print 'Reading finished%d' %len(t)
if __name__ == "__main__":
    ######## Constant defined here ########
    pi        =     3.1415926535897932384626
    q0        =     1.602176565e-19 # C
    m0        =     9.10938291e-31  # kg
    v0        =     2.99792458e8    # m/s^2
    kb        =     1.3806488e-23   # J/K
    mu0       =     4.0e-7*pi       # N/A^2
    epsilon0  =     8.8541878176203899e-12 # F/m
    h_planck  =     6.62606957e-34  # J s
    # lamada


    wavelength=     const.lamada     #10.6e-6

    ####

    frequency =     v0*2*pi/wavelength
    micron    =     1e-6
    c         =     3e8
    exunit    =     m0*v0*frequency/q0
    bxunit    =     m0*frequency/q0
    denunit    =     frequency**2*epsilon0*m0/q0**2
    print('electric field unit: '+str(exunit))
    print('magnetic field unit: '+str(bxunit))
    print('density unit nc: '+str(denunit))
    font = {'family' : 'monospace',  
        'color'  : 'black',  
        'weight' : 'normal',  
        'size'   : 28,  
    }  
    if (os.path.isdir(savedir) == False):
        os.mkdir(savedir)
        
    if (os.path.isdir(fftdir) == False):
        os.mkdir(fftdir)    
    ######### Script code drawing figure ################
    # constant
    ###
    c       =  3e8
    micron  =  1e-6
    lamada  =  const.lamada #10.6 * micron
    gridnumber = const.Nx     #2400
    start   =  1
    stop    =  const.stop       #5889 #17000
    step    =  1
    dt_snapshot= const.dt_snapshot     #1e-15
    dt      =  dt_snapshot*1e15      #fs
    x_max   =  const.x_max      #80 * lamada   #60 * lamada    #micron
    x_min   =  0 * micron
    x_end   =  x_max - x_min
    y       =  const.Ny/2 
    window_start_time =  (x_max - x_min) / c
    # start_move_number = window_start_time * 1e15      #fs
    start_move_number =  int(window_start_time / dt_snapshot)
    delta_x =  x_end/gridnumber
    t_end   =  stop * dt_snapshot
    #x_interval=const.x_interval          #10
    t_total=1e15*x_end/c         #fs
    t_size=t_total/(dt_snapshot*1e15)+1           #t_grid_number
    if t_end-window_start_time<0:
        xgrid   =  int(gridnumber)
    else: 
        xgrid   =  int(gridnumber + c*(t_end-window_start_time)/delta_x)

####################
    #x_interval= const.x_interval      #10
    t_total=1e15*x_end/c         #fs
    t_size=int(t_total/dt)+1+1   

# allay define
    SHAPE = ((int(xgrid/x_interval)+1,t_size))

    # xRange = int(xgrid/x_interval + 1)
    xRange = int(xEnd - xStart)
    tRange = t_size
    # xStart = c * (tStart-start_move_number) * const.dt_snapshot / const.delta_x
    # xEnd = c * (tStart-start_move_number) *const.dt_snapshot / const.delta_x + const.Nx

    tStart = float(xStartDistance)/c/const.dt_snapshot #xStart*x_interval * const.delta_x / const.dt_snapshot / c # + start_move_number - const.Nx*const.delta_x/c/const.dt_snapshot
    tEnd = tStart + const.delta_x * const.Nx/c/const.dt_snapshot
    print('tStart,tEnd',tStart,tEnd)
    tEnd = min(tEnd,const.stop)
    print(xRange,tRange,const.Ny)
    a = np.zeros((xRange+2,tRange+2,int((const.Ny-1)/y_interval+1)))
    print('a.shape',a.shape)
    print(xRange,tRange,const.Ny)
    shm = shared_memory.SharedMemory(create=True, size=a.nbytes)

    ss1,ss2=a.shape,a.dtype
    pool = multiprocessing.Pool(processes=96,initargs=(ss1,ss2))
    print('range:',np.arange(int(tStart),int(tEnd)))
    results = pool.map(extract,np.arange(int(tStart),int(tEnd)))
    pool.close()
    pool.join()
    xt = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)
    np.save(savedir+savename, xt)
    np.save(savedir + 'Xarr.npy',Xarr)
    shm.close()
    shm.unlink()
    print('XtMatr saved')
    Xf = np.fft.rfft(xt,axis=1)
    np.save(savedir + 'XfMatr.npy',Xf)
    print('XfMatr saved')
