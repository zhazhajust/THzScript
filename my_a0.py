import os
from scipy.signal import chirp, find_peaks, peak_widths
import scipy.signal as signal
import matplotlib.pyplot as plt
import numpy as np
import constant as const
import multiprocessing
plt.switch_backend('agg')

b = const.x_max/3e8/const.dt_snapshot/2
x = int(b)
Ey=np.load("baktxt/"+const.data_name+str(x)+"Ey_y0.npy")
data=Ey
x=np.abs(np.fft.rfft(Ey))
max_x=x.max()/10


def a0_x(x):
    if os.path.exists("baktxt/"+const.data_name+str(x)+"Ey_y0.npy")==False:
        #print("baktxt/"+const.data_name+str(x)+"Ey_y0.txt")
        return np.nan,np.nan,np.nan

    #p "draw",x
    Ey=np.load("baktxt/"+const.data_name+str(x)+"Ey_y0.npy")


    #Ey=np.loadtxt('3500Ey_y0.txt')
    data=Ey

    x=np.abs(np.fft.rfft(Ey))
    x.max()/3
    peaks, _ = find_peaks(x,prominence=max_x)
    if len(peaks) == 0:
        return np.nan,np.nan,np.nan
    T=const.x_end/3e8
    fs_1=1/T/1e12

    fff=peaks[0]*fs_1

    if fff > 10:
        return np.nan,np.nan,np.nan


    results_half = peak_widths(x, [peaks[0]], rel_height=0.5)
    width=results_half[0]*fs_1  # widths

    #print(peaks*fs_1)
    #print(results_half,peaks[0])

    T=const.x_end/3e8
    fs_1=1/T/1e12

    def multi_fs(array):
        new_array=array*1
        for i in range(len(array)):
                #print(i)
            if i !=1:
                #print(results_half[i])
                new_array[i][0] = array[i][0] * fs_1
        return new_array

    a_h=multi_fs(results_half)

    #plt.plot(np.arange(Nx/2+1)*fs_1,x)
    #plt.plot(peaks*fs_1, x[peaks], "x")
    #plt.hlines(*a_h[1:], color="C2")
    #plt.xlim([0,40])

    #Ey=np.loadtxt('3500Ey_y0.txt')
    data=Ey
    dx=const.x_end/const.Nx
    #print(dx)
    T=dx/3e8
    #print(T)
    fs=1/(2*T)
    w1=a_h[2]*1e12
    w2=a_h[3]*1e12

    Ey_y0=Ey
    k_bz=np.fft.fft(Ey_y0)
    delta_k=3.14/const.delta_x/(const.Nx/2)
    k_bz2=k_bz*1
    k_n=[]
    for n in range(0,const.Nx):
        mi = 3e8/w1
        ma = 3e8/w2
        if 2 * 3.14 / ma  > n * delta_k and  n * delta_k > 2 * 3.14 / mi:
            k_n.append(n)
    k_bz2[0:k_n[0]]=0    #k_bz.argmin()
    k_bz2[k_n[-1]:-k_n[-1]]=0  #k_bz.argmin()
    k_bz2[-k_n[0]:]=0    #k_bz.argmin()
    bz_filter=np.fft.ifft(k_bz2)

    E0_w0=np.abs(bz_filter.real).max()
    #print('E0:'+str(E0_w0))
    c=3e8
    #w0=4e12
    me=9.10956e-31
    e=1.602176565e-19
    freqs=peaks*fs_1*1e12
    w0=freqs*2*3.1415926
    a0_w0=e*E0_w0/(me*c*w0)
    #return a0_w0
    '''
    #print(w1,w2)
    b, a = signal.butter(8,w2, 'lowpass')  
    filtedData = signal.filtfilt(b, a, data)       #

    b, a = signal.butter(8,w1, 'highpass')  
    filtedData2 = signal.filtfilt(b, a, filtedData)       #

    #print(np.abs(filtedData2).max())
    c=3e8
    #w0=4e12
    me=9.10956e-31
    e=1.602176565e-19
    freqs=peaks*fs_1*1e12
    E0_w0=np.abs(filtedData2).max()[0]
    w0=freqs*2*3.1415926
    a0_w0=e*E0_w0/(me*c*w0)
    #print(a0_w0)
    '''
    #plt.plot(filtedData2)
    #plt.show()
    #print('a,f',a0_w0,fff)
    #print(width)
    return [a0_w0[0],fff,width[0]]
#a,f=a0_x(1)
#a0=[]
#freqs=[]

def m_a0(i):
	#print(i)
	a,f,w=a0_x(i)
	#a0.append(a)
	#freqs.append(f)	
	return [a,f,w]
#a0_x(1)
pool = multiprocessing.Pool(processes=96)
results = pool.map(m_a0,range(1,const.stop+1))
'''
a0=np.array(results[:][0])

max_a0=np.nanmax(a0)

i_a0=a0.index(max_a0)
width=results[:][2]
width_a0=width[i_a0]
'''


results=np.array(results)
print(results,results.shape)
pool.close()
pool.join()

a0=results[:,0]
freqs=results[:,1]
width=results[:,2]
#a0=np.array(a0)
#freqs=np.array(freqs)
np.save(const.txtdir+'a0_fwhm.npy',a0)
np.save(const.txtdir+'freqs_min.npy',freqs)
np.save(const.txtdir+'width_max.npy',width)


time = np.arange(int(1),int(const.stop+1))
locate = (time*const.dt_snapshot - const.window_start_time)*3e8*1e6

np.save(const.txtdir + 'a0_distance.npy',locate)


plt.plot(locate,a0,label='a0')
plt.plot(locate,width,label='width')
plt.legend()
plt.savefig(const.figdir+'a0_width.jpg',dpi=160)
plt.close('all')

plt.plot(locate,freqs,label='freqs')
plt.plot(locate,width,label='width')
plt.plot(locate,a0,label='a0')
#plt.ylim([0,10])
plt.legend()
plt.savefig(const.figdir+'a0_freqs.jpg',dpi=160)

max_a0=np.nanmax(a0)

max_width=np.nanmax(width)

with open("txt/scan_new.txt","a") as f:
        f.write(const.case_name+":"+"\n"+'max_a0:'+str(max_a0)+" "+'min_freqs:'+ str(np.nanmin(freqs))+"\n"+"width:"+str(max_width)+"\n")#+"\n"+'const.dt_snapshot,const.window_start_time:'+"\n"+str(const.dt_snapshot)+','+str(const.window_start_time)+"\n")
#print(a0,freqs)
#print(np.nanmax(a0),np.nanmin(freqs))
