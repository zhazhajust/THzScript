import os
import sdf
import Processing
import matplotlib.pyplot as plt
import constant as const
import numpy as np
from numba import njit
import multiprocessing
import pandas as pd
plt.switch_backend('agg')

start = 0 #const.start
#stop = int(const.stop/10)*10
step = 10#const.step
FinalNumber = 4600


stop = FinalNumber

def saveCSV(dataframe,filepath,create='False'):
    df = dataframe
    if create == 'True':
        df.to_csv(filepath,mode = 'w')#,header = False)
        return
    if os.path.exists(filepath)==True:
        df.to_csv(filepath,mode = 'a',header = False)#, index = False)
    else:
        df.to_csv(filepath,mode = 'a')#,index = False)
    #if exist:
    #    dfEy = pd.DataFrame(mode = 'a',index=n,head=False)#,columns=colums)
    return

def getField(n):
    sdfdir=const.sdfdir +str(n).zfill(const.filenumber)+".sdf"
    data = sdf.read(sdfdir,dict=True)
    Ex = data['Electric Field/Ex'].data
    Ey = data['Electric Field/Ey'].data
    return Ex,Ey

#arr = range(50,stop+10,50)
#TimeX = np.zeros([tsize,len(idNumber)])
#arr = [1000]

##########
##########
arrx = np.linspace(const.x_min + const.delta_x,const.x_max + const.delta_x,const.Nx)
arry = np.linspace(const.y_min + const.delta_y,const.y_max + const.delta_y,const.Ny)

XX,YY = np.meshgrid(arrx,arry)
##########
##########


#print('X,Y.shape',X.shape,Y.shape)

#XX = XX[::10,::10]
#XY = YY[::10,::10]

'''
TimeX = []
TimeX = []
TimeY = []
TimeEx = []
TimeEy = []
TimePx = []
TimePy = []
TimeEk = []
idNumber = []
'''

def createDataframe(IDFinal):
    colums = IDFinal
    Time = np.arange(start,stop,step)
    dfEy = pd.DataFrame(index=Time,columns=colums) 
    return dfEy

def getFinalParticleID(n):
    Pdict = Processing.getTracer(n)
    #ID , X , TracerEx, Px , Y , TracerEy , Py , Ek = Processing.getTracer(n)
    #ID , X , TracerEx, Px , Y , TracerEy , Py , Ek , Vx,Vy = 0
    #ID , X , TracerEx, Px , Y , TracerEy , Py , Ek , Vx,Vy = fromDict([ID , X , TracerEx, Px , Y , TracerEy , Py , Ek , Vx , Vy],Pdict)
    ID , X , TracerEx, Px , Y , TracerEy , Py , Ek , Vx,Vy = fromDict(['ID' , 'X' , 'TracerEx', 'Px' , 'Y', 'TracerEy' , 'Py' , 'Ek' , 'Vx' , 'Vy'],Pdict)

    #ID , X , TracerEx, Px , Y , TracerEy , Py , Ek = Processing.getTracer(n)
    EkMin = 0.01
    subscript = 10
    IDFinal = ID[Ek>EkMin][::subscript]
    
    '''
    X = X[Ek>EkMin][::subscript]    
    Y = Y[Ek>EkMin][::subscript]
    TracerEx = TracerEx[Ek>EkMin][::subscript]
    TracerEy = TracerEy[Ek>EkMin][::subscript]
    Px = Px[Ek>EkMin][::subscript]
    Py = Py[Ek>EkMin][::subscript]
    Ek = Ek[Ek>EkMin][::subscript]
    print('X.shape:',X.shape)
    '''
    return IDFinal

def MoveData(TrackData,Data,ID,IDFinal):
    for i in range(len(IDFinal)):
    #print(IDFinal[i])
    #print(TracerEx[ID==IDFinal[i]])
        try:
            Data[i]=float(TrackData[ID==IDFinal[i]])
        except:
            Data[i]=0.0
        #Ey[i]=float(TracerEy[ID==IDFinal[i]])
        #EkId[i] = float(Ek[ID==IDFinal[i]])
        #Xid[i]=float(X[ID==IDFinal[i]])
        #Yid[i]=float(Y[ID==IDFinal[i]])
    return Data


def fromDict(names,Pdict):
    for i in range(len(names)):
        names[i] = Pdict[str(names[i])]
    return names
    

def addIdData(n,IDFinal):
    Pdict = Processing.getTracer(n)
    #ID , X , TracerEx, Px , Y , TracerEy , Py , Ek = Processing.getTracer(n)
    #ID , X , TracerEx, Px , Y , TracerEy , Py , Ek , Vx,Vy = 0
    ID , X , TracerEx, Px , Y , TracerEy , Py , Ek , Vx,Vy = fromDict(['ID' , 'X' , 'TracerEx', 'Px' , 'Y', 'TracerEy' , 'Py' , 'Ek' , 'Vx' , 'Vy'],Pdict)
    #print('len',len(X))
    #TimeX = np.zeros([tsize,len(idNumber)])
    #print('X.shape,',X.shape)
    #for index,IdFinal in zip(range(len(IDFinal)),IDFinal):
        #print('index,i',index,i)
    #print('IDFinal',len(IDFinal))
    Ex=IDFinal*np.nan
    Ey=IDFinal*np.nan
    EkId = IDFinal*np.nan
    Xid = IDFinal*np.nan
    Yid = IDFinal*np.nan
    Pxid = IDFinal*np.nan
    Pyid = IDFinal*np.nan
    Vxid = IDFinal*np.nan

    Vyid = IDFinal*np.nan


    Ex = MoveData(TracerEx,Ex,ID,IDFinal)
    Ey = MoveData(TracerEy,Ey,ID,IDFinal)
    Xid = MoveData(X,Xid,ID,IDFinal)
    Yid = MoveData(Y,Yid,ID,IDFinal)
    EkId = MoveData(Ek,EkId,ID,IDFinal)

    Pxid = MoveData(Px,Pxid,ID,IDFinal)
    Pyid = MoveData(Py,Pyid,ID,IDFinal)


    Vxid = MoveData(Vx,Pxid,ID,IDFinal)
    Vyid = MoveData(Vy,Pyid,ID,IDFinal)

    '''
    for i in range(len(IDFinal)):
        #print(IDFinal[i])
        #print(TracerEx[ID==IDFinal[i]])
        try:
            Ex[i]=float(TracerEx[ID==IDFinal[i]])
        except:
            Ex[i]=0.0
        Ey[i]=float(TracerEy[ID==IDFinal[i]])
        EkId[i] = float(Ek[ID==IDFinal[i]])
        Xid[i]=float(X[ID==IDFinal[i]])
        Yid[i]=float(Y[ID==IDFinal[i]])
    '''

    ######  add eff to csv  #####
    #############################
    #print(TracerEy.shape)
    Pydf = pd.DataFrame(data=Pyid.reshape(1,-1),index=[n],columns=IDFinal)#columns = ['index','ETHz','ETotal'])
    filepathPy = const.txtdir + 'TracerPy.csv'
    Pxdf = pd.DataFrame(data=Pxid.reshape(1,-1),index=[n],columns=IDFinal)#columns = ['index','ETHz','ETotal'])
    filepathPx = const.txtdir + 'TracerPx.csv'

    Vydf = pd.DataFrame(data=Vyid.reshape(1,-1),index=[n],columns=IDFinal)#columns = ['index','ETHz','ETotal'])
    filepathVy = const.txtdir + 'TracerVy.csv'
    Vxdf = pd.DataFrame(data=Vxid.reshape(1,-1),index=[n],columns=IDFinal)#columns = ['index','ETHz','ETotal'])
    filepathVx = const.txtdir + 'TracerVx.csv'


    Eydf = pd.DataFrame(data=Ey.reshape(1,-1),index=[n],columns=IDFinal)#columns = ['index','ETHz','ETotal'])
    filepathEy = const.txtdir + 'TracerEy.csv'
    Exdf = pd.DataFrame(data=Ex.reshape(1,-1),index=[n],columns=IDFinal)#columns = ['index','ETHz','ETotal'])
    filepathEx = const.txtdir + 'TracerEx.csv'

    Ekdf = pd.DataFrame(data=EkId.reshape(1,-1),index=[n],columns=IDFinal)#columns = ['index','ETHz','ETotal'])
    filepathEk = const.txtdir + 'TracerEk.csv'

    Xdf = pd.DataFrame(data=Xid.reshape(1,-1),index=[n],columns=IDFinal)#columns = ['index','ETHz','ETotal'])
    filepathX = const.txtdir + 'TracerX.csv'

    Ydf = pd.DataFrame(data=Yid.reshape(1,-1),index=[n],columns=IDFinal)#columns = ['index','ETHz','ETotal'])
    filepathY = const.txtdir + 'TracerY.csv'

    datadict = [Vydf,Vxdf,Pydf,Pxdf,Eydf,Exdf,Ekdf,Xdf,Ydf]
    filedict = [filepathVy,filepathVx,filepathPy,filepathPx,filepathEy,filepathEx,filepathEk,filepathX,filepathY]
    #print(df)
    for dataframe,filepath in zip(datadict,filedict):
        if n == 0:
            saveCSV(dataframe,filepath,create = 'True')
            continue
        saveCSV(dataframe,filepath)

    #if exist:
    #    dfEy = pd.DataFrame(mode = 'a',index=n,head=False)#,columns=colums)
    #dfEy.loc[n,:]=TracerEy

    #TimeEy.append(TracerEy)


    return X,Y
    '''
    TimeX.append(X)
    TimeY.append(Y)
    TimeEx.append(TracerEx)
    TimeEy.append(TracerEy)
    TimePx.append(Px)
    TimePy.append(Py)
    TimeEk.append(Ek)
    '''
def plotFig(n,X,Y):
    Ex,Ey = getField(n)

    #plt.scatter(X,Y,s=0.1)
    plt.pcolormesh(XX[::10,::10],YY[::10,::10],Ex[::10,::10].T,cmap = plt.cm.bwr)
    plt.colorbar()
    plt.scatter(X[::5],Y[::5],s=0.1)
    plt.title('Ex')
    #plt.colorbar()
    plt.savefig('test/Ex'+str(n)+'.jpg',dpi=160)
    plt.clf()
    plt.close('all')


    #plt.scatter(X,Y,s=0.1)    
    plt.pcolormesh(XX[::10,::10],YY[::10,::10],Ey[::10,::10].T,cmap = plt.cm.bwr)
    plt.colorbar()
    #plt.scatter(X[::5],Y[::5],s=0.1)
    plt.title('Ey')
    #plt.colorbar()
    plt.savefig('test/Ey'+str(n)+'.jpg',dpi=160)
    plt.clf()
    plt.close('all')

#arr = range(10,stop+10,50)
#arr = [1000,2000]
#tsize = len(arr)
#idNumber = getTracer(1300)
#TimeX = np.zeros([tsize,len(idNumber)])
#TimeY = np.zeros([tsize,len(idNumber)])
#TimeEy = np.zeros([tsize,len(idNumber)])

#print('len(idNumber)',len(idNumber))

#def main(n,IDFinal):

def main(n):
    print('Proncessing:',n)
    #idNumber = getTracer(1300)
    X,Y = addIdData(n,IDFinal)
    plotFig(n,X,Y)

global IDFinal
IDFinal = getFinalParticleID(FinalNumber)

for n in range(start,stop,step):
    main(n)#,IDFinal)


'''

#@njit
for sdfnumber in range(tsize):
    #n = arr[sdfnumber]
    print(n)
    main(n)


'''
pool = multiprocessing.Pool(processes=96,initargs=(IDFinal))   #,initargs=(ss1,ss2))
#arr = Processing.flist()
#arr = arr[::int(len(arr)/100)]
#print(arr)
#arr = [100]
#results = pool.map(getTracer,arr)
#results = pool.map(main,range(start,stop,step))
pool.close()
pool.join()
'''


#TimeArr = [TimeX,TimeX,TimeY,TimeEx,TimeEy,TimePx,TimePy,TimeEk,idNumber]


def to_np_arr(*args):
    for arg in args:
        arg = np.array(arg)
    return args

#for arr in TimeArr:
#    arr = np.array(arr)
#TimeX,TimeX,TimeY,TimeEx,TimeEy,TimePx,TimePy,TimeEk,idNumber = to_np_arr(TimeX,TimeX,TimeY,TimeEx,TimeEy,TimePx,TimePy,TimeEk,idNumber)
    

TimeX = np.array(TimeX)
TimeY = np.array(TimeY)
TimeEy = np.array(TimeEy)

for i in range(len(TimeX)):
    try:
        plt.plot(TimeX[:,i],TimeY[:,i])
        plt.savefig('test/TraceXY/'+str(idNumber[i])+'.jpg',dpi=160)
        plt.clf()
        plt.close('all')
    except:
        print('Wrong plot XY')
        pass
    try:

        plt.plot(arr*const.dt_snapshot/1e-15,TimeEy[:i])
        plt.savefig('test/TraceXY/'+str(idNumber[i])+'Ey.jpg',dpi=160)
        plt.clf()
        plt.close('all')
    except:
        print('Wrong plot Ey')
'''
