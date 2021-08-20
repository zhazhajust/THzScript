import numpy as np
import constant as const
import scipy.signal
from scipy.signal import chirp, find_peaks, peak_widths
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt

load_dir = const.txtdir+"xt.npy"
xt = np.load(load_dir)
xt = xt.real
xtProfile = [] #* (0+0*1j)
#xt = xt.astype('complex128')
FWHM=[]

print(xt.shape)
x = np.arange(xt.shape[1])
for i in range(0,xt.shape[0],1000):
    #print(xt[i].shape)
    index=np.argmax(xt[i])
    Xmax=xt[i,index]
    #print(scipy.signal.hilbert(xt[i]))
    xtProfile.append(scipy.signal.hilbert(xt[i]))
    #f = UnivariateSpline(x , xtProfile[-1],s = 100)
    #xtProfile[-1] = f(x)
    peaks, _ = find_peaks(xtProfile[-1])
    results_half = peak_widths(xtProfile[-1], peaks, rel_height=0.5)
    #print(results_half[0])
    try:
        FWHM.append(results_half[0].max())
    except:
        FWHM.append(np.nan)
    #print(np.where(xt[i]>Xmax/2,0,1))
    #FWHM[i] = np.where(xt[i],Xmax/2)

print(FWHM)
