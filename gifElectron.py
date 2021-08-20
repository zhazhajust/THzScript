from scipy.interpolate import interpn
import sdf
import constant as const
#import numpy as np
#import matplotlib.pyplot as plt
import os
import multiprocessing
#import Kpolar
#import colorbar
import Processing
import THzPlot
import ThetaElectronMedian
import ThetaElectronLog
import ThetaElectron
import StreamE
#interval = 100
#Limit = 30
pngdir = const.gifdir + 'Kpolarpng/'
os.makedirs(pngdir,exist_ok = True)
MaxIndex = (const.las_t_fwhm1/const.dt_snapshot)*2


def ThetaEMedianWrapper(x):
    #pngdir = const.gifdir + ''
    pngdir = const.gifdir  +'ThetaEMedian/'
    os.makedirs(pngdir,exist_ok = True) 
    savedir = pngdir + 'ThetaE' + str(x) + 'median.jpg'
    ThetaElectronMedian.plotThetaE(x,savedir)

def ThetaELogWrapper(x):
    #pngdir = const.gifdir + ''
    pngdir = const.gifdir  +'ThetaELog/'
    os.makedirs(pngdir,exist_ok = True)
    savedir = pngdir + 'ThetaE' + str(x) + 'Log.jpg'
    ThetaElectronLog.plotThetaE(x,savedir)

def ThetaEWrapper(x):
    #pngdir = const.gifdir + ''
    pngdir = const.gifdir  +'ThetaE/'
    os.makedirs(pngdir,exist_ok = True)
    savedir = pngdir + 'ThetaE' + str(x) + '.jpg'
    ThetaElectron.plotThetaE(x,savedir)

def StreamWrapper(x):
    ####
    pngdir = const.gifdir +'StreamElectron/'
    os.makedirs(pngdir,exist_ok = True)
    savedir = pngdir + 'XY_' + str(x) + 'Stream.jpg'
    #Sx,Sy,SPx,SPy,Ek,count = getStream(x)
    StreamE.plotStream(x,savedir)

def main(x):
    print('x',x)
    #ThetaEMedianWrapper(x)
    StreamWrapper(x)
    ThetaELogWrapper(x)
    ThetaEWrapper(x)
pool = multiprocessing.Pool(processes=96)   #,initargs=(ss1,ss2))
arr = Processing.flist()
MaxIndex = arr[int(MaxIndex)]

#if len(arr) > 100:
#    arr = arr[::int(len(arr)/100)]
arr = arr[::20]

#arr[0] = MaxIndex
print(arr)


#arr = [100]

main(arr[0])
results = pool.map(main,arr[1:])
 
 
#for x in range(1,const.stop,int(const.stop/interval)):
#        image_list.append(png_savedir+str(x)+"ref_k.png")
pool.close()
pool.join()
