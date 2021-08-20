from scipy.interpolate import interpn
import sdf
import constant as const
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
plt.switch_backend('agg')


pi = 3.1415926
delta_x=const.delta_x
delta_y=const.delta_y

x = 1000


savedir = const.figdir + 't' + str(x) + 'Ktheta.jpg'
sdfdir=const.sdfdir +str(x).zfill(const.filenumber)+".sdf"
data=sdf.read(sdfdir,dict=True)
Bz=data['Magnetic Field/Bz']
bz=Bz.data
#k_bz=np.fft.fft2(bz)
k_bz2d=np.fft.fft2(bz)
#fig,axs=plt.subplots(figsize=[4,3])
#k0=2*pi/10.6e-6
kx=np.linspace(0,pi/delta_x,int(const.Nx/2))
ky=np.linspace(0,pi/delta_y,int(const.Ny/2))
Kx,Ky=np.meshgrid(kx,ky)
Kxy=np.abs(k_bz2d[:int(const.Nx/2),:int(const.Ny/2)])**2
Kxy = Kxy.T
#im4=axs.pcolormesh(Kx,Ky,Kyx,cmap=plt.get_cmap('jet'))

#k_bz = np.abs(np.fft.rfft2(bz))

#theta = np.linspace(0,pi,500)
lamada=const.lamada
k0 = 2*pi/lamada * 1.2
#k0 = pi/delta_x
fthz = 1e12
c=3e8

#k0 = 10e12 *2*pi /c#2*pi/30.8e-6

k = np.linspace(0,k0,50)
theta = np.linspace(0,pi*1/2,50)
K , Theta = np.meshgrid(k,theta)

Value = K * 0.

for i in range(len(theta)):
    for j in range(len(k)):
        xis=(k[j]*np.cos(theta[i]),k[j]*np.sin(theta[i]))
        print(xis)
        Value[i,j] = interpn(points=(kx, ky), values=Kxy, xi=xis)

#f = interpolate.interp2d(kx, ky, Kxy, kind='cubic')
#Value = f(k*np.cos(theta),k*np.sin(theta))

#Value = interpn(points=(kx, ky), values=Kxy, xi=(K*np.cos(Theta),K*np.sin(Theta)))

#plt.subplot(projection = "polar")
plt.pcolormesh(Theta*180/pi,K*c/2/pi/fthz,Value,cmap=plt.cm.jet)
plt.colorbar()
plt.xlabel('THz')
plt.ylabel('Theta')
plt.savefig(savedir,dpi=160,bbox_inches = 'tight')
