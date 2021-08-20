import sdf
import Processing
import matplotlib.pyplot as plt
import constant as const
import numpy as np
from numba import njit
import multiprocessing
plt.switch_backend('agg')

start = const.start
stop = const.stop



def getField(n):
    sdfdir=const.sdfdir +str(n).zfill(const.filenumber)+".sdf"
    data = sdf.read(sdfdir,dict=True)
    Ex = data['Electric Field/Ex'].data
    Ey = data['Electric Field/Ey'].data
    return Ex,Ey

arr = range(50,stop+10,50)
#TimeX = np.zeros([tsize,len(idNumber)])
#arr = [1000]

arrx = np.linspace(const.x_min + const.delta_x,const.x_max + const.delta_x,const.Nx)
arry = np.linspace(const.y_min + const.delta_y,const.y_max + const.delta_y,const.Ny)

XX,YY = np.meshgrid(arrx,arry)

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
def getFinalParticleID(n):
    ID , X , TracerEx, Px , Y , TracerEy , Py , Ek = Processing.getTracer(n)
    return ID[Ek>1]

def getTracer(n,IDFinal):
    ID , X , TracerEx, Px , Y , TracerEy , Py , Ek = Processing.getTracer(n)
    
    for i in range(IDFinal.shape):
        TracerEx[i]=float(Ex[ID==IDFinal[i]])
        TracerEy[i]=float(Ey[ID==IDFinal[i]])

    #TracerEx[ID == IDFinal]
    #XT = XT.append(X)

    #YT = YT.append(Y)

    #TracerEx

    #TracerEx
    print('len',len(X))

    idNumber = np.arange(len(X))
    EkMin = 1
    subscript = 10

    idNumber = idNumber[Ek>EkMin][::subscript]
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
    return idNumber


def addID(n,idNumber,i):
    X , TracerEx, Px , Y , TracerEy , Py , Ek = Processing.getTracer(n)
    print('len',len(X))
    #TimeX = np.zeros([tsize,len(idNumber)])
    print('X.shape,',X.shape)
    indexT = i

    for index,idnumber in zip(range(len(idNumber)),idNumber):
        #print('index,i',index,i)

        TimeX[indexT,index] = X[idnumber]
        TimeY[indexT,index] = Y[idnumber]
        TimeEy[indexT,index] = TracerEy[idnumber]
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

arr = range(10,stop+10,50)
arr = [1000,2000]
tsize = len(arr)
idNumber = getTracer(1300)
TimeX = np.zeros([tsize,len(idNumber)])
TimeY = np.zeros([tsize,len(idNumber)])
TimeEy = np.zeros([tsize,len(idNumber)])

print('len(idNumber)',len(idNumber))
def main(n,i):
    #idNumber = getTracer(1300)
    X,Y = addID(n,idNumber,i)
    plotFig(n,X,Y)

#@njit
for i in range(tsize):
    n = arr[i]
    print(n,i)
    main(n,i)


'''
pool = multiprocessing.Pool(processes=96)   #,initargs=(ss1,ss2))
#arr = Processing.flist()
#arr = arr[::int(len(arr)/100)]
print(arr)
#arr = [100]
results = pool.map(getTracer,arr)
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
