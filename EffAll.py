import pandas as pd
import constant as const
import matplotlib.pyplot as plt
import os
import Processing
import colorbar
import numpy as np
plt.switch_backend('agg')

Limit = 10

###
#MaxIndex = (const.las_t_fwhm1/const.dt_snapshot)*2
MaxIndex = Processing.MaxIndex #int(const.x_spot/2/c/const.dt_snapshot)
###
def name(var):
    return list(dict(var=var).keys())[0]
###
def getMaxEnerge(data):
    data = data.sort_values(by=['index'],na_position='first')
    #print(data)
    index = data.iloc[:,0]
    maxIndex = np.argmin(np.abs(index - MaxIndex))
    maxEnerge = data.iloc[maxIndex,2]
    #maxEnerge = float(maxEnerge)
    return maxEnerge

def getEff(Field = 'Bz'):
    filepath = const.txtdir + str(Field) + '_' +str(Limit) + 'THz' +'Ksqrt.csv'
    #filepath = const.txtdir +'Ksqrt.csv'
    data =pd.read_csv(filepath)
    #maxEnerge = data.iloc[0,2]
    data = data.sort_values(by=['index'],na_position='first')
    print(data)
    index = data.iloc[:,0]
    maxIndex = np.argmin(np.abs(index - MaxIndex))
    maxEnerge = data.iloc[maxIndex,2]
    #maxEnerge = float(maxEnerge)
    #arr = data/maxEnerge
    #eff = arr.iloc[:,1] 
    THzEnerge = np.array(data.iloc[:,1])
    #arr = data/maxEnerge
    #eff = arr.iloc[:,1]
    eff = THzEnerge / maxEnerge


    return index,eff



def getEffDirect(direction = 'Right',Field = 'Bz'):
    ####
    filepath = const.txtdir + str(Field) + '_' +str(Limit) + 'THz' +'Ksqrt.csv'
    #filepath = const.txtdir +'Ksqrt.csv'
    data =pd.read_csv(filepath)
    #data.sort()
    #maxEnerge = data.iloc[0,2]
    maxEnerge = getMaxEnerge(data)

    ####
    ####
    filepath = const.txtdir + str(Field) + direction + 'THz' +'Ksqrt.csv'
    data =pd.read_csv(filepath)
    data = data.sort_values(by=['index'],na_position='first')
    print(data)
    index = data.iloc[:,0]
    #maxIndex = (index - MaxIndex).argmin()
    #a = data/maxEnerge
    #maxEnerge = data.iloc[maxIndex,2]
    THzEnerge = np.array(data.iloc[:,1])
    #arr = data/maxEnerge
    #eff = arr.iloc[:,1]
    eff = THzEnerge / maxEnerge
    return index,eff


def plotlines(argList,savedir):
    plt.figure(figsize=(4,3))
    for index,eff in argList:
        plt.plot(index*const.dt_snapshot/1e-15,eff,label = name(index))
    plt.legend() 
   # plt.plot(locate,total_energe)
    plt.xlabel('time[fs]')
    plt.ylabel('efficiency')
    plt.savefig(savedir,dpi=200,bbox_inches ='tight')
    plt.close('all')

def main(Field):
    savedir = const.figdir + str(Field) + '_' +str(Limit) + 'THz' + 'EffAll.jpg'
    ####
    index,eff = getEff()
    indexLeft ,effLeft = getEffDirect(direction = 'Right',Field = 'Bz')
    indexRight ,effRight = getEffDirect(direction = 'Left',Field = 'Bz')

    argList = ([index,eff],[indexLeft,effLeft],[indexRight,effRight])

    plotlines(argList,savedir)
    
if __name__ == '__main__':
    Field = Processing.Field
    main(Field)
