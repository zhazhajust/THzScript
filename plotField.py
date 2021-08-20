import matplotlib.pyplot as plt
import Processing
import matplotlib as mpl
import sys
import constant as const
import numpy as np
plt.switch_backend('agg')
pi = 3.1415926

#datadir = savedir
#datadir = '/home/yujq/users/caijie/epoch2d/txt/MassLimit/new_a3_w9.1_n0.2/y50x300/318.0$mu m$TimeSequence.npy'
#Field = Processing.Field



def plotField(Field,title,savedir):
    #Theta , Time = Theta*180/3.14 , Time/1e-15
    #plt.pcolormesh(theta,time,data,cmap = plt.cm.bwr)
    x = np.linspace(-const.x_min,const.x_max,const.Nx)
    y = np.linspace(-const.y_min,const.y_max,const.Ny)
    X , Y = np.meshgrid(x,y)

    plt.pcolormesh(X,Y,Field.T,cmap = plt.cm.bwr)
    
    plt.colorbar()
    plt.title(title)
    plt.savefig(savedir + 'Field.jpg',dpi=160)
    plt.close('all')


def main(x,Field = 'Ey'):
    if Field == 'Ey':
        ElectricField , title = Processing.getEy(x)
    if Field == 'Ex':
        ElectricField , title = Processing.getEx(x)
    savedir = const.figdir + Field + str(x)
    plotField(ElectricField,title,savedir)

if __name__ == '__main__':
    Field = 'Ey'
    x = 400
    main(x)