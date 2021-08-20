from scipy.interpolate import interpn
import sdf
import constant as const
import numpy as np
import matplotlib.pyplot as plt
import os
import multiprocessing
import Kpolar
import colorbar
import Processing
import KTHzPolarRight
import KTHzPolarLeft
import sys
import pandas as pd

#interval = 100
#Limit = 10
#pngdir = const.gifdir + 'Kpolarpng/'
#os.makedirs(pngdir,exist_ok = True)

#distance = 318e-6 
#if len(sys.argv) > 2:
#    distance = sys.argv[2]
####################
Field = Processing.Field
####################
######constant######
try:
    x_right = const.start_move_locate
    print('x_right = const.start_move_locate')
except:
    x_right = const.x_max/2
    print('x_right = const.x_max/2')
distance = x_right #300e-6
if len(sys.argv) > 2:
    distance = sys.argv[2]
####################
####################

def creatCSV(Field):
    df = pd.DataFrame(columns = ['index','ETHz','ETotal'])
    filepath = const.txtdir + str(Field) + 'Right' + 'THz' +'Ksqrt.csv'
    df.to_csv(filepath,mode = 'w', index = False)
    filepath = const.txtdir + str(Field) + 'Right' + 'THz' +'Ksqrt.csv'
    df.to_csv(filepath,mode = 'w', index = False)
    return


def KpolarWrapper(x,Field):
    print(x)
    #savedir = pngdir + 'polar' + str(x) + 'Ktheta.jpg'
    #x = 1900
    Limit = 30
    ####
    iname = 'jet'
    cmap = colorbar.getTransCmap(lambda x:(0.7 + (1/256*x) *0.3),iname)
    pngdir = const.gifdir + Field +'Kpolarpng/'
    os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    savedir = pngdir + 'F' + str(Limit)+'polar' + str(x) + 'Ktheta.jpg'
    #try:
    Kpolar.main(x,Limit,savedir,cmap,Field)
    #except:
    #    pass
        #Kpolar.main(x+1,Limit,savedir,cmap)
    #bz = Processing.getBz(x)
    #Kx,Ky,Kxy = Processing.getKBz(bz)
    #KKx,KKy,KKxy = helper.unravel(Kx,Ky,Kxy)
    #theta,K = helper.getThetaK(KKx,KKy)
    #helper.draw(theta,K,KKxy,Limit,savedir,cmap)

def KpolarTHzWrapper(x,Field):
    print(x)
    #savedir = pngdir + 'polar' + str(x) + 'Ktheta.jpg'
    #x = 1900
    Limit = 10
    ####
    iname = 'jet'
    cmap = colorbar.getTransCmap(lambda x:(0.7 + (1/256*x) *0.3),iname)
    pngdir = const.gifdir + Field +'KTHzpolar/'
    os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    savedir = pngdir + 'THz' + str(Limit)+ 'polar' + str(x) + 'Ktheta.jpg'
    #try:
    Kpolar.main(x,Limit,savedir,cmap,Field)

def KpolarTHzRightWrapper(x,Field):
    print(x)
    #savedir = pngdir + 'polar' + str(x) + 'Ktheta.jpg'
    #x = 1900
    Limit = 10
    ####
    iname = 'jet'
    cmap = colorbar.getTransCmap(lambda x:(0.7 + (1/256*x) *0.3),iname)
    pngdir = const.gifdir + Field + 'KTHzRightpolar/'
    os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    #savedir = pngdir + 'THz' + str(Limit)+'polar' + str(x) + 'Ktheta.jpg'
    savedirIM = pngdir + Field  + str(Limit)+'KPolarRight' + str(x) + 'Ktheta.jpg'
    savedirLine = pngdir + Field  + str(Limit)+'KPolarRight' + str(x) + 'KthetaLine.jpg'
    savedirDict = [savedirIM,savedirLine]

    #try:
    #KTHzPolarRight.main(x,Limit,savedir,cmap,Field)
    KTHzPolarRight.main(x,distance,Limit,savedirDict,cmap,Field)#,'Right')

def KpolarTHzLeftWrapper(x,Field):
    print(x)
    #savedir = pngdir + 'polar' + str(x) + 'Ktheta.jpg'
    #x = 1900
    Limit = 10
    ####
    iname = 'jet'
    cmap = colorbar.getTransCmap(lambda x:(0.7 + (1/256*x) *0.3),iname)
    pngdir = const.gifdir + Field +'KTHzLeftpolar/'
    os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    #savedir = pngdir + 'THz' + str(Limit)+'polar' + str(x) + 'Ktheta.jpg'
    savedirIM = pngdir + Field  + str(Limit)+'KPolarRight' + str(x) + 'Ktheta.jpg'
    savedirLine = pngdir + Field  + str(Limit)+'KPolarRight' + str(x) + 'KthetaLine.jpg'
    savedirDict = [savedirIM,savedirLine]

    #try:
    #KTHzPolarLeft.main(x,Limit,savedir,cmap,Field)
    KTHzPolarLeft.main(x,distance,Limit,savedirDict,cmap,Field)#,direction = 'Left')

def main(x):
    try:
        Field = Processing.Field
    #KpolarWrapper(x,Field)
    #KpolarTHzWrapper(x,Field)
        KpolarTHzRightWrapper(x,Field)
        KpolarTHzLeftWrapper(x,Field)
    except:
        print('wrong')
        pass

if __name__ == '__main__':
    ################
    ####constant####
    #distance = 318e-6
    #if len(sys.argv) > 2:
    #    distance = sys.argv[2]
    ################
    ################

    #filepath = const.txtdir + str(Field) + 'Right' + 'THz' +'Ksqrt.csv'
    #os.remove(filepath)
    #filepath = const.txtdir + str(Field) + 'Left' + 'THz' +'Ksqrt.csv'
    #os.remove(filepath)


    creatCSV(Field)    
    #############
    #arr = Processing.flist()
    #arr = arr[1::int(len(arr)/100)]
    pool = multiprocessing.Pool(processes=96)   #,initargs=(ss1,ss2))
               #for i in range(start,stop+step,step):
        #       results.append(pool.apply_async(extract, (i, ))) 
 
#arr = range(1,const.stop,int(const.stop/interval))

    arr = Processing.flist()
    arr = arr[::int(len(arr)/100)]

#print(arr)
    #arr = [100]
    results = pool.map(main,arr)
 
#for x in range(1,const.stop,int(const.stop/interval)):
#        image_list.append(png_savedir+str(x)+"ref_k.png")
    pool.close()
    pool.join()
    #for i in arr:
    #    main(i)
