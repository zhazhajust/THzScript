from scipy.interpolate import interpn
import sdf
import constant as const
import numpy as np
import matplotlib.pyplot as plt
import os
import multiprocessing
import KThetaMax
import colorbar
import Processing

interval = 100
Limit = 30
pngdir = const.gifdir + 'Kpolarpng/'
os.makedirs(pngdir,exist_ok = True)


def main(x):
    Limit = 30
    print(x)
    Field = 'Ey'
    pngdir = const.gifdir + 'MaxTheta/' 
    os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    savedir = pngdir + Field + str(x) + 'KMaxtheta.jpg'
    KThetaMax.main(x,'Ey',Limit,savedir)

 
pool = multiprocessing.Pool(processes=96)   #,initargs=(ss1,ss2))
               #for i in range(start,stop+step,step):
        #       results.append(pool.apply_async(extract, (i, ))) 
 
#arr = range(1,const.stop,int(const.stop/interval))

arr = Processing.flist()
arr = arr[::int(len(arr)/100)]

print(arr)
#arr = [100]
results = pool.map(main,arr)
 
 
#for x in range(1,const.stop,int(const.stop/interval)):
#        image_list.append(png_savedir+str(x)+"ref_k.png")
pool.close()
pool.join()
