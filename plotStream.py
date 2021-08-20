from scipy.interpolate import interpn
import sdf
import constant as const
import numpy as np
import matplotlib.pyplot as plt
import os
import Processing
import colorbar

plt.switch_backend('agg')


x = 1900
sdfdir=const.sdfdir +str(x).zfill(const.filenumber)+".sdf"
data = sdf.read(sdfdir,dict=True)

ArrX = data['Grid/Particles/subset_selected1/electron1'].data[0]
ArrY = data['Grid/Particles/subset_selected1/electron1'].data[1]

Px = data['Particles/Px/subset_selected1/electron1'].data
Py = data['Particles/Py/subset_selected1/electron1'].data

plt.streamplot(ArrX, ArrY, Px, Py)
plt.savefig('test/test.jpg',dpi=160)
