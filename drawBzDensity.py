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
# import wigner
plt.switch_backend('agg')
###
####
pi = math.pi
interval = 100
image_list = []
pngdir = const.gifdir + 'BzDensitypng/'
os.makedirs(pngdir, exist_ok=True)
png_savedir = pngdir  # './gif/png/'#const.gifdir


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

# def draw(x):
	# savefigdir=const.figdir+str(int(locate/1e-6))+'_'+str(Thz1)+'_'+str(Thz2)+'k_bz.png'


def getData(x):
    sdfdir = const.sdfdir + str(x).zfill(const.filenumber) + ".sdf"
    data = sdf.read(sdfdir, dict=True)
    return data
# getData = lambda x : data=sdf.read(const.sdfdir
# +str(x).zfill(const.filenumber)+".sdf",dict=True)


# def getBz(data):
#	Bz=data['Magnetic Field/Bz'].data
#    return Bz

getBz = lambda data: data['Magnetic Field/Bz'].data


def getTime(data):
    time = data['Header']['time']
    ###
    T = 0
    # global T
    time = data['Header']['time']
    if time - const.window_start_time < 0:
        T = 0
    else:
        T = time - const.window_start_time
    ###
    return T


def fftBz(bz):
	k_bz = np.fft.fft2(bz)
    return k_bz
# fftBz = lambda bz : k_bz=np.fft.fft2(bz)
def Kfilter(k_bz2,R1,R2):
	# k_bz2d=np.fft.fft2(bz)
	delta_k=3.14/const.delta_x/(const.Nx/2)
	# k_bz2=k_bz*1
	# print("n",k_n[0],k_n[-1])
	# R1=k_n[0]
	# R2=k_n[-1]
	x1=const.Nx-1
	y1=const.Ny-1
	for i in range(0,const.Nx):
		for j in range(0,const.Ny):
			if math.sqrt(i**2+j**2) > R2 and math.sqrt((i-x1)**2+j**2) > R2 and math.sqrt(i**2+(j-y1)**2) > R2 and math.sqrt((i-x1)**2+(j-y1)**2) > R2:
				k_bz2[i,j]=0
			if math.sqrt(i**2+j**2) < R1 and math.sqrt(i**2+(j-y1)**2) < R1 and math.sqrt((i-x1)**2+j**2) < R1 and math.sqrt((i-x1)**2+(j-y1)**2) < R1:
                                k_bz2[i,j]=0
    return k_bz2

def rfftBz(k_bz2):
	bz_filter=np.fft.ifft2(k_bz2)
    return bz_filter

# rfftBz = lambda k_bz2 : bz_filter=np.fft.ifft2(k_bz2)

# def TotalEnerge(bz):
#	E_x=np.sum(np.sum(np.square(bz)))
#    return E_x


def TotalEnerge(bz_filter):
	E_Thz=np.sum(np.sum(np.square(bz_filter.real)))
    return E_Thz

# TotalEnerge = lambda Bz : E_x=np.sum(np.sum(np.square(Bz)))
	# eff=E_Thz/E_x
	# print("efficiency",E_x,E_Thz,eff)
# def getNe(data):
#	ne=data['Derived/Number_Density/electron1'].data
	# ne_y0=ne[...,int(const.Ny/2)]
def getNe(data):
    ne=data['Derived/Number_Density/electron1'].data
    return ne
# getNe = lambda data : ne=data['Derived/Number_Density/electron1'].data

def draw():
	ne=ne.T	
	fig,axs=plt.subplots(2,2)
	im=axs[0][0].pcolormesh(bz.T,cmap=plt.get_cmap('bwr'))   
	im2=axs[1][0].pcolormesh(ne)#,norm=mpl.colors.LogNorm(),cmap=plt.cm.jet)
	cbNe=fig.colorbar(im2,ax=axs[1][0])
	im3=axs[0][1].pcolormesh(bz_filter.real.T,cmap=plt.get_cmap('bwr'))
	fig.colorbar(im,ax=axs[0][0])
	cb=fig.colorbar(im3,ax=axs[0][1])
	cb.set_label('E(V/m)')
	emax=np.abs(bz_filter.real).max()
	im3.set_clim([-emax,emax])
	###
	k0=2*pi*1e12/3e8#2*pi/10.6e-6
	kx=np.linspace(0,pi/const.delta_x/k0,int(const.Nx/2))
	ky=np.linspace(0,pi/const.delta_y/k0,int(const.Ny/2))
	Kx,Ky=np.meshgrid(kx,ky)
	Kyx=abs(k_bz2d[:int(const.Nx/2),:int(const.Ny/2)].T)
	im4=axs[1][1].pcolormesh(Kx,Ky,Kyx,cmap=plt.get_cmap('jet'))
	# cb4 = fig.colorbar(im3,ax=axs[0][1])
	# im4=axs[1][1].pcolormesh(abs(k_bz2d[:int(const.Nx/2),:int(const.Ny/2)].T),cmap=plt.get_cmap('bwr'))
	# fig.savefig(savefigdir,dpi=200)
	axs[1][1].set_ylim((0,30))
	axs[1][1].set_xlim((0,30))
	t_fs=int(time/1e-15)
	axs[0][0].set_title("t="+str(t_fs),fontsize=12,color='r')
	# axs[0][0].set_title(str(x*const.dt_snapshot))
	axs[0][0].xaxis.set_major_formatter( FuncFormatter( x_formatter ) )

	fig.savefig(png_savedir+str(x)+"ref_k.png",dpi=200)
	image_list.append(png_savedir+str(x)+"ref_k.png")
	plt.clf()
	plt.close('all')


# wigner.aaa() 
'''        
for i in range(0,const.stop,interval):
        draw(i)
'''
image_list=[]
k_n=k_n()
# pool = multiprocessing.Pool(processes=96)   #,initargs=(ss1,ss2))
               # for i in range(start,stop+step,step):
        #       results.append(pool.apply_async(extract, (i, ))) 
# results = pool.map(draw,range(1,const.stop,int(const.stop/interval)))
# for x in range(1,const.stop,int(const.stop/interval)):
#        image_list.append(png_savedir+str(x)+"ref_k.png")
# pool.close()
# pool.join()



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
    gif_name = const.gifdir + "EyDensity.gif"
    duration = 0.2
    create_gif(image_list, gif_name, duration)

if __name__ == '__main__':
    k_n = k_n()
    data = getData(x)
    T=getTime(x)
    Bz = getBz(data)  
    KBz = getKBz(Bz)  
    R1=k_n[0]
    R2=k_n[-1]
    ne = getNe(data)    
    k_bz2 = Processing.Kfilter(k_bz2,R1,R1)
    draw(2900)
