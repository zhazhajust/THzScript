from scipy.interpolate import interpn
import sdf
import constant as const
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')

pi = 3.1415926
delta_x=const.delta_x
delta_y=const.delta_y

x = 100

Limit = 500
savedir = const.figdir + 't' + str(x) + 'Ktheta.jpg'


####read sdf####
sdfdir=const.sdfdir +str(x).zfill(const.filenumber)+".sdf"
data=sdf.read(sdfdir,dict=True)
Bz=data['Magnetic Field/Bz']
bz=Bz.data
#k_bz=np.fft.fft2(bz)

####fourier transform#####
k_bz2d=np.fft.fft2(bz)
#fig,axs=plt.subplots(figsize=[4,3])
#k0=2*pi/10.6e-6
k0=2*pi*1e12/3e8
kx=np.linspace(0,pi/delta_x/k0,int(const.Nx/2))
ky=np.linspace(0,pi/delta_y/k0,int(const.Ny/2))
Ky,Kx=np.meshgrid(ky,kx)
Kxy=np.abs(k_bz2d[:int(const.Nx/2),:int(const.Ny/2)])#**2

#######unravel########
_1DKxy=Kxy.flatten()
_1DKx=Kx.flatten()
_1DKy=Ky.flatten()
maxK = Kxy.max()
KKxy=_1DKxy[_1DKxy>maxK/100]
KKy=_1DKy[_1DKxy>maxK/100]
KKx=_1DKx[_1DKxy>maxK/100]
#KKx[KKx==0] = 1/np.inf
KKxy=KKxy[KKx>0]
KKy=KKy[KKx>0]
KKx=KKx[KKx>0]

######theta , k generator####
theta = np.arctan(KKy/KKx)
K = np.sqrt(KKx**2+KKy**2)

#im4=axs.pcolormesh(Kx,Ky,Kyx,cmap=plt.get_cmap('jet'))

#k_bz = np.abs(np.fft.rfft2(bz))

#theta = np.linspace(0,pi,500)
#lamada=const.lamada
#k0 = 2*pi/lamada * 1.2
#k0 = pi/delta_x
#fthz = 1e12
#c=3e8


#maxK = Kxy.max()

'''
#k0 = 10e12 *2*pi /c#2*pi/30.8e-6

k = np.linspace(0,k0,50)
theta = np.linspace(0,pi*1/2,50)
K , Theta = np.meshgrid(k,theta)

Value = K * 0.
for i in range(len(theta)):
    for j in range(len(k)):
        xis=(k[j]*np.cos(theta[i]),j*np.sin(theta[i]))
        print(xis)
        Value[i,j] = interpn(points=(kx, ky), values=Kxy, xi=xis)


#Value = interpn(points=(kx, ky), values=Kxy, xi=(K*np.cos(Theta),K*np.sin(Theta)))
'''

####plot####
plt.subplot(projection = "polar")
#plt.pcolormesh(Theta,K*c/2/pi/fthz,Value.T,cmap=plt.cm.jet)
plt.scatter(theta[K<Limit],K[K<Limit],s=1,marker = 'o',c=KKxy[K<Limit],cmap=plt.cm.jet)
#plt.scatter(theta,K,s=0.1,marker = '.',c=KKxy,cmap=plt.cm.jet)

plt.colorbar()
plt.xlabel('THz')
plt.ylabel('Theta')
plt.savefig(savedir,dpi=160,bbox_inches = 'tight')
