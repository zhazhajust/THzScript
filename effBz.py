import numpy as np
import matplotlib.pyplot as plt
import sdf
import os
import sys
import scipy.signal as signal
import constant as const
import scipy.fftpack as fftpack
import multiprocessing
from matplotlib.ticker import MultipleLocator, FuncFormatter
from numba import njit
plt.switch_backend('agg')


start = const.start
stop = const.stop
x_interval = const.x_interval
limit_min = 0.1e12
limit_max = 10e12
i1 = const.start
i2 = const.stop + const.step
savefigdir = const.figdir + 'BzThz' + 'Efficiency2d.png'
savefigdir2 = const.figdir + 'field_energe.png'
interval = 100


@njit
def Kfilter(k_bz2, R1, R2):
    x1 = const.Nx #- 1
    y1 = const.Ny #- 1
    delta_kx = 3.14 / const.delta_x / (const.Nx / 2)
    delta_ky = 3.14 / const.delta_y / (const.Ny / 2)
    for i in range(0, const.Nx):
        for j in range(0, const.Ny):
            if i**2 + (j * delta_ky / delta_kx)**2 > R2**2 and (i - x1)**2 + (j * delta_ky / delta_kx)**2 > R2**2 and i**2 + \
                       ((j - y1) * delta_ky / delta_kx)**2 > R2**2 and (i - x1)**2 + ((j - y1) * delta_ky / delta_kx)**2 > R2**2:
                k_bz2[i, j] = 0
            if i**2 + (j * delta_ky / delta_kx)**2 < R1**2 or i**2 + ((j - y1) * delta_ky / delta_kx)**2 < R1**2 or (
                i - x1)**2 + (j * delta_ky / delta_kx)**2 < R1**2 or (i - x1)**2 + ((j - y1) * delta_ky / delta_kx)**2 < R1**2:
                k_bz2[i, j] = 0
    return k_bz2

def ThetaFilter(KBz,theta):
    for i in range(0,const.Nx/2):
        for j in range(0,const.Ny/2):
            if np.acrtan(i/(j * delta_ky / delta_kx)) > theta * pi/180:
                KBz[i, j] = 0
    KBz[const.Nx/2:,0:const.Ny/2]=KBz[const.Nx/2:0:-1,:0:const.Ny/2] 
    KBz[0:const.Nx/2,const.Ny/2:]=KBz[0:const.Nx/2,const.Ny/2:0:-1]
    KBz[const.Nx/2:,const.Ny/2:]=KBz[const.Nx/2:0:-1,:const.Ny/2:-1]
    return KBz
def plotE(E,x,savedir):
    #const.figdir + str(x) + str(E) + 'Field.jpg'
    plt.figure(figsize=[4,3])
    x = np.linspace(0,const.x_end/1e-6,const.Nx)
    y = np.linspace(0,const.y_lenth/1e-6,const.Ny)
    X,Y = np.meshgrid(x,y)
    #plt.pcolormesh(X[::int(E.shape[1]/500),::int(E.shape[0]/500)],Y[::int(E.shape[1]/500),::int(E.shape[0]/500)],E[::int(E.shape[0]/500),::int(E.shape[1]/500)].T)
    plt.pcolormesh(X,Y,E.T,cmap=plt.cm.bwr)
    plt.colorbar()
    plt.xlabel('um')
    plt.ylabel('um')
    #title = str(str(float(x)*const.dt_snapshot/1e-15) + 'fs')
    #plt.title(title)
    plt.savefig(savedir,dpi=160,bbox_inches = 'tight')
    plt.close('all')

def k_n():
	k_n = []
	delta_k = 3.14 / const.delta_x / (const.Nx / 2)
	for n in range(0, const.Nx):
		mi = 3e8 / limit_min
		ma = 3e8 / limit_max
		if 2 * 3.14 / ma > n * delta_k and n * delta_k > 2 * 3.14 / mi:
			k_n.append(n)
	return k_n


def draw(x):
    savefigdir = const.figdir + str(x) + 'k_bz.png'
    sdfdir = const.sdfdir + str(x).zfill(const.filenumber) + ".sdf"

    if os.path.exists(sdfdir) == False:
        return[np.nan, np.nan, np.nan]

    data = sdf.read(sdfdir, dict=True)

    try:
        Bz = data['Magnetic Field/Bz']
    except:
        print('not Bz exists')
        return [np.nan, np.nan, np.nan]

    time = data['Header']['time']

    try:
        total = data['Total Field Energy in Simulation (J)'].data
    except:
        total = 0

    bz = Bz.data
    k_bz = np.fft.fft2(bz)
    delta_k = 3.14 / const.delta_x / (const.Nx / 2)
    k_bz2 = k_bz * 1
    #######
    R1 = k_n[0]
    R2=k_n[-1]
    k_bz2 = Kfilter(k_bz2,R1,R2)
    bz_filter=np.fft.ifft2(k_bz2)
    E_x=np.sum(np.sum(np.square(bz)))
    E_Thz=np.sum(np.sum(np.square(bz_filter.real)))
    eff=E_Thz/E_x
    ############
    ####plot####
    ############

    pngdir = const.gifdir + 'Fieldfileter/'
    os.makedirs(pngdir,exist_ok = True)
    ###savedir###
    savedir = pngdir + 'F' + str(x) + 'BzFieldfilter.jpg'
    plotE(bz_filter.real,x,savedir)
    print("efficiency",E_x,E_Thz,total)
    return [E_x,E_Thz,total]
print(const.window_start_time)


#if os.path.exists(const.txtdir + 'EffEy.npy') == True:
#        sys.exit()


k_n=k_n()

const.txtdir + 'bz_energe.txt'

pool = multiprocessing.Pool(processes=96)
# final_energe = pool.map(draw,range(int(i1-1),int(i2+interval),interval))

mapList=np.arange(start,stop+int(stop/interval),int(stop/interval))
# final_energe = pool.map(draw,mapList)
final_energe = pool.map(draw,mapList)

#
###
# total_energe_max

total_energe=(np.array(final_energe))[:,2]

# os.path.exists(const.txtdir + 'bz_energe.txt')
# const.txtdir + 'eff_locate_bz.txt'
# b=(np.nanargmax(total_energe))*interval

######fwhm*2####
b=(const.las_t_fwhm1/const.dt_snapshot)*2
#########

#####1/2 of window####
# b = const.x_max/3e8/const.dt_snapshot/2
######
b = int(b)


print('b',b)
start=draw(b)
# print(start)

Energe=np.array(final_energe)
Energe=Energe[:,1]
S_E=start[0]



print('sdf1,sdf2',i1,i2)
print('Thz',limit_min,limit_max)
# efficiency=np.array(np.array(final_energe)/start[0])[:,1]

efficiency=Energe/S_E

max_index = i1+efficiency.argmax() 
max_distance = 3e8 * (max_index * const.dt_snapshot - const.window_start_time) * 1e6
print('max_index',str(max_index))
print('distance:',str(max_distance))
print('eff:',str(np.nanmax(efficiency)))
np.save(const.txtdir + 'EffBz.npy',efficiency)

time=mapList
# time = np.arange(int(i1-1),int(i2+interval),interval)
locate = (time*const.dt_snapshot - const.window_start_time)*3e8*1e6


np.save(const.txtdir + 'EffLocateBz.npy',locate)

plt.figure(figsize=(4,3))
plt.plot(locate,efficiency)
# plt.plot(locate,total_energe)
plt.xlabel('$\mu m$')
plt.ylabel('efficiency')
plt.savefig(savefigdir,dpi=200,bbox_inches ='tight')

plt.close('all')


plt.figure(figsize=(4,3))
# plt.plot(locate,efficiency)
plt.plot(locate,total_energe)
plt.xlabel('$\mu m$')
plt.ylabel('total_ey')
plt.savefig(savefigdir2,dpi=200,bbox_inches ='tight')




# plt.plot(locate,efficiency)
# plt.savefig(savefigdir,dpi=200)

