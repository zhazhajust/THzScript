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

#interval = 100
#Limit = 30
#pngdir = const.gifdir + 'Kpolarpng/'
#os.makedirs(pngdir,exist_ok = True)

#MaxIndex = (const.las_t_fwhm1/const.dt_snapshot)*2
MaxIndex = Processing.MaxIndex #int(const.x_spot/2/c/const.dt_snapshot)

print('dt:',const.dt_snapshot)
Field = Processing.Field
#####

THzPlot.creatCSV(Field)

def main(x):
    print('x',x)
    THzPlot.main(x,Field)
 
pool = multiprocessing.Pool(processes=96)   #,initargs=(ss1,ss2))
arr = Processing.flist()
MaxIndex = arr[int(MaxIndex)]

if len(arr) > 100:
    arr = arr[::int(len(arr)/100)]
arr[0] = MaxIndex
print(arr)
#arr = [100]

main(arr[0])
results = pool.map(main,arr[1:])
 
 
#for x in range(1,const.stop,int(const.stop/interval)):
#        image_list.append(png_savedir+str(x)+"ref_k.png")
pool.close()
pool.join()
