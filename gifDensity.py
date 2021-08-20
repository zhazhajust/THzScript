import numpy as np
import matplotlib.pyplot as plt
import sdf
import math
import os
import scipy.signal as signal
import constant as const
import imageio
import function as func
import scipy.fftpack as fftpack
from matplotlib.ticker import MultipleLocator, FuncFormatter
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing
import matplotlib as mpl
import Processing
# import wigner
plt.switch_backend('agg')
###
####
pi = math.pi
interval = 100
image_list = []
pngdir = const.gifdir + 'Densitypng/'
os.makedirs(pngdir, exist_ok=True)
png_savedir = pngdir  # './gif/png/'#const.gifdir
intervel = 100e-6
Ny = intervel / const.delta_y
Ny = int(Ny)


def k_n():
	delta_k = 3.14 / const.delta_x / (const.Nx / 2)
	k_n = []
	for n in range(0, const.Nx):
		mi = 3e8 / 0.1e12
		ma = 3e8 / 10e12
		if 2 * 3.14 / ma > n * delta_k and n * delta_k > 2 * 3.14 / mi:
			k_n.append(n)
	return k_n


def x_formatter(x, pos):
    a = (const.delta_x * x + const.c * T) * 1e6
    return "%d" % int(a)


def x_formatter2(x, pos):
    # locate = x * const.nperseg
    a = x + const.c * T * 1e6
    return "%d" % int(a)


def draw(x):
    # savefigdir=const.figdir+str(int(locate/1e-6))+'_'+str(Thz1)+'_'+str(Thz2)+'k_bz.png'
    sdfdir = const.sdfdir + str(x).zfill(const.filenumber) + ".sdf"
    data=sdf.read(sdfdir,dict=True)
    time=data['Header']['time']
    ###
    global T
    # time=data['Header']['time']
    if time-const.window_start_time<0:
        T=0
    else:
        T=time-const.window_start_time
    ne=data['Derived/Number_Density/electron1'].data
    ne=ne.T	
    ne = ne[Ny:-Ny,:]
    fig,axs=plt.subplots(figsize=(4,3))
    #im2=axs.pcolormesh(ne)#,norm=mpl.colors.LogNorm())#,cmap=plt.cm.jet)
    im = plt.pcolormesh(ne)
    plt.colorbar()
    t_fs=int(time/1e-15)
    plt.set_label("t="+str(t_fs),fontsize=12,color='r')

    # axs[0][0].set_title(str(x*const.dt_snapshot))
    #axs.xaxis.set_major_formatter( FuncFormatter( x_formatter ) )

    fig.savefig(png_savedir+str(x)+"ref_k.png",dpi=200)
    image_list.append(png_savedir+str(x)+"ref_k.png")
    plt.clf()
    plt.close('all')
    return
image_list=[]
k_n=k_n()
pool = multiprocessing.Pool(processes=96)   #,initargs=(ss1,ss2))

arr = Processing.flist()
if len(arr) > 100:
    arr = arr[::int(len(arr)/100)]
print(arr)
# arr = [100]
results = pool.map(draw,arr[1:])
# results = pool.map(draw,range(1,const.stop,int(const.stop/interval)))
for x in range(1,const.stop,int(const.stop/interval)):
        image_list.append(png_savedir+str(x)+"ref_k.png")
pool.close()
pool.join()

def create_gif(image_list, gif_name, duration = 0.5):
    '''
    '''
    frames = []
    # for image_name in image_list:
        # frames.append(imageio.imread(image_name))

    # imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
 
    pool = ThreadPool()
    frames = pool.map(imageio.imread,image_list)
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    pool.close()
    pool.join()
    return

def main():
    # image_list = ['1.jpg', '2.jpg', '3.jpg']
    gif_name = const.gifdir + "eDensity.gif"
    duration = 0.2
    create_gif(image_list, gif_name, duration)

# if __name__ == '__main__':
const.checkdir()
main()
