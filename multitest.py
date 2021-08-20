from scipy.interpolate import interpn
import sdf
import constant as const
import numpy as np
import matplotlib.pyplot as plt
import os
import multiprocessing
import Kpolar as helper
import colorbar
import Processing

interval = 100
Limit = 500
pngdir = const.gifdir + 'Kpolarpng/'
os.makedirs(pngdir,exist_ok = True)


def main(x):
    print(x)
    #savedir = pngdir + 'polar' + str(x) + 'Ktheta.jpg'
    #x = 1900
    Limit = 500
    ####
    iname = 'jet'
    cmap = colorbar.getTransCmap(lambda x:(0.7 + (1/256*x) *0.3),iname)
    pngdir = const.gifdir + 'Kpolarpng/'
    os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    savedir = const.figdir + 'F' + str(Limit)+'polar' + str(x) + 'Ktheta.jpg'


    bz = Processing.getBz(x)
    Kx,Ky,Kxy = Processing.getKBz(bz)
    KKx,KKy,KKxy = helper.unravel(Kx,Ky,Kxy)
    theta,K = helper.getThetaK(KKx,KKy)
    helper.draw(theta,K,KKxy,Limit,savedir,cmap)
 
pool = multiprocessing.Pool(processes=96)   #,initargs=(ss1,ss2))
               #for i in range(start,stop+step,step):
        #       results.append(pool.apply_async(extract, (i, ))) 
 
#arr = range(1,const.stop,int(const.stop/interval))
arr = [100]
results = pool.map(main,arr)
 
 
#for x in range(1,const.stop,int(const.stop/interval)):
#        image_list.append(png_savedir+str(x)+"ref_k.png")
pool.close()
pool.join()
