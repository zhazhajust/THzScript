from scipy.interpolate import interpn
import sdf
import constant as const
import numpy as np
import matplotlib.pyplot as plt
import os
import Processing
import colorbar
import Kpolar
import KTHzTheta
plt.switch_backend('agg')

#cmap = colorbar.cmap_trans
####
####constant####
pi = 3.1415926
delta_x=const.delta_x
delta_y=const.delta_y
#####
def getThetaK(KKx,KKy):
    ######theta , k generator####
    #theta = np.arctan(KKy/KKx)
    #K = np.sqrt(KKx**2+KKy**2)

    K = np.sqrt(KKx**2+KKy**2)
    KKx[KKx==0] = 1/1e12
    KKy[KKy==0] = 1/1e12
    theta = np.arctan(KKy/KKx)+pi
    #return theta,K
    return theta,K


def main(x,distance,Limit,savedir,cmap,Field = 'Bz',direction = 'Left'):
    #direction = 'Left'
    if Field == 'Bz':
        #bz ,title = Processing.getBz(x)
        bz ,title = Processing.getBz(x)
    #distance = const.x_end/2 + 18e-6
    Kx,Ky,Kxy = Processing.KPolarTHzWrapper(x,bz,Field,distance,direction)
    Kxy = np.abs(Kxy)
    print(Kxy.shape)
    KKx,KKy,KKxy = Kpolar.unravel(Kx,Ky,Kxy)
    theta,K = getThetaK(KKx,KKy)
    Kpolar.draw(theta,K,KKxy,x,Limit,savedir[0],title,cmap)

    Phi,I = KTHzTheta.ThetaMaxLeft(theta,K,KKxy)
    KTHzTheta.drawMaxTheta(Phi,I,x,savedir[1],title)
 

if __name__ == '__main__':
    Field = 'Bz'
    x = 1250
    distance = 300e-6
    Limit = 10
    ####
    iname = 'jet'
    cmap = colorbar.getTransCmap(lambda x:(0.7 + (1/256*x) *0.3),iname)
    pngdir = const.gifdir + Field + 'KpolarLeft/'
    os.makedirs(pngdir,exist_ok = True)
    ####savedir###
    #savedir = const.figdir + Field  + str(Limit)+'KPolarLeft' + str(x) + 'Ktheta.jpg'
    savedirIM = const.figdir + Field  + str(Limit)+'KPolarLeft' + str(x) + 'Ktheta.jpg'
    savedirLine = const.figdir + Field  + str(Limit)+'KPolarLeft' + str(x) + 'KthetaLine.jpg'
    savedir = [savedirIM,savedirLine]

    main(x,distance,Limit,savedir,cmap,Field)
    #main(x,Limit)
