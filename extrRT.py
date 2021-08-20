import math
import matplotlib.pyplot as plt
import numpy as np
import constant as const
plt.switch_backend('agg')

y_interval = 1
x_interval = 10
delta_x = const.delta_x #600e-6/1908
delta_y = const.delta_y #200e-6/188

#for i in range(10000):
#    if i * delta_x < 1e-6:
#        x_interval = i
#    if i * delta_y < 1e-6:
#        y_interval = i

Ny = const.Ny
x_end = const.x_end  #600e-6
c = 3e8
dt_snapshot = const.dt_snapshot  #10e-15
fs = 1e-15
#Xf=np.load(const.txtdir+'XtMatr.npy')
Xf = np.load(const.txtdir + str(x_interval)+'_'+str(y_interval) +'XfMatr.npy')
#print(Xf.shape[1:].T)
#Xt=np.zeros((Xf.shape[2],Xf.shape[1]))
R = 200e-6
thetaSequence=[]
timeSequence = []
print(Xf.shape[2])


tTotal = x_end/c
tSize = tTotal / dt_snapshot + 3
time = dt_snapshot * np.arange(tSize)

Xt=[]
###Xt generaor###

for j in range(Xf.shape[2]):
    try:
        y = j * delta_y * y_interval - Ny*delta_y/2
        print('R,y',R,y)
        x = math.sqrt(R**2 - y**2)
        i = int(x/delta_x/x_interval)
        print('i',i)
        theta = np.arctan(y/x)
        thetaSequence.append(theta)
        #Xt[j,:]=Xf[i,:,j]
        Xt.append(Xf[i,:,j])
    except:
        pass
 #   Xt[j,:]=np.nan

Xt=np.array(Xt)
print(Xt.shape)

################
theta=np.asarray(thetaSequence)
Time ,Theta= np.meshgrid(time,theta)
print(np.asarray(thetaSequence)*180/(2*3.14))
plt.figure(figsize=[4,3])
#plt.pcolormesh(Time/fs,Theta*180/(2*3.1415926),Xt,cmap=plt.cm.bwr)
plt.pcolormesh(Xt.real,cmap=plt.cm.bwr)

plt.ylabel('Degree')
plt.xlabel('fs')
XF = np.fft.rfft(Xt)#,axis=1)

#plt.pcolormesh(XF.real,cmap=plt.cm.rainbow)

plt.colorbar()
plt.savefig(const.figdir + str(R)+'testRt.jpg',dpi=160,bbox_inches = 'tight')
plt.close()

#time = Xt.shape[1]
Nt = Xt.shape[1]
fs = 1/dt_snapshot
freqs = np.linspace(0,fs/2,int(Nt/2+1))
#plt.plot(freqs/1e12)
#freqs.shape
Freqs,Theta = np.meshgrid(freqs,theta)
XF.shape
plt.figure(figsize=[4,3])
#plt.pcolormesh(Freqs/1e12,Theta*180/(2*3.1415926),np.abs(XF)**2,cmap=plt.cm.jet)
plt.pcolormesh(np.abs(XF)**2,cmap=plt.cm.jet)

plt.colorbar()
plt.xlabel('THz')
plt.ylabel('Degree')
plt.savefig(const.figdir + str(R)+'testFreqs.jpg',dpi=160,bbox_inches = 'tight')
plt.close()


