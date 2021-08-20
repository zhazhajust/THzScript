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
#from bz_field_filter import Bz_field_filter
from lib.ey.field_filter import Ey_field_filter
plt.switch_backend('agg')
x_interval=const.x_interval
start=const.start
stop=const.stop
limit_min=0.1e12
limit_max=10e12
i1=const.start
i2=const.stop+const.step
savefigdir=const.figdir+'ey_Thz_'+'efficiency.png'
savefigdir2=const.figdir+'ey_field_energe.png'
interval = 100


print(const.window_start_time)


if os.path.exists(const.txtdir + 'eff_ey.npy') == True:
        sys.exit()


#k_n=k_n()

#const.txtdir + 'bz_energe.npy'


def task(x):
	list=Ey_field_filter(x,const.Nx,const.Ny,const.delta_x,const.figdir,const.sdfdir,const.filenumber)
	return list
pool = multiprocessing.Pool(processes=96)
mapList=np.arange(start,stop+int(stop/interval),int(stop/interval))
final_energe = pool.map(draw,mapList)

#final_energe = pool.map(task,range(int(i1-1),int(i2+interval),interval))
###
####total_energe_max

total_energe=(np.array(final_energe))[:,2]

#os.path.exists(const.txtdir + 'bz_energe.txt')
#const.txtdir + 'eff_locate_bz.txt'
#b=(np.nanargmax(total_energe))*interval

######fwhm*2####
b=(float(const.las_t_fwhm1)/float(const.dt_snapshot))*2
#########

#####1/2 of window####
#b = const.x_max/3e8/const.dt_snapshot/2
######
b = int(b)


print('b',b)
start=task(b)#Bz_field_filter(b)
#print(start)

Energe=np.array(final_energe)
Energe=Energe[:,1]
S_E=start[0]



print('sdf1,sdf2',i1,i2)
print('Thz',limit_min,limit_max)
#efficiency=np.array(np.array(final_energe)/start[0])[:,1]

efficiency=Energe/S_E

max_index = i1+efficiency.argmax() 
max_distance = 3e8 * (max_index * const.dt_snapshot - const.window_start_time) * 1e6
print('max_index',str(max_index))
print('distance:',str(max_distance))
print('eff:',str(np.nanmax(efficiency)))
np.save(const.txtdir + 'eff_ey.npy',efficiency)

#time = np.arange(int(i1-1),int(i2+interval),interval)
#locate = (time*const.dt_snapshot - const.window_start_time)*3e8*1e6

time=mapList
locate = (time*const.dt_snapshot)*3e8*1e6


np.save(const.txtdir + 'eff_locate_ey.npy',locate)

plt.figure(figsize=(4,3))
plt.plot(locate,efficiency)
#plt.plot(locate,total_energe)
plt.xlabel('$\mu m$')
plt.ylabel('efficiency')
plt.savefig(savefigdir,dpi=200,bbox_inches ='tight')

plt.close('all')


plt.figure(figsize=(4,3))
#plt.plot(locate,efficiency)
plt.plot(locate,total_energe)
plt.xlabel('$\mu m$')
plt.ylabel('total_ey')
plt.savefig(savefigdir2,dpi=200,bbox_inches ='tight')




#plt.plot(locate,efficiency)
#plt.savefig(savefigdir,dpi=200)

