import pandas as pd
import constant as const
import matplotlib.pyplot as plt
import os
import Processing
import colorbar
import numpy as np
plt.switch_backend('agg')

#####
Limit = 10

c = 299792458
pi = 3.1415926


#MaxIndex = (const.las_t_fwhm1/const.dt_snapshot)*2
#MaxIndex = int(const.x_spot/2/c/const.dt_snapshot)
MaxIndex = Processing.MaxIndex
print('MaxIndex',MaxIndex)
#####
'''
def getEff(Field = 'Bz'):
    filepath = const.txtdir + str(Field) + '_' +str(Limit) + 'THz' +'Ksqrt.csv'
    #filepath = const.txtdir +'Ksqrt.csv'
    data =pd.read_csv(filepath)
    #data.sort()
    maxEnerge = data.iloc[0,2]
    data = data.sort_values(by=['index'],na_position='first')
    print(data)
    index = data.iloc[:,0]
    a = data/maxEnerge
    eff = a.iloc[:,1] 
    return index,eff
'''

def getEff(Field = 'Bz'):
    filepath = const.txtdir + str(Field) + '_' +str(Limit) + 'THz' +'Ksqrt.csv'
    #filepath = const.txtdir +'Ksqrt.csv'
    data =pd.read_csv(filepath)
    #maxEnerge = data.iloc[0,2]
    print(data)
    data = data.sort_values(by=['index'],na_position='first')
    print(data)
    index = data.iloc[:,0]
    #index = np.array(index)
    maxIndex = np.argmin(np.abs(index - MaxIndex))#.argmin()
    print('maxIndex',maxIndex)
    maxEnerge = data.iloc[maxIndex,2]

    arr = data/maxEnerge
    eff = arr.iloc[:,1]
    return index,eff

def plotlines(index,eff,savedir):
    plt.figure(figsize=(4,3))
    plt.plot(index*const.dt_snapshot/1e-15,eff)
    # plt.plot(locate,total_energe)
    plt.xlabel('time[fs]')
    plt.ylabel('efficiency')
    plt.savefig(savedir,dpi=200,bbox_inches ='tight')

    plt.close('all')
def main(Field):
    savedir = const.figdir + str(Field) + '_' +str(Limit) + 'THz' + 'eff.jpg'
    ####
    index,eff = getEff()
    plotlines(index,eff,savedir)
    
if __name__ == '__main__':
    Field = Processing.Field
    main(Field)
