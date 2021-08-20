import sdf
import Processing
import matplotlib.pyplot as plt
import constant as const
import numpy as np
from numba import njit
import multiprocessing
plt.switch_backend('agg')


X = [10,50,100,300]
Y = [0.007528926829856885,0.011155827595351395,0.006525566468580776,0.003281146936419214]
Y=np.array(Y)
plt.figure(figsize=[4,3])
plt.plot(X,Y*100,'cs-.')#,linewidth=1)
plt.xlabel('YLength[$\mu m$]')
plt.ylabel('Efficiency[%]')
plt.savefig('line/eff.jpg',dpi=160,bbox_inches='tight')
