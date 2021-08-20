import numpy as np
import constant as const
import matplotlib.pyplot as plt
import pandas as pd
import sdf
plt.switch_backend('agg')
MeV = 1.6021766208e-13

def getData(n,setName='subset_selected1',particle='electron2'):
    ParticleName = setName + '/' + particle
    sdfdir=const.sdfdir +str(n).zfill(const.filenumber)+".sdf"
    data=sdf.read(sdfdir,dict=True)
    #Ek=data['Electric Field/Ey'].data
    Ek = data['Particles/Ek/' + ParticleName].data
    Ek = np.array(Ek)*1000/MeV

    SumEk = np.sum(Ek)
    
    return SumEk
    
def getTotalE(n,setName='subset_selected1',particle='electron2'):
    ParticleName = setName + '/' + particle
    sdfdir=const.sdfdir +str(n).zfill(const.filenumber)+".sdf"
    data=sdf.read(sdfdir,dict=True)
    #Ek=data['Electric Field/Ey'].data
    E = data['Total Particle Energy in Simulation (J)'].data
    E = np.array(E)*1000

    SumE = np.sum(E)

    return SumE

EkT = []

start = const.start
stop = const.stop

for i in range(0,stop,10):
    EkT.append(getData(i))

plt.plot(np.arange(0,stop,10)*const.dt_snapshot,EkT)
plt.savefig(const.figdir+'EkT.jpg')

plt.clf()
plt.close('all')


ET = []
for i in range(0,stop,10):
    ET.append(getTotalE(i))
plt.plot(np.arange(0,stop,10)*const.dt_snapshot,ET)
plt.savefig(const.figdir+'ET.jpg')




